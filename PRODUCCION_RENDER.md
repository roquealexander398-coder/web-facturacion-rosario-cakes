# 🚀 Guía de Despliegue en Render - Sistema de Facturación

## Cambios Realizados para Producción

Este proyecto ha sido completamente adaptado para desplegar en Render. A continuación se detallan todos los cambios realizados:

### 📋 Archivos Modificados:

#### 1. **requirements.txt**
- ✅ Agregado: `whitenoise>=6.6` - Para servir archivos estáticos en producción
- ✅ Ya incluido: `gunicorn>=21.0` - Servidor WSGI para producción
- ℹ️ Nota: Redis/Celery no están configurados (no gratuito en Render)

#### 2. **facturacion/settings.py**
**Cambios de Configuración de Archivos Estáticos:**
- ✅ Agregado WhiteNoise middleware en MIDDLEWARE (posición correcta)
- ✅ Configurado STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' para producción
- ✅ STATIC_ROOT apunta a 'staticfiles' (para collectstatic)
- ✅ STATICFILES_DIRS apunta a 'static' (archivos fuente)

**Cambios de Seguridad:**
- ✅ ALLOWED_HOSTS dinámico para soportar RENDER_EXTERNAL_HOSTNAME
- ✅ SECURE_SSL_REDIRECT = True en producción
- ✅ SESSION_COOKIE_SECURE = True
- ✅ CSRF_COOKIE_SECURE = True
- ✅ SECURE_HSTS_SECONDS = 31536000 (1 año)
- ✅ SECURE_BROWSER_XSS_FILTER = True
- ✅ SECURE_CONTENT_SECURITY_POLICY configurada

**Cambios de CORS y CSRF:**
- ✅ CORS_ALLOWED_ORIGINS dinámico según DEBUG
- ✅ CSRF_TRUSTED_ORIGINS configurado para Render

**Cambios de Debug Toolbar:**
- ✅ debug_toolbar solo en desarrollo (no en producción)

**Cambios de Logging:**
- ✅ Configurado para usar console en producción (Render no tiene FS persistente)
- ✅ Logging a archivo solo en desarrollo

**Cambios de Base de Datos:**
- ✅ SQLite para desarrollo
- ✅ PostgreSQL para producción (automático con render.yaml)

**Cambios de Celery:**
- ✅ Configuración opcional (solo si CELERY_BROKER_URL está disponible)

#### 3. **facturacion/wsgi.py**
- ✅ Agregado WhiteNoise wrapper para servir archivos estáticos
- ✅ Configurable: Solo se activa si DEBUG=False

#### 4. **render.yaml**
- ✅ buildCommand mejorado: incluye `--noinput` y orden correcto
- ✅ startCommand mejorado: Gunicorn con socket vinculado a puerto, 2 workers y timeout de 60s
- ✅ Agregadas variables de email (EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS)
- ✅ Documentadas variables opcionales (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

#### 5. **build.sh**
- ✅ Mantiene los mismos pasos que render.yaml (backup local)

---

## 🔧 Configuración en Render

### Paso 1: Crear la Base de Datos PostgreSQL
1. Ve a Render dashboard
2. Crea una nueva **PostgreSQL Database**
3. Copia los datos de conexión (serán usados automáticamente)

### Paso 2: Crear el Servicio Web
1. Conecta tu repositorio GitHub
2. Crea un nuevo **Web Service**
3. Usa el archivo `render.yaml` para la configuración
4. Las variables de entorno se configuran automáticamente:
   - `SECRET_KEY`: Generada automáticamente ✅
   - `DEBUG`: False ✅
   - `ALLOWED_HOSTS`: *.onrender.com ✅
   - `DB_*`: Conectadas a PostgreSQL ✅

### Paso 3: Variables de Entorno Adicionales (si usas email)
En Render dashboard, añade:
- `EMAIL_HOST_USER`: Tu correo
- `EMAIL_HOST_PASSWORD`: Contraseña de aplicación (no contraseña normal)

---

## 📁 Estructura de Archivos Estáticos

```
proyecto/
├── static/                  # Archivos estáticos fuente (CSS, JS, imágenes)
│   ├── css/
│   │   └── style.css       # ✅ Servido por WhiteNoise
│   └── js/
│       └── main.js         # ✅ Servido por WhiteNoise
└── staticfiles/            # Generado por 'collectstatic' (no commitar)
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

---

## ✅ Verificación Local (Antes de Desplegar)

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Simular colectar archivos estáticos (como en Render)
```bash
python manage.py collectstatic --noinput
```

### 3. Ejecutar migraciones
```bash
python manage.py migrate
```

### 4. Crear usuario superuser (si no existe)
```bash
python manage.py createsuperuser
```

### 5. Probar con DEBUG=False localmente
```bash
DEBUG=False python manage.py runserver
```

Deberías ver:
- ✅ Login en `/login/` con estilos cargados correctamente
- ✅ Dashboard accesible después del login
- ✅ Archivos CSS y JS cargando desde `/static/`
- ✅ Sin errores 404 en la consola

---

## 🐛 Troubleshooting

### Problema: Archivos estáticos devuelven 404
**Solución:**
```bash
python manage.py collectstatic --noinput --clear
```

### Problema: Error "Secret key not set"
**Solución:** Render genera automáticamente SECRET_KEY. Si necesitas uno local, añade a `.env`:
```
SECRET_KEY=your-secure-key-123456789
```

### Problema: Error de conexión a base de datos en producción
**Solución:** Verifica que:
1. PostgreSQL está creada en Render
2. Variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` están configuradas
3. La red de Render permite la conexión (está habilitada por defecto)

### Problema: Login no funciona en producción
**Solución:** Verifica:
1. Migraciones se ejecutaron correctamente: `python manage.py migrate`
2. Usuario existe: `python manage.py shell` → `from apps.accounts.models import User; User.objects.all()`
3. CSRF está configurado correctamente (ya está en settings.py)

---

## 🔐 Checklist de Seguridad

- ✅ DEBUG = False en producción
- ✅ SECRET_KEY único y generado por Render
- ✅ SSL/HTTPS habilitado (Render lo maneja)
- ✅ ALLOWED_HOSTS configurado
- ✅ CSRF_TRUSTED_ORIGINS configurado
- ✅ CORS solo permite dominios específicos
- ✅ Cookies seguras (SECURE flags activados)
- ✅ HSTS habilitado
- ✅ XSS protection activado

---

## 📊 URLs Importantes en Producción

Una vez desplegado en Render:
- **Login:** `https://tu-app.onrender.com/login/`
- **Dashboard:** `https://tu-app.onrender.com/dashboard/`
- **Admin:** `https://tu-app.onrender.com/admin/`
- **API:** `https://tu-app.onrender.com/api/`

---

## 🚀 Comando de Despliegue Final

Desde la terminal local:
```bash
git add .
git commit -m "Producción: Configuración completada para Render"
git push origin main
```

Render detectará los cambios automáticamente y desplegará.

---

## 📝 Notas

- Los archivos en `staticfiles/` son generados automáticamente por `collectstatic` - NO deben ser commiteados a Git
- Agregados a `.gitignore`: `staticfiles/`, `*.log`, `db.sqlite3`
- Las migraciones se ejecutan automáticamente en cada despliegue
- Los logs se muestran en la consola de Render (Settings > Logs)

---

**Proyecto adaptado para producción: ✅ LISTO PARA DESPLEGAR**
