from django.urls import path
from .views import ExpenseCreateView, ExpenseView, ExpenseGrandTotal, ExpenseSortView

urlpatterns = [
    path('', ExpenseCreateView.as_view(), name="expenses-all"),
    path('<int:pk>/', ExpenseView.as_view(), name="expense-detail"),
    path('total/', ExpenseGrandTotal.as_view(), name="expense-total"),
    path('sort/<int:pk>/', ExpenseSortView.as_view(), name="expense-sort"), # 1 - data, 2 - name, 3 - amount  
]