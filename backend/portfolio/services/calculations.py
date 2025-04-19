from datetime import date
from decimal import Decimal

from ..domain.models import Portfolio, Asset, Price, Holding

def get_prices_in_range(start_date: date, end_date: date):
    """
    return a queryset with the prices between two dates.
    """
    return Price.objects.filter(date__range=(start_date, end_date)).select_related('asset')


def get_holdings_for_portfolio(portfolio: Portfolio):
    """
    return the initial quantities of the assets for the given portfolio.
    """
    return Holding.objects.filter(portfolio=portfolio).select_related('asset')


def calculate_daily_values(portfolio: Portfolio, start_date: date, end_date: date):
    """
    get daily values for a portfolio between two dates.:
    - x_{i,t} = p_{i,t} * c_{i,0}
    - V_t = sum(x_{i,t})
    - w_{i,t} = x_{i,t} / V_t
    return a dictionary with the following structure:
    {
        '2022-02-15': {
            'total_value': V_t,
            'assets': {
                'EEUU': {
                    'price': ...,
                    'quantity': ...,
                    'value': x_{i,t},
                    'weight': w_{i,t}
                },
                ...
            }
        },
        ...
    }
    """
    result = {}

    holdings = get_holdings_for_portfolio(portfolio)
    prices = get_prices_in_range(start_date, end_date)

    prices_by_date = {}
    for price in prices:
        prices_by_date.setdefault(price.date, {})[price.asset.id] = price

    for date_key in sorted(prices_by_date.keys()):
        daily_prices = prices_by_date[date_key]
        day_data = {'total_value': Decimal(0), 'assets': {}}

        for holding in holdings:
            asset = holding.asset
            quantity = holding.quantity
            price_obj = daily_prices.get(asset.id)

            if not price_obj:
                continue

            price = price_obj.price
            value = price * quantity
            day_data['total_value'] += value

            day_data['assets'][asset.name] = {
                'price': price,
                'quantity': quantity,
                'value': value,
                'weight': Decimal(0)  # asign a default weight of 0 for now #TODO: note for myself: check if this is correct
            }

        for asset_data in day_data['assets'].values():
            asset_data['weight'] = asset_data['value'] / day_data['total_value']

        result[str(date_key)] = day_data

    return result
