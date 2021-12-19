from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginApiVew.as_view(), name='login'),
    path('refresh/', views.RefreshApiView.as_view(), name='refresh'),
    path('employee-create/', views.CreateEmployeeApiView.as_view(), name='employee-create'),
    path('employee-list/', views.EmployeeListApiView.as_view(), name='employee-list'),
    path('delete-employee/<int:id>/', views.DeleteEmployeeApiView.as_view(), name='delete-employee'),
    path('hold-employee/<int:id>/', views.HoldEmployeeApiView.as_view(), name='hold-employee'),
    path('employee-detail/<int:id>/', views.EmployeeDetailApiView.as_view(), name='employee-detail'),
    path('profile/<int:id>/', views.ProfileApiView.as_view(), name='profile'),
]
