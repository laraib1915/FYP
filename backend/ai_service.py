import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from .schemas import PatientBase, PredictionResult

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("Warning: API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

def predict_mortality(data: PatientBase) -> PredictionResult:
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
    Act as a highly accurate medical burn mortality prediction model (simulating Baux Score, Revised Baux Score, and SOFA Score logic).
    
    Patient Data:
    - Age: {data.age}
    - Gender: {data.gender}
    - TBSA: {data.tbsa}%
    - Burn Depth: {data.burnDepth}
    - Inhalation Injury: {"YES" if data.inhalationInjury else "NO"}
    - Comorbidities: {data.comorbidities or "None reported"}
    
    Clinical Vitals & Labs:
    - Heart Rate: {data.heartRate} bpm
    - BP: {data.systolicBP}/{data.diastolicBP} mmHg
    - SpO2: {data.spo2}%
    - PaO2: {data.pao2} mmHg
    - FiO2: {data.fio2}%
    - Platelets: {data.platelets} x10^3/µL
    - Bilirubin: {data.bilirubin} mg/dL
    - Creatinine: {data.creatinine} mg/dL
    - Glasgow Coma Scale: Eye={data.gcsEye}, Verbal={data.gcsVerbal}, Motor={data.gcsMotor} (Total: {data.gcsEye + data.gcsVerbal + data.gcsMotor})

    Task:
    1. Calculate the SOFA (Sequential Organ Failure Assessment) score based on the provided labs and vitals (Respiration, Coagulation, Liver, Cardiovascular, CNS, Renal).
    2. Estimate the mortality risk percentage considering both the Burn Injury (Revised Baux) and Organ Failure (SOFA).
    3. Provide a medical reasoning summary explaining the Baux Score and SOFA Score contribution.
    4. List 3 key clinical recommendations.
    
    Return strict JSON.
    """

    generation_config = {
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40,
        "response_mime_type": "application/json",
    }

    try:
        response = model.generate_content(prompt, generation_config=generation_config)
        result = json.loads(response.text)
        return PredictionResult(**result)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        # Fallback or error handling
        return PredictionResult(
            mortalityRiskPercent=0.0,
            riskLevel="Unknown",
            sofaScore=0.0,
            reasoning="AI Service Error: " + str(e),
            recommendations=["Check API Key", "Retry prediction"]
        )
