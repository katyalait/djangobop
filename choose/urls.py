
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('see-all', views.allimages, name='allimages'),
    path('<int:image_id>/', views.image_detail, name='image_detail'),
    path('new', views.process_form, name='process_form'),

]
