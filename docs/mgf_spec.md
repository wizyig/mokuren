# MGF v1.0 — MOKUREN Grid Format

Status: **MGF v1.0 format lock (OBSERVED)**.

Not Pi³XI CR-frozen. Not Ed25519. Not Trust-L4.

Owner: https://github.com/wizyig/mokuren

```
Store observations.
Do not store conclusions.
Allowed: Y | N | 0
```

## Frozen targets

- Enum: Y / N / 0
- Flags: A01 .. A05
- IDs: run_id, record_id, node_id, node_type, observed_date, status
- observed_date: ISO YYYY-MM-DD and a real calendar day (2026-02-31 fails)
- run_id: YYYYMMDD-NNN
- additionalProperties: false

## Compatibility Policy

MGF v1.0 guarantees lossless interchange across CSV, YAML, and JSON Schema
for the core primitives.

Extensions (A06+, custom COND-XXX) MUST be optional non-breaking layers.
They MUST NOT change Y|N|0, replace A01..A05, add required top-level keys,
store scores as authority, or loosen additionalProperties on the v1.0 object.

A breaking change requires mgf_version other than "1.0".
