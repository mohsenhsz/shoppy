from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='create'),
    path('<int:order_id>/', views.order_details, name='details'),
    path('<int:order_id>/<int:price>/', views.payment, name='payment'),
    path('verify/', views.verify, name='verify'),
]
