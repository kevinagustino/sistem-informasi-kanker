from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from cancer_app.models import (
    Profile, CancerType, CauseCategory, 
    Cause, Prevention, Treatment
)
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ProfileSerializer, CancerTypeSerializer, CancerTypeDetailSerializer,
    CauseCategorySerializer, CauseSerializer,
    PreventionSerializer, TreatmentSerializer
)
from .permissions import IsAdminOrReadOnly
from .paginators import CustomPagination


class RegisterAPIView(generics.CreateAPIView):
    """View untuk registrasi pengguna baru"""
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': UserSerializer(user).data,
            'message': 'Registrasi berhasil. Silakan login di /api/token/.'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """View untuk login pengguna"""
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({
                'error': 'Username atau password salah'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'user': UserSerializer(user).data,
            'message': 'Login berhasil. Gunakan endpoint /api/token/ untuk mendapatkan token.'
        }, status=status.HTTP_200_OK)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """View untuk mengambil atau mengupdate profil pengguna"""
    
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    
    def get_object(self):
        return self.request.user.profile


class CancerTypeListAPIView(generics.ListCreateAPIView):
    """View untuk daftar dan pembuatan CancerType"""
    
    queryset = CancerType.objects.all()
    serializer_class = CancerTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['risk_level']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class CancerTypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View untuk detail, update, dan delete CancerType"""
    
    queryset = CancerType.objects.all()
    serializer_class = CancerTypeDetailSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Mengembalikan 200 OK dengan pesan sukses
        return Response(
            {"message": "Jenis kanker berhasil dihapus!"},
            status=status.HTTP_200_OK
        )

class CauseCategoryListAPIView(generics.ListCreateAPIView):
    """View untuk daftar dan pembuatan CauseCategory"""
    
    queryset = CauseCategory.objects.all()
    serializer_class = CauseCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class CauseCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View untuk detail, update, dan delete CauseCategory"""
    
    queryset = CauseCategory.objects.all()
    serializer_class = CauseCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)


class CauseListAPIView(generics.ListCreateAPIView):
    """View untuk daftar dan pembuatan Cause"""
    
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cancer_type', 'category']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'risk_factor']


class CauseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View untuk detail, update, dan delete Cause"""
    
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)


class PreventionListAPIView(generics.ListCreateAPIView):
    """View untuk daftar dan pembuatan Prevention"""
    
    queryset = Prevention.objects.all()
    serializer_class = PreventionSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cancer_type', 'effectiveness']
    search_fields = ['title', 'description']
    ordering_fields = ['title']


class PreventionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View untuk detail, update, dan delete Prevention"""
    
    queryset = Prevention.objects.all()
    serializer_class = PreventionSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)


class TreatmentListAPIView(generics.ListCreateAPIView):
    """View untuk daftar dan pembuatan Treatment"""
    
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cancer_type', 'treatment_type']
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class TreatmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View untuk detail, update, dan delete Treatment"""
    
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
