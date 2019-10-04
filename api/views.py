from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .serializer import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from . import models
from rest_framework import generics
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.

class UserProfile(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        username = request.user.get_username()
        users = User.objects.filter(username=username).last()
        new_user = users.__dict__
        forbidden = ['_state','password','is_superuser','is_staff']
        dic = {k:v for k,v in new_user.items() if k not in forbidden}
        dic['phone'] = users.profile.phone
        dic['limit'] = users.profile.limit
        return Response(dic)
    def put(self, request):
        username = request.user.get_username()
        phone = request.data.get('phone')
        limit = request.data.get('limit')
        users = User.objects.filter(username=username).last()
        users.profile.phone = phone
        users.profile.limit = limit
        users.save()
        new_user = users.__dict__
        forbidden = ['_state', 'password', 'is_superuser', 'is_staff']
        dic = {k: v for k, v in new_user.items() if k not in forbidden}
        dic['phone'] = users.profile.phone
        dic['limit'] = users.profile.limit
        return Response(dic)


class Dashboard(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        username = request.user.get_username()
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
    permission_classes = [IsAuthenticated, ]
    def post(self, request, *args, **kwargs):
        username = request.user.get_username()
        users = User.objects.filter(username=username).last()
        total = 0
        for i in models.Expense.objects.filter(created_by=username):
            if int(i.created_on.split('_')[1]) == datetime.now().month:
                total+= int(i.amount)
        if total > int(users.profile.limit):
            return Response({'Error':'You have reach your monthly limit'})
        else:
            serializer = ExpenseSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(created_by = self.request.user.get_username(),
                                created_on = datetime.now().strftime('%Y_%m_%d'))
                return Response(serializer.data)
            else:
                return Response('Invalid request')

class AllExpenseView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        username = request.user.get_username()
        expense = []
        try:
            for i in models.Expense.objects.filter(created_by = username):
                expense.append({'Items': i.item,
                                    'Amount':i.amount,
                                    'Description': i.description,
                                'created_on':i.created_on,
                                'purchase_date':i.purchase_date})
            return Response(dict(enumerate(expense)))

        except:
            return Response({'error':'Error occured!!'})



class MonthlyViews(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        username = request.user.get_username()
        monthly = []
        try:
            for i in models.Expense.objects.filter(created_by = username):
                if int(i.created_on.split('_')[1]) == datetime.now().month:
                    monthly.append({'Items': i.item,
                                    'Amount':i.amount,
                                    'Description': i.description})
            return Response(dict(enumerate(monthly)))
        except:
            return Response({'error': 'Error occured'}, status=status.HTTP_400_BAD_REQUEST)

class WeeklyViews(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        username = request.user.get_username()
        monthly = []
        try:
            for i in models.Expense.objects.filter(created_by = username):
                if int(i.created_on.split('_')[2]) >= datetime.now().day - 7:
                    monthly.append({'Name': i.item,
                                    'Amount':i.amount,
                                    'Description': i.description})
            return Response(dict(enumerate(monthly)))
        except:
            return Response({'error': 'Error occured'}, status=status.HTTP_400_BAD_REQUEST)

class YearlyViews(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        username = request.user.get_username()
        monthly = []
        try:
            for i in models.Expense.objects.filter(created_by = username):
                if int(i.created_on.split('_')[0]) == datetime.now().year:
                    monthly.append({'Name': i.item,
                                    'Amount':i.amount,
                                    'Description': i.description})
            return Response(dict(enumerate(monthly)))
        except:
            return Response({'error': 'Error occurred'}, status=status.HTTP_400_BAD_REQUEST)







