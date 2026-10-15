from django.urls import URLPattern

from django.urls import path

from spendings.views import ExpenseListCreateView

from spendings.views import SignUpView

from spendings.views import GetMeView

from spendings.views import ExpenseRetrieveUpdateDeleteView

from spendings.views import BudgetPlanView

from spendings.views import ExpenseSummaryView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [

    path("register/",SignUpView.as_view()),
    path("me/",GetMeView.as_view()),
    path("expenses/",ExpenseListCreateView.as_view()),
    path("expenses/summary/",ExpenseSummaryView.as_view()),

    path("expenses/<int:pk>/",ExpenseRetrieveUpdateDeleteView.as_view()),
    path("expenses/summary/",ExpenseSummaryView.as_view()),
    path("expenses/budget/",BudgetPlanView.as_view()),


    path("token/",ObtainAuthToken.as_view()),



]