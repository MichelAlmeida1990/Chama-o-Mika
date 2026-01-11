from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, VendaViewSet, CompraViewSet, ContaPagarViewSet,
    ContaReceberViewSet, RelatorioFinanceiroViewSet
)
from .enhanced_views import EnhancedRelatorioViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'contas-pagar', ContaPagarViewSet)
router.register(r'contas-receber', ContaReceberViewSet)
router.register(r'relatorios', RelatorioFinanceiroViewSet, basename='relatorios')
router.register(r'relatorios-avancados', EnhancedRelatorioViewSet, basename='relatorios-avancados')

urlpatterns = [
    path('', include(router.urls)),
]

