from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CancerType, CauseCategory, Cause, Prevention, Treatment
from .forms import CancerTypeForm, UserUpdateForm
from django.http import JsonResponse 

def index(request):
    """View untuk halaman beranda"""
    cancer_types = CancerType.objects.all()[:5]  # ambil 5 jenis kanker
    context = {
        'cancer_types': cancer_types,
        'title': 'Beranda - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/index.html', context)

def cancer_type_list(request):
    """View untuk menampilkan daftar jenis kanker"""
    cancer_types = CancerType.objects.all()
    context = {
        'cancer_types': cancer_types,
        'title': 'Jenis Kanker - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/cancer_type_list.html', context)

def cancer_type_detail(request, slug):
    """View untuk menampilkan detail jenis kanker"""
    cancer_type = get_object_or_404(CancerType, slug=slug)
    causes = cancer_type.causes.all()
    preventions = cancer_type.preventions.all()
    treatments = cancer_type.treatments.all()
   
    context = {
        'cancer_type': cancer_type,
        'causes': causes,
        'preventions': preventions,
        'treatments': treatments,
        'title': f'{cancer_type.name} - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/cancer_type_detail.html', context)

@login_required
def cancer_type_create(request):
    """View untuk membuat jenis kanker baru"""
    if request.method == 'POST':
        form = CancerTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jenis kanker berhasil ditambahkan!')
            return redirect('cancer_type_list')
    else:
        form = CancerTypeForm()
    
    context = {
        'form': form,
        'title': 'Tambah Jenis Kanker - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/cancer_type_form.html', context)

@login_required
def cancer_type_update(request, slug):
    """View untuk mengupdate jenis kanker"""
    cancer_type = get_object_or_404(CancerType, slug=slug)
    
    if request.method == 'POST':
        form = CancerTypeForm(request.POST, instance=cancer_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jenis kanker berhasil diperbarui!')
            return redirect('cancer_type_detail', slug=cancer_type.slug)
    else:
        form = CancerTypeForm(instance=cancer_type)
    
    context = {
        'form': form,
        'cancer_type': cancer_type,
        'title': f'Edit {cancer_type.name} - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/cancer_type_form.html', context)


@login_required
def cancer_type_delete(request, slug):
    """View untuk menghapus jenis kanker"""
    cancer_type = get_object_or_404(CancerType, slug=slug)
    
    if request.method == 'POST':
        cancer_type.delete()
        
        # Cek apakah permintaan adalah AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'message': 'Jenis kanker berhasil dihapus!',
                'deleted_id': cancer_type.id
            }, status=200)
        
        # Jika bukan AJAX, tampilkan pesan sukses dan redirect
        messages.success(request, 'Jenis kanker berhasil dihapus!')
        return redirect('cancer_type_list')
    
    context = {
        'cancer_type': cancer_type,
        'title': f'Hapus {cancer_type.name} - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/cancer_type_confirm_delete.html', context)


@login_required
def user_list(request):
    """View untuk menampilkan daftar pengguna"""
    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki izin untuk mengakses halaman ini!')
        return redirect('index')
    
    users = User.objects.all()
    context = {
        'users': users,
        'title': 'Daftar Pengguna - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/user_list.html', context)

@login_required
def user_detail(request, pk):
    """View untuk menampilkan detail pengguna"""
    if not request.user.is_staff and request.user.id != pk:
        messages.error(request, 'Anda tidak memiliki izin untuk mengakses halaman ini!')
        return redirect('index')
    
    user = get_object_or_404(User, pk=pk)
    context = {
        'user_detail': user,
        'title': f'Profil {user.username} - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/user_detail.html', context)

@login_required
def user_update(request, pk):
    """View untuk mengupdate pengguna"""
    if not request.user.is_staff and request.user.id != pk:
        messages.error(request, 'Anda tidak memiliki izin untuk mengakses halaman ini!')
        return redirect('index')
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil pengguna berhasil diperbarui!')
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserUpdateForm(instance=user)
    
    context = {
        'form': form,
        'user_detail': user,
        'title': f'Edit Profil {user.username} - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/user_form.html', context)

@login_required
def user_delete(request, pk):
    """View untuk menghapus pengguna"""
    if not request.user.is_staff and request.user.id != pk:
        messages.error(request, 'Anda tidak memiliki izin untuk mengakses halaman ini!')
        return redirect('index')
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Pengguna berhasil dihapus!')
        if request.user.id == pk:
            return redirect('logout')
        return redirect('user_list')
    
    context = {
        'user_detail': user,
        'title': f'Hapus Pengguna {user.username} - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/user_confirm_delete.html', context)

def cause_list(request):
    """View untuk menampilkan daftar penyebab kanker"""
    categories = CauseCategory.objects.all()
    context = {
        'categories': categories,
        'title': 'Penyebab Kanker - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/cause_list.html', context)

def prevention_list(request):
    """View untuk menampilkan daftar pencegahan kanker"""
    preventions = Prevention.objects.all()
    context = {
        'preventions': preventions,
        'title': 'Pencegahan Kanker - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/prevention_list.html', context)

def treatment_list(request):
    """View untuk menampilkan daftar pengobatan kanker"""
    treatments = Treatment.objects.all()
    context = {
        'treatments': treatments,
        'title': 'Pengobatan Kanker - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/treatment_list.html', context)

def about(request):
    """View untuk halaman tentang"""
    context = {
        'title': 'Tentang - Sistem Informasi Kanker'
    }
    return render(request, 'cancer_app/about.html', context)