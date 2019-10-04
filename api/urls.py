from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
# Inlcude the schema view in our urls.
urlpatterns =[
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('monthly/', views.MonthlyViews.as_view(), name='monthly'),
    path('weekly/', views.WeeklyViews.as_view(), name='weekly'),
    path('yearly/', views.YearlyViews.as_view(), name='yearly'),
    path('items/', views.ExpenseView.as_view(), name = 'items'),
    path('expense/', views.AllExpenseView.as_view(), name='expenses'),
    path('profile/', views.UserProfile.as_view())]