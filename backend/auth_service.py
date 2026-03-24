from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os
import uuid
import models, schemas

# Load environment variables from parent directory
import sys
from pathlib import Path

# Add backend parent to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

# JWT Configuration - Make sure to load from environment
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    print("WARNING: SECRET_KEY not set in .env, using default")
    SECRET_KEY = "your-secret-key-change-in-production"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication and authorization service"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            print(f"JWT Verification Error: {str(e)}")
            print(f"SECRET_KEY being used: {SECRET_KEY[:20]}...")
            return None
    
    @staticmethod
    def create_admin(db: Session, request: schemas.AdminSignupRequest) -> models.User:
        """Create admin user with hospital"""
        # Check if hospital exists
        existing_hospital = db.query(models.Hospital).filter(
            models.Hospital.name == request.hospital_name
        ).first()
        
        if existing_hospital:
            raise ValueError("Hospital already exists")
        
        # Create admin user first (without hospital reference)
        user_id = str(uuid.uuid4())
        user = models.User(
            id=user_id,
            email=request.email,
            password_hash=AuthService.hash_password(request.password),
            name=request.name,
            role="Admin",
            hospital_id=None,  # Will set after hospital is created
            is_active=True,
            is_first_login=False
        )
        db.add(user)
        db.commit()  # Commit user first
        
        # Create hospital with admin_id
        hospital_id = str(uuid.uuid4())
        hospital = models.Hospital(
            id=hospital_id,
            name=request.hospital_name,
            location="",
            admin_id=user_id  # Now user exists in DB
        )
        db.add(hospital)
        db.commit()
        
        # Update user with hospital_id
        user.hospital_id = hospital_id
        db.commit()
        
        return user
    
    @staticmethod
    def create_doctor(db: Session, request: schemas.DoctorSignupRequest, 
                      hospital_id: str, temp_password: str = None) -> models.User:
        """Create doctor user"""
        # Check if email exists
        existing_user = db.query(models.User).filter(
            models.User.email == request.email
        ).first()
        
        if existing_user:
            raise ValueError("Email already registered")
        
        # Check if license number exists
        existing_doctor = db.query(models.Doctor).filter(
            models.Doctor.license_number == request.license_number
        ).first()
        
        if existing_doctor:
            raise ValueError("License number already registered")
        
        # Create user
        user_id = str(uuid.uuid4())
        user = models.User(
            id=user_id,
            email=request.email,
            password_hash=AuthService.hash_password(temp_password or request.password),
            name=request.name,
            role="Doctor",
            department=request.department,
            hospital_id=hospital_id,
            is_active=True,
            is_first_login=True if temp_password else False
        )
        db.add(user)
        db.commit()
        
        # Create doctor record
        doctor_id = str(uuid.uuid4())
        doctor = models.Doctor(
            id=doctor_id,
            user_id=user_id,
            license_number=request.license_number,
            specialization=request.specialization
        )
        db.add(doctor)
        db.commit()
        
        return user
    
    @staticmethod
    def create_staff(db: Session, request: schemas.StaffSignupRequest, 
                     hospital_id: str, temp_password: str = None) -> models.User:
        """Create staff user"""
        # Check if email exists
        existing_user = db.query(models.User).filter(
            models.User.email == request.email
        ).first()
        
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user
        user_id = str(uuid.uuid4())
        user = models.User(
            id=user_id,
            email=request.email,
            password_hash=AuthService.hash_password(temp_password or request.password),
            name=request.name,
            role="Staff",
            department=request.department,
            hospital_id=hospital_id,
            is_active=True,
            is_first_login=True if temp_password else False
        )
        db.add(user)
        db.commit()
        
        # Create staff record
        staff_id = str(uuid.uuid4())
        staff = models.Staff(
            id=staff_id,
            user_id=user_id,
            designation=request.designation,
            shift=request.shift
        )
        db.add(staff)
        db.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
        """Authenticate user with email and password"""
        user = db.query(models.User).filter(models.User.email == email).first()
        
        if not user:
            return None
        
        if not AuthService.verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def change_password(db: Session, user_id: str, current_password: str, 
                        new_password: str) -> bool:
        """Change user password"""
        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        if not user:
            raise ValueError("User not found")
        
        if not AuthService.verify_password(current_password, user.password_hash):
            raise ValueError("Current password is incorrect")
        
        user.password_hash = AuthService.hash_password(new_password)
        user.is_first_login = False
        db.commit()
        
        return True
