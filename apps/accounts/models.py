from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager personalizado para el modelo User"""
    
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El usuario debe tener un nombre de usuario')
        user = self.model(usuario=usuario, **extra_fields)
        user.password = password or usuario
        user.save(using=self._db)
        return user
    
    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')
        return self.create_user(usuario, password, **extra_fields)


class User(models.Model):
    """Modelo de usuario - Mapea a tabla usuarios en MySQL"""
    
    ROLE_CHOICES = [
        ('admin', _('Administrador')),
        ('vendedor', _('Vendedor')),
        ('repostero', _('Repostero')),
    ]
    
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    usuario = models.CharField(max_length=50, unique=True, db_column='usuario')
    password = models.CharField(max_length=100, db_column='password')
    nombre = models.CharField(max_length=100, db_column='nombre')
    rol = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='vendedor',
        db_column='rol'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    
    # Campos adicionales para compatibilidad con Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        managed = False  # No crear/eliminar tabla
    
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombre']
    
    def __str__(self):
        return f"{self.usuario} - {self.get_rol_display()}"
    
    def get_rol_display(self):
        return dict(self.ROLE_CHOICES).get(self.rol, self.rol)
    
    @property
    def is_admin(self):
        return self.rol == 'admin'
    
    @property
    def is_seller(self):
        return self.rol == 'vendedor'
    
    @property
    def is_baker(self):
        return self.rol == 'repostero'
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def get_full_name(self):
        return self.nombre
    
    def get_short_name(self):
        return self.usuario
    
    def has_perm(self, perm, obj=None):
        """Verificar permiso"""
        return self.is_superuser or self.is_staff
    
    def has_module_perms(self, app_label):
        """Verificar acceso a módulo"""
        return self.is_superuser or self.is_staff


class UserProfile(models.Model):
    """Perfil extendido del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Perfil de {self.user.usuario}"
