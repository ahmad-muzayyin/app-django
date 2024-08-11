from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 
# from .decorators import login_perlindungan
from django.contrib.auth import views as auth_views


urlpatterns = [

# URL untuk login admin dengan trailing slash
    path('', views.login_mahasiswa, name='loginmahasiswa'),
    # 
    path('hello/', views.hello, name='helloadmin'),
    
    
    path('mahasiswa/dashboard/', views.mahasiswa_dashboard, name='mahasiswa_dashboard'),
    path('daftar_calon_anggota', views.daftar_calon, name='daftar_calon'),
    path('calon_anggota_bem', views.calon_list, name='calon_list'),
    path('jadwal_wawancara', views.wawancara_list, name='jadwal_wawancara'),
    path('delete-calon/<int:calon_id>/', views.delete_calon, name='delete_calon'),

    path('hasil-wawancara/', views.wawancarahasil_list, name='wawancara_list'),

    path('logout/', auth_views.LogoutView.as_view(next_page='loginmahasiswa'), name='logoutmahasiswa'),
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)