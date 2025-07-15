# EMCL (Encrypted Model Context Layer)

A secure protocol for AI tools with encrypted, signed, identity-aware JSON-RPC calls.

EMCL is to MCP what TLS is to HTTP — a secure transport layer for agent–tool communication.

## 🔐 Features

- AES-256-GCM encryption of tool input/output
- HMAC-SHA256 request signing
- JWT-based agent identity and scopes
- Replay protection with timestamp and nonce
- Gateway policy enforcement and audit logs

## 🧪 Example Components

- `example_client.py` — sends encrypted, signed request
- `gateway/server.py` — verifies and proxies to real tool
- `mock_tool_server.py` — dummy backend tool for testing
- `keys.py` — symmetric AES & HMAC keys

## 📚 Spec

See `spec/EMCL-v0.1.md` for full protocol details.

## 🔗 Related

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2025-06-18/basic)

## 📝 License

MIT

## 👤 Author

Created by Balachandar Manikandan
