from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 
# from .decorators import login_perlindungan
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [

# URL untuk login admin dengan trailing slash
    path('', views.login_admin, name='loginadmin'),
    path('beranda-admin/', views.beranda_admin, name='berandaadmin'),

    path('program-studi/', views.program_studi_list, name='program_studi_list'),
    path('program-studi/create/', views.create_program_studi, name='create_program_studi'),
    path('program-studi/update/<int:pk>/', views.update_program_studi, name='update_program_studi'),
    path('program-studi/delete/<int:pk>/', views.delete_program_studi, name='delete_program_studi'),

    path('semesters/', views.semester_list, name='semester_list'),
    path('add-semester/', views.add_semester, name='add_semester'),
    path('edit-semester/<int:pk>/', views.edit_semester, name='edit_semester'),
    path('delete-semester/<int:pk>/', views.delete_semester, name='delete_semester'),

    path('mahasiswa/', views.mahasiswa_list, name='mahasiswa_list'),
    path('add-mahasiswa/create', views.mahasiswa_create, name='mahasiswa_create'),
    path('edit-mahasiswa/<int:pk>/', views.mahasiswa_update, name='mahasiswa_update'),
    path('delete-mahasiswa/<int:pk>/', views.mahasiswa_delete, name='mahasiswa_delete'),
    path('download-mahasiswa-format/', views.download_mahasiswa_format, name='mahasiswa_format'),
     path('import-mahasiswa/', views.import_mahasiswa, name='import_mahasiswa'),
    path('import-success/', TemplateView.as_view(template_name=""), name='import_success'),
    

    path('datalatih/', views.datalatih_list, name='datalatih_list'),
    path('import/', views.import_datalatih, name='import_datalatih'),
    path('delete/', views.delete_datalatih, name='delete_datalatih'),

    path('calonanggota/', views.calon_anggota_list, name='calonanggota_list'),
    path('calonanggota/<int:calon_id>/update_publish_status/', views.update_publish_status, name='update_publish_status'),

    path('wawancaralistinformasi/', views.wawancara_list, name='wawancara_list_informasi'),
    path('add-wawancara/', views.add_wawancara, name='add_wawancara'),
    path('edit-wawancara/<int:pk>/', views.wawancara_update, name='wawancara_update'),
    path('delete-wawancara/<int:pk>/', views.delete_wawancarainfo, name='infowawancara_delete'),
  
    path('logout/', auth_views.LogoutView.as_view(next_page='loginadmin'), name='logoutadmin'),

    path('hasil-wawancara/', views.hasil_wawancara_list, name='hasil_wawancara_list'),
    path('hasil-wawancara/create/', views.hasil_wawancara_create, name='hasil_wawancara_create'),
    path('<int:pk>/delete/', views.hasil_wawancara_delete, name='hasil_wawancara_delete'),
    # path('hasil-wawancara/<int:pk>/update/', views.hasil_wawancara_update, name='hasil_wawancara_update'),
    # path('hasil-wawancara/<int:pk>/delete/', views.hasil_wawancara_delete, name='hasil_wawancara_delete'),
    path('fakultas/', views.fakultas_list, name='fakultas_list'),
    path('fakultas/create/', views.create_fakultas, name='create_fakultas'),
    path('fakultas/<int:pk>/update/', views.update_fakultas, name='update_fakultas'),
    path('fakultas/<int:pk>/delete/', views.delete_fakultas, name='delete_fakultas'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
