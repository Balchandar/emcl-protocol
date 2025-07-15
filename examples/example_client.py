import json, os, uuid, base64, requests
from datetime import datetime, timezone
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from keys import aes_key, hmac_key

def encrypt_params(data, key):
    nonce = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(data).encode())
    return base64.b64encode(nonce + tag + ciphertext).decode(), nonce

def sign_request(payload, key):
    canonical = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode()
    h = HMAC.new(key, digestmod=SHA256)
    h.update(canonical)
    return h.hexdigest()

def main():
    method = "toolCall"
    params = {"vitalSigns": {"bp": "120/80", "hr": 72}}
    params_encrypted, _ = encrypt_params(params, aes_key)
    meta = {
        "agentId": "agent-123",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "nonce": str(uuid.uuid4())[:16]
    }
    key_id = "aes-v1"
    payload = {
        "method": method,
        "params_encrypted": params_encrypted,
        "meta": meta,
        "keyId": key_id
    }
    signature = sign_request(payload, hmac_key)
    payload["sig"] = signature
    headers = {
        "Authorization": "Bearer test.jwt.token",
        "Content-Type": "application/json"
    }
    r = requests.post("http://localhost:8000/emcl-call", json=payload, headers=headers)
    print("Response:", r.text)

if __name__ == "__main__":
    main()
