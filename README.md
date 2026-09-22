# MOKUREN

**Machine Observation / Knowledge Representation / Engine for Reviewable Evidence Networks**

OfanimRing の人間向け変換器。目目連（無数の目）を英語圏でも通る固有名にしたもの。

Human UI = Excel方眼紙 / ポンチ絵  
LLM IR  = CSV graph + 5-check pattern `[Y Y N Y Y]`

判定しない。保存する。集計する。レビューする。

```
Article
  ↓
Observation
  ↓
CR Candidate
  ↓
Periodic Review
```

## Why 5 + 0

精度と監査可能性のトレードオフはここで止める。

- 3 state → 粗い
- 5-check + 0 → 紙監査で1分で追える
- 36 state / 64+座標 → まだ追跡可能
- それ以上の圧縮スコア → 監査不能

`score = 0.734218` は出さない。出すのはパターンだけ。

## Layout

```
A run_id
B record_id
C node_id
D node_type
E parent_node_id
F next_node_id
G source_id
H observed_date
I-M A01..A05
N status
O notes
```

Workbook: `templates/mokuren_observed.xlsx` (local pack; binary not in first commit if API text-only)

## Usage

```bash
python scripts/validate.py templates/observed_template.csv
python scripts/to_dot.py templates/observed_template.csv
python scripts/graph_view.py templates/observed_template.csv -o examples/graph.png
```

## Names considered

| Name | Note |
|---|---|
| MOKUREN | preferred. 目目連 + acronym |
| Wall of Eyes | yokai-adjacent, English-clear |
| ThousandEyes | taken / product collision |
| Ofanim Lens | ring → human view |
| EyeWall | short GitHub name |
| Witness / LedgerEyes | audit-first |

Repo: `mokuren`

## Contract

See `docs/CONTRACT.md`. OBSERVED only. Not CR-frozen.
