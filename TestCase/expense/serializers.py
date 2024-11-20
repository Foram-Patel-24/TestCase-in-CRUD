from expense.models import Transaction
from rest_framework import serializers

class expenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','title','Transaction_type','amount']