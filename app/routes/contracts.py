import os
import uuid
from config import ALLOWED_FILE_EXTENSIONS, MAX_FILE_SIZE_MB, UPLOAD_DIR
from fastapi import APIRouter, File, HTTPException, UploadFile
from services.document_parser import extract_text
from models import Contract
from database import contracts_collection

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    # Validate file extension
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code = 400,
            detail=f"Unsupported file extension {ext}. Allowed: {ALLOWED_FILE_EXTENSIONS}"
        )

    # Read file bytes & validate max size
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            details=f"File exceeds maximum allowed size of {MAX_FILE_SIZE_MB}",
        )

    # Ensure storage directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file locally with unique UUID filename
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Extract text content from document
    parsed = extract_text(file_path)

    contract_data = Contract(
    filename=unique_name,
    original_name=file.filename,
    text_content=parsed["text"] if isinstance(parsed, dict) else parsed,
    page_count=int(parsed["page_count"]) if isinstance(parsed, dict) else len(parsed.splitlines()),
    word_count=int(parsed["word_count"]) if isinstance(parsed, dict) else len(parsed.split())
)

    doc = contract_data.model_dump()
    result = contracts_collection.insert_one(doc)
    contract_data.id = str(result.inserted_id)

    return {
    "message": "File uploaded and processed successfully",
    "contract": contract_data.model_dump(),
    "id"      : contract_data.id
}

@router.get("/")
async def list_contracts():
    """
    List all uploaded contracts.
    """
    contracts = []
    for doc in contracts_collection.find({}, {"text_content": 0}):
        contract = Contract(**doc)
        contract.id = str(doc["_id"])
        contracts.append(contract.model_dump())
        
    return {"contracts": contracts}

@router.get("/{contract_id}")
async def get_contract(contract_id: str):
    """
    Retrieve a specific contract by its ID.
    """
    from bson import ObjectId
    
    doc = contracts_collection.find_one({"_id": ObjectId(contract_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    contract = Contract(**doc)
    contract.id = str(doc["_id"])
    
    return {"contract": contract.model_dump()}

