# EMCL: Encrypted Model Context Layer

## Overview

**EMCL** (Encrypted Model Context Layer) is a secure protocol layer built on top of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2025-06-18/basic). It provides encryption, integrity, and identity protection for AI agent–to–tool communication.

While MCP defines a flexible JSON-RPC–style standard for invoking tools, EMCL adds the production-grade security needed for real-world deployments.

### EMCL enhances MCP with:

- 🔒 AES-256-GCM encryption of tool inputs and outputs
- ✅ HMAC-SHA256 request signing
- 🔑 JWT-based agent identity and scope propagation
- 🛡 Timestamp + nonce–based replay protection
- ⚙️ Gateway policy enforcement and auditing

> EMCL is to MCP what **TLS is to HTTP** — a secure transport layer for tool calls.

EMCL is transport-agnostic (HTTP/S, IPC, local loopback) and compatible with any JSON-compatible tool server.

## 1. Message Structure

### EMCL Request

```json
{
  "method": "toolCall",
  "params_encrypted": "Base64(AES-GCM(...))",
  "sig": "HMAC-SHA256(...)",
  "keyId": "aes-v1",
  "meta": {
    "agentId": "agent-123",
    "timestamp": "2025-07-15T12:34:00Z",
    "nonce": "7f3c9f42-b872"
  }
}
```

### EMCL Response

```json
{
  "result_encrypted": "Base64(AES-GCM(...))"
}
```

## 2. Cryptographic Model

### Encryption

- Algorithm: AES-256-GCM
- Nonce: Random 12-byte (per message)
- Tag: 16-byte authentication tag

**Payload:**

```
nonce || tag || ciphertext
```

### Signing

- HMAC-SHA256 over canonical JSON of:

```json
{
  "method": ...,
  "params_encrypted": ...,
  "meta": ...,
  "keyId": ...
}
```

## 3. Security Requirements

### Timestamp

- ISO-8601 UTC
- Gateway must reject requests older than 300s

### Nonce

- Must be unique per request (UUID or random string)
- Gateway must track seen nonces for 300s and reject reuse

### Signature

- Must be verified using key bound to `keyId`
- Verification must use constant-time comparison

### Key Rotation

- Keys identified by `keyId`
- Old keys can remain for verification only
- New requests must use `CURRENT_KEY_ID`

## 4. Identity & Authorization

### JWT

- Agent must send JWT in `Authorization: Bearer <token>`
- Claims should include:
  - `sub`: agent ID
  - `scope`: list of allowed methods
  - Optional: rate limits, tool groups

### Policy Enforcement

- Gateway may apply `.emcl-policy.json` to restrict:
  - Method access
  - Rate limits
  - Payload size

## 5. Tool Isolation

- Tool servers must be private to the gateway (localhost, mTLS, or internal network)
- Tool input/output must never be logged or leaked
- Tools must validate schema

## 6. Error Handling

All errors should return:

```json
{ "error": "<reason>" }
```

Never return decrypted payloads or stack traces.

## 7. Audit Log (Recommended)

Fields to log:

- `timestamp`
- `agentId`
- `method`
- `keyId`
- `toolEndpoint`
- `resultCode` (OK, ERR:message)

## Future Extensions

- Nested encryption for `meta`
- JWE-compatible payload format
- Rewind-safe audit log hashing
- LLM call graph tracing

## License

MIT

## Authors

Proposed by Balachandar Manikandan, EMCL Protocol Maintainer

## Draft Version

v0.1 – July 15, 2025
