from django.contrib import admin
from .models import (
    Profile, CancerType, CauseCategory, 
    Cause, Prevention, Treatment
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_joined')
    search_fields = ('user__username', 'user__email')


@admin.register(CancerType)
class CancerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'risk_level', 'created_at', 'updated_at')
    list_filter = ('risk_level',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CauseCategory)
class CauseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')


@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ('name', 'cancer_type', 'category', 'risk_factor')
    list_filter = ('cancer_type', 'category')
    search_fields = ('name', 'description')


@admin.register(Prevention)
class PreventionAdmin(admin.ModelAdmin):
    list_display = ('title', 'cancer_type', 'effectiveness')
    list_filter = ('cancer_type', 'effectiveness')
    search_fields = ('title', 'description')


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'cancer_type', 'treatment_type')
    list_filter = ('cancer_type', 'treatment_type')
    search_fields = ('name', 'description')
