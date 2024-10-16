from django.urls import path
from adminrental import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('rental/', views.RentalListView.as_view(), name='rental_info'),
    path("rental/search", views.RentalSearch.as_view(), name="rental_search"),
    path('rental/customer/<int:pk>', views.CustomerInfo.as_view(), name='customer_info'),
    
    path('rental/addemployee/', views.AddEmployee.as_view(), name='add_employee'),
    path('rental/employeelist/', views.EmployeeList.as_view(), name='employee_list'),
    path('rental/employeelist/delete/<int:pk>/', views.EmployeeList.as_view(), name='delete_employee'),

    path('category/', views.ManageCar.as_view(), name="manage_car"),
    path('category/<int:pk>/', views.SelectCategory.as_view(), name="catcar_id"),
    path('category/search/<int:pk>/', views.CategorySearch.as_view(), name="category_search"),

    path('category/addcar/', views.AddCar.as_view(), name="add_car"),
    path('category/editcar/<int:pk>', views.EditCar.as_view(), name="edit_car"),
    path('category/delete/<int:pk>/', views.DeleteCar.as_view(), name='delete_car')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)