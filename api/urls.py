<<<<<<< HEAD
from django.urls import path
from . import views
=======
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
>>>>>>> f272bdc1837cb9baf669b7ca43add7f07b2b14b6

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

<<<<<<< HEAD
# Inlcude the schema view in our urls.
urlpatterns =[
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('monthly/', views.MonthlyViews.as_view(), name='monthly'),
    path('weekly/', views.WeeklyViews.as_view(), name='weekly'),
    path('yearly/', views.YearlyViews.as_view(), name='yearly'),
    path('items/', views.ExpenseView.as_view(), name = 'items'),
    path('expense/', views.AllExpenseView.as_view(), name='expenses'),
    path('profile/', views.UserProfile.as_view())
=======
class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a user instance.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^users/', include(router.urls)),
]

# Create our schema's view w/ the get_schema_view() helper method. Pass in the proper Renderers for swagger
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

# Inlcude the schema view in our urls.
urlpatterns = [
    url(r'^', schema_view, name="docs"),
    url(r'^users/', include(router.urls)),
>>>>>>> f272bdc1837cb9baf669b7ca43add7f07b2b14b6
]