from extensions import db
from flask_login import UserMixin
import uuid
from .role import Role
from .association import roles_users

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(150), unique=True, nullable=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    
    def check_password(self, password):
        """Simple plaintext password check - no hashing"""
        return self.password == password
    
    def set_password(self, password):
        """Set password without hashing"""
        self.password = password
    
    def get_id(self):
        """Flask-Login method to return user ID as string"""
        return str(self.id)
    
    def is_authenticated(self):
        """Flask-Login method"""
        return True
    
    def is_active(self):
        """Flask-Login method"""
        return self.active
    
    def is_anonymous(self):
        """Flask-Login method"""
        return False 