# Generated by Django 5.0.6 on 2024-06-16 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundryappapi', '0007_laundryitem_order_delete_laundry_laundryitem_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laundry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hp', models.CharField(max_length=15)),
                ('nama', models.CharField(max_length=100)),
                ('jenis_laundry', models.CharField(max_length=50)),
                ('jumlah_berat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tanggal_masuk', models.DateField()),
                ('tanggal_selesai', models.DateField()),
                ('total_harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('catatan_khusus', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('0', 'Proses'), ('1', 'Selesai')], max_length=1)),
            ],
        ),
        migrations.DeleteModel(
            name='LaundryItem',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]