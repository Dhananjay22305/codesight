# CodeSight - AI-Powered Code Analyzer

An intelligent code analysis tool that automatically detects errors, provides corrections, and evaluates code quality metrics using AI.

## 🚀 Features

- **Automatic Error Detection**: Identifies syntax and runtime errors in your code
- **Smart Code Correction**: Provides corrected, working code automatically
- **Quality Metrics**: Evaluates code across multiple dimensions:
  - Code Quality (0-100)
  - Complexity Analysis (0-100)
  - Security Assessment (0-100)
  - Overall Score (average of all metrics)
- **Clean UI**: Modern, cyberpunk-inspired interface with syntax highlighting
- **Real-time Analysis**: Fast processing powered by Groq's AI models
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- OpenAI SDK - AI model integration
- Groq API - High-performance LLM inference
- Pydantic - Data validation

**Frontend:**
- Vanilla JavaScript - No framework dependencies
- Custom CSS - Cyberpunk-themed design
- Monaco-style editor - Clean code viewing experience

## 📋 Prerequisites

- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com))

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/Dhananjay22305/codesight.git
cd codesight
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🚀 Usage

1. **Start the server**
```bash
uvicorn app:app --reload
```

2. **Open your browser**

Navigate to `http://localhost:8000`

3. **Analyze your code**
   - Paste or type code in the left editor
   - Click "ANALYZE"
   - View corrected code and metrics on the right

## 📁 Project Structure
```
codesight/
├── app.py                 # FastAPI backend
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
└── static/
    ├── index.html        # Frontend interface
    ├── script.js         # Client-side logic
    └── style.css         # UI styling
```

## 🎯 How It Works

1. User submits code through the web interface
2. Backend sends code to Groq's AI model (kimi-k2-instruct)
3. AI analyzes the code for errors and quality issues
4. Returns corrected code and calculated metrics
5. Frontend displays results with visual indicators

## 🔒 Security Notes

- Never commit your `.env` file
- Keep your Groq API key confidential
- The app runs locally by default (localhost:8000)

## 📊 Metrics Explained

- **Quality**: Code readability, best practices, and maintainability
- **Complexity**: Algorithmic complexity and code structure
- **Security**: Potential vulnerabilities and security issues
- **Overall**: Average of all three metrics

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📧 Contact

**Developer**: Dhananjay Bhoyar  
**LinkedIn**: [linkedin.com/in/dhananjay-bhoyar-872254302](https://www.linkedin.com/in/dhananjay-bhoyar-872254302/)  
**Phone**: +91 9699034225

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Groq](https://groq.com/) for lightning-fast AI inference
- Powered by MoonshotAI's kimi-k2-instruct model
- UI inspired by modern cyberpunk aesthetics

---

**Made with ❤️ by Dhananjay Bhoyar**
