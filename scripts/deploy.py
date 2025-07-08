#!/usr/bin/env python3
"""
Deployment script for Transport Admin Portal
This script helps deploy the application to cloud platforms
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking deployment requirements...")
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git"):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Check if Heroku CLI is installed
    if not run_command("heroku --version", "Checking Heroku CLI"):
        print("❌ Heroku CLI is not installed.")
        print("📥 Please install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    return True

def setup_heroku_app():
    """Set up Heroku app and database"""
    print("\n🚀 Setting up Heroku deployment...")
    
    # Get app name from user or generate one
    app_name = input("Enter Heroku app name (or press Enter for auto-generated name): ").strip()
    
    if not app_name:
        import uuid
        app_name = f"transport-admin-{str(uuid.uuid4())[:8]}"
        print(f"Generated app name: {app_name}")
    
    # Create Heroku app
    if not run_command(f"heroku create {app_name}", "Creating Heroku app"):
        return None
    
    # Add PostgreSQL database
    if not run_command(f"heroku addons:create heroku-postgresql:mini --app {app_name}", "Adding PostgreSQL database"):
        return None
    
    # Set environment variables
    secret_key = os.urandom(24).hex()
    run_command(f"heroku config:set SECRET_KEY={secret_key} --app {app_name}", "Setting secret key")
    
    return app_name

def deploy_to_heroku(app_name):
    """Deploy the application to Heroku"""
    print(f"\n🚀 Deploying to Heroku app: {app_name}")
    
    # Initialize git if not already done
    if not os.path.exists('.git'):
        run_command("git init", "Initializing Git repository")
        run_command("git add .", "Adding files to Git")
        run_command('git commit -m "Initial commit"', "Making initial commit")
    
    # Add Heroku remote
    run_command(f"heroku git:remote -a {app_name}", "Adding Heroku remote")
    
    # Deploy to Heroku
    if run_command("git push heroku main", "Deploying to Heroku"):
        print(f"\n🎉 Deployment successful!")
        print(f"🌐 Your app is available at: https://{app_name}.herokuapp.com")
        return True
    
    return False

def main():
    """Main deployment function"""
    print("🚀 Transport Admin Portal - Cloud Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Please run this script from the transport application directory")
        print("   Expected: python/plugins/transPort/")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Deployment requirements not met. Please install missing tools.")
        sys.exit(1)
    
    # Setup Heroku app
    app_name = setup_heroku_app()
    if not app_name:
        print("\n❌ Failed to setup Heroku app")
        sys.exit(1)
    
    # Deploy
    if deploy_to_heroku(app_name):
        print(f"\n🎉 Success! Your Transport Admin Portal is now live!")
        print(f"🌐 URL: https://{app_name}.herokuapp.com")
        print(f"👤 Default admin credentials:")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"\n⚠️  IMPORTANT: Change the default password after first login!")
    else:
        print("\n❌ Deployment failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 