from django import forms

ORDER_TYPES = [('market', 'Market')]
FEE_TIERS = [('tier_1', 'Tier 1'), ('tier_2', 'Tier 2'), ('tier_3', 'Tier 3')]

class TradeInputForm(forms.Form):
    exchange = forms.CharField(initial='OKX', disabled=True)
    symbol = forms.CharField(initial='BTC-USDT-SWAP')
    order_type = forms.ChoiceField(choices=ORDER_TYPES, initial='market')
    quantity_usd = forms.DecimalField(min_value=1, initial=100)
    volatility = forms.DecimalField(min_value=0, initial=0.5)
    fee_tier = forms.ChoiceField(choices=FEE_TIERS, initial='tier_1')
