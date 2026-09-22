#!/usr/bin/env python3
"""Optional NetworkX view. Default audit display is the 5-check pattern, not a score."""

from __future__ import annotations

import argparse

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def build(df: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    for _, row in df.iterrows():
        node = str(row["node_id"]).strip()
        if not node:
            continue
        checks = [str(row[k]).strip() for k in ("A01", "A02", "A03", "A04", "A05")]
        label = f"{node}\n{row['node_type']}\n[{' '.join(checks)}]"
        G.add_node(node, label=label)
        nxt = row.get("next_node_id")
        if pd.notna(nxt) and str(nxt).strip():
            G.add_edge(node, str(nxt).strip())
    return G


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("csv_path")
    p.add_argument("-o", "--output", default="graph.png")
    args = p.parse_args()
    df = pd.read_csv(args.csv_path)
    G = build(df)
    plt.figure(figsize=(12, 7))
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_node_attributes(G, "label")
    nx.draw_networkx_nodes(G, pos, node_size=4200)
    nx.draw_networkx_edges(G, pos, arrows=True)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.title("MOKUREN Observation Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(args.output, dpi=140)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
