from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/<slug:slug>/', views.product_details, name='product_details'),
    path('category/<slug:slug>/', views.home, name='category'),
]
