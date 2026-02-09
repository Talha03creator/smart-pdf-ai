# 📄 Smart PDF AI Helper

An intelligent PDF assistant powered by OpenRouter's StepFun 3.5 Flash API. Upload PDFs, ask questions, generate summaries, and create quizzes with beautiful Markdown-formatted responses.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)

## ✨ Features

- 📤 **PDF Upload** - Extract text from PDF files instantly
- 💬 **Ask Questions** - Get AI-powered answers from your PDF content
- 📝 **Summarize** - Generate professional summaries with key points
- 🎯 **Generate Quiz** - Create multiple-choice questions automatically
- 🎨 **Markdown Rendering** - Beautiful ChatGPT-style formatted responses
- 📋 **Copy to Clipboard** - One-click copy for all AI outputs
- 🚀 **No Login Required** - Simple, straightforward interface
- 🔓 **Free API** - Uses OpenRouter's free StepFun model

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **PDF Processing**: pdfplumber
- **AI Model**: StepFun 3.5 Flash (via OpenRouter)
- **Markdown Rendering**: marked.js
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom ChatGPT-inspired design

## 📋 Prerequisites

- Python 3.8 or higher
- OpenRouter API key (free tier available)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Talha03creator/smart-pdf-ai.git
   cd smart-pdf-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```
   
   Or edit `api.py` directly to hardcode your key (line 12):
   ```python
   OPENROUTER_API_KEY = "your_api_key_here"
   ```

## 🔑 Getting Your OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into your `.env` file

The StepFun 3.5 Flash model is **completely free** to use!

## 💻 Usage

1. **Start the server**
   ```bash
   python -m uvicorn api:app --reload --port 8001
   ```

2. **Open your browser**
   
   Navigate to: `http://localhost:8001`

3. **Use the app**
   - Upload a PDF file
   - Ask questions about the content
   - Generate summaries
   - Create quizzes
   - Copy results with one click

## 📁 Project Structure

```
smart-pdf-ai/
├── api.py                 # Main FastAPI application
├── templates/
│   └── index.html        # Frontend HTML with Markdown rendering
├── static/
│   └── style.css         # ChatGPT-style CSS
├── uploads/              # Temporary PDF storage
├── requirements.txt      # Python dependencies
├── .env                  # API key configuration (create this)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🎯 How It Works

1. **PDF Upload**: User uploads a PDF file
2. **Text Extraction**: pdfplumber extracts text from the PDF
3. **AI Processing**: Questions/requests sent to StepFun API with PDF context
4. **Markdown Generation**: AI returns professionally formatted Markdown
5. **Frontend Rendering**: marked.js parses Markdown to beautiful HTML
6. **Display**: ChatGPT-style interface shows formatted results

## 🌟 Features in Detail

### Markdown Rendering
All AI responses are formatted in Markdown and rendered as beautiful HTML:
- **Bold headings** for structure
- **Bold text** for important terms
- Bullet points for lists
- Proper paragraph spacing
- Professional typography

### Copy to Clipboard
Every AI response includes a copy button that:
- Copies the full formatted text
- Shows visual confirmation
- Works with all modern browsers

### Responsive Design
- Clean, modern interface
- Gradient background
- Smooth animations
- Mobile-friendly layout

## 🔧 Configuration

### Change the Port
Edit the last line of `api.py`:
```python
uvicorn.run(app, host=\"0.0.0.0\", port=YOUR_PORT)
```

### Change the AI Model
Edit `api.py` line 25:
```python
STEPFUN_MODEL = "stepfun/step-3.5-flash:free"  # or another model
```

## 🚀 Deployment

### Deploy to Render/Railway/Fly.io

1. **Build Command**: `pip install -r requirements.txt`
2. **Start Command**: `python -m uvicorn api:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**: Set `OPENROUTER_API_KEY`

### Deploy with Docker

```bash
docker build -t smart-pdf-ai .
docker run -p 8001:8001 -e OPENROUTER_API_KEY=your_key smart-pdf-ai
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai/) for free AI API access
- [StepFun](https://www.stepfun.com/) for the powerful AI model
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent framework
- [marked.js](https://marked.js.org/) for Markdown rendering

## 📧 Contact

Talha - [@Talha03creator](https://github.com/Talha03creator)

LinkedIn Profile: https://www.linkedin.com/in/muhammad-talha-6278463a1

Project Link: [https://github.com/Talha03creator/smart-pdf-ai](https://github.com/Talha03creator/smart-pdf-ai)

---

**Made with ❤️ using FastAPI and OpenRouter**
