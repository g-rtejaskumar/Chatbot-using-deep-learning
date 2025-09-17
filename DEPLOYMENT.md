# Chatbot Deployment Guide

This guide will help you deploy your Django chatbot application to Railway (recommended) or other platforms.

## ✅ Pre-Deployment Checklist

The following files have been created/modified for production deployment:

### New Files Added:
- `Procfile` - Defines how Railway runs your app
- `runtime.txt` - Specifies Python version
- `railway.json` - Railway deployment configuration
- `.env.example` - Environment variables template
- `download_nltk_data.py` - Script to download required NLTK data
- `build.sh` - Build script for deployment

### Modified Files:
- `requirements.txt` - Updated with production dependencies
- `Chatbot/settings.py` - Production-ready Django settings

## 🚀 Deployment Options

### Option 1: Railway (Recommended)

Railway is perfect for this project due to its ease of use and automatic PostgreSQL database provisioning.

#### Step 1: Push Changes to GitHub

1. **Add all new files to your repository:**
   ```bash
   git add .
   git commit -m "Add production deployment configuration"
   git push origin main
   ```

#### Step 2: Deploy to Railway

1. **Create a Railway account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with your GitHub account

2. **Deploy your repository:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `Chatbot-using-deep-learning` repository
   - Railway will automatically detect it's a Python project

3. **Add a PostgreSQL database:**
   - In your project dashboard, click "New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

4. **Set environment variables:**
   - Go to your service → "Variables" tab
   - Add the following variables:
     ```
     SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
     DEBUG=False
     ALLOWED_HOSTS=*.railway.app
     ```

5. **Deploy:**
   - Railway will automatically build and deploy your application
   - You'll get a URL like `https://your-app-name.railway.app`

#### Step 3: Verify Deployment

1. Visit your Railway app URL
2. The chatbot interface should load
3. Test the chatbot functionality

### Option 2: Render

1. **Create a Render account:**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Create a new Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command:** `chmod +x build.sh && ./build.sh`
     - **Start Command:** `gunicorn Chatbot.wsgi:application`
     - **Python Version:** `3.9.18`

3. **Add PostgreSQL database:**
   - Create a new PostgreSQL database in Render
   - Copy the External Database URL
   - Add it as `DATABASE_URL` environment variable

4. **Set environment variables:**
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_URL=postgresql://user:pass@hostname:port/dbname
   ```

### Option 3: Heroku

1. **Install Heroku CLI and login:**
   ```bash
   # Install Heroku CLI first
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create your-chatbot-app-name
   ```

3. **Add PostgreSQL addon:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY="your-super-secret-key-here"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

## 🔧 Local Development Setup

For testing locally with the new configuration:

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with:
   ```
   SECRET_KEY=your-local-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

4. **Download NLTK data and run migrations:**
   ```bash
   python download_nltk_data.py
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## 🐛 Troubleshooting

### Common Issues:

1. **NLTK Data Missing:**
   - The `download_nltk_data.py` script should handle this automatically
   - If issues persist, manually run: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

2. **Static Files Not Loading:**
   - Run `python manage.py collectstatic` locally to test
   - Ensure `STATIC_ROOT` is set correctly in settings

3. **Database Connection Issues:**
   - Verify `DATABASE_URL` environment variable is set
   - Check that PostgreSQL addon is properly connected

4. **TensorFlow/TFLearn Issues:**
   - The app uses TensorFlow v1 compatibility mode
   - If deployment fails, check that all model files are included in git

5. **Template Not Found:**
   - Verify template paths are correct in settings.py
   - Templates should be in `MyChatBot/templates/`

## 📁 File Structure

After deployment setup, your project structure should look like:

```
Chatbot-using-deep-learning/
├── Chatbot/                    # Django project settings
│   ├── settings.py            # ✅ Updated for production
│   ├── urls.py
│   └── wsgi.py
├── MyChatBot/                 # Django app
│   ├── static/               # CSS, JS files
│   ├── templates/            # HTML templates
│   ├── dataset/              # Training data
│   ├── model/                # Pre-trained model files
│   ├── views.py              # App logic
│   └── ...
├── requirements.txt           # ✅ Updated dependencies
├── Procfile                   # ✅ Railway/Heroku configuration
├── runtime.txt                # ✅ Python version
├── railway.json              # ✅ Railway settings
├── .env.example              # ✅ Environment variables template
├── download_nltk_data.py     # ✅ NLTK data downloader
├── build.sh                  # ✅ Build script
└── manage.py                 # Django management script
```

## 🔐 Security Notes

- Never commit your actual `.env` file to git
- Use strong, unique SECRET_KEY values
- Keep DEBUG=False in production
- Regularly update dependencies for security patches

## ✅ Next Steps

1. Test your deployed application thoroughly
2. Monitor performance and logs
3. Set up custom domain if needed
4. Consider implementing user authentication
5. Add monitoring and error tracking (e.g., Sentry)

Your chatbot application is now ready for production deployment! 🎉