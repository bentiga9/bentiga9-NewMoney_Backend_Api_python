from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, nom, prenom, telephone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email requis')
        email = self.normalize_email(email)
        user = self.model(
            email=email, nom=nom, prenom=prenom, 
            telephone=telephone, username=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nom, prenom, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, nom, prenom, telephone, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [('client', 'Client'), ('agent', 'Agent'), ('admin', 'Admin')]
    
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    adresse = models.CharField(max_length=255, default='')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    reset_code = models.CharField(max_length=255, null=True, blank=True)
    reset_code_expires_at = models.DateTimeField(null=True, blank=True)
    
    username = models.CharField(max_length=150, unique=True, blank=True)
    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    @property
    def full_name(self):
        return f"{self.nom} {self.prenom}"
