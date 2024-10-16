from django.urls import path

from authen.views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="regis"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("changepass/", PasswordChangeView.as_view(), name="pass"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('staffprofile/', StaffProfileView.as_view(), name='staffprofile')

]