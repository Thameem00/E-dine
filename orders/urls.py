from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # API endpoints
    path('api/orders/<int:pk>/update-status/', views.update_order_status, name='update-order-status'),
    path('api/orders/<int:pk>/', views.OrderAPIDetail.as_view(), name='order-api-detail'),
    path('api/orders/', views.OrderAPIList.as_view(), name='order-api-list'),
    
    # Regular views
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('staff/dashboard/', views.StaffDashboardView.as_view(), name='staff-dashboard'),
]