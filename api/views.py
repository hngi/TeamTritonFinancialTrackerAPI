from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .serializer import ExpenseSerializer
from . import models
from rest_framework import generics
from rest_framework import status

# Create your views here.

class Dashboard(APIView):
    def get(self, request):
        username = 'cy'#request.user.get_username()
        weekly,yearly, monthly = 0,0,0
        try:
            for i in models.Expense.objects.filter(created_by = username):
                if int(i.created_on.split('_')[1]) == datetime.now().month:
                    monthly += i.amount
                if int(i.created_on.split('_')[0]) == datetime.now().year:
                    yearly += i.amount
                if int(i.created_on.split('_')[2]) >= datetime.now().day - 7:
                    weekly += i.amount
            sub = {'username': username,
                'weekly':weekly,
                   'monthly':monthly,
                   'yearly': yearly}
            return Response(sub, status=status.HTTP_200_OK)
        except:
            return Response({'error':'Error occured'}, status=status.HTTP_400_BAD_REQUEST)

class ExpenseView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = models.Expense

    def perform_create(self, serializer):
        serializer.save(
            created_by = self.request.user.get_username(),
            created_on = datetime.now().strftime('%Y_%m_%d')
        )



