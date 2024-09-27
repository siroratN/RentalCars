from django.urls import path

from authen.views import *


urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="regis"),

    path('logout/', LogoutView.as_view(), name="logout")
]