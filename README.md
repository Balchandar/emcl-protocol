# EMCL (Encrypted Model Context Layer)

A universal secure transport layer for AI agents and tools, providing encrypted,
signed, identity-aware JSON-RPC communication across any agent framework.

EMCL is to agent communication what TLS is to HTTP — a general-purpose, zero-trust
encryption layer that works with *any* JSON-RPC–based system, including (but not limited to) MCP.

---

## 🔐 Features

EMCL provides end-to-end encryption and authenticated messaging for any
JSON-RPC workflow, independent of the tool or agent architecture.

- AES-256-GCM encryption of request/response payloads  
- HMAC-SHA256 request signing  
- JWT-based agent identity, scopes, and claims  
- Replay protection via timestamps + nonce  
- Gateway policy enforcement + audit logging  
- Framework-agnostic secure envelope for agent-to-agent & agent-to-tool calls  

---

## 🌐 Protocol-Agnostic Design

EMCL is *not tied* to any specific agent protocol.  
It wraps and protects arbitrary JSON-RPC messages, enabling secure communication for:

- AI agents talking to each other  
- Tools and services accessed via JSON-RPC  
- Custom or proprietary agent frameworks  
- Local or remote model/tool backends  
- Open standards such as MCP (optional integration)

Its goal is to remain a general-purpose, zero-trust encrypted envelope for all AI communication.

---

## 🧪 Example Components

- `example_client.py` — sends encrypted + signed EMCL-wrapped request  
- `gateway/server.py` — verifies, decrypts, authorizes, and proxies to a real tool backend  
- `mock_tool_server.py` — sample unencrypted tool endpoint for testing  
- `keys.py` — symmetric AES & HMAC key utilities  

These files demonstrate end-to-end secure request flow using EMCL’s encryption and signing model.

---


## 🧩 Architecture (Simplified)

```text
Client → EMCL Wrapper → Encrypted JSON-RPC → EMCL Gateway → Tool Server


The gateway validates signatures, decrypts payloads, checks identity + policies,
and forwards clean JSON-RPC calls to actual tools.

---

## 📚 Specification

See [`spec/EMCL-v0.1.md`](spec/EMCL-v0.1.md) for:

- message structure  
- envelope format  
- encryption/signing rules  
- nonce & replay protection  
- identity propagation  
- optional MCP interoperability  

---

## 🔗 Related

- Compatible with OpenAI's Model Context Protocol (MCP)  
  *(EMCL works without MCP; this integration is optional and transport-level only)*  

---

## 📝 License

MIT

---

## 👤 Author

Created by **Balachandar Manikandan**

---

## 🔎 Keywords

**EMCL**, **Encrypted Model Context Layer**, secure JSON-RPC protocol,  
zero-trust AI communication, encrypted agent messaging, AI security protocol,  
AES-GCM JSON-RPC, HMAC-SHA256 signing, secure agent transport layer,  
agent identity propagation, encrypted tool communication.

