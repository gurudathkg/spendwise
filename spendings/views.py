from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView
# Create your views here.
from spendings.serializers import UserSerializer
from spendings.models import Expense

from spendings.serializers import ExpenseSerializer

from django.contrib.auth.models import User

from rest_framework import authentication,permissions
from rest_framework.response import Response

from spendings.permissions import IsOwner

from spendings.ai_service import get_budget_plan

class SignUpView(APIView):

    def post(self,request):

        form_data=request.data

        serializer_instance=UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data=serializer_instance.validated_data


            instance=User.objects.create_user(**cleaned_data,owner=request.user)

            serializer_instance=UserSerializer(instance)

            return Response(data=serializer_instance.data)
        else:

            return Response(data=serializer_instance.errors)


class GetMeView(APIView):
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get(self,request):
        auth_user = request.user

        instance=User.objects.get(username=auth_user)

        serializer_instance = UserSerializer(instance)

        return Response(data=serializer_instance.data)

class ExpenseListCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        instance=Expense.objects.filter(owner=request.user)

        serializer_instance=ExpenseSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    
    def post(self,request):

        form_data=request.data

        serializer_instance=ExpenseSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

 #from rest_framework.generics import RetrieveAPIView,DestroyAPIView,UpdateAPIView
class ExpenseRetrieveUpdateDeleteView(APIView):
    #authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]

    #permission_classes=[IsOwner]

    def get(self,request,pk=None):

        #instance=Expense.objects.get(id=pk)

        instance= get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance=ExpenseSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        form_data=request.data

        serializer_instance=ExpenseSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():


            serializer_instance.save()

            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk=None):
        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"deleted"})

from datetime import datetime
from django.db.models import Sum
class ExpenseSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={
            "todays_total":0
        }

        cur_date=datetime.now().date()

        cur_year = datetime.now().year

        cur_month= datetime.now().month

        #monthly summary

        monthly_transactions=Expense.objects.filter(
            owner=request.user,
            created_at__month=cur_month,
            created_at__year=cur_year,
        )

        if monthly_transactions:
            monthly_total=monthly_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            response_data["monthly_total"]=monthly_total

        todays_transactions=Expense.objects.filter(
            owner=request.user,
            created_at__date=cur_date,
        )
        
        if todays_transactions:
            todays_total= todays_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            category_summary=todays_transactions.values("category").annotate(total=Sum("amount"))

            response_data["todays_total"]=todays_total

            response_data["category_summary"]=category_summary

        return Response(data=response_data)




class BudgetPlanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        user=request.user

        cur_date=datetime.now().date()
        cur_year=datetime.now().year
        cur_month=datetime.now().month

        response_data={
            "daily_Expense_Total":0,
            "Monthly_Total":0
                  
        }

        monthly_transactions=Expense.objects.filter(owner=user,created_at__year=cur_year,created_at__month=cur_month)

        if monthly_transactions:
            monthly_total=monthly_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            response_data["monthly_total"]=monthly_total

            category_summary=monthly_transactions.values("category").annotate(total=Sum("amount"))

            response_data["category_summary"]=category_summary

            
            response_data["budget_plan"] = get_budget_plan(response_data)
        return Response(response_data)    
    
        