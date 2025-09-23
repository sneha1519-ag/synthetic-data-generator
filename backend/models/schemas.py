from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal


class DataGenerationRequest(BaseModel):
    rowCount: int = Field(..., description="Number of rows to generate", ge=10, le=10000)
    fields: Optional[List[str]] = Field(None, description="List of field IDs to generate")
    realism: str = Field("realistic", description="Data realism mode: realistic, randomized, or biased")
    generationMode: str = Field(..., description="Generation mode: manual or ai")
    prompt: Optional[str] = Field(None, description="AI prompt for data generation")

    class Config:
        schema_extra = {
            "example": {
                "rowCount": 100,
                "fields": ["name", "email", "address", "phone"],
                "realism": "realistic",
                "generationMode": "manual",
                "prompt": None
            }
        }


class DataGenerationResponse(BaseModel):
    datasetId: str = Field(..., description="Unique identifier for the generated dataset")
    rowCount: int = Field(..., description="Number of rows generated")
    fields: List[str] = Field(..., description="List of field names in the dataset")
    sampleData: List[Dict[str, Any]] = Field(..., description="Sample of the generated data (up to 10 rows)")

    class Config:
        schema_extra = {
            "example": {
                "datasetId": "550e8400-e29b-41d4-a716-446655440000",
                "rowCount": 100,
                "fields": ["name", "email", "address", "phone"],
                "sampleData": [
                    {
                        "name": "John Smith",
                        "email": "john.smith@example.com",
                        "address": "123 Main St",
                        "phone": "555-123-4567"
                    }
                ]
            }
        }