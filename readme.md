# 🚀 Dating Profile Description Generator (Backend)

A FastAPI backend service that powers the **Dating Profile Description Generator** by handling image uploads and generating personalized dating bios using AI. This backend is flexible and supports adding new AI providers, image-based enhancements, and spam detection in the future.

---

## 🌐 Demo

**Live API URL**: [https://dpd-generator-backend.vercel.app/](https://dpd-generator-backend.vercel.app/)  
**GitHub**: [https://github.com/greedchikara/DPD-Generator-backend](https://github.com/greedchikara/DPD-Generator-backend)

---

## ⚙️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – Lightning-fast web framework
- [Pydantic](https://docs.pydantic.dev/) – Data validation
- [Python 3.9+](https://www.python.org/)
- Gemini (Google's AI platform) – For description generation

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/greedchikara/DPD-Generator-backend.git
cd DPD-Generator-backend
```

### 2. Create Environment Variables

Create a `.env` file in the project root with:

```env
UPLOAD_DIR=uploads
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Local Development

```bash
fastapi dev main.py
```

The API will be running at [http://localhost:8000](http://localhost:8000)

---

## 🎯 API Endpoints

### `POST /upload/chunks`

Uploads photos in **1MB chunks**. This is done to support Vercel’s upload limits (max 4.5MB per request). Files are saved locally to the `UPLOAD_DIR`.

**Request**: Multipart form with image chunks  
**Response**: `{ "url": "saved_file_path_or_url" }`

---

### `POST /generate-description`

Takes uploaded **photo URLs** and optional answers to generate a dating profile description.

**Request**:

```json
{
  "photo_urls": ["url1", "url2", ...],
  "answers": ["interest": "dogs"]
}
```

**Response**:

```json
{
  "description": "Just a dog-loving goofball looking for someone to talk for hours. Check out my pics!"
}
```

---

## 🧠 Description Generation Logic

- Uses the **number of uploaded photos** and **optional answers** to build a prompt.
- The prompt instructs the AI to:
  - Act as a **funny and friendly dating profile writer**
  - Omit or ignore **vulgar/inappropriate input**
  - Include a **call-to-action** referencing the uploaded photos
- Future versions can:
  - Analyze photo content using vision APIs
  - Flag users for inappropriate content or spam
  - Swap in different AI providers using a pluggable architecture

---

## 🏗️ Extensibility

This backend uses a **Factory + Dependency Injection** pattern to allow swapping AI providers easily.

- Current AI provider: **Gemini**
- Easily plug in: OpenAI, Claude, Cohere, etc.

---

## 📂 Project Structure (Simplified)

```
/main.py                     # FastAPI app entry point
/ai_providers/
  base.py                   # Abstract AI interface
  gemini_provider.py        # Current AI implementation
  factory.py                # AI provider factory
.env                        # API keys and upload paths
```

---

## 👨‍💻 Author

Made with 💡 by [greedchikara](https://github.com/greedchikara)
