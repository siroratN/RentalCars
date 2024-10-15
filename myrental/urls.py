from django.conf import settings
from . import views
from django.urls import include, path
from django.views.generic import TemplateView
from django.urls import *
from django.conf.urls.static import static
from authen.views import *

urlpatterns = [
    path("rental/", views.RentalViewFirst.as_view(), name="Rental"),
    path("rental/<str:start_date>/<str:end_date>/", views.FilterView.as_view(), name="RentalSearch"),
    path("rental/<str:start_date>/<str:end_date>/search/", views.SearchView.as_view(), name="RentalSearchBar"),
    path("rental/history", views.RentHistory.as_view(), name='Rent-History'),

    path("car/detail/<int:pk>/<str:start_date>/<str:end_date>/", views.CarDetail.as_view(), name="CarDetail"),
    
    path("confirm/<int:pk>/", views.ConfirmBill.as_view(), name="confirm"),
    
    path("date/", views.DateRental.as_view(), name="Date"),
    
    path("create-checkout-session/", views.CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    
    path("success/", views.Success.as_view(), name="success"),
    path("success/detail/", views.Success.as_view(), name="success"),
    
    path("cancel/", views.Cancel.as_view(), name="cancel"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
