from fastapi import FastAPI, Form, UploadFile, File, Depends
from typing import List, Dict
import os, shutil, json
import uuid
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from services.ai.factory import ai_provider_dependency
from services.ai.ai_providers.base import AIProvider

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(os.environ.get("UPLOAD_DIR"), exist_ok=True)

@app.get("/health-checkup")
async def health_checkup():
    return {"message": "Everything is fine!"}

@app.post("/generate-description")
async def generate_description(photos: List[UploadFile] = File(...), answers: str = Form(default=None), ai_provider: AIProvider = Depends(ai_provider_dependency)):
    
    filenames = []

    for photo in photos:
        uid = str(uuid.uuid4()) + "_" + photo.filename
        path = os.path.join(os.environ.get("UPLOAD_DIR"), uid)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        filenames.append(uid)
    
    answers_list = []
    if (answers):
        answers_list = json.loads(answers)    
    
    prompt = build_prompt(answers_list, filenames)
    description = ai_provider.generate_content("gemini-2.0-flash", prompt)
    return {"description": description}
    
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