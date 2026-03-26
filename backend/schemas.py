from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    tbsa: float
    burnDepth: str
    inhalationInjury: bool
    comorbidities: Optional[str] = None
    burnedRegions: List[str] = []

    heartRate: float
    systolicBP: float
    diastolicBP: float
    temperature: float
    
    spo2: float
    pao2: float
    fio2: float
    
    urineOutput: float
    
    platelets: float
    bilirubin: float
    creatinine: float
    
    gcsEye: int
    gcsVerbal: int
    gcsMotor: int

class PredictionResult(BaseModel):
    mortalityRiskPercent: float
    riskLevel: str
    sofaScore: Optional[float] = None
    reasoning: str
    recommendations: List[str]

class PatientResponse(PatientBase, PredictionResult):
    id: str
    timestamp: str
    status: str
    hourlyVitals: List[dict] = []
    
    currentMortalityRisk: Optional[float] = None
    currentRiskLevel: Optional[str] = None
    currentSofaScore: Optional[float] = None

    class Config:
        from_attributes = True


class TBSAResultRequest(BaseModel):
    total_tbsa: float
    breakdown: Optional[dict] = None
    regions: Optional[list] = None


# ========== AUTHENTICATION SCHEMAS ==========

class AdminSignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    hospital_name: str


class DoctorSignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    license_number: str
    specialization: str
    department: str  # Ward or ICU


class StaffSignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    designation: str
    department: str  # Ward or ICU
    shift: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    department: Optional[str]
    hospital_id: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class HospitalResponse(BaseModel):
    id: str
    name: str
    location: str
    created_at: datetime

    class Config:
        from_attributes = True


class DoctorResponse(BaseModel):
    id: str
    user_id: str
    license_number: str
    specialization: str
    created_at: datetime

    class Config:
        from_attributes = True


class StaffResponse(BaseModel):
    id: str
    user_id: str
    designation: str
    shift: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
