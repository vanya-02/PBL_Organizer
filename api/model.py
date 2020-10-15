from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
migrate = Migrate()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.INTEGER, primary_key=True)
    creation_date = db.Column(db.DATETIME)
    first_name = db.Column(db.VARCHAR(60))
    last_name = db.Column(db.VARCHAR(60))
    email = db.Column(db.VARCHAR(150), unique=True)
    password = db.Column(db.VARCHAR(120), unique=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
