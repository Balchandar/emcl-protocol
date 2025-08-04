# EMCL-001: Encrypted Model Context Layer (EMCL)

## Summary

The Encrypted Model Context Layer (EMCL) defines a secure communication protocol that wraps JSON-RPC-based MCP tool-agent communication with encryption, authentication, and message integrity. EMCL provides a lightweight, pluggable mechanism for securing model input/output payloads using AES-256-GCM, HMAC/RSA signatures, and JWT-based identity propagation.

## Authors

* Balachandar Manikandan ([@Balchandar](https://github.com/Balchandar))

## Status

Draft

## Motivation

The current Model Context Protocol (MCP) lacks built-in security at the protocol layer. While HTTPS can protect transport, it does not enforce:

* fine-grained identity and role validation
* replay attack protection
* payload integrity or tamper-proofing
* secure multi-agent pipelines

EMCL solves these gaps by securing the protocol layer, enabling toolchains to work securely even in untrusted environments.

## Goals

* Encrypt and decrypt parameters and results end-to-end
* Verify agent and tool authenticity
* Prevent payload tampering
* Support nonce/timestamp replay protection
* Provide SDKs for easy integration

## Specification

### Encryption

* All MCP payloads (params, results) are encrypted using **AES-256-GCM**
* The AES key is symmetric and shared between trusted peers (agent/gateway/tool)

### Signing

* Payloads are signed using **HMAC-SHA256** or optionally **RSA-SHA256**
* Signature is validated before decryption to ensure authenticity

### Identity

* JWT-based identity propagation using headers:

  * `x-emcl-agent-token`: signed JWT with claims like `agentId`, `roles`, `scopes`
* JWTs are validated against shared secret or public key

### Anti-Replay

* Each message includes a `nonce` and `timestamp`
* Duplicate nonces or old timestamps are rejected by EMCL Gateway

### Protocol Structure

EMCL-wrapped payload structure:

```json
{
  "emcl_version": "1.0",
  "enc": "base64(AES256GCM_ENCRYPTED_BODY)",
  "sig": "HMAC_SIGNATURE",
  "nonce": "UUIDv4",
  "ts": "2025-08-04T12:00:00Z"
}
```

### Gateway Enforcement

* EMCL Gateway acts as middleware
* Validates JWT, signature, nonce, and decrypts the payload
* Injects decrypted content into tool runtime
* Optionally logs audit trail

## Compatibility

* Compatible with any tool or agent using JSON-RPC over HTTP
* LangChain, AutoGen, and other LLM frameworks can adopt EMCL via simple SDK wrappers

## Limitations

* Requires shared key management or public key infrastructure
* Streaming and bidirectional agent-to-agent EMCL is not yet defined

## Security Considerations

* Keys should be rotated regularly
* All messages must be timestamped and nonce-tracked
* JWTs must have short TTL and limited scope

## References

* EMCL GitHub: [https://github.com/Balchandar/emcl-protocol](https://github.com/Balchandar/emcl-protocol)
* Reddit: [https://www.reddit.com/r/mcp/comments/1m17afj/emcl\_a\_secure\_protocol\_for\_ai\_agents\_to\_call/](https://www.reddit.com/r/mcp/comments/1m17afj/emcl_a_secure_protocol_for_ai_agents_to_call/)
* JSON-RPC 2.0: [https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)

---

This RFC is intended for discussion and collaboration. Suggestions for implementation, edge case handling, and formalization are welcome.
