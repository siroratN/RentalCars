from django.urls import path
from adminrental import views

urlpatterns = [
    path('rental/', views.RentalListView.as_view(), name='rental_info'),
    path("rental/search", views.RentalSearch.as_view(), name="rental_search"),
    
    path('category/', views.ManageCar.as_view(), name="manage_car"),
    path('category/<int:pk>/', views.SelectCategory.as_view(), name="catcar_id"),
    path('category/search/<int:pk>/', views.CategorySearch.as_view(), name="category_search"),

    path('car/addcar/', views.AddCar.as_view(), name="add_car"),
    path('car/editcar/', views.EditCar.as_view(), name="edit_car"),

]
