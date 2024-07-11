from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from uuid import uuid4

# Choices untuk status pesanan
ORDER_STATUS_CHOICES = [
    ('0', 'Proses'),
    ('1', 'Selesai'),
]

# Choices untuk status pembayaran
PAYMENT_STATUS_CHOICES = [
    ('0', 'Belum'),
    ('1', 'Lunas'),
]

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, email, password, **extra_fields)

# Model untuk pengguna (Admin/Kasir)
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=[('Admin', 'Admin'), ('Kasir', 'Kasir')])
    laundry_store = models.ForeignKey('LaundryStore', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# Model untuk toko laundry
class LaundryStore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Model untuk pelanggan
class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    laundry_store = models.ForeignKey('LaundryStore', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Model untuk pesanan
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    hp = models.CharField(max_length=15)
    nama = models.CharField(max_length=100)
    tanggal_masuk = models.DateField()
    tanggal_selesai = models.DateField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    catatan_khusus = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default='0')
    status_pembayaran = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    laundry_store = models.ForeignKey('LaundryStore', on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id}"

# Model untuk item pesanan
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    jenis_laundry = models.CharField(max_length=50)
    jumlah_berat = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.id} - {self.jenis_laundry}"

# Model untuk layanan laundry
class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    laundry_store = models.ForeignKey('LaundryStore', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Model untuk pembayaran
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=10, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Transfer', 'Transfer')])
    laundry_store = models.ForeignKey('LaundryStore', on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment {self.id}"
