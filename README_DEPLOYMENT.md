# Transport Admin Portal - Cloud Deployment Guide

This guide will help you deploy the Transport Admin Portal to the cloud so everyone can access it.

## 🚀 Quick Deployment (Recommended)

### Option 1: Automated Deployment Script

1. **Navigate to the transport directory:**
   ```bash
   cd python/plugins/transPort
   ```

2. **Run the deployment script:**
   ```bash
   python deploy.py
   ```

3. **Follow the prompts:**
   - Enter a Heroku app name (or press Enter for auto-generated)
   - The script will handle everything else automatically

### Option 2: Manual Deployment

#### Prerequisites

1. **Install Git:**
   - Download from: https://git-scm.com/downloads
   - Or install via package manager

2. **Install Heroku CLI:**
   - Download from: https://devcenter.heroku.com/articles/heroku-cli
   - Or install via package manager

3. **Create Heroku Account:**
   - Sign up at: https://signup.heroku.com/

#### Step-by-Step Deployment

1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Navigate to transport directory:**
   ```bash
   cd python/plugins/transPort
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL database:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   ```

6. **Initialize Git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

7. **Deploy to Heroku:**
   ```bash
   git push heroku main
   ```

8. **Open the application:**
   ```bash
   heroku open
   ```

## 🌐 Alternative Cloud Platforms

### Railway.app (Free Tier Available)

1. **Sign up at:** https://railway.app/
2. **Connect your GitHub repository**
3. **Deploy automatically**

### Render.com (Free Tier Available)

1. **Sign up at:** https://render.com/
2. **Create a new Web Service**
3. **Connect your repository**
4. **Set build command:** `pip install -r requirements.txt`
5. **Set start command:** `gunicorn app:app`

### PythonAnywhere (Free Tier Available)

1. **Sign up at:** https://www.pythonanywhere.com/
2. **Upload your files**
3. **Set up a web app**
4. **Configure WSGI file**

## 🔧 Configuration

### Environment Variables

Set these in your cloud platform:

- `SECRET_KEY`: A secure random string for session encryption
- `DATABASE_URL`: Database connection string (auto-set by Heroku)

### Database Setup

The application will automatically create tables on first run. For production:

1. **Create admin user:**
   ```python
   from app import app, db, User
   with app.app_context():
       admin = User(username='admin', password_hash='...')
       db.session.add(admin)
       db.session.commit()
   ```

2. **Default credentials:**
   - Username: `admin`
   - Password: `admin123`

## 📱 Access Your Application

Once deployed, your application will be available at:
- **Heroku:** `https://your-app-name.herokuapp.com`
- **Railway:** `https://your-app-name.railway.app`
- **Render:** `https://your-app-name.onrender.com`

## 🔒 Security Considerations

1. **Change default password** immediately after first login
2. **Use HTTPS** (automatically provided by cloud platforms)
3. **Set strong SECRET_KEY** in production
4. **Regular backups** of your database
5. **Monitor application logs** for issues

## 🛠️ Troubleshooting

### Common Issues

1. **Build fails:**
   - Check `requirements.txt` has all dependencies
   - Verify Python version in `runtime.txt`

2. **Database connection errors:**
   - Ensure `DATABASE_URL` is set correctly
   - Check database addon is provisioned

3. **Application crashes:**
   - Check logs: `heroku logs --tail`
   - Verify all environment variables are set

### Getting Help

- **Heroku Documentation:** https://devcenter.heroku.com/
- **Application Logs:** `heroku logs --tail`
- **Database Console:** `heroku pg:psql`

## 💰 Cost Considerations

### Free Tiers Available:
- **Heroku:** Free tier discontinued, but affordable paid plans
- **Railway:** $5/month for basic plan
- **Render:** Free tier available
- **PythonAnywhere:** Free tier available

### Recommended for Production:
- **Heroku:** $7/month (Hobby plan)
- **Railway:** $5/month
- **Render:** $7/month

## 🎉 Success!

Once deployed, your Transport Admin Portal will be accessible to everyone with the URL. Share the link with your team and start managing your transport operations from anywhere! 