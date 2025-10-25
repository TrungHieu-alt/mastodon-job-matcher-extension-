# 🏗️ Mastodon CV Matcher - Clean Architecture

A clean, minimal Mastodon bot with **two-way matching** that automatically processes both job postings and CVs, matching them using ChromaDB vector database and LLM evaluation.

## 📁 **Clean Project Structure**

```
mastodon-job-matcher-extension/
├── 📁 listener/                     # Event listeners for Mastodon posts
│   ├── __init__.py
│   ├── cv_listener.py              # #cv hashtag listener
│   └── job_listener.py             # #tuyendungAI hashtag listener
├── 📁 logic/                        # Main logic: parsing, matching, AI processing
│   ├── __init__.py
│   ├── resume_parser.py            # CV parsing with Gemini AI
│   ├── job_processor.py            # Job post processing
│   └── candidate_matcher.py        # Candidate matching logic
├── 📁 db/                          # Database and ChromaDB storage
│   ├── __init__.py
│   ├── chroma_connection.py        # ChromaDB connection management
│   ├── cv_storage.py               # CV database operations
│   └── job_storage.py              # Job description storage
├── 📁 utils/                        # Small reusable helpers
│   ├── __init__.py
│   ├── text_utils.py               # Text processing utilities
│   ├── file_utils.py               # File handling utilities
│   ├── llm_utils.py                # LLM evaluation utilities
│   ├── mastodon_utils.py           # Mastodon API utilities
│   └── logging_config.py           # Logging configuration
├── 📁 config/                       # Configuration
│   ├── __init__.py
│   └── settings.py                 # Application settings
├── 📁 examples/                     # Example files
│   ├── sample_job.json
│   └── sample_cv_data.json
├── 📄 mastodon_bot.py              # Main bot entry point
├── 📄 cli.py                       # Command-line interface
├── 📄 main.py                      # Legacy main file
├── 📄 requirements.txt             # Dependencies
└── 📄 README.md                    # This file
```

## 🚀 **Quick Start**

### **1. Installation**
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Create directories
mkdir -p logs data/chroma_db temp cv_folder
```

### **2. Run the Bot**
```bash
# Start the Mastodon bot with two-way matching
python mastodon_bot.py
```

### **3. Process CVs**
```bash
# Process CVs from folder
python cli.py process-cvs cv_folder

# Add a job description
python cli.py add-job --interactive

# Search for matching CVs
python cli.py search-cvs --query "Python developer"
```

## 🎯 **Architecture Principles**

### **✅ Clean Structure**
- **One folder = one purpose** ✅
- **One file = one responsibility** ✅
- **Small, focused modules** ✅
- **Clear separation of concerns** ✅

### **✅ Minimal Design**
- **No unnecessary abstractions** ✅
- **Simple, readable code** ✅
- **Easy to understand and maintain** ✅
- **Follows the exact folder structure requested** ✅

## 📋 **Module Overview**

### **📡 Listener (`listener/`)**
- **`cv_listener.py`**: Listens for #cv posts → processes CVs → finds matching jobs
- **`job_listener.py`**: Listens for #tuyendungAI posts → processes jobs → finds matching candidates

### **🧠 Logic (`logic/`)**
- **`resume_parser.py`**: CV parsing using Gemini AI
- **`job_processor.py`**: Job post processing and extraction
- **`candidate_matcher.py`**: Job → CV matching using ChromaDB + LLM
- **`cv_job_matcher.py`**: CV → Job matching using ChromaDB + LLM

### **🗄️ Database (`db/`)**
- **`chroma_connection.py`**: ChromaDB connection management
- **`cv_storage.py`**: CV database operations
- **`job_storage.py`**: Job description storage

### **🛠️ Utils (`utils/`)**
- **`text_utils.py`**: Text processing and extraction
- **`file_utils.py`**: File handling utilities
- **`llm_utils.py`**: LLM evaluation functions
- **`mastodon_utils.py`**: Mastodon API helpers

## 🔧 **Key Features**

### **✅ Two-Way Matching System**
- **#cv hashtag**: When someone posts a CV → Find matching jobs
- **#tuyendungAI hashtag**: When someone posts a job → Find matching candidates
- Automatic processing and intelligent matching
- Sends results via DM

### **✅ ChromaDB Vector Search**
- Fast semantic similarity search
- Efficient CV and job storage
- Configurable similarity thresholds

### **✅ LLM Evaluation**
- GPT-4o for detailed candidate assessment
- Structured evaluation output
- Composite scoring algorithm

### **✅ Clean Architecture**
- Minimal, focused modules
- Easy to understand and maintain
- No unnecessary complexity

## 🔄 **Two-Way Matching Workflow**

### **📥 CV → Job Matching (#cv hashtag)**
1. User posts CV with #cv hashtag
2. Bot downloads and parses CV using Gemini AI
3. Bot searches for matching jobs using ChromaDB
4. Bot evaluates job matches using LLM
5. Bot sends ranked job recommendations via DM

### **📤 Job → CV Matching (#tuyendungAI hashtag)**
1. User posts job with #tuyendungAI hashtag
2. Bot extracts job information
3. Bot searches for matching CVs using ChromaDB
4. Bot evaluates candidate matches using LLM
5. Bot sends ranked candidate recommendations via DM

## 📊 **Usage Examples**

### **Process CVs**
```bash
# Process all CVs in a folder
python cli.py process-cvs cv_folder
```

### **Add Job Description**
```bash
# Interactive mode
python cli.py add-job --interactive

# From JSON file
python cli.py add-job --file examples/sample_job.json
```

### **Search for Candidates**
```bash
# Search by query
python cli.py search-cvs --query "Python developer with Django experience"

# Search by job ID
python cli.py search-cvs --job-id jd_abc123
```

### **List CVs**
```bash
# List all CVs
python cli.py list-cvs --limit 10
```

## 🧪 **Testing**

### **Test Database Connection**
```python
from db.chroma_connection import chroma_connection
print(chroma_connection.test_connection())
```

### **Test CV Processing**
```python
from logic.resume_parser import parse_resume
result = parse_resume("path/to/cv.pdf")
print(result)
```

### **Test Matching**
```python
from logic.candidate_matcher import find_matching_candidates
candidates = find_matching_candidates("Python developer")
print(candidates)
```

## 🔄 **Migration from Original**

The project has been refactored to follow the exact folder structure you requested:

- **`listener/`** - Event listeners for Mastodon posts
- **`logic/`** - Main logic: parsing, matching, AI processing  
- **`db/`** - Database and ChromaDB storage handling
- **`utils/`** - Small reusable helpers

All files have been moved to the correct folders and import paths updated accordingly.

## 📈 **Benefits of Clean Architecture**

| Feature | Before | After | Improvement |
|---------|--------|-------|-------------|
| **File Organization** | Mixed | Clean folders | **Much better** |
| **Code Readability** | Complex | Simple | **Much better** |
| **Maintainability** | Hard | Easy | **Much better** |
| **Testability** | Difficult | Simple | **Much better** |

## 🤝 **Contributing**

1. **Follow the folder structure**: Keep files in the correct folders
2. **Write simple functions**: One task per function
3. **Keep modules focused**: One purpose per file
4. **Update imports**: When moving files, update import paths

## 📄 **License**

This project is licensed under the MIT License.

---

**🎉 Enjoy the clean, minimal architecture!**