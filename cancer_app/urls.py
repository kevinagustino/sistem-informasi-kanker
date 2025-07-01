from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cancer-types/', views.cancer_type_list, name='cancer_type_list'),
    path('cancer-types/new/', views.cancer_type_create, name='cancer_type_create'),
    path('cancer-types/<slug:slug>/', views.cancer_type_detail, name='cancer_type_detail'),
    path('cancer-types/<slug:slug>/update/', views.cancer_type_update, name='cancer_type_update'),
    path('cancer-types/<slug:slug>/delete/', views.cancer_type_delete, name='cancer_type_delete'),
    path('causes/', views.cause_list, name='cause_list'),
    path('preventions/', views.prevention_list, name='prevention_list'),
    path('treatments/', views.treatment_list, name='treatment_list'),
    path('about/', views.about, name='about'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]