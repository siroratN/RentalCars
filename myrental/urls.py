from . import views
from django.urls import include, path
from django.views.generic import TemplateView
from django.urls import *

urlpatterns = [
    path("rental/", views.RentalView.as_view(), name="Rental"),
    path("rental/<str:start_date>/<str:end_date>/", views.RentalView.as_view(), name="RentalSearch"),
    path("car/<int:pk>/detail/", views.CarDetail.as_view(), name="CarDetail"),
    path("confirm/<int:pk>/", views.ConfirmBill.as_view(), name="confirm"),
    path("date/", views.DateRental.as_view(), name="Date"),
    path("create-checkout-session/<int:pk>/", views.CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("success/", views.Success.as_view(), name="success"),
    path("cancel/", views.Cancel.as_view(), name="cancel"),

]
