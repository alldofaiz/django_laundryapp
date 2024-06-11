from django.contrib import admin
from .models import Laundry

# Register your models here.


class LaundryAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jenis_laundry', 'jumlah_berat', 'tanggal_masuk', 'tanggal_selesai', 'total_harga', 'status')
    list_filter = ('status', 'tanggal_masuk')
    search_fields = ('nama', 'hp')

admin.site.register(Laundry, LaundryAdmin)