from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_plot(fig, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    supplier_kpis = pd.read_csv(ROOT / "outputs" / "supplier_kpis.csv")
    monthly_kpis = pd.read_csv(ROOT / "outputs" / "monthly_kpis.csv")

    if not supplier_kpis.empty:
        supplier_kpis = supplier_kpis.sort_values("spend_total", ascending=False)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(supplier_kpis["supplier"], supplier_kpis["spend_total"], color="#2E86DE")
        ax.set_title("Spend total par fournisseur")
        ax.set_ylabel("Spend total")
        ax.tick_params(axis="x", rotation=45)
        save_plot(fig, "spend_by_supplier.png")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(supplier_kpis["supplier"], supplier_kpis["savings_pct"], color="#28A745")
        ax.set_title("Économie (%) par fournisseur")
        ax.set_ylabel("Savings %")
        ax.tick_params(axis="x", rotation=45)
        save_plot(fig, "savings_pct_by_supplier.png")

        fig, ax = plt.subplots(figsize=(10, 5))
        x = range(len(supplier_kpis))
        ax.bar(x, supplier_kpis["otd_pct"], color="#F39C12", label="OTD %")
        ax.bar(x, supplier_kpis["quality_pct"], color="#8E44AD", alpha=0.7, label="Quality %")
        ax.set_xticks(list(x))
        ax.set_xticklabels(supplier_kpis["supplier"], rotation=45)
        ax.set_title("OTD et qualité par fournisseur")
        ax.set_ylabel("Pourcentage")
        ax.legend()
        save_plot(fig, "otd_quality_by_supplier.png")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(supplier_kpis["spend_total"], supplier_kpis["rse_score"], s=120, color="#16A085")
        for i, row in supplier_kpis.iterrows():
            ax.text(row["spend_total"], row["rse_score"], row["supplier"], fontsize=8)
        ax.set_title("Score RSE vs Spend")
        ax.set_xlabel("Spend total")
        ax.set_ylabel("RSE Score")
        save_plot(fig, "rse_vs_spend.png")

    if not monthly_kpis.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly_kpis["period"], monthly_kpis["spend_total"], marker="o", color="#1F77B4")
        ax.set_title("Évolution mensuelle du spend")
        ax.set_xlabel("Période")
        ax.set_ylabel("Spend total")
        ax.tick_params(axis="x", rotation=45)
        save_plot(fig, "monthly_spend_trend.png")

    print(f"Graphiques générés dans {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
