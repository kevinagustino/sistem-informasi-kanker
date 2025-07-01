from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CancerType, CauseCategory, Cause, Prevention, Treatment

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.cancer_type = CancerType.objects.create(
            name='Kanker Paru-paru',
            description='Deskripsi kanker paru-paru',
            symptoms='Gejala kanker paru-paru',
            risk_level='HIGH'
        )
        
        self.cause_category = CauseCategory.objects.create(
            name='Lingkungan',
            description='Faktor lingkungan'
        )
        
        self.cause = Cause.objects.create(
            cancer_type=self.cancer_type,
            category=self.cause_category,
            name='Merokok',
            description='Merokok meningkatkan risiko kanker paru-paru',
            risk_factor=2.5
        )
        
        self.prevention = Prevention.objects.create(
            cancer_type=self.cancer_type,
            title='Berhenti Merokok',
            description='Berhenti merokok dapat mengurangi risiko',
            effectiveness='HIGH'
        )
        
        self.treatment = Treatment.objects.create(
            cancer_type=self.cancer_type,
            name='Kemoterapi',
            description='Deskripsi kemoterapi',
            side_effects='Efek samping kemoterapi',
            treatment_type='CHEMOTHERAPY'
        )
    
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/index.html')
        self.assertContains(response, 'Kanker Paru-paru')
    
    def test_cancer_type_list_view(self):
        response = self.client.get(reverse('cancer_type_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/cancer_type_list.html')
        self.assertContains(response, 'Kanker Paru-paru')
    
    def test_cancer_type_detail_view(self):
        response = self.client.get(
            reverse('cancer_type_detail', kwargs={'slug': self.cancer_type.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/cancer_type_detail.html')
        self.assertContains(response, 'Kanker Paru-paru')
        self.assertContains(response, 'Merokok')
        self.assertContains(response, 'Berhenti Merokok')
        self.assertContains(response, 'Kemoterapi')
    
    def test_cancer_type_create_view_unauthorized(self):
        response = self.client.get(reverse('cancer_type_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_cancer_type_create_view_authorized(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('cancer_type_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/cancer_type_form.html')
    
    def test_cancer_type_create_post(self):
        self.client.login(username='admin', password='adminpassword')
        data = {
            'name': 'Kanker Kulit',
            'description': 'Deskripsi kanker kulit',
            'symptoms': 'Gejala kanker kulit',
            'risk_level': 'MEDIUM'
        }
        response = self.client.post(reverse('cancer_type_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(CancerType.objects.filter(name='Kanker Kulit').exists())
    
    def test_cancer_type_update_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            reverse('cancer_type_update', kwargs={'slug': self.cancer_type.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/cancer_type_form.html')
    
    def test_cancer_type_update_post(self):
        self.client.login(username='admin', password='adminpassword')
        data = {
            'name': 'Kanker Paru-paru Updated',
            'description': 'Deskripsi updated',
            'symptoms': 'Gejala updated',
            'risk_level': 'MEDIUM'
        }
        response = self.client.post(
            reverse('cancer_type_update', kwargs={'slug': self.cancer_type.slug}),
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.cancer_type.refresh_from_db()
        self.assertEqual(self.cancer_type.name, 'Kanker Paru-paru Updated')
    
    def test_cancer_type_delete_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            reverse('cancer_type_delete', kwargs={'slug': self.cancer_type.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/cancer_type_confirm_delete.html')
    
    def test_cancer_type_delete_post(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            reverse('cancer_type_delete', kwargs={'slug': self.cancer_type.slug})
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(CancerType.objects.filter(pk=self.cancer_type.pk).exists())
    
    def test_user_list_view_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/user_list.html')
        self.assertContains(response, 'admin')
        self.assertContains(response, 'testuser')
    
    def test_user_list_view_normal_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 302)  # Redirect away (not authorized)
    
    def test_user_detail_view_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            reverse('user_detail', kwargs={'pk': self.normal_user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/user_detail.html')
        self.assertContains(response, 'testuser')
    
    def test_user_detail_view_own_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('user_detail', kwargs={'pk': self.normal_user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/user_detail.html')
    
    def test_user_detail_view_other_profile_unauthorized(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('user_detail', kwargs={'pk': self.admin_user.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirect away (not authorized)
    
    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('user_update', kwargs={'pk': self.normal_user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/user_form.html')
    
    def test_user_update_post(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': 'updated_user',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.post(
            reverse('user_update', kwargs={'pk': self.normal_user.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.username, 'updated_user')
        self.assertEqual(self.normal_user.email, 'updated@example.com')
    
    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('user_delete', kwargs={'pk': self.normal_user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancer_app/user_confirm_delete.html')
    
    def test_user_delete_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': self.normal_user.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(User.objects.filter(pk=self.normal_user.pk).exists())