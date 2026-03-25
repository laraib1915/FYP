from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, crud, database, auth_service
from services.prediction_service import predict_mortality 

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://192.168.100.13:5173",
        "http://192.168.100.13:3000",
        "http://192.168.100.13:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWT Security
security = HTTPBearer()


def get_current_user(credentials: HTTPBearer = Depends(security), 
                     db: Session = Depends(get_db)) -> models.User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = auth_service.AuthService.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user


# --------------------------------------------------------
# AUTHENTICATION ENDPOINTS
# --------------------------------------------------------

@app.post("/auth/admin-signup", response_model=schemas.LoginResponse)
def admin_signup(request: schemas.AdminSignupRequest, db: Session = Depends(get_db)):
    """Admin self-registration"""
    try:
        user = auth_service.AuthService.create_admin(db, request)
        
        # Generate token
        token = auth_service.AuthService.create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role}
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "hospital_id": user.hospital_id
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    """User login"""
    user = auth_service.AuthService.authenticate_user(db, request.email, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    # Generate token
    token = auth_service.AuthService.create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role}
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "department": user.department,
            "hospital_id": user.hospital_id,
            "is_first_login": user.is_first_login
        }
    }


@app.post("/auth/create-doctor")
def create_doctor(request: schemas.DoctorSignupRequest, 
                  current_user: models.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    """Admin creates doctor account"""
    # Check if current user is admin
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Only admin can create doctors")
    
    try:
        import secrets
        temp_password = secrets.token_urlsafe(12)
        
        user = auth_service.AuthService.create_doctor(
            db, request, current_user.hospital_id, temp_password
        )
        
        # TODO: Send email with temp_password to user
        
        return {
            "message": "Doctor created successfully",
            "user_id": user.id,
            "email": user.email,
            "temp_password": temp_password  # In real app, send via email only
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/create-staff")
def create_staff(request: schemas.StaffSignupRequest,
                 current_user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    """Admin creates staff account"""
    # Check if current user is admin
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Only admin can create staff")
    
    try:
        import secrets
        temp_password = secrets.token_urlsafe(12)
        
        user = auth_service.AuthService.create_staff(
            db, request, current_user.hospital_id, temp_password
        )
        
        # TODO: Send email with temp_password to user
        
        return {
            "message": "Staff created successfully",
            "user_id": user.id,
            "email": user.email,
            "temp_password": temp_password  # In real app, send via email only
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/change-password")
def change_password(request: schemas.ChangePasswordRequest,
                   current_user: models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """Change password (for first login)"""
    try:
        auth_service.AuthService.change_password(
            db, current_user.id, request.current_password, request.new_password
        )
        
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/auth/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """Get current user info"""
    return current_user


@app.get("/users", response_model=list)
def list_hospital_users(current_user: models.User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """List all users in the hospital (admin only)"""
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Only admin can view hospital users")
    
    users = db.query(models.User).filter(
        models.User.hospital_id == current_user.hospital_id
    ).all()
    
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "department": u.department,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]


@app.delete("/users/{user_id}")
def deactivate_user(user_id: str,
                    current_user: models.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """Deactivate a user (admin only)"""
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Only admin can deactivate users")
    
    user = db.query(models.User).filter(
        models.User.id == user_id,
        models.User.hospital_id == current_user.hospital_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == "Admin":
        raise HTTPException(status_code=400, detail="Cannot deactivate admin user")
    
    user.is_active = False
    db.commit()
    
    return {"message": "User deactivated successfully"}


# --------------------------------------------------------
# CREATE PATIENT + RUN LOCAL LIGHTGBM MORTALITY PREDICTION
# --------------------------------------------------------
# --------------------------------------------------------
# CREATE PATIENT + RUN LOCAL LIGHTGBM MORTALITY PREDICTION
# --------------------------------------------------------
@app.post("/patients/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientBase, db: Session = Depends(get_db)):
    try:
        # Run local machine-learning model
        mortality, risk, sofa_score = predict_mortality(patient)

        # Reasoning and recommendations (example)
        reasoning = "Predicted based on burn severity, vitals, and lab values."
        recommendations = [
            "Monitor vitals closely",
            "Provide supportive care",
            "Adjust treatment based on response"
        ]

        prediction = schemas.PredictionResult(
            mortalityRiskPercent=mortality,
            riskLevel=risk,
            sofaScore=sofa_score,
            reasoning=reasoning,
            recommendations=recommendations
        )

        # Save to database
        db_patient = crud.create_patient(db=db, patient=patient, prediction=prediction)
        return db_patient
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# --------------------------------------------------------
# READ LIST OF PATIENTS
# --------------------------------------------------------
@app.get("/patients/", response_model=List[schemas.PatientResponse])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip=skip, limit=limit)


# --------------------------------------------------------
# READ A SINGLE PATIENT
# --------------------------------------------------------
@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def read_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# --------------------------------------------------------
# UPDATE PATIENT
# --------------------------------------------------------
@app.put("/patients/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(patient_id: str, updates: dict, db: Session = Depends(get_db)):
    updated = crud.update_patient(db, patient_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Run LSTM Monitoring Model on updates
    try:
        from services import lstm_service
        # LSTM prediction based on history
        mortality, risk, sofa = lstm_service.predict_mortality(updated)
        
        # Save new dynamic risk
        updated = crud.update_patient_risk(db, patient_id, mortality, risk, sofa)
        
        # If High Risk, maybe add a visual alert flag? taking advantage of 'reasoning' or similar?
        # For now, updating the fields is sufficient as the frontend displays them.
        
    except Exception as e:
        print(f"LSTM Monitoring Error: {e}")
        # Don't fail the request, just log error
        
    return updated


# --------------------------------------------------------
# DELETE PATIENT
# --------------------------------------------------------
@app.delete("/patients/{patient_id}", response_model=schemas.PatientResponse)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_patient(db, patient_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return deleted


# --------------------------------------------------------
# START SERVER
# --------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
