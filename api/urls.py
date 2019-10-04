from django.urls import path
from . import views


# Inlcude the schema view in our urls.
urlpatterns =[
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('monthly/', views.MonthlyViews.as_view(), name='monthly'),
    path('weekly/', views.WeeklyViews.as_view(), name='weekly'),
    path('yearly/', views.YearlyViews.as_view(), name='yearly'),
    path('items/', views.ExpenseView.as_view(), name = 'items'),
    path('expense/', views.AllExpenseView.as_view(), name='expenses'),
    path('profile/', views.UserProfile.as_view())
]