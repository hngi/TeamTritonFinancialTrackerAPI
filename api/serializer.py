from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from . import models


class ExpenseSerializer(serializers.ModelSerializer):
    purchase_date = serializers.DateField()
    class Meta:
        model = models.Expense
        fields = '__all__'


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=255, required=False)
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone': self.validated_data.get('phone', ''),
            'age': self.validated_data.get('age', ''),
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
        }