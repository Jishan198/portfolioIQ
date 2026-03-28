from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet, HoldingViewSet, add_holding, delete_holding

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'holdings', HoldingViewSet, basename='holding')

urlpatterns = [
    path('', include(router.urls)),
    path('holdings/add/', add_holding, name='add_holding'),
    path('holdings/delete/<int:pk>/', delete_holding, name='delete_holding'),

]