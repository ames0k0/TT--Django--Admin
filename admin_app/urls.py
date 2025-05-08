from django.urls import path
from .views import CustomLoginView, dashboard, logout_view

app_name = 'admin_app'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
] 