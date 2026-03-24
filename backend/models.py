from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True) # Keeping string ID to match frontend generation or UUID
    timestamp = Column(String)
    status = Column(String, default="Active")
    
    # Patient Data
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    tbsa = Column(Float)
    burnDepth = Column(String)
    inhalationInjury = Column(Boolean)
    comorbidities = Column(String)
    burnedRegions = Column(JSON) # List of strings

    # Hemodynamics
    heartRate = Column(Float)
    systolicBP = Column(Float)
    diastolicBP = Column(Float)
    temperature = Column(Float)

    # Respiratory
    spo2 = Column(Float)
    pao2 = Column(Float)
    fio2 = Column(Float)

    # Renal
    urineOutput = Column(Float)

    # Labs
    platelets = Column(Float)
    bilirubin = Column(Float)
    creatinine = Column(Float)

    # Neurological
    gcsEye = Column(Integer)
    gcsVerbal = Column(Integer)
    gcsMotor = Column(Integer)

    # Prediction Results
    mortalityRiskPercent = Column(Float, nullable=True)
    riskLevel = Column(String, nullable=True)
    sofaScore = Column(Float, nullable=True)
    reasoning = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True) # List of strings

    # History
    hourlyVitals = Column(JSON, default=list)

    # Real-time Monitoring (LSTM)
    currentMortalityRisk = Column(Float, nullable=True)
    currentRiskLevel = Column(String, nullable=True)
    currentSofaScore = Column(Float, nullable=True)


# ========== AUTHENTICATION MODELS ==========

class Hospital(Base):
    __tablename__ = "hospitals"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    admin_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    role = Column(String)  # Admin, Doctor, Staff
    department = Column(String, nullable=True)  # Ward, ICU (if applicable)
    hospital_id = Column(String, ForeignKey("hospitals.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_first_login = Column(Boolean, default=True)  # For temp password change
    created_at = Column(DateTime, default=datetime.utcnow)


class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    license_number = Column(String, unique=True, index=True)
    specialization = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Staff(Base):
    __tablename__ = "staff"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    designation = Column(String)  # Nurse, Technician, etc
    shift = Column(String, nullable=True)  # Morning, Evening, Night
    created_at = Column(DateTime, default=datetime.utcnow)
