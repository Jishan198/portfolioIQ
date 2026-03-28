from rest_framework import serializers
from .models import Portfolio, Holding
from .services import get_live_stock_data
from decimal import Decimal

class HoldingSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField()
    current_value = serializers.SerializerMethodField()
    profit_loss = serializers.SerializerMethodField()

    class Meta:
        model = Holding
        fields = ['id', 'ticker', 'quantity', 'buy_price', 'buy_date', 'current_price', 'current_value', 'profit_loss']

    def get_current_price(self, obj):
        data = get_live_stock_data(obj.ticker)
        return data['current_price'] if data else obj.buy_price

    def get_current_value(self, obj):
        price = self.get_current_price(obj)
        return round(Decimal(str(price)) * obj.quantity, 2)

    def get_profit_loss(self, obj):
        current_value = self.get_current_value(obj)
        total_cost = obj.buy_price * obj.quantity
        return round(current_value - total_cost, 2)

class PortfolioSerializer(serializers.ModelSerializer):
    holdings = HoldingSerializer(many=True, read_only=True)
    total_portfolio_value = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'created_at', 'holdings', 'total_portfolio_value']

    def get_total_portfolio_value(self, obj):
        # Sum up the current value of all holdings in this portfolio
        holdings = obj.holdings.all()
        if not holdings:
            return 0.00
        
        total = sum([HoldingSerializer(h).get_current_value(h) for h in holdings])
        return total