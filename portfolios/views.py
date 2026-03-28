from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, Holding
from .serializers import PortfolioSerializer, HoldingSerializer
import datetime


# --- REST API VIEWS ---
class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HoldingViewSet(viewsets.ModelViewSet):
    serializer_class = HoldingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Holding.objects.filter(portfolio__user=self.request.user)


# --- WEB DASHBOARD VIEW ---
@login_required(login_url='/api/v1/auth/login/')
def main_dashboard(request):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user).first()
    holdings = Holding.objects.filter(portfolio=portfolio) if portfolio else []

    total_invested = 0
    current_value = 0

    for holding in holdings:
        total_invested += (holding.quantity * holding.buy_price)
        live_price = getattr(holding, 'current_price', holding.buy_price)
        current_value += (holding.quantity * live_price)

    total_pl = current_value - total_invested
    pl_percentage = round((total_pl / total_invested * 100), 2) if total_invested > 0 else 0

    context = {
        'portfolio': portfolio,
        'holdings': holdings,
        'total_invested': round(total_invested, 2),
        'current_value': round(current_value, 2),
        'total_pl': round(total_pl, 2),
        'pl_percentage': pl_percentage,
    }
    return render(request, 'dashboard.html', context)


# --- ADD HOLDING VIEW ---
@login_required(login_url='/api/v1/auth/login/')
def add_holding(request):
    if request.method == 'POST':
        user = request.user

        # Auto-create portfolio if it doesn't exist
        portfolio, _ = Portfolio.objects.get_or_create(
            user=user,
            defaults={'name': 'My Portfolio'}
        )

        ticker = request.POST.get('ticker', '').strip().upper()
        quantity = request.POST.get('quantity', '0')
        buy_price = request.POST.get('buy_price', '0')
        buy_date = request.POST.get('buy_date') or datetime.date.today()

        if not ticker:
            return HttpResponse("Ticker is required.", status=400)

        Holding.objects.create(
            portfolio=portfolio,
            ticker=ticker,
            quantity=quantity,
            buy_price=buy_price,
            buy_date=buy_date
        )

    # Always return updated holdings partial
    user = request.user
    portfolio = Portfolio.objects.filter(user=user).first()
    holdings = list(Holding.objects.filter(portfolio=portfolio)) if portfolio else []
    return render(request, 'partials/holdings_table.html', {'holdings': holdings})


# --- DELETE HOLDING VIEW ---
@login_required(login_url='/api/v1/auth/login/')
def delete_holding(request, pk):
    try:
        holding = Holding.objects.get(pk=pk, portfolio__user=request.user)
        holding.delete()
    except Holding.DoesNotExist:
        pass

    user = request.user
    portfolio = Portfolio.objects.filter(user=user).first()
    holdings = list(Holding.objects.filter(portfolio=portfolio)) if portfolio else []
    return render(request, 'partials/holdings_table.html', {'holdings': holdings})