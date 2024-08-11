from django import forms
from .models import Fakultas,ProgramStudi,Semester,Mahasiswa,CalonAnggota,PengumumanWawancara,HasilWawancara

class ProgramStudiForm(forms.ModelForm):
    class Meta:
        model = ProgramStudi
        fields = ['kode_program_studi', 'nama_program_studi', 'fakultas']

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['kode_semester', 'nama_semester']

class MahasiswaForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nim', 'nama', 'program_studi', 'semester', 'jenis_kelamin', 'tanggal_lahir', 'alamat', 'telepon', 'email', 'status_akademik']

   
class CalonBemForm(forms.ModelForm):
    class Meta:
        model = CalonAnggota
        # fields = ['mahasiswa', 'tanggal_daftar', 'ipk', 'jumlah_ekstrakurikuler', 'lama_ekstrakurikuler']
        fields = ['tanggal_daftar', 'ipk', 'bukti_ipk', 'jumlah_ekstrakurikuler', 'lama_ekstrakurikuler',
                  'bukti_ekstrakurikuler', 'keaktifan_kegiatan', 'bukti_kegiatan_kampus', 'pengalaman_kepemimpinan',
                  'bukti_kepemimpinan', 'prestasi_penghargaan', 'bukti_prestasi_penghargaan']

class SettingPengumumanWawancaraForm(forms.ModelForm):
    class Meta:
        model = PengumumanWawancara
        fields = ['tanggal_wawancara', 'isi_wawancara', 'status_aktif']

class HasilWawancaraForm(forms.ModelForm):
    class Meta:
        model = HasilWawancara
        fields = ['mahasiswa', 'nilai_wawancara', 'status']

class UploadFileForm(forms.Form):
    file = forms.FileField()

class FakultasForm(forms.ModelForm):
    class Meta:
        model = Fakultas
        fields = ['kode_fakultas', 'nama_fakultas']
    