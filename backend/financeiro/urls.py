from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, VendaViewSet, CompraViewSet, ContaPagarViewSet,
    ContaReceberViewSet, RelatorioFinanceiroViewSet
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'contas-pagar', ContaPagarViewSet)
router.register(r'contas-receber', ContaReceberViewSet)
router.register(r'relatorios', RelatorioFinanceiroViewSet, basename='relatorios')

urlpatterns = [
    path('', include(router.urls)),
]

