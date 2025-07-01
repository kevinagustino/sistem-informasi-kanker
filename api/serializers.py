from rest_framework import serializers
from django.contrib.auth.models import User
from cancer_app.models import (
    Profile, CancerType, CauseCategory, 
    Cause, Prevention, Treatment
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer untuk model User"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer untuk registrasi pengguna baru"""
    
    password = serializers.CharField(
        max_length=128, 
        min_length=8, 
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        """Metode untuk membuat dan mengembalikan user baru"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer untuk login pengguna"""
    
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=128, 
        write_only=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        fields = ('username', 'password', 'token')


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer untuk model Profile"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'username', 'avatar', 'bio', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class CancerTypeSerializer(serializers.ModelSerializer):
    """Serializer untuk model CancerType"""
    
    class Meta:
        model = CancerType
        fields = ('id', 'name', 'slug', 'description', 'symptoms', 
                 'risk_level', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


class CauseCategorySerializer(serializers.ModelSerializer):
    """Serializer untuk model CauseCategory"""
    
    class Meta:
        model = CauseCategory
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class CauseSerializer(serializers.ModelSerializer):
    """Serializer untuk model Cause"""
    
    cancer_type_name = serializers.CharField(source='cancer_type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Cause
        fields = ('id', 'cancer_type', 'category', 'name', 'description', 
                 'risk_factor', 'cancer_type_name', 'category_name')
        read_only_fields = ('id',)


class PreventionSerializer(serializers.ModelSerializer):
    """Serializer untuk model Prevention"""
    
    cancer_type_name = serializers.CharField(source='cancer_type.name', read_only=True)
    
    class Meta:
        model = Prevention
        fields = ('id', 'cancer_type', 'title', 'description', 
                 'effectiveness', 'cancer_type_name')
        read_only_fields = ('id',)


class TreatmentSerializer(serializers.ModelSerializer):
    """Serializer untuk model Treatment"""
    
    cancer_type_name = serializers.CharField(source='cancer_type.name', read_only=True)
    
    class Meta:
        model = Treatment
        fields = ('id', 'cancer_type', 'name', 'description', 'side_effects',
                 'success_rate', 'treatment_type', 'cancer_type_name')
        read_only_fields = ('id',)


class CancerTypeDetailSerializer(CancerTypeSerializer):
    """Serializer detail untuk model CancerType dengan relasi"""
    
    causes = CauseSerializer(many=True, read_only=True)
    preventions = PreventionSerializer(many=True, read_only=True)
    treatments = TreatmentSerializer(many=True, read_only=True)
    
    class Meta(CancerTypeSerializer.Meta):
        fields = CancerTypeSerializer.Meta.fields + ('causes', 'preventions', 'treatments')
