# MOKUREN

Human-readable observation transformer for OfanimRing.

日本人: あー、Excel方眼紙。

```
MOKUREN

Excel方眼紙を
監査可能なグラフへ変換する。

Observe.
Record.
Review.

No autonomous judgement.
No automatic enforcement.
```

価値は **MGF (MOKUREN Grid Format)** にある。

```
方眼紙 → MGF CSV → VALIDATION_PASSED → MGF YAML → Graph → Review
```

See `docs/mgf_spec.md` and `schema/mgf.schema.json`.

```bash
python cli.py validate samples/sample_valid.csv
python cli.py graph samples/sample_valid.csv
python -m pytest -q
```

argparse only. OBSERVED. Not CR-frozen. Not Ed25519. Not Trust-L4.
