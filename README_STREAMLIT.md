# 🧙‍♂️ SyntaxSage - AI-Powered Code Analysis Tool

**SyntaxSage** is an intelligent Streamlit web application that provides comprehensive Python code analysis using AI. Built with Streamlit and powered by Google's Gemma3 model through Docker, it offers real-time code execution, intelligent summaries, optimization suggestions, and complexity analysis - all with parallel processing for optimal performance.

## ✨ Key Features

- **⚡ Real-time Code Execution**: Execute Python code safely and capture output
- **🤖 AI-Powered Analysis**: Comprehensive code analysis using Gemma3 model
- **💡 Smart Suggestions**: Get intelligent optimization and improvement recommendations  
- **📊 Complexity Analysis**: Understand your code's time and space complexity with Big O notation
- **🔄 Parallel Processing**: Fast analysis through concurrent execution of multiple AI tasks
- **🎨 Modern Streamlit UI**: Clean, responsive interface with interactive components
- **🐳 Docker Integration**: Complete containerized deployment with Gemma3 model
- **☁️ Streamlit Cloud Ready**: Optimized for deployment on Streamlit Cloud

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.28+
- **Backend**: Python 3.9+
- **AI Engine**: Google Gemma3 (4B-Q4_K_M) via Docker
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx (optional)
- **Processing**: Concurrent.futures for parallel AI analysis

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Prerequisites**
   ```bash
   # Install Docker and Docker Compose
   # Windows: Docker Desktop
   # Linux: sudo apt install docker.io docker-compose
   # macOS: Docker Desktop
   ```

2. **Clone and Deploy**
   ```bash
   git clone https://github.com/akhil-varsh/SyntaxSage.git
   cd SyntaxSage
   
   # Windows
   deploy.bat
   
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Access Application**
   - **Streamlit App**: http://localhost:8501
   - **Gemma3 API**: http://localhost:8080 (internal)
   - **Nginx Proxy**: http://localhost:80

### Option 2: Local Streamlit Development

1. **Setup Environment**
   ```bash
   git clone https://github.com/akhil-varsh/SyntaxSage.git
   cd SyntaxSage
   
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Run Gemma3 Model**
   ```bash
   # Pull and run Gemma3 model separately
   docker pull ai/gemma3:4B-Q4_K_M
   docker run -p 8080:8080 ai/gemma3:4B-Q4_K_M
   ```

3. **Start Streamlit App**
   ```bash
   streamlit run streamlit_app.py
   ```

## 🐳 Docker Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   Streamlit     │    │   Gemma3        │
│   (Port 80)     │◄──►│   (Port 8501)   │◄──►│   (Port 8080)   │
│   Reverse Proxy │    │   Frontend      │    │   AI Model      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Services Overview

- **`syntaxsage`**: Streamlit application container
- **`gemma3`**: Gemma3 AI model container
- **`nginx`**: Reverse proxy for production (optional)

## 💻 Usage

1. **Write Python Code**: Use the interactive editor in the sidebar
2. **Choose Examples**: Select from pre-built code examples
3. **Configure API**: Set Gemma3 API endpoint (default: internal Docker)
4. **Analyze**: Click "Analyze Code with AI" 
5. **Review Results**: Get four types of analysis:

   ### 📊 Analysis Types
   - **⚡ Execution Results**: Real-time code execution output
   - **📝 Code Summary**: AI-generated explanation of functionality
   - **💡 Improvement Suggestions**: Optimization and best practice recommendations
   - **⏱️ Complexity Analysis**: Time and space complexity with Big O notation

## 🎯 Example Analysis

**Input Code:**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

**SyntaxSage Analysis:**
- ✅ **Execution**: Shows Fibonacci sequence 0-9
- 📝 **Summary**: "Recursive implementation of Fibonacci sequence calculator..."
- 💡 **Suggestions**: "Consider memoization to improve performance..."
- ⏱️ **Complexity**: "Time: O(2^n), Space: O(n) - Exponential time complexity..."

## ⚙️ Configuration

### Environment Variables
```bash
# Gemma3 API Configuration
GEMMA_API_URL=http://gemma3:8080

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Streamlit Cloud Deployment

1. **Fork this repository**
2. **Create Streamlit Cloud account** at https://streamlit.io/cloud
3. **Deploy app** by connecting your GitHub repository
4. **Set secrets** in Streamlit Cloud dashboard:
   ```toml
   [general]
   GEMMA_API_URL = "your_gemma3_endpoint"
   ```

### Docker Customization

Edit `docker-compose.yml` to customize:
- **Memory allocation** for Gemma3 model
- **Port mappings** for different configurations
- **Health check intervals**
- **Resource limits**

## 🧪 Testing

Run the deployment test suite:

```bash
# Test Docker deployment
python test_deployment.py

# Manual health checks
curl http://localhost:8501/_stcore/health
curl http://localhost:8080/health
```

## 🚀 Production Deployment

### Docker Swarm
```bash
docker swarm init
docker stack deploy -c docker-compose.yml syntaxsage
```

### Kubernetes
```bash
# Convert docker-compose to k8s manifests
kompose convert
kubectl apply -f .
```

### Cloud Platforms
- **AWS**: ECS, EKS, or EC2 with Docker
- **GCP**: Cloud Run, GKE, or Compute Engine
- **Azure**: Container Instances, AKS, or VMs

## 🔧 Development

### Project Structure
```
SyntaxSage/
├── streamlit_app.py          # Main Streamlit application
├── app.py                    # Legacy Flask version
├── docker-compose.yml        # Docker services configuration
├── Dockerfile               # Streamlit app container
├── nginx.conf               # Reverse proxy configuration
├── requirements.txt         # Python dependencies
├── .streamlit/
│   ├── config.toml         # Streamlit configuration
│   └── README.md           # Streamlit app documentation
├── deploy.sh/.bat          # Deployment scripts
└── test_deployment.py      # Testing utilities
```

### Local Development
```bash
# Hot reload development
streamlit run streamlit_app.py --server.runOnSave=true

# Debug mode
streamlit run streamlit_app.py --logger.level=debug
```

## 📈 Performance

### Resource Requirements
- **Minimum**: 6GB RAM, 2 CPU cores
- **Recommended**: 8GB RAM, 4 CPU cores
- **Storage**: 10GB for Docker images

### Optimization Tips
- Use quantized Gemma3 model (Q4_K_M) for better performance
- Enable Docker BuildKit for faster builds
- Configure nginx caching for static assets
- Use GPU acceleration if available

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Test changes** (`python test_deployment.py`)
4. **Commit changes** (`git commit -m 'Add amazing feature'`)
5. **Push to branch** (`git push origin feature/amazing-feature`)
6. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints to new functions
- Include docstrings for public methods
- Test Docker deployment before submitting

## 🔒 Security

- **Code Execution**: Sandboxed Python execution environment
- **API Access**: Internal Docker network communication
- **Rate Limiting**: Nginx-based request throttling
- **Container Security**: Non-root user execution

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google DeepMind** for the Gemma3 model
- **Streamlit** team for the excellent framework
- **Docker** for containerization platform
- **Community contributors** and users

## 📞 Support & Resources

- 🐛 **Issues**: [GitHub Issues](https://github.com/akhil-varsh/SyntaxSage/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/akhil-varsh/SyntaxSage/discussions)
- 📖 **Documentation**: [Streamlit Docs](https://docs.streamlit.io)
- 🤖 **Gemma3 Info**: [Docker Hub](https://hub.docker.com/r/ai/gemma3)

## 🚀 Quick Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services  
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Scale Streamlit instances
docker-compose up --scale syntaxsage=3
```

---

**Made with ❤️ by [Akhil Varsh](https://github.com/akhil-varsh) | Powered by Gemma3 🤖**