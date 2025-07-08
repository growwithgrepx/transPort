from extensions import db

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(db.UnicodeText)  # Flask-Security-Too expects this

    def get_permissions(self):
        if self.permissions:
            return self.permissions.split(',')
        return [] 