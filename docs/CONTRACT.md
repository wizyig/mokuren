# MOKUREN Contract v0.1 (OBSERVED)

Status: OBSERVED, not CR-frozen, not Ed25519, not Trust-L4.

## What this is

Human-readable grid + LLM-readable graph for the same observation.

```
Excel方眼紙
→ CSV
→ Graph
→ 5-check pattern
→ Periodic Review
```

## Store

- observation rows
- check results (Y / N / 0)
- graph edges (parent_node_id / next_node_id)
- run_id

## Do not store as authority

- composite score
- dynamic weights
- auto-fire thresholds
- model opinion / root_cause / explanation in the observation body

## Allowed values

A01-A05: Y | N | 0
node_type: input | observed | candidate | review
status: active | observed | candidate | pending | closed
run_id: YYYYMMDD-NNN

## State space

5 checks × {Y,N} plus 0 (unevaluated) is the operational surface.

Countable yes-state: 0..5.
Pattern space (Y/N only): 32.
With 0 mixed in: larger, but review still traces cell-by-cell.

Beyond 64+coordinate compression, audit cost exceeds information value.

## Pipeline

Observe → Record → Aggregate counts → Mark for review → Human review.

Aggregate is COUNTIF only. Decision stays with the reviewer.
