
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), name=name, surname=surname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None):
        user = self.create_user(email=email, name=name, surname=surname, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    company_code=models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Todo(models.Model):
    sender = models.ForeignKey(User, related_name="sent_todos", on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=255)
    sender_surname = models.CharField(max_length=255)
    message = models.TextField()
    reciver = models.ForeignKey(User, related_name="received_todos", on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)


class Payments(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('awaiting', 'Awaiting'),
        ('unpaid', 'Unpaid'),
    ]

    date = models.DateField(auto_now_add=True)
    invoice = models.CharField(max_length=20)
    customer = models.CharField(max_length=255)
    amount = models.IntegerField()
    product = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unpaid')


    def __str__(self):
        return f"{self.invoice} - {self.customer}"



class Exhibition(models.Model):
    event_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.URLField()

    def __str__(self):
        return  f"{self.event_name}"