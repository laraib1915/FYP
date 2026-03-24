# Burn Care Management System - Setup Guide

## Prerequisites
- **Node.js** (v16+)
- **Python** (v3.10+)
- **PostgreSQL** (v18+)
- **Git**

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/burncare.git
cd burncare
```

### 2. Backend Setup

#### Install PostgreSQL
- Download from: https://www.postgresql.org/download/
- Install PostgreSQL 18+
- Note your `postgres` password during installation

#### Create Environment Variables
```bash
cd backend
copy .env.example .env
```
Edit `.env` and fill in your PostgreSQL credentials:
```
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=burncare
```

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Create Database
```bash
psql -U postgres -h localhost -c "CREATE DATABASE burncare;"
```

#### Start Backend Server
```bash
python main.py
```
Server runs on: `http://localhost:8000`

Check API: `http://localhost:8000/docs` (Swagger UI)

---

### 3. Frontend Setup

```bash
cd ..
npm install
npm run dev
```
App runs on: `http://localhost:5173`

---

## Database Management

### View Database in pgAdmin
1. Download pgAdmin: https://www.pgadmin.org/download/
2. Open pgAdmin → Add PostgreSQL server
3. Host: `localhost`, User: `postgres`, Password: your password
4. Navigate to `burncare` → `Tables` → `patients`

### Check API Endpoints
- **Swagger UI**: http://localhost:8000/docs
- **Get all patients**: GET http://localhost:8000/patients/
- **Create patient**: POST http://localhost:8000/patients/

---

## Troubleshooting

**Port 8000 already in use:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**PostgreSQL connection error:**
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database `burncare` exists

**Node modules not working:**
```bash
rm -r node_modules
npm install
```

---

## Team Collaboration

- Create feature branches: `git checkout -b feature/your-feature`
- Push to GitHub and create Pull Requests
- Use Swagger UI to test API changes
- Check pgAdmin for database changes

---

## Project Structure
```
burncare/
├── backend/              # FastAPI server
│   ├── main.py          # API endpoints
│   ├── models.py        # Database models
│   ├── database.py      # PostgreSQL config
│   ├── schemas.py       # Data validation
│   ├── crud.py          # Database operations
│   ├── requirements.txt  # Python dependencies
│   └── services/        # AI services (LSTM, LightGBM)
├── components/          # React components
├── services/           # Frontend services
├── App.tsx            # Main app
├── package.json       # Node dependencies
└── vite.config.ts     # Vite config

```
