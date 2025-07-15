from flask import Flask, request, jsonify
import base64, json, os, requests
from datetime import datetime, timezone
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from keys import aes_key, hmac_key

app = Flask(__name__)
TOOL_URL = "http://localhost:5001/tool/run"
CURRENT_KEY_ID = "aes-v1"

def decrypt_params(b64_data, key):
    raw = base64.b64decode(b64_data)
    nonce, tag, ciphertext = raw[:12], raw[12:28], raw[28:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(b"")
    return json.loads(cipher.decrypt_and_verify(ciphertext, tag))

def encrypt_result(data, key):
    nonce = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(data).encode())
    return base64.b64encode(nonce + tag + ciphertext).decode()

def verify_signature(payload, sig, key):
    canonical = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode()
    h = HMAC.new(key, digestmod=SHA256)
    h.update(canonical)
    try:
        h.hexverify(sig)
        return True
    except ValueError:
        return False

@app.route("/emcl-call", methods=["POST"])
def emcl_call():
    body = request.json
    required = ["method", "params_encrypted", "sig", "keyId", "meta"]
    if not all(k in body for k in required):
        return jsonify({"error": "Missing EMCL fields"}), 400

    method, params_encrypted, sig, key_id, meta = body["method"], body["params_encrypted"], body["sig"], body["keyId"], body["meta"]
    sig_payload = {"method": method, "params_encrypted": params_encrypted, "meta": meta, "keyId": key_id}

    if not verify_signature(sig_payload, sig, hmac_key):
        return jsonify({"error": "Invalid signature"}), 401

    timestamp = datetime.fromisoformat(meta["timestamp"])
    if abs((datetime.now(timezone.utc) - timestamp).total_seconds()) > 300:
        return jsonify({"error": "Replay protection: timestamp too old"}), 403

    try:
        params = decrypt_params(params_encrypted, aes_key)
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 400

    try:
        tool_resp = requests.post(TOOL_URL, json=params)
        result = tool_resp.json()
    except Exception as e:
        return jsonify({"error": f"Tool call failed: {str(e)}"}), 500

    result_encrypted = encrypt_result(result, aes_key)
    return jsonify({"result_encrypted": result_encrypted})

if __name__ == "__main__":
    app.run(port=8000)
