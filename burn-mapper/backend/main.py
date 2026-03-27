"""
main.py — FastAPI app
Run: uvicorn server.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os, json, uuid
from .tbsa import calculate_tbsa_from_mask

router = APIRouter()
app = FastAPI(title="Burn Mapper API")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)
ASSESSMENTS_FILE = os.path.join(DATA_DIR, 'assessments.json')

def load_assessments():
    if not os.path.exists(ASSESSMENTS_FILE):
        return {}
    with open(ASSESSMENTS_FILE,'r') as f:
        return json.load(f)

def save_assessments(d):
    with open(ASSESSMENTS_FILE,'w') as f:
        json.dump(d, f, indent=2)

class MaskPayload(BaseModel):
    mask_base64: str

class SavePayload(BaseModel):
    timestamp: Optional[str]
    mask_base64: Optional[str]
    strokes: Optional[List[Dict[str,Any]]]
    view: Optional[str]

@router.post("/calculate-tbsa")
async def calculate_tbsa(payload: MaskPayload):
    try:
        result = calculate_tbsa_from_mask(payload.mask_base64)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-assessment")
async def save_assessment(payload: SavePayload):
    db = load_assessments()
    aid = str(uuid.uuid4())
    entry = payload.dict()
    entry['id'] = aid
    db[aid] = entry
    save_assessments(db)
    return {"status":"ok","id":aid}

@router.get("/load-assessment")
async def load_assessment(id: Optional[str] = None):
    db = load_assessments()
    if id:
        if id in db:
            return db[id]
        raise HTTPException(status_code=404, detail="Assessment not found")
    return list(db.values())


app.include_router(router)

# ---------------------------
# Project Notes
# ---------------------------
"""
How to use:

1) Paste your front/back base64 data URIs into static/script.js FRONT_IMAGE_BASE64 and BACK_IMAGE_BASE64.
   - Alternatively serve your images under a static path and set imgFront.src / imgBack.src accordingly.

2) Run backend:
   pip install fastapi uvicorn pillow
   uvicorn server.main:app --reload --port 8000

3) Serve static files:
   - For dev, open static/index.html in browser (but for server calls to work, host static files on same origin or proxy).
   - To serve both, add a simple static file server (e.g. mount static dir in FastAPI) or run a small static server (e.g., `python -m http.server 8080` in static/).

Debug overlay:
 - Click "Toggle Overlay" to show polygon outlines and labels to validate alignment. If a polygon seems off, we can tweak its normalized coordinates here.

Important:
 - The frontend and server share the same normalized polygons. If you edit polygons, edit both `static/script.js` and `server/region_mapping.py`.
"""