from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('students/search/', views.student_search, name='student_search'),
    path('register/<int:student_id>/', views.register_course, name='register_course'),  # เพิ่มการรับ student_id
    path('registration_list/', views.registration_list, name='registration_list'),
]
