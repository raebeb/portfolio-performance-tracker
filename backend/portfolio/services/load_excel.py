import pandas as pd
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from tqdm import tqdm
from django.db import transaction

from ..domain.models import Asset, Portfolio, Weight, Price, Holding


def load_excel_data(filepath: str):
    print(f"Reading file: {filepath}")
    xls = pd.ExcelFile(filepath)

    print("Processing Weights sheet...")
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

    print("Saving prices...")
    for fecha, row in tqdm(df_prices.iterrows(), total=len(df_prices)):
        for asset_name, price in row.items():
            if pd.isna(price) or price == 0:
                print(f"Warning: No valid price for asset {asset_name} on {fecha}")
                continue

            asset, _ = Asset.objects.get_or_create(name=asset_name)
            price_value = Decimal(str(price)).quantize(Decimal("0.0001"))

            Price.objects.update_or_create(
                asset=asset,
                date=fecha,
                defaults={"price": price_value}
            )

    V0 = Decimal("1000000000")  # 1B
    fecha_0 = date_0

    print("Calculating and saving holdings...")
    with transaction.atomic():
        for portfolio_name in ["Portafolio 1", "Portafolio 2"]:
            portfolio = Portfolio.objects.get(name=portfolio_name)

            total_weight = sum(w.weight for w in Weight.objects.filter(portfolio=portfolio))
            if not (Decimal("0.99") <= total_weight <= Decimal("1.01")):
                print(f"Warning: Weights for {portfolio_name} sum to {total_weight}, not 1.0")

            for weight in Weight.objects.filter(portfolio=portfolio):
                asset = weight.asset
                w = weight.weight

                try:
                    price_obj = Price.objects.get(asset=asset, date=fecha_0)
                    p = price_obj.price

                    # C_{i,0} = w_{i,0} * V_0 / P_{i,0}
                    quantity = (w * V0 / p).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

                    Holding.objects.update_or_create(
                        portfolio=portfolio,
                        asset=asset,
                        defaults={"quantity": quantity}
                    )
                except Price.DoesNotExist:
                    print(f"Error: No price data for asset {asset.name} on {fecha_0}")
                except Exception as e:
                    print(f"Error calculating holding for {asset.name} in {portfolio_name}: {str(e)}")

    print(f"Successfully loaded data for {Portfolio.objects.count()} portfolios and {Asset.objects.count()} assets.")
    print(f"Total holdings created: {Holding.objects.count()}")