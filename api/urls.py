# api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth endpoints
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),

    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Cancer types
    path('cancer-types/', views.CancerTypeListAPIView.as_view(), name='cancer-types-list'),
    path('cancer-types/<slug:slug>/', views.CancerTypeDetailAPIView.as_view(), name='cancer-types-detail'),

    # Cause categories
    path('cause-categories/', views.CauseCategoryListAPIView.as_view(), name='cause-categories-list'),
    path('cause-categories/<int:pk>/', views.CauseCategoryDetailAPIView.as_view(), name='cause-categories-detail'),

    # Causes
    path('causes/', views.CauseListAPIView.as_view(), name='causes-list'),
    path('causes/<int:pk>/', views.CauseDetailAPIView.as_view(), name='causes-detail'),

    # Preventions
    path('preventions/', views.PreventionListAPIView.as_view(), name='preventions-list'),
    path('preventions/<int:pk>/', views.PreventionDetailAPIView.as_view(), name='preventions-detail'),

    # Treatments
    path('treatments/', views.TreatmentListAPIView.as_view(), name='treatments-list'),
    path('treatments/<int:pk>/', views.TreatmentDetailAPIView.as_view(), name='treatments-detail'),
]
# Hapus baris berikut jika ada di sini:
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)