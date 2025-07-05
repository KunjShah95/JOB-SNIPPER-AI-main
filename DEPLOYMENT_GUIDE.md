# 🚀 JobSniper AI - Complete Deployment Guide

## 🎯 Quick Start (Recommended)

### 1. **Clone & Setup**
```bash
# Clone the repository
git clone https://github.com/KunjShah95/JOB-SNIPPER-AI-main.git
cd JOB-SNIPPER-AI-main

# Install dependencies
pip install -r requirements_fixed.txt

# Test everything works
python test_all_features.py

# Run the application
python run_fixed.py
```

### 2. **Access the Application**
- **URL:** http://localhost:8501
- **Default:** Fixed version with working resume parsing
- **Features:** Resume analysis, job matching, analytics

## 📱 Available Versions

### 🔧 **Fixed Version** (Recommended)
```bash
streamlit run app_fixed.py
```
- ✅ Working resume parsing
- ✅ Visible UI with high contrast
- ✅ Multiple file format support
- ✅ Reliable error handling
- ✅ Fast performance

### 🚀 **Ultimate Version** (Advanced)
```bash
streamlit run app_ultimate.py
```
- ✅ All fixed version features
- ✅ Advanced analytics dashboard
- ✅ Enhanced visualizations
- ✅ Career insights
- ✅ Premium UI design
- ✅ Multiple themes

### 📝 **Simple Version** (Minimal)
```bash
streamlit run app_simple.py
```
- ✅ Basic functionality
- ✅ Lightweight
- ✅ Quick testing

## 🛠️ Installation Options

### Option 1: Minimal Installation
```bash
# Core packages only
pip install streamlit plotly pandas PyPDF2 python-docx
```

### Option 2: Full Installation
```bash
# All features and fallbacks
pip install -r requirements_fixed.txt
```

### Option 3: Development Installation
```bash
# With testing and development tools
pip install -r requirements_fixed.txt
pip install pytest black flake8
```

## 🔧 System Requirements

### **Minimum Requirements**
- Python 3.8+
- 2GB RAM
- 500MB disk space
- Modern web browser

### **Recommended Requirements**
- Python 3.9+
- 4GB RAM
- 1GB disk space
- Chrome/Firefox/Safari

### **Supported Platforms**
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 18.04+)
- ✅ Docker containers

## 📁 File Structure

```
JOB-SNIPPER-AI-main/
├── 🔥 app_fixed.py              # Main fixed application
├── 🚀 app_ultimate.py           # Ultimate version
├── 📝 app_simple.py             # Simple version
├── 🏃 run_fixed.py              # Easy launcher
├── 🧪 test_all_features.py      # Test suite
├── 📦 requirements_fixed.txt    # Dependencies
├── 📚 README_FIXED.md           # Documentation
├── utils/
│   ├── simple_resume_parser.py  # Reliable parser
│   ├── enhanced_file_reader.py  # File processing
│   └── pdf_reader.py           # Original PDF reader
├── agents/                     # Original agent system
├── ui/                        # Original UI components
└── tests/                     # Test files
```

## 🚀 Deployment Options

### 1. **Local Development**
```bash
# Quick start
python run_fixed.py

# Manual start
streamlit run app_fixed.py --server.port 8501
```

### 2. **Streamlit Cloud** (Free)
1. Fork the repository
2. Connect to Streamlit Cloud
3. Deploy `app_fixed.py`
4. Set secrets for API keys

### 3. **Heroku Deployment**
```bash
# Create Procfile
echo "web: streamlit run app_fixed.py --server.port \$PORT --server.address 0.0.0.0" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 4. **Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_fixed.txt .
RUN pip install -r requirements_fixed.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app_fixed.py", "--server.address", "0.0.0.0"]
```

```bash
# Build and run
docker build -t jobsniper-ai .
docker run -p 8501:8501 jobsniper-ai
```

### 5. **AWS EC2 Deployment**
```bash
# On EC2 instance
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements_fixed.txt

# Run with nohup
nohup streamlit run app_fixed.py --server.port 8501 --server.address 0.0.0.0 &
```

## 🔐 Environment Configuration

### **API Keys** (Optional)
Create `.env` file:
```env
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
MISTRAL_API_KEY=your_mistral_key_here
```

### **Streamlit Secrets**
Create `.streamlit/secrets.toml`:
```toml
[api_keys]
gemini = "your_gemini_key"
openai = "your_openai_key"
mistral = "your_mistral_key"
```

## 🧪 Testing & Validation

### **Run Test Suite**
```bash
# Test all features
python test_all_features.py

# Expected output: All tests passed
```

### **Manual Testing**
1. **Upload Resume:** Test with PDF, DOCX, TXT
2. **Sample Resume:** Use built-in sample
3. **Text Input:** Paste resume text directly
4. **Navigation:** Test all pages and features
5. **Error Handling:** Try invalid inputs

### **Performance Testing**
```bash
# Test with large files
# Monitor memory usage
# Check response times
```

## 🐛 Troubleshooting

### **Common Issues & Solutions**

#### 1. **Resume Not Parsing**
```bash
# Check file format
# Supported: PDF, DOCX, TXT

# Try sample resume first
# Click "📝 Use Sample Resume"

# Check file size (max 10MB)
```

#### 2. **Dependencies Missing**
```bash
# Install missing packages
pip install streamlit plotly pandas PyPDF2

# Or install all
pip install -r requirements_fixed.txt
```

#### 3. **Text Not Visible**
```bash
# Use app_fixed.py (not app.py)
streamlit run app_fixed.py

# Clear browser cache
# Try different browser
```

#### 4. **PDF Reading Fails**
```bash
# Install additional PDF libraries
pip install pdfplumber PyMuPDF

# Try different PDF file
# Check if PDF is scanned/image-based
```

#### 5. **Port Already in Use**
```bash
# Use different port
streamlit run app_fixed.py --server.port 8502

# Kill existing process
pkill -f streamlit
```

#### 6. **Memory Issues**
```bash
# Reduce file size
# Close other applications
# Use simple version: app_simple.py
```

### **Error Messages**

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | `pip install streamlit` |
| `FileNotFoundError: [Errno 2] No such file` | Check file paths and structure |
| `PermissionError: [Errno 13] Permission denied` | Check file permissions |
| `UnicodeDecodeError` | Check file encoding, try different file |
| `Memory Error` | Reduce file size or use more RAM |

## 📊 Performance Optimization

### **Speed Improvements**
```python
# Use caching
@st.cache_data
def parse_resume(text):
    # Cached parsing
    pass

# Optimize file reading
# Use streaming for large files
# Implement pagination
```

### **Memory Optimization**
```python
# Clear session state
if 'large_data' in st.session_state:
    del st.session_state.large_data

# Use generators for large datasets
# Implement lazy loading
```

## 🔒 Security Considerations

### **Data Protection**
- Resume data is processed locally
- No data sent to external servers (unless API keys configured)
- Files are temporarily stored and cleaned up
- Session data cleared on browser close

### **API Key Security**
- Store API keys in environment variables
- Use Streamlit secrets for deployment
- Never commit API keys to version control
- Rotate keys regularly

## 📈 Monitoring & Analytics

### **Application Metrics**
- Response times
- Error rates
- User sessions
- File processing success rates

### **Usage Analytics**
- Most used features
- File format preferences
- Error patterns
- Performance bottlenecks

## 🔄 Updates & Maintenance

### **Regular Updates**
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements_fixed.txt --upgrade

# Run tests
python test_all_features.py
```

### **Backup Strategy**
- Regular code backups
- User data export options
- Configuration backups
- Database backups (if applicable)

## 🆘 Support & Help

### **Getting Help**
1. **Check README_FIXED.md** - Comprehensive documentation
2. **Run test suite** - `python test_all_features.py`
3. **Check logs** - Streamlit console output
4. **Try different versions** - Fixed, Ultimate, Simple
5. **Open GitHub issue** - Detailed problem description

### **Community Resources**
- GitHub Issues
- Documentation
- Example files
- Video tutorials (coming soon)

## 🎯 Success Checklist

Before going live, ensure:

- [ ] ✅ All tests pass (`python test_all_features.py`)
- [ ] ✅ Resume parsing works with sample data
- [ ] ✅ UI is visible and responsive
- [ ] ✅ File upload works (PDF, DOCX, TXT)
- [ ] ✅ Error handling is graceful
- [ ] ✅ Performance is acceptable (<5 seconds)
- [ ] ✅ All pages load correctly
- [ ] ✅ Charts and visualizations display
- [ ] ✅ Mobile compatibility (if needed)
- [ ] ✅ Security measures in place

## 🚀 Go Live!

Once everything is tested and working:

```bash
# Final test
python test_all_features.py

# Start the application
python run_fixed.py

# Or deploy to cloud
# Follow deployment option above
```

**🎉 Congratulations! Your JobSniper AI application is now live and ready to help users analyze resumes and find jobs!**

---

**📞 Need Help?**
- 📧 Create GitHub issue with detailed description
- 📚 Check README_FIXED.md for more information
- 🧪 Run `python test_all_features.py` for diagnostics