# 🧙‍♂️ SyntaxSage - AI-Powered Code Analysis Tool

**SyntaxSage** is an intelligent web application that provides comprehensive Python code analysis using AI. Built with Flask and powered by LLaMA 3.1 through Ollama, it offers real-time code execution, intelligent summaries, optimization suggestions, and complexity analysis - all with parallel processing for optimal performance.

## ✨ Key Features

- **⚡ Real-time Code Execution**: Execute Python code safely and capture output
- **🤖 AI-Powered Analysis**: Comprehensive code analysis using LLaMA 3.1
- **💡 Smart Suggestions**: Get intelligent optimization and improvement recommendations  
- **📊 Complexity Analysis**: Understand your code's time and space complexity with Big O notation
- **🔄 Parallel Processing**: Fast analysis through concurrent execution of multiple AI tasks
- **🎨 Modern UI**: Clean, responsive interface with syntax highlighting via CodeMirror
- **⌨️ Developer-Friendly**: Keyboard shortcuts (Ctrl+Enter) for quick analysis

## 🛠️ Tech Stack

- **Backend**: Python 3.7+, Flask
- **AI Engine**: Ollama with LLaMA 3.1 model
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Code Editor**: CodeMirror with Python syntax highlighting
- **UI Framework**: Bootstrap 5
- **Processing**: Concurrent.futures for parallel AI analysis

## � Quick Start

### Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running with LLaMA 3.1 model
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.1
   ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/akhil-varsh/SyntaxSage.git
   cd SyntaxSage
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## 💻 Usage

1. **Write Python Code**: Use the built-in editor with syntax highlighting
2. **Analyze**: Click "Analyze Code with AI" or press `Ctrl+Enter`
3. **Review Results**: Get four types of analysis:
   - **Execution Results**: See your code's output
   - **Code Summary**: AI-generated explanation of functionality
   - **Improvement Suggestions**: Optimization and best practice recommendations
   - **Complexity Analysis**: Time and space complexity with Big O notation

## 🎯 Example Analysis

Input code:
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

SyntaxSage provides:
- ✅ **Execution**: Shows Fibonacci sequence output
- 📝 **Summary**: Explains recursive Fibonacci implementation
- 💡 **Suggestions**: Recommends memoization for optimization
- ⏱️ **Complexity**: Identifies O(2^n) time complexity issue

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask App     │    │   AI Engine     │
│                 │    │                 │    │                 │
│ CodeMirror      │◄──►│ Parallel        │◄──►│ Ollama          │
│ Bootstrap UI    │    │ Processing      │    │ LLaMA 3.1       │
│ JavaScript      │    │ ThreadPool      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

- **`app.py`**: Main Flask application with parallel processing
- **`templates/index.html`**: Modern responsive UI with CodeMirror
- **`static/css/style.css`**: Custom styling and accessibility features
- **`requirements.txt`**: Dependency management

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Configure Flask settings
export FLASK_ENV=development
export FLASK_DEBUG=True

# Optional: Configure Ollama endpoint
export OLLAMA_HOST=http://localhost:11434
```

### Ollama Setup
```bash
# Ensure Ollama is running
ollama serve

# Verify LLaMA 3.1 is available
ollama list
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Acknowledgments

- **Ollama Team** for the excellent local LLM runtime
- **LLaMA** team at Meta for the powerful language model
- **CodeMirror** for the excellent code editor component
- **Flask** community for the robust web framework

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/akhil-varsh/SyntaxSage/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/akhil-varsh/SyntaxSage/discussions)
- 📧 **Email**: [Contact the maintainer](mailto:akhil.varsh@example.com)

---

**Made with ❤️ by [Akhil Varsh](https://github.com/akhil-varsh)**


