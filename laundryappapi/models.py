# laundryappapi/models.py

from django.db import models

class Laundry(models.Model):
    hp = models.CharField(max_length=15)
    nama = models.CharField(max_length=100)
    jenis_laundry = models.CharField(max_length=50)
    jumlah_berat = models.DecimalField(max_digits=5, decimal_places=2)
    tanggal_masuk = models.DateField()
    tanggal_selesai = models.DateField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    catatan_khusus = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=[
        ('0', 'Proses'),
        ('1', 'Selesai'),
    ])