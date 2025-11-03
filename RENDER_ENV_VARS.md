# Render Environment Variables Configuration

## 🔧 Required Environment Variables

Go to your Render Dashboard → Your Service → Environment Tab and add these variables:

### 1. Django Core Settings

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.12.7` | Python runtime version (set automatically from runtime.txt) |
| `SECRET_KEY` | `c*nvuc(oy*29017knmo7@_(n9a-3ny6!po=_v%b-*g7ic_p3^@` | Django secret key for cryptography |
| `DEBUG` | `False` | **CRITICAL:** Must be False in production |
| `DJANGO_SETTINGS_MODULE` | `artscope.settings` | Django settings module path |

### 2. Database Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://neondb_owner:npg_eX2Cu1dbNzfF@ep-curly-boat-ahq7twdx-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require` | Neon PostgreSQL connection string |

**⚠️ IMPORTANT:** Remove `psql` command and quotes - just the plain connection URL!

### 3. Allowed Hosts

| Variable | Value | Description |
|----------|-------|-------------|
| `ALLOWED_HOSTS` | `realmeta.onrender.com,localhost,127.0.0.1` | Comma-separated list of allowed hosts |

**Note:** `RENDER_EXTERNAL_HOSTNAME` is automatically provided by Render, so realmeta.onrender.com will be auto-added.

### 4. CORS Settings (Optional - if you have a separate frontend)

| Variable | Value | Description |
|----------|-------|-------------|
| `CORS_ALLOWED_ORIGINS` | `https://realmeta.onrender.com,http://localhost:3000` | Comma-separated allowed origins |

---

## 🚀 Optional Environment Variables

These have default values but can be customized:

### Redis/Caching (Recommended for Production)

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection for caching |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery message broker |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/0` | Celery result storage |

**To add Redis on Render:**
1. Create a new Redis service on Render
2. Copy the Internal Redis URL
3. Set it as `REDIS_URL` environment variable

### AI/ML Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `EMBEDDING_MODEL` | `clip-ViT-B-32` | CLIP model for image embeddings |
| `MAX_UPLOAD_SIZE` | `10485760` | Max file upload size (10MB) |
| `CACHE_TTL` | `3600` | Cache time-to-live in seconds |

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_LOG_LEVEL` | `INFO` | Django log level (DEBUG, INFO, WARNING, ERROR) |

### AWS S3 Storage (Optional - for production file storage)

| Variable | Required | Description |
|----------|----------|-------------|
| `USE_S3` | `False` | Enable S3 storage (`True`/`False`) |
| `AWS_ACCESS_KEY_ID` | - | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | - | AWS secret key |
| `AWS_STORAGE_BUCKET_NAME` | - | S3 bucket name |
| `AWS_S3_REGION_NAME` | `us-east-1` | AWS region |

---

## 📋 Quick Setup Checklist

### Step 1: Go to Render Dashboard
1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Select your **realmeta** service
3. Click **Environment** tab

### Step 2: Add Required Variables

Click **Add Environment Variable** for each:

```
SECRET_KEY = c*nvuc(oy*29017knmo7@_(n9a-3ny6!po=_v%b-*g7ic_p3^@
DEBUG = False
DATABASE_URL = postgresql://neondb_owner:npg_eX2Cu1dbNzfF@ep-curly-boat-ahq7twdx-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
ALLOWED_HOSTS = realmeta.onrender.com,localhost,127.0.0.1
```

### Step 3: Save and Deploy
1. Click **Save Changes**
2. Render will automatically redeploy
3. Wait 2-3 minutes for deployment

### Step 4: Run Migrations (First Time Only)

After deployment, you may need to run migrations manually:

1. Go to **Shell** tab in Render Dashboard
2. Run:
```bash
python manage.py migrate
```

Or use Render's manual deploy with:
```bash
python manage.py migrate && gunicorn artscope.wsgi:application
```

---

## 🔍 Verify Configuration

### Check Deployment Logs

In Render Dashboard → Logs, you should see:

```
✅ Server running at https://realmeta.onrender.com
✅ PostgreSQL connected successfully
✅ Static files collected
⚠️  CLIP not available (expected - optional AI feature)
```

### Test Endpoints

1. **Homepage:** https://realmeta.onrender.com/
2. **Scanner:** https://realmeta.onrender.com/scanner/
3. **API Health:** https://realmeta.onrender.com/api/health/
4. **Sessions:** https://realmeta.onrender.com/api/sessions/ (POST)
5. **Admin:** https://realmeta.onrender.com/admin/

---

## 🐛 Troubleshooting

### Error: "No support for ''"
**Problem:** DATABASE_URL is empty or invalid
**Solution:** Make sure DATABASE_URL is set correctly without `psql` command

### Error: "DisallowedHost"
**Problem:** Hostname not in ALLOWED_HOSTS
**Solution:** Add your domain to ALLOWED_HOSTS or rely on RENDER_EXTERNAL_HOSTNAME auto-detection

### Error: "OperationalError: relation does not exist"
**Problem:** Migrations not applied
**Solution:** Run `python manage.py migrate` in Render Shell

### Error: 500 Internal Server Error
**Problem:** DEBUG=True in production or missing SECRET_KEY
**Solution:** Set DEBUG=False and add SECRET_KEY

---

## 📦 Current Package Dependencies

These are already in `requirements.txt` and will be installed automatically:

```
Django==5.0.0
djangorestframework==3.14.0
psycopg2-binary==2.9.9
pgvector==0.2.4
gunicorn==21.2.0
deep-translator==1.11.4
gtts==2.5.0
qrcode==7.4.2
geopy==2.4.1
```

No additional installation needed on Render! 🎉

---

## 🔐 Security Notes

1. **Never commit `.env` file to Git** (already in `.gitignore`)
2. **Use strong SECRET_KEY in production** (current one is secure)
3. **Always set DEBUG=False in production**
4. **Use HTTPS only** (Render provides this automatically)
5. **Keep DATABASE_URL secret** (never share publicly)

---

## 🎯 What's Configured

Your ArtScope app now has:

✅ **Auto-translation:** English → 14 languages (Kannada, Hindi, Tamil, Telugu, etc.)
✅ **Text-to-Speech:** Audio narration in all languages
✅ **Geofencing:** GPS-based museum boundary checking
✅ **QR Codes:** Fallback scanning method
✅ **AR Scanner:** Real-time artwork recognition with capture button
✅ **Visitor Sessions:** Anonymous analytics tracking
✅ **Museum Dashboard:** Staff management interface
✅ **PostgreSQL + pgvector:** Production-grade database with AI embeddings
✅ **HTTPS:** Automatic SSL certificate from Render

---

## 📱 Next Steps After Deployment

1. Visit https://realmeta.onrender.com/ to see the new homepage
2. Click "Start Scanning" to test visitor sessions
3. Go to https://realmeta.onrender.com/register/ to register your museum
4. Upload artwork with GPS coordinates
5. Test geofencing and AR scanning

**Deployment Status:** Check at https://dashboard.render.com/

🚀 **Your app is ready for production!**
