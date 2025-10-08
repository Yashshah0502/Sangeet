from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add/', views.add_product, name='add_product'),
    path('dashboard/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('dashboard/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('dashboard/orders/', views.order_list, name='order_list'),
    path('dashboard/orders/delete/<int:pk>/', views.delete_order, name='delete_order'),

]
