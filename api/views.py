from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .serializer import ExpenseSerializer, ChangePasswordSerializer
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
        forbidden = ['_state', 'password', 'is_superuser', 'is_staff']
        dic = {k: v for k, v in new_user.items() if k not in forbidden}
        dic['phone'] = users.profile.phone
        dic['limit'] = users.profile.limit
        return Response(dic, status=status.HTTP_200_OK)

    def put(self, request):
        username = request.user.get_username()
        phone = request.data.get('phone')
        limit = request.data.get('limit')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not phone:
            phone = request.user.profile.phone
        if not limit:
            limit = request.user.profile.limit
        if not email:
            email = request.user.email
        if not first_name:
            first_name = request.user.first_name
        if not last_name:
            last_name = request.user.last_name
        users = User.objects.filter(username=username).last()
        users.profile.phone = phone
        users.profile.limit = limit
        users.email = email
        users.first_name = first_name
        users.last_name = last_name
        users.save()
        return Response(request.data, status=status.HTTP_200_OK)


class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'success': 'Password changed succesfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Dashboard(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        username = request.user.get_username()
        weekly, yearly, monthly = 0, 0, 0
        try:
            for i in models.Expense.objects.filter(created_by=username):
                if int(i.created_on.split('_')[1]) == datetime.now().month:
                    monthly += i.amount
                if int(i.created_on.split('_')[0]) == datetime.now().year:
                    yearly += i.amount
                if int(i.created_on.split('_')[2]) >= datetime.now().day - 7:
                    weekly += i.amount
            sub = {'username': username,
                   'weekly': weekly,
                   'monthly': monthly,
                   'yearly': yearly}
            return Response(sub, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Error occured'}, status=status.HTTP_400_BAD_REQUEST)


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
                total += int(i.amount)
        if total > int(users.profile.limit):
            return Response({'Error': 'You have reach your monthly limit'})
        else:
            serializer = ExpenseSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(created_by=self.request.user.get_username(),
                                created_on=datetime.now().strftime('%Y_%m_%d'))
                return Response(serializer.data)
            else:
                return Response('Invalid request')


class AllExpenseView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        username = request.user.get_username()
        expense = []
        try:
            for i in models.Expense.objects.filter(created_by=username):
                expense.append({'Items': i.item,
                                'Amount': i.amount,
                                'Description': i.description})
            return Response(dict(enumerate(expense)))

        except:
            return Response({'error': 'Error occured!!'})


class MonthlyViews(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        username = request.user.get_username()
        monthly = []
        try:
            for i in models.Expense.objects.filter(created_by=username):
                if int(i.created_on.split('_')[1]) == datetime.now().month:
                    monthly.append({'Items': i.item,
                                    'Amount': i.amount,
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
            for i in models.Expense.objects.filter(created_by=username):
                if int(i.created_on.split('_')[2]) >= datetime.now().day - 7:
                    monthly.append({'Name': i.item,
                                    'Amount': i.amount,
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
            for i in models.Expense.objects.filter(created_by=username):
                if int(i.created_on.split('_')[0]) == datetime.now().year:
                    monthly.append({'Name': i.item,
                                    'Amount': i.amount,
                                    'Description': i.description})
            return Response(dict(enumerate(monthly)))
        except:
            return Response({'error': 'Error occurred'}, status=status.HTTP_400_BAD_REQUEST)
