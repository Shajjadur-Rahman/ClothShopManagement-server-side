from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.TaskCreateApiView.as_view(), name='create'),
    path('task-list/', views.TaskListApiView.as_view(), name='task-list'),
    path('all-employee-task/', views.AllEmployeeTaskListApiView.as_view(), name='all-employee-task'),
    path('task-complete/<int:id>/', views.TaskCompleteApiView.as_view(), name='task-complete'),
    path('update-task/<int:id>/', views.UpdateTaskApiView.as_view(), name='update-task'),
    path('delete-task/<int:id>/', views.DeteTaskApiView.as_view(), name='delete-task'),
]
