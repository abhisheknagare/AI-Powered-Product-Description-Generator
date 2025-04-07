# backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from services.llm_service import (
    generate_product_description,
    generate_seo_elements,
    generate_marketing_copy,
    generate_dalle_prompt
)

app = FastAPI(
    title="Product Content Generator API",
    description="API for generating product descriptions, SEO elements, marketing copy, and image prompts",
    version="1.0.0"
)

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only specify the methods you actually need
    allow_headers=["Content-Type", "Authorization"],
)

class ProductRequest(BaseModel):
    product: Dict[str, Any]
    tone: Optional[str] = Field(default="default", description="Tone of the generated content")
    length: Optional[str] = Field(default="medium", description="Length of the generated content")
    style: Optional[str] = Field(default="standard", description="Style of the generated content")
    platform: Optional[str] = Field(default="email", description="Platform for marketing content") 

    class Config:
        schema_extra = {
            "example": {
                "product": {
                    "name": "Example Product",
                    "description": "Basic product description",
                    "features": ["Feature 1", "Feature 2"]
                },
                "tone": "professional",
                "length": "medium",
                "style": "standard",
                "platform": "email"
            }
        }

@app.post("/generate/description", response_model=Dict[str, str], tags=["Content Generation"])
async def generate_description(req: ProductRequest):
    """Generate a product description based on the provided product information."""
    try:
        result = generate_product_description(req.product, req.tone, req.length, req.style)
        return {"description": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/seo", response_model=Dict[str, Any], tags=["Content Generation"])
async def generate_seo(req: ProductRequest):
    """Generate SEO elements for a product."""
    try:
        result = generate_seo_elements(req.product, req.tone, req.length, req.style)
        return {"seo": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/marketing", response_model=Dict[str, str], tags=["Content Generation"])
async def generate_marketing(req: ProductRequest):
    """Generate marketing copy for a product on a specific platform."""
    try:
        result = generate_marketing_copy(req.product, req.platform, req.tone, req.length, req.style)
        return {"marketing": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/image-prompt", response_model=Dict[str, str], tags=["Content Generation"])
async def generate_image_prompt(req: ProductRequest):
    """Generate an image prompt for DALL-E based on product information."""
    try:
        result = generate_dalle_prompt(req.product)
        return {"image_prompt": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

