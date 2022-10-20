_A='utf-8'
import bcrypt
def hash_password(password):password=password.encode(_A);return bcrypt.hashpw(password,bcrypt.gensalt())
def check_password(password,hashed):password=password.encode(_A);return bcrypt.hashpw(password,hashed)==hashed