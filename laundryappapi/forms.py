from django import forms
from .models import Order, LaundryItem

class LaundryItemForm(forms.ModelForm):
    class Meta:
        model = LaundryItem
        fields = ['jenis_laundry', 'jumlah_berat']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'hp', 'nama', 'tanggal_masuk', 'tanggal_selesai',
            'total_harga', 'catatan_khusus', 'status', 'status_pembayaran'
        ]

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        # Tambahkan validasi atau modifikasi di sini jika diperlukan
        return nama

    def clean_hp(self):
        hp = self.cleaned_data.get('hp')
        # Validasi khusus untuk nomor HP, contoh: panjang atau format nomor
        if not hp.isdigit():
            raise forms.ValidationError("Nomor HP harus terdiri dari angka.")
        return hp
