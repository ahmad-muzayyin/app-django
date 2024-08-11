from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Mahasiswa, CalonAnggota, Semester, ProgramStudi,DataLatih,PengumumanWawancara,HasilWawancara,Fakultas
from .forms import FakultasForm, ProgramStudiForm,SemesterForm,MahasiswaForm,SettingPengumumanWawancaraForm,HasilWawancaraForm,UploadFileForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Simpan username di dalam sesi
            request.session['username'] = username
            # Redirect ke halaman yang sesuai
            return redirect('berandaadmin')  # Ganti 'berandaadmin' dengan nama view yang sesuai
        else:
            # Autentikasi gagal, tampilkan pesan kesalahan atau form login kembali
            return redirect('berandaadmin') 
    else:
        return render(request, 'loginadmin.html')

def beranda_admin(request):
    # Get counts
    # total_mahasiswa = Mahasiswa.objects.count()
    total_mahasiswa = Mahasiswa.objects.exclude(is_staff=True).count()
    total_calon_anggota = CalonAnggota.objects.count()
    total_semester = Semester.objects.count()
    total_program_studi = ProgramStudi.objects.count()

    context = {
        'menu':'berandaadmin',
        'total_mahasiswa': total_mahasiswa,
        'total_calon_anggota': total_calon_anggota,
        'total_semester': total_semester,
        'total_program_studi': total_program_studi,
    }
    return render(request, 'berandaadmin.html', context)
# program studi
def program_studi_list(request):
    program_studi_list = ProgramStudi.objects.select_related('fakultas').all()

    # Pencarian berdasarkan nama program studi
    query = request.GET.get('q')
    if query:
        program_studi_list = program_studi_list.filter(nama_program_studi__icontains=query)

    paginator = Paginator(program_studi_list, 10)  # Tampilkan 10 program studi per halaman
    page = request.GET.get('page')
    try:
        program_studi = paginator.page(page)
    except PageNotAnInteger:
        program_studi = paginator.page(1)
    except EmptyPage:
        program_studi = paginator.page(paginator.num_pages)

    context = {
        'menu': 'master',
        'program_studi': program_studi,
    }
    return render(request, 'program_studi_list.html', context)


def create_program_studi(request):
    form = ProgramStudiForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('program_studi_list')
    context = {
            'menu':'master',
            'form': form,
    }
    return render(request, 'program_studi_tambah.html', context)


def update_program_studi(request, pk):
    program_studi = get_object_or_404(ProgramStudi, pk=pk)
    form = ProgramStudiForm(instance=program_studi)
    
    if request.method == 'POST':
        form = ProgramStudiForm(request.POST, instance=program_studi)
        if form.is_valid():
            form.save()
            return redirect('program_studi_list')  # Redirect to the list view after successful edit
    context = {
                'menu':'master',
                'form': form,
        }
    return render(request, 'program_studi_edit.html', context)

def delete_program_studi(request, pk):
    program_studi = get_object_or_404(ProgramStudi, pk=pk)
    if request.method == 'POST':
        program_studi.delete()
        return redirect('program_studi_list')
    context = {
                'menu':'master',
                'program_studi': program_studi,
        }
    return render(request, 'program_studi_confirm_delete.html', context)

# semester
def semester_list(request):
    semester_list = Semester.objects.all()
    
    # Pagination
    paginator = Paginator(semester_list, 10)  # Show 10 semesters per page
    page = request.GET.get('page')
    try:
        semesters = paginator.page(page)
    except PageNotAnInteger:
        semesters = paginator.page(1)
    except EmptyPage:
        semesters = paginator.page(paginator.num_pages)

    context = {
            'menu':'master',
            'semesters': semesters,
    }
    return render(request, 'semester_list.html',context)

def add_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semester_list')
    else:
        form = SemesterForm()
    context = {
            'menu':'master',
            'form': form,
    }
    return render(request, 'semester_tambah.html',context)

def edit_semester(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            return redirect('semester_list')
    else:
        form = SemesterForm(instance=semester)

    context = {
            'menu':'master',
            'form': form,
            'semester': semester,
    }
    return render(request, 'semester_edit.html',context)
   

def delete_semester(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        semester.delete()
        return redirect('semester_list')
    context = {
            'menu':'master',
            'semester': semester,
    }
    return render(request, 'semester_confirm_delete.html',context)

# 

def mahasiswa_list(request):
    # Filter untuk menampilkan hanya mahasiswa biasa (is_staff=False)
    mahasiswa_list = Mahasiswa.objects.filter(is_staff=False)

    query = request.GET.get('q')
    if query:
        mahasiswa_list = mahasiswa_list.filter(nama__icontains=query)

    paginator = Paginator(mahasiswa_list, 10)  # Menampilkan 10 mahasiswa per halaman
    page = request.GET.get('page')

    try:
        mahasiswa_list = paginator.page(page)
    except PageNotAnInteger:
        mahasiswa_list = paginator.page(1)
    except EmptyPage:
        mahasiswa_list = paginator.page(paginator.num_pages)

    context = {
        'menu': 'master',
        'mahasiswa_list': mahasiswa_list,
    }
    return render(request, 'mahasiswa_list.html', context)
def mahasiswa_create(request):
    program_studi_list = ProgramStudi.objects.all()
    semester_list = Semester.objects.all()
    if request.method == 'POST':
        form = MahasiswaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mahasiswa_list')
    else:
        form = MahasiswaForm()
    return render(request, 'mahasiswa_tambah.html', {'form': form,'program_studi_list':program_studi_list,'semester_list':semester_list})

def mahasiswa_update(request, pk):
    mahasiswa = get_object_or_404(Mahasiswa, pk=pk)
    program_studi_list = ProgramStudi.objects.all()
    semester_list = Semester.objects.all()
    if request.method == 'POST':
        form = MahasiswaForm(request.POST, instance=mahasiswa)
        if form.is_valid():
            form.save()
            return redirect('mahasiswa_list')
    else:
        form = MahasiswaForm(instance=mahasiswa)
    return render(request, 'mahasiswa_edit.html', {'form': form,'mhs':mahasiswa,'program_studi_list':program_studi_list,'semester_list':semester_list})

def mahasiswa_delete(request, pk):
    mahasiswa = get_object_or_404(Mahasiswa, pk=pk)
    if request.method == 'POST':
        mahasiswa.delete()
        return redirect('mahasiswa_list')
    return render(request, 'mahasiswa_confirm_delete.html', {'mahasiswa': mahasiswa})


def datalatih_list(request):
    data_latih = DataLatih.objects.all()
    context = {
        'menu': 'master',
        'data_latih': data_latih,
    }
    return render(request, 'datalatih_list.html', context)

def import_datalatih(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            for index, row in df.iterrows():
                DataLatih.objects.create(
                    ipk=row['ipk'],
                    jumlah_ekstrakurikuler=row['jumlah_ekstrakurikuler'],
                    lama_ekstrakurikuler=row['lama_ekstrakurikuler'],
                    keaktifan_kegiatan=row['keaktifan_kegiatan'],
                    pengalaman_kepemimpinan=row['pengalaman_kepemimpinan'],
                    prestasi_penghargaan=row['prestasi_penghargaan'],
                    class_field=row['class']
                )
            return redirect('datalatih_list')
    return render(request, 'import_datalatih.html')
# def import_datalatih(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         if file.name.endswith('.xlsx'):
#             df = pd.read_excel(file)
#             for index, row in df.iterrows():
#                 DataLatih.objects.create(
#                     ipk=row['ipk'],
#                     jumlah_ekstrakurikuler=row['jumlah_ekstrakurikuler'],
#                     lama_ekstrakurikuler=row['lama_ekstrakurikuler'],
#                     class_field=row['class']
#                 )
#             return redirect('datalatih_list')
#     return render(request, 'import_datalatih.html')

def delete_datalatih(request):
    DataLatih.objects.all().delete()
    return redirect('datalatih_list')

def calon_anggota_list(request):
    calon_list = CalonAnggota.objects.all()

    # Cari berdasarkan nama mahasiswa jika query diberikan
    query = request.GET.get('q')
    if query:
        calon_list = calon_list.filter(mahasiswa__nama__icontains=query)

    # Pagination
    paginator = Paginator(calon_list, 10)  # Menampilkan 10 calon anggota per halaman
    page = request.GET.get('page')
    try:
        calon_list = paginator.page(page)
    except PageNotAnInteger:
        calon_list = paginator.page(1)
    except EmptyPage:
        calon_list = paginator.page(paginator.num_pages)

    context = {
        'menu': 'pengolahandata',
        'calon_list': calon_list,
    }
    return render(request, 'calon_anggota_list.html', context)

def update_publish_status(request, calon_id):
    calon = CalonAnggota.objects.get(id=calon_id)
    if calon.publish_status == 'Tidak':
        calon.publish_status = 'Ya'
    else:
        calon.publish_status = 'Tidak'
    calon.save()
    return redirect('calonanggota_list')
def add_wawancara(request):
    if request.method == 'POST':
        form = SettingPengumumanWawancaraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wawancara_list_informasi')
    else:
        form = SettingPengumumanWawancaraForm()
    context = {
            'menu':'pengolahandata',
            'form': form,
    }
    return render(request, 'setting_wawancara_create.html',context)

def wawancara_list(request):
    calon_tanggal_wawancara = PengumumanWawancara.objects.all()
    context = {
        'menu': 'pengolahandata',
        'list_wawancara': calon_tanggal_wawancara,
    }
    return render(request, 'setting_wawancara.html', context)
def delete_wawancarainfo(request, pk):
    calon_tanggal_wawancara = get_object_or_404(PengumumanWawancara, pk=pk)
    if request.method == 'POST':
        calon_tanggal_wawancara.delete()
        return redirect('wawancara_list_informasi')
    context = {
            'menu':'pengolahandata',
            'calon_tanggal_wawancara': calon_tanggal_wawancara,
    }
    return render(request, 'wawancarainfo_confirm_delete.html',context)

def wawancara_update(request, pk):
    PengumumanWawancara1 = get_object_or_404(PengumumanWawancara, pk=pk)
    if request.method == 'POST':
        form = SettingPengumumanWawancaraForm(request.POST, instance=PengumumanWawancara1)
        if form.is_valid():
            form.save()
            return redirect('add_wawancara')
    else:
        form = SemesterForm(instance=PengumumanWawancara1)

    context = {
            'menu':'pengolahandata',
            'form': form,
            'wawancara': PengumumanWawancara1,
            
    }
    return render(request, 'setting_wawancara_update.html',context)

def hasil_wawancara_list(request):
    nama_mahasiswa = request.GET.get('nama_mahasiswa', '')
    selected_semester = request.GET.get('semester', '')
    selected_program_studi = request.GET.get('program_studi', '')

    # Queryset untuk semua entri Semester dan ProgramStudi
    semesters = Semester.objects.all()
    program_studis = ProgramStudi.objects.all()

    hasil_wawancara_list = HasilWawancara.objects.all()

    # Filter data berdasarkan nama mahasiswa
    if nama_mahasiswa:
        hasil_wawancara_list = hasil_wawancara_list.filter(mahasiswa__nama__icontains=nama_mahasiswa)

    # Filter data berdasarkan semester
    if selected_semester:
        hasil_wawancara_list = hasil_wawancara_list.filter(mahasiswa__semester__nama_semester=selected_semester)

    # Filter data berdasarkan program studi
    if selected_program_studi:
        hasil_wawancara_list = hasil_wawancara_list.filter(mahasiswa__program_studi__nama_program_studi=selected_program_studi)

    paginator = Paginator(hasil_wawancara_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'nama_mahasiswa': nama_mahasiswa,
        'selected_semester': selected_semester,
        'selected_program_studi': selected_program_studi,
        'semesters': semesters,
        'program_studis': program_studis,
    }
    return render(request, 'hasil_wawancara_list.html', context)

def hasil_wawancara_create(request):
    if request.method == 'POST':
        form = HasilWawancaraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hasil_wawancara_list')
    else:
        # Query untuk mendapatkan daftar mahasiswa yang merupakan CalonAnggota dan hasil_prediksi sama dengan Layak
        # mahasiswa_list = Mahasiswa.objects.filter(calon_anggota__hasil_prediksi='Layak')
        mahasiswa_list = Mahasiswa.objects.filter(calon_anggota__hasil_prediksi='Layak', calon_anggota__publish_status='Ya')
        form = HasilWawancaraForm()
    return render(request, 'hasil_wawancara_formtambah.html', {'form': form, 'mahasiswa_list': mahasiswa_list})

def hasil_wawancara_update(request, pk):
    hasil_wawancara = get_object_or_404(HasilWawancara, pk=pk)
    if request.method == 'POST':
        form = HasilWawancaraForm(request.POST, instance=hasil_wawancara)
        if form.is_valid():
            form.save()
            return redirect('hasil_wawancara_list')
    else:
        form = HasilWawancaraForm(instance=hasil_wawancara)
    return render(request, 'hasil_wawancara_formedit.html', {'form': form})

def hasil_wawancara_delete(request, pk):
    hasil_wawancara = get_object_or_404(HasilWawancara, pk=pk)
    if request.method == 'POST':
        hasil_wawancara.delete()
        return redirect('hasil_wawancara_list')
    return render(request, 'hasil_wawancara_confirm_delete.html', {'hasil_wawancara': hasil_wawancara})

def download_mahasiswa_format(request):
    # Define the columns for Mahasiswa data based on the model fields
    mahasiswa_columns = [
        'nim',
        'nama',
        'program_studi_kode',  # Foreign key should reference ProgramStudi kode
        'semester_kode',        # Foreign key should reference Semester kode
        'jenis_kelamin',
        'tanggal_lahir',
        'alamat',
        'telepon',
        'email',
        'status_akademik'
    ]

    # Example data for Mahasiswa
    example_mahasiswa_data = [
        ['1234567890', 'John Doe', 'PROG01', 'RPL', 'Laki-laki', '1990-01-01', 'Jl. Contoh 123', '081234567890', 'john.doe@example.com', 'Aktif'],
        ['0987654321', 'Jane Smith', 'PROG02', 'TI', 'Perempuan', '1992-02-02', 'Jl. Contoh 456', '081234567891', 'jane.smith@example.com', 'Cuti']
    ]

    # Create a DataFrame for Mahasiswa data
    mahasiswa_df = pd.DataFrame(example_mahasiswa_data, columns=mahasiswa_columns)

    # Fetch data from ProgramStudi model
    program_studi_data = ProgramStudi.objects.all().values('kode_program_studi', 'nama_program_studi')
    program_studi_df = pd.DataFrame(list(program_studi_data))

    # Fetch data from Semester model
    semester_data = Semester.objects.all().values('kode_semester', 'nama_semester')
    semester_df = pd.DataFrame(list(semester_data))

    # Create a Pandas Excel writer using openpyxl as the engine
    with pd.ExcelWriter('mahasiswa_import_template.xlsx', engine='openpyxl') as writer:
        # Write each DataFrame to a specific sheet
        mahasiswa_df.to_excel(writer, sheet_name='Mahasiswa', index=False)
        program_studi_df.to_excel(writer, sheet_name='ProgramStudi', index=False)
        semester_df.to_excel(writer, sheet_name='Semester', index=False)

    # Get the Excel file content as a binary stream
    with open('mahasiswa_import_template.xlsx', 'rb') as f:
        file_data = f.read()

    # Create the HttpResponse with the appropriate header
    response = HttpResponse(file_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="mahasiswa_import_template.xlsx"'

    return response
# def import_datalatih(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         if file.name.endswith('.xlsx'):
#             df = pd.read_excel(file)
#             for index, row in df.iterrows():
#                 DataLatih.objects.create(
#                     ipk=row['ipk'],
#                     jumlah_ekstrakurikuler=row['jumlah_ekstrakurikuler'],
#                     lama_ekstrakurikuler=row['lama_ekstrakurikuler'],
#                     keaktifan_kegiatan=row['keaktifan_kegiatan'],
#                     pengalaman_kepemimpinan=row['pengalaman_kepemimpinan'],
#                     prestasi_penghargaan=row['prestasi_penghargaan'],
#                     class_field=row['class']
#                 )
#             return redirect('datalatih_list')
#     return render(request, 'import_datalatih.html')

def import_mahasiswa(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file, sheet_name='Mahasiswa')

            # Iterasi setiap baris dan buat objek Mahasiswa
            for index, row in df.iterrows():
                try:
                    Mahasiswa.objects.create(
                        nim=row["nim"],
                        nama=row["nama"],
                        program_studi=row["program_studi_kode"],  # Sesuaikan dengan field program_studi yang ada di model Mahasiswa Anda
                        semester=row["semester_kode"],  # Sesuaikan dengan field semester yang ada di model Mahasiswa Anda
                        jenis_kelamin=row["jenis_kelamin"],
                        tanggal_lahir=row["tanggal_lahir"],
                        alamat=row["alamat"],
                        telepon=row["telepon"],
                        email=row["email"],
                        status_akademik=row["status_akademik"]
                    )
                except Exception as e:
                    # Tangani pengecualian (misalnya, catat atau simpan pesan kesalahan)
                    print(f"Error pada baris {index}: {e}")

            # return HttpResponseRedirect(reverse("import_success"))  # Sesuaikan dengan nama URL yang sesuai
            return redirect('datalatih_list')
#     return render(request, 'import_datalatih.html')
    else:
        form = UploadFileForm()
    return render(request, "import_mahasiswa.html", {"form": form})

def fakultas_list(request):
    query = request.GET.get('q')
    if query:
        fakultas_list = Fakultas.objects.filter(nama_fakultas__icontains=query)
    else:
        fakultas_list = Fakultas.objects.all()

    paginator = Paginator(fakultas_list, 10)  # Show 10 faculties per page
    page_number = request.GET.get('page')
    fakultas_list = paginator.get_page(page_number)
    context = {
        'menu': 'master',
        'fakultas_list': fakultas_list,
    }
    
    return render(request, 'fakultas_list.html', context)

def create_fakultas(request):
    if request.method == "POST":
        form = FakultasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('fakultas_list'))
    else:
        form = FakultasForm()
    
    context = {
        'menu': 'master',
        'form': form,
    }
    return render(request, 'fakultas_form.html', context)

def update_fakultas(request, pk):
    fakultas = get_object_or_404(Fakultas, pk=pk)
    if request.method == "POST":
        form = FakultasForm(request.POST, instance=fakultas)
        if form.is_valid():
            form.save()
            return redirect(reverse('fakultas_list'))
    else:
        form = FakultasForm(instance=fakultas)
    
    context = {
        'menu': 'master',
        'form': form,
    }
    return render(request, 'fakultas_form.html', context)

def delete_fakultas(request, pk):
    fakultas = get_object_or_404(Fakultas, pk=pk)
    if request.method == "POST":
        fakultas.delete()
        return redirect(reverse('fakultas_list'))
    context = {
        'menu': 'master',
        'fakultas': fakultas,
    }
    return render(request, 'fakultas_confirm_delete.html',context)