from django.urls import path
from .views import ExpenseCreateView, ExpenseView, ExpenseGrandTotal

urlpatterns = [
    path('', ExpenseCreateView.as_view(), name="expenses-all"),
    path('<int:pk>/', ExpenseView.as_view(), name="expense-detail"),
    path('total/', ExpenseGrandTotal.as_view(), name="expense-total")
]
