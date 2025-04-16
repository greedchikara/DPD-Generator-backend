from fastapi import Body, FastAPI, Form, UploadFile, File, Depends
from typing import List, Dict
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from services.ai.factory import ai_provider_dependency
from services.ai.ai_providers.base import AIProvider
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(os.environ.get("UPLOAD_DIR"), exist_ok=True)

class Item(BaseModel):
    photos: list
    answers: dict

@app.get("/health-checkup")
async def health_checkup():
    return {"message": "Everything is fine!"}

@app.post("/upload/chunks")
async def upload_chunks(file: UploadFile =File(...), name: str = Form(...), chunk_number: int = Form(0), total_chunks: int = Form(1)):
    is_last = int(chunk_number) + 1 == int(total_chunks)
    file_name = f"{name}-{chunk_number}"
    chunk_path = os.path.join(os.environ.get("UPLOAD_DIR"), file_name)
    with open(chunk_path, "wb") as buffer:
        while content := await file.read(1024 * 64):  # 64KB buffer read
            buffer.write(content)
    
    if is_last:
        full_file_path = os.path.join(os.environ.get("UPLOAD_DIR"), name)
        with open(full_file_path, "wb") as buffer:
            chunk = 0
            while chunk < total_chunks:
                chunk_path = os.path.join(os.environ.get("UPLOAD_DIR"), f"{name}-{chunk}")
                with open(chunk_path, "rb") as infile:
                    buffer.write(infile.read())
                    infile.close()
                os.remove(f"{os.environ.get('UPLOAD_DIR')}/{name}-{chunk}")
                chunk += 1
        buffer.close()
        return {"message": "File uploaded successfully!"}
    return {"message": f"Chunk number {chunk_number} uploaded successfully!", "file_url": os.path.join(os.environ.get("UPLOAD_DIR"), name)}
    

@app.post("/generate-description")
async def generate_description(data: Item = Body(...), ai_provider: AIProvider = Depends(ai_provider_dependency)):
    if (len(data.photos) == 0):
        return {"message": "Please select atleast 1 photo!"}  
    
    prompt = build_prompt(data.answers, data.photos)
   
    description = ai_provider.generate_content("gemini-2.0-flash", prompt)
    return {"message": "Successfully created description", "description": description}
    
def build_prompt(answers: Dict, photos: List[str]):

    formatted_answers = ""
    if any(answers):
        for i, a in answers.items():
            formatted_answers += f"{i}: "
            if (a.strip()):
                formatted_answers += f"{a}\n"
            else:
                formatted_answers += "No written answer provided.\n"
                
    prompt = f"""
        You are an expert dating profile copywriter who helps users create fun, engaging, and respectful dating bios. Your goal is to craft a 4-5 sentence dating profile based on the user's uploaded photos (represented by a count) and optional written answers. 

        Instructions:
        - Use confident, creative, and friendly language (use emoji's).
        - If the user has provided information about their interests, personality, or what they are looking for in a partner, include it naturally.
        - If no written answers are provided, create a compelling and general description based on the idea that the user has uploaded {len(photos)} photo(s).
        - Always include a friendly prompt to check out the user’s photos (e.g., “Check out my pics to get a glimpse!”).
        - Avoid using or referencing any vulgar or disrespectful language. If inappropriate content is present, simply omit it.
        - Keep the tone positive, respectful, and engaging.
        - End with a light call to action or flirty teaser if appropriate.

        User Answers:
        {formatted_answers}
    """
    return prompt