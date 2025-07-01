from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.text import slugify
from django.utils import timezone


class Profile(models.Model):
    """Model untuk menyimpan informasi profil tambahan dari pengguna"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        """Override metode save untuk melakukan resize pada gambar avatar"""
        super().save(*args, **kwargs)
        
        img = Image.open(self.avatar.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class CancerType(models.Model):
    """
    Model untuk menyimpan informasi tentang berbagai jenis kanker
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    symptoms = models.TextField()
    risk_level = models.CharField(max_length=20, choices=[
        ('LOW', 'Rendah'),
        ('MEDIUM', 'Sedang'),
        ('HIGH', 'Tinggi'),
    ], default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['name']


class CauseCategory(models.Model):
    """ Model untuk mengkategorikan penyebab kanker (misalnya: genetik, lingkungan, gaya hidup) """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Cause Categories"


class Cause(models.Model):
    """Model untuk menyimpan informasi tentang penyebab spesifik kanker """
    cancer_type = models.ForeignKey(CancerType, on_delete=models.CASCADE, related_name='causes')
    category = models.ForeignKey(CauseCategory, on_delete=models.CASCADE, related_name='causes')
    name = models.CharField(max_length=100)
    description = models.TextField()
    risk_factor = models.FloatField(default=1.0, help_text="Faktor risiko relatif")
    
    def __str__(self):
        return f"{self.name} - {self.cancer_type.name}"


class Prevention(models.Model):
    """
    Model untuk menyimpan informasi tentang pencegahan kanker
    """
    cancer_type = models.ForeignKey(CancerType, on_delete=models.CASCADE, related_name='preventions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    effectiveness = models.CharField(max_length=20, choices=[
        ('LOW', 'Rendah'),
        ('MEDIUM', 'Sedang'),
        ('HIGH', 'Tinggi'),
    ], default='MEDIUM')
    
    def __str__(self):
        return f"{self.title} - {self.cancer_type.name}"


class Treatment(models.Model):
    """
    Model untuk menyimpan informasi tentang pengobatan kanker
    """
    cancer_type = models.ForeignKey(CancerType, on_delete=models.CASCADE, related_name='treatments')
    name = models.CharField(max_length=200)
    description = models.TextField()
    side_effects = models.TextField()
    success_rate = models.CharField(max_length=100, blank=True)
    treatment_type = models.CharField(max_length=50, choices=[
        ('SURGERY', 'Operasi'),
        ('RADIATION', 'Terapi Radiasi'),
        ('CHEMOTHERAPY', 'Kemoterapi'),
        ('IMMUNOTHERAPY', 'Imunoterapi'),
        ('TARGETED', 'Terapi Target'),
        ('HORMONE', 'Terapi Hormon'),
        ('STEM_CELL', 'Transplantasi Sel Induk'),
        ('ALTERNATIVE', 'Terapi Alternatif'),
        ('OTHER', 'Lainnya'),
    ])
    
    def __str__(self):
        return f"{self.name} - {self.cancer_type.name}"