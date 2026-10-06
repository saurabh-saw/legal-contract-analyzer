from database import init_db
from fastapi import FastAPI
from routes.contracts import router as contracts_router
from routes.analysis import router as analysis_router

app = FastAPI(
    title="Legal Contract Analyzer API",
    description="AI-powered contract analysis using AI",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def read_root():
    return{
        "title": "Vakil Contract API",
        "version": "1.0.0",
        "endpoints": {
            "POST /contracts/upload": "Upload a PDF or TXT contract for analysis",
            "GET /contracts": "Retrieve all list of contracts",
            "GET /contracts/{contract_id}": "Fetch a contract by a specific ID",
            "POST /analysis/analyze/{contract_id}": "Start the contract analysis process",
            "GET /analysis/{analysis_id}": "Retrieve an analysis by ID",
            "GET /analysis/contract/{contract_id}": "Retrieve list of analyses for a particular contract ID",
        }
    }

app.include_router(contracts_router)
app.include_router(analysis_router)
