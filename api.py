import os
import pdfplumber
import requests
import json
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

# Hardcoded API Key
OPENROUTER_API_KEY = "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"

app = FastAPI(title="Smart PDF AI Lite")

app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

STEPFUN_MODEL = "stepfun/step-3.5-flash:free"

# Global storage for PDF text (simple in-memory storage)
current_pdf_text = ""
current_filename = ""

def search_web(query, max_results=3):
    """Search the web using DuckDuckGo and return text from top results"""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=max_results)
        
        web_text = ""
        for result in results:
            # Get the snippet from search results
            web_text += f"\n\n{result.get('title', '')}\n{result.get('body', '')}"
            
            # Optionally scrape the full page (commented out for speed)
            # try:
            #     response = requests.get(result['href'], timeout=5)
            #     soup = BeautifulSoup(response.content, 'html.parser')
            #     paragraphs = soup.find_all('p')
            #     page_text = ' '.join([p.get_text() for p in paragraphs[:5]])
            #     web_text += f"\n{page_text}"
            # except:
            #     pass
        
        return web_text[:2000]  # Limit web context
    except Exception as e:
        return f"Web search error: {str(e)}"

def ask_stepfun(question, context=""):
    """Call StepFun API via OpenRouter"""
    prompt = f"""Answer the question based on the following context.
    
Context:
{context}

Question: {question}

IMPORTANT: Format your response ONLY in Markdown with:
- Use ## for main headings (e.g., ## Answer)
- Use **bold** for all important terms and concepts
- Use bullet points (- item) for lists
- Use proper paragraph spacing
- Make it professional and ChatGPT-style
- NO plain text blocks, ONLY Markdown formatting"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": STEPFUN_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error calling API: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    global current_pdf_text, current_filename
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pdf_uploaded": bool(current_pdf_text),
        "filename": current_filename
    })

@app.post("/upload_pdf", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    global current_pdf_text, current_filename
    
    file_path = os.path.join("uploads", file.filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    pdf_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error processing PDF: {str(e)}"
        })
    
    current_pdf_text = pdf_text
    current_filename = file.filename
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"✅ PDF '{file.filename}' uploaded successfully!",
        "pdf_uploaded": True,
        "filename": file.filename
    })

@app.post("/ask_question", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    global current_pdf_text, current_filename
    
    if not current_pdf_text:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please upload a PDF first"
        })
    
    answer = ask_stepfun(question, current_pdf_text[:4000])
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pdf_uploaded": True,
        "filename": current_filename,
        "question": question,
        "answer": answer
    })

@app.post("/ask_with_web", response_class=HTMLResponse)
async def ask_with_web(request: Request, question: str = Form(...)):
    """Ask question with web search fallback for enhanced answers"""
    global current_pdf_text, current_filename
    
    if not current_pdf_text:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please upload a PDF first"
        })
    
    # Get PDF context
    pdf_context = current_pdf_text[:4000]
    
    # Search web for additional context
    web_context = search_web(question)
    
    # Combine contexts
    combined_context = f"PDF Content:\n{pdf_context}\n\nWeb Search Results:\n{web_context}"
    
    # Generate answer with combined context
    answer = ask_stepfun(question, combined_context)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pdf_uploaded": True,
        "filename": current_filename,
        "question": question,
        "answer": answer,
        "web_search_used": True
    })

@app.post("/summarize", response_class=HTMLResponse)
async def summarize_pdf(request: Request):
    global current_pdf_text, current_filename
    
    if not current_pdf_text:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please upload a PDF first"
        })
    
    summary_prompt = """Summarize the following text in Markdown format.

IMPORTANT: Use ONLY Markdown formatting:
- Start with ## Summary heading
- Use **bold** for the main topic
- Use bullet points (- item) for 3-5 key points
- Use **bold** for important terms
- Add proper paragraph spacing
- Make it professional and ChatGPT-style
- NO plain text, ONLY Markdown"""
    
    summary = ask_stepfun(summary_prompt, current_pdf_text[:6000])
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pdf_uploaded": True,
        "filename": current_filename,
        "summary": summary
    })

@app.post("/generate_quiz", response_class=HTMLResponse)
async def generate_quiz(request: Request):
    global current_pdf_text, current_filename
    
    if not current_pdf_text:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please upload a PDF first"
        })
    
    quiz_prompt = """Generate 5 multiple choice questions from the text.

IMPORTANT: Format ONLY in Markdown:
- Start with ## Quiz heading
- Use **Question 1:**, **Question 2:**, etc. for each question
- List options as:
  - A) Option
  - B) Option
  - C) Option
  - D) Option
- Use **Correct Answer:** for answers
- Add proper spacing between questions
- Make it professional and ChatGPT-style
- NO plain text, ONLY Markdown"""
    
    quiz = ask_stepfun(quiz_prompt, current_pdf_text[:4000])
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pdf_uploaded": True,
        "filename": current_filename,
        "quiz": quiz
    })

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("Smart PDF AI Lite - OpenRouter Edition")
    print("="*50)
    print("Using StepFun 3.5 Flash API")
    print("Server: http://localhost:8001")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8001)
