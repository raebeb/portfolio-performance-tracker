import pandas as pd
from datetime import datetime
from decimal import Decimal

from ..domain.models import Asset, Portfolio, Weight, Price


def load_excel_data(filepath: str):
    print(f"Reading file: {filepath}")
    xls = pd.ExcelFile(filepath)

    print("processing Weights sheet...")
    df_weights = pd.read_excel(xls, "weights")

    df_weights.columns = ["Fecha", "Activo", "Portafolio 1", "Portafolio 2"]
    date_0 = pd.to_datetime(df_weights["Fecha"].iloc[0]).date()

    for name in ["Portafolio 1", "Portafolio 2"]:
        Portfolio.objects.get_or_create(name=name)

    for _, row in df_weights.iterrows():
        asset_name = row["Activo"]
        asset, _ = Asset.objects.get_or_create(name=asset_name)

        for portfolio_name in ["Portafolio 1", "Portafolio 2"]:
            portfolio = Portfolio.objects.get(name=portfolio_name)
            weight_value = Decimal(str(row[portfolio_name])).quantize(Decimal("0.0001"))

            Weight.objects.update_or_create(
                portfolio=portfolio,
                asset=asset,
                defaults={"weight": weight_value}
            )

    print("Processing Prices sheet...")
    df_prices = pd.read_excel(xls, "Precios")
    df_prices["Dates"] = pd.to_datetime(df_prices["Dates"]).dt.date
    df_prices.set_index("Dates", inplace=True)

    for fecha, row in df_prices.iterrows():
        for asset_name, price in row.items():
            asset, _ = Asset.objects.get_or_create(name=asset_name)
            price_value = Decimal(str(price)).quantize(Decimal("0.0001"))

            Price.objects.update_or_create(
                asset=asset,
                date=fecha,
                defaults={"price": price_value}
            )

    print("Loading completed.")
