from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from administrator.models import Mahasiswa,CalonAnggota,DataLatih,PengumumanWawancara,HasilWawancara
from administrator.forms import CalonBemForm
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from django.shortcuts import get_object_or_404
def hello(request):
    return render(request, 'hello.html')
def login_mahasiswa(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to mahasiswa dashboard or any desired page after successful login
                return redirect('mahasiswa_dashboard')
            else:
                # Handle inactive user
                return render(request, 'login_mahasiswa.html', {'error_message': 'Akun Anda tidak aktif.'})
        else:
            # Handle invalid login credentials
            return render(request, 'login_mahasiswa.html', {'error_message': 'Username atau password salah.'})
    else:
        return render(request, 'login_mahasiswa.html', {})
    
@login_required
def mahasiswa_dashboard(request):
    # Mengambil data mahasiswa yang sedang login
    mahasiswa = request.user
    context = {'mhs': mahasiswa}
    return render(request, 'mahasiswa_dashboard.html', context)

@login_required
def daftar_calon(request):
    calon_exist = CalonAnggota.objects.filter(mahasiswa=request.user).exists()
    mahasiswa = request.user
    
    if request.method == 'POST':
        form = CalonBemForm(request.POST, request.FILES)
        
        if form.is_valid():
             # Simpan dokumen terkait
            form.instance.mahasiswa = request.user
            form.save()  # Simpan formulir untuk menyimpan file ke sistem file
            # form.instance.mahasiswa = request.user
            # form.save()
            
            # Prepare training data from DataLatih model
            data_latih_query = DataLatih.objects.all()

            data_latih = {
                'ipk': [data.ipk for data in data_latih_query],
                'jumlah_ekstrakurikuler': [data.jumlah_ekstrakurikuler for data in data_latih_query],
                'lama_ekstrakurikuler': [data.lama_ekstrakurikuler for data in data_latih_query],
                'keaktifan_kegiatan': [data.keaktifan_kegiatan for data in data_latih_query],
                'pengalaman_kepemimpinan': [data.pengalaman_kepemimpinan for data in data_latih_query],
                'prestasi_penghargaan': [data.prestasi_penghargaan for data in data_latih_query],
                'class': [data.class_field for data in data_latih_query]
            }
            df_latih = pd.DataFrame(data_latih)

            # Prepare new data for prediction
            data_baru = {
                'ipk': [form.cleaned_data['ipk']],
                'jumlah_ekstrakurikuler': [form.cleaned_data['jumlah_ekstrakurikuler']],
                'lama_ekstrakurikuler': [form.cleaned_data['lama_ekstrakurikuler']],
                'keaktifan_kegiatan': [form.cleaned_data['keaktifan_kegiatan']],
                'pengalaman_kepemimpinan': [form.cleaned_data['pengalaman_kepemimpinan']],
                'prestasi_penghargaan': [form.cleaned_data['prestasi_penghargaan']]
            }
           
            df_baru = pd.DataFrame(data_baru)

            # Train KNN model
            X_train = df_latih[['ipk', 'jumlah_ekstrakurikuler', 'lama_ekstrakurikuler', 'keaktifan_kegiatan', 'pengalaman_kepemimpinan', 'prestasi_penghargaan']]
            y_train = df_latih['class']
            knn = KNeighborsClassifier(n_neighbors=3)
            knn.fit(X_train, y_train)

            # Make prediction
            prediksi = knn.predict(df_baru)

            # Update the saved CalonAnggota with the prediction result
            calon = CalonAnggota.objects.get(mahasiswa=request.user, publish_status='Tidak')
            calon.hasil_prediksi = prediksi[0]
            calon.save()

            return redirect('calon_list')
    else:
        form = CalonBemForm()
    context = {'form': form, 'calon_exist': calon_exist, 'mhs': mahasiswa, 'menu': 'menusiswa'}
    return render(request, 'calon_anggota.html', context)

@login_required
def calon_list(request):
    # Filter untuk menampilkan hanya calon anggota yang terkait dengan mahasiswa yang sedang login
    calon_list = CalonAnggota.objects.filter(mahasiswa=request.user)
    context = {       
        'calon_list': calon_list,
        'menu': 'menusiswa',
    }
    return render(request, 'calon_list.html', context)

import os
from django.conf import settings

def delete_calon(request, calon_id):
    calon = CalonAnggota.objects.get(pk=calon_id)

    # Menghapus file-file terkait
    try:
        if calon.bukti_ipk:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(calon.bukti_ipk)))
        if calon.bukti_ekstrakurikuler:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(calon.bukti_ekstrakurikuler)))
        if calon.bukti_kegiatan_kampus:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(calon.bukti_kegiatan_kampus)))
        if calon.bukti_kepemimpinan:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(calon.bukti_kepemimpinan)))
        if calon.bukti_prestasi_penghargaan:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(calon.bukti_prestasi_penghargaan)))
    except FileNotFoundError:
        # Tangani kesalahan jika file tidak ditemukan
        pass

    # Menghapus entri CalonAnggota dari database
    calon.delete()
    
    return redirect('calon_list')


def wawancara_list(request):
    # Filter untuk menampilkan hanya calon anggota yang terkait dengan mahasiswa yang sedang login
    calon_list = CalonAnggota.objects.filter(mahasiswa=request.user)
    calon_terakhir = PengumumanWawancara.objects.all().order_by('-id')

    context = {       
        'calon_list': calon_list,
        'wawancara_terakhir' : calon_terakhir,
        
    }
    return render(request, 'wawancara.html', context)

@login_required
def wawancarahasil_list(request):
    mahasiswa = request.user
    hasil_wawancara = HasilWawancara.objects.filter(mahasiswa=mahasiswa)
    context = {'hasil_wawancara': hasil_wawancara}
    return render(request, 'wawancara_list.html', context)