from django.contrib.auth.models import AbstractUser
from django.db import models

class Fakultas(models.Model):
    kode_fakultas = models.CharField(max_length=10, unique=True)
    nama_fakultas = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_fakultas

class ProgramStudi(models.Model):
    kode_program_studi = models.CharField(max_length=10, unique=True)
    nama_program_studi = models.CharField(max_length=100)
    fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE, related_name='program_studi',blank=True, null=True )

    def __str__(self):
        return self.nama_program_studi

class Semester(models.Model):
    kode_semester = models.CharField(max_length=10, unique=True)
    nama_semester = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_semester

class Mahasiswa(AbstractUser):
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255,blank=True, null=True)  # Tambah kolom nama
    program_studi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE, related_name='mahasiswa_program_studi',blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='mahasiswa_semester',blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=10,blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    telepon = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    STATUS_AKADEMIK_CHOICES = [
        ('Aktif', 'Aktif'),
        ('Cuti', 'Cuti'),
        ('Lulus', 'Lulus'),
    ]
    status_akademik = models.CharField(max_length=10, choices=STATUS_AKADEMIK_CHOICES,blank=True, null=True)

    def save(self, *args, **kwargs):
        self.username = self.nim
        self.set_password(self.nim)
        super(Mahasiswa, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama
    
class CalonAnggota(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='calon_anggota')
    tanggal_daftar = models.DateField()
    ipk = models.DecimalField(max_digits=4, decimal_places=2)
    bukti_ipk = models.FileField(upload_to='dokumen/ipk/', blank=True, null=True)
    jumlah_ekstrakurikuler = models.IntegerField()
    lama_ekstrakurikuler = models.IntegerField()
    bukti_ekstrakurikuler = models.FileField(upload_to='dokumen/ekstrakurikuler/', blank=True, null=True)
    keaktifan_kegiatan = models.IntegerField()
    bukti_kegiatan_kampus = models.FileField(upload_to='dokumen/kegiatan_kampus/', blank=True, null=True)
    pengalaman_kepemimpinan = models.IntegerField()
    bukti_kepemimpinan = models.FileField(upload_to='dokumen/kepemimpinan/', blank=True, null=True)
    prestasi_penghargaan = models.IntegerField()
    bukti_prestasi_penghargaan = models.FileField(upload_to='dokumen/prestasi_penghargaan/', blank=True, null=True)
    publish_status = models.CharField(max_length=5, choices=(('Ya', 'Ya'), ('Tidak', 'Tidak')), default='Tidak')
    hasil_prediksi = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.tanggal_daftar}"

class DataLatih(models.Model):
    ipk = models.DecimalField(max_digits=4, decimal_places=2)
    jumlah_ekstrakurikuler = models.IntegerField()
    lama_ekstrakurikuler = models.IntegerField()
    keaktifan_kegiatan = models.IntegerField()
    pengalaman_kepemimpinan = models.IntegerField()
    prestasi_penghargaan = models.IntegerField()
    CLASS_CHOICES = [
        ('Layak', 'Layak'),
        ('Belum', 'Belum'),
    ]
    class_field = models.CharField(max_length=10, choices=CLASS_CHOICES)

    def __str__(self):
        return (f"{self.ipk}, {self.jumlah_ekstrakurikuler}, {self.lama_ekstrakurikuler}, "
                f"{self.keaktifan_kegiatan}, {self.pengalaman_kepemimpinan}, {self.prestasi_penghargaan}, {self.class_field}")

class PengumumanWawancara(models.Model):
    STATUS_CHOICES = [
        ('Aktif', 'Aktif'),
        ('Tidak', 'Tidak'),
    ]
    tanggal_wawancara = models.DateField()
    isi_wawancara = models.TextField()
    status_aktif = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Aktif')


class HasilWawancara(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='hasil_wawancara')
    nilai_wawancara = models.IntegerField()
    STATUS_CHOICES = [
        ('Lulus', 'Lulus'),
        ('Tidak Lulus', 'Tidak Lulus'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)


