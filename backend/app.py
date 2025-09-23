from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uuid
import os
import json
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import random
import pandas as pd
from datetime import datetime
import pathlib

from models.schemas import DataGenerationRequest, DataGenerationResponse
from generators.faker_generator import generate_fake_data
from generators.random_generator import generate_random_data
from generators.ai_generator import generate_ai_data
from utils.csv_utils import save_data_to_csv

# Create temp directory for storing generated files
TEMP_DIR = pathlib.Path("./temp_data")
TEMP_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Synthetic Data Generator API",
    description="API for generating synthetic data for various use cases",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for generated datasets (in a real app, use a database)
datasets = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Synthetic Data Generator API"}

@app.post("/api/generate-data", response_model=DataGenerationResponse)
async def generate_data(request: DataGenerationRequest):
    try:
        # Generate a unique dataset ID
        dataset_id = str(uuid.uuid4())

        # Determine which generator to use based on the realism setting
        if request.generationMode == "ai":
            if not request.prompt:
                raise HTTPException(status_code=400, detail="Prompt is required for AI generation mode")

            # Use AI-powered generation
            data, fields = generate_ai_data(
                prompt=request.prompt,
                row_count=request.rowCount,
                realism=request.realism
            )
        else:  # Manual field selection mode
            if not request.fields or len(request.fields) == 0:
                raise HTTPException(status_code=400, detail="At least one field must be selected")

            # Use appropriate generator based on realism setting
            if request.realism == "realistic":
                data = generate_fake_data(request.fields, request.rowCount)
            elif request.realism == "randomized":
                data = generate_random_data(request.fields, request.rowCount)
            elif request.realism == "biased":
                # For biased data, we'll use the fake generator but with biasing applied
                data = generate_fake_data(request.fields, request.rowCount, biased=True)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported realism mode: {request.realism}")

            fields = request.fields

        # Save the data to a CSV file
        csv_path = save_data_to_csv(data, dataset_id)

        # Store dataset information
        datasets[dataset_id] = {
            "path": str(csv_path),
            "created_at": datetime.now().isoformat(),
            "fields": fields,
            "row_count": request.rowCount,
            "realism": request.realism,
        }

        # Return a sample of the generated data (first 10 rows)
        sample_data = data[:10] if len(data) > 10 else data

        return DataGenerationResponse(
            datasetId=dataset_id,
            rowCount=len(data),
            fields=fields,
            sampleData=sample_data
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{dataset_id}")
async def download_dataset(dataset_id: str):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset_info = datasets[dataset_id]
    file_path = dataset_info["path"]

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV file not found")

    filename = f"synthetic_data_{dataset_id}.csv"

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )

@app.delete("/api/datasets/{dataset_id}")
async def delete_dataset(dataset_id: str):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset_info = datasets[dataset_id]
    file_path = dataset_info["path"]

    # Delete the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remove from our dataset tracking
    del datasets[dataset_id]

    return {"message": "Dataset deleted successfully"}

# Clean up function for expired datasets (could be called by a scheduler)
@app.post("/api/cleanup")
async def cleanup_old_datasets(background_tasks: BackgroundTasks):
    # In a real app, this would remove datasets older than a certain threshold
    background_tasks.add_task(cleanup_expired_datasets)
    return {"message": "Cleanup task started"}

def cleanup_expired_datasets():
    # This would clean up datasets older than a certain time
    # Simplified for this example
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)