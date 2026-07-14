from django.contrib import admin

from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('avatar', 'bio', 'last_login_ip')


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre', 'rol', 'is_active', 'fecha_creacion')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('usuario', 'nombre')
    fields = ('usuario', 'password', 'nombre', 'rol', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('id_usuario', 'fecha_creacion')
    inlines = [UserProfileInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_login_ip')
    search_fields = ('user__usuario',)

