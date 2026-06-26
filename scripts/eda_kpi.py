from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    renamed = {}
    for col in df.columns:
        renamed[col] = str(col).strip().lower().replace(" ", "_").replace("-", "_")
    return df.rename(columns=renamed)


def find_column(columns: list[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.strip().str.replace("%", "", regex=False).str.replace(",", ".", regex=False),
        errors="coerce",
    )


def normalize_percentage(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    if values.notna().any():
        values = values.mask(values.between(0, 1), values * 100)
    return values


def build_kpis(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    supplier_col = find_column(df.columns, ["supplier", "vendor", "fournisseur", "supplier_name"])
    spend_col = find_column(df.columns, ["spend", "amount", "total_spend", "purchase_value", "purchase_amount", "cost"])
    savings_col = find_column(df.columns, ["savings", "savings_amount", "savings_value"])
    otd_col = find_column(df.columns, ["otd", "on_time_delivery", "delivery_rate", "otd_pct"])
    quality_col = find_column(df.columns, ["quality", "quality_rate", "quality_pct", "defect_rate"])
    rse_col = find_column(df.columns, ["rse", "esg", "rse_score", "csr_score", "sustainability_score", "sustainability"])
    date_col = find_column(df.columns, ["date", "order_date", "purchase_date", "invoice_date", "month", "period"])

    if supplier_col is None or spend_col is None:
        raise ValueError("Le dataset doit contenir au moins une colonne fournisseur et une colonne spend.")

    df = df.copy()
    df[supplier_col] = df[supplier_col].astype(str).str.strip()

    df["spend"] = clean_numeric(df[spend_col])
    if savings_col is not None:
        df["savings_amount"] = clean_numeric(df[savings_col])
    else:
        df["savings_amount"] = 0.0

    if otd_col is not None:
        df["otd_pct"] = normalize_percentage(df[otd_col])
    else:
        df["otd_pct"] = np.nan

    if quality_col is not None:
        df["quality_pct"] = normalize_percentage(df[quality_col])
    else:
        df["quality_pct"] = np.nan

    if rse_col is not None:
        df["rse_score"] = normalize_percentage(df[rse_col])
    else:
        df["rse_score"] = np.nan

    df["savings_pct"] = np.where(df["spend"] > 0, df["savings_amount"] / df["spend"] * 100, np.nan)

    supplier_kpis = (
        df.groupby(supplier_col, dropna=False)
        .agg(
            spend_total=("spend", "sum"),
            savings_amount=("savings_amount", "sum"),
            savings_pct=("savings_pct", "mean"),
            otd_pct=("otd_pct", "mean"),
            quality_pct=("quality_pct", "mean"),
            rse_score=("rse_score", "mean"),
            order_count=("spend", "size"),
        )
        .reset_index()
        .rename(columns={supplier_col: "supplier"})
    )
    supplier_kpis["spend_share_pct"] = supplier_kpis["spend_total"] / supplier_kpis["spend_total"].sum() * 100

    overall_kpis = pd.DataFrame(
        [
            {
                "spend_total": df["spend"].sum(),
                "savings_amount": df["savings_amount"].sum(),
                "savings_pct": (df["savings_amount"].sum() / df["spend"].sum() * 100) if df["spend"].sum() else np.nan,
                "otd_pct": df["otd_pct"].mean(),
                "quality_pct": df["quality_pct"].mean(),
                "rse_score": df["rse_score"].mean(),
                "supplier_count": supplier_kpis["supplier"].nunique(),
                "top_10_pct_spend_concentration": (
                    supplier_kpis.nlargest(max(1, int(round(len(supplier_kpis) * 0.1))), "spend_total")["spend_total"].sum()
                    / supplier_kpis["spend_total"].sum()
                    * 100
                    if supplier_kpis["spend_total"].sum() else np.nan
                ),
            }
        ]
    )

    if date_col is not None:
        df["period"] = pd.to_datetime(df[date_col], errors="coerce").dt.to_period("M").astype(str)
        monthly_kpis = (
            df.groupby("period", dropna=False)
            .agg(
                spend_total=("spend", "sum"),
                savings_amount=("savings_amount", "sum"),
                savings_pct=("savings_pct", "mean"),
                otd_pct=("otd_pct", "mean"),
                quality_pct=("quality_pct", "mean"),
                rse_score=("rse_score", "mean"),
                supplier_count=("supplier", "nunique"),
            )
            .reset_index()
        )
    else:
        monthly_kpis = pd.DataFrame(columns=["period", "spend_total", "savings_amount", "savings_pct", "otd_pct", "quality_pct", "rse_score", "supplier_count"])

    return overall_kpis, supplier_kpis, monthly_kpis


def main() -> None:
    parser = argparse.ArgumentParser(description="Génère des KPI d'achat à partir d'un fichier CSV procurement")
    parser.add_argument("--input", default="data/raw/sample_procurement.csv", help="Chemin du fichier CSV d'entrée")
    parser.add_argument("--output-dir", default="outputs", help="Répertoire de sortie")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input
    output_dir = root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Le fichier d'entrée est introuvable : {input_path}")

    df = pd.read_csv(input_path)
    df = normalize_columns(df)

    overall_kpis, supplier_kpis, monthly_kpis = build_kpis(df)

    overall_kpis.to_csv(output_dir / "overall_kpis.csv", index=False)
    supplier_kpis.to_csv(output_dir / "supplier_kpis.csv", index=False)
    monthly_kpis.to_csv(output_dir / "monthly_kpis.csv", index=False)

    print(f"Fichiers générés dans {output_dir}")
    print("KPI globaux :")
    print(overall_kpis.to_string(index=False))


if __name__ == "__main__":
    main()
