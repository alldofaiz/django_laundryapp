# Import model User
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    # Cari pengguna dengan username 'testing'
    user = User.objects.get(username='testing')
    # Lakukan pengecekan password
    print(user.check_password('password123'))
except User.DoesNotExist:
    print("User 'testing' not found")
