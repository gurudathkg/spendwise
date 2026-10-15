from rest_framework import serializers
from spendings.models import Expense
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["id","username","email","password"]

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:

        model=Expense

        fields = '__all__'
        read_only_fields=["id","owner","created_at","updated_at"]
