from django.urls import path
from . import views


# Inlcude the schema view in our urls.
urlpatterns =[
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('items/', views.ExpenseView.as_view(), name = 'items')
]