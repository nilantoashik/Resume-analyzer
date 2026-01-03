# 🎯 AI Resume Analyzer

An AI-powered web application that analyzes resumes and provides intelligent feedback, scoring, and improvement suggestions using OpenAI's GPT technology.

## ✨ Features

- **📄 Resume Parsing**: Supports PDF and DOCX formats
- **🤖 AI Analysis**: Comprehensive resume evaluation using OpenAI GPT
- **📊 Smart Scoring**: Multi-dimensional scoring system
  - Content Quality
  - Format & Structure
  - Skills Match
  - Experience Level
- **🔍 Information Extraction**: Automatically extracts:
  - Contact information (email, phone)
  - Skills and technologies
  - Years of experience
  - Education background
- **💡 Actionable Insights**:
  - Strengths identification
  - Areas for improvement
  - Specific recommendations
- **🎨 Modern UI**: Clean, responsive web interface
- **🎯 Job Matching**: Optional job description comparison

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Run the setup script**:
   ```batch
   setup.bat
   ```

2. **Configure your API key**:
   - Open the `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```

3. **Start the application**:
   ```batch
   run.bat
   ```

4. **Access the application**:
   - Open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

```
Resume analyzer/
├── app.py                 # Main Flask application
├── resume_parser.py       # Resume text extraction and parsing
├── ai_analyzer.py         # OpenAI integration for analysis
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── setup.bat             # Windows setup script
├── run.bat               # Windows run script
├── static/               # Frontend files
│   ├── index.html        # Main HTML page
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
├── uploads/              # Temporary file storage
└── README.md            # Documentation
```

## 🛠️ Manual Setup (Alternative)

If you prefer manual setup:

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   copy .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

## 📖 Usage

1. **Upload Resume**:
   - Click "Choose a file" or drag and drop your resume (PDF or DOCX)

2. **Add Job Description (Optional)**:
   - Paste a job description for targeted analysis

3. **Analyze**:
   - Click "Analyze Resume" button
   - Wait for AI processing (usually 10-30 seconds)

4. **Review Results**:
   - Overall score and category scores
   - Extracted information
   - Strengths and weaknesses
   - Specific recommendations

## 🔧 API Endpoints

### `GET /api/health`
Health check endpoint
- Response: `{"status": "healthy"}`

### `POST /api/analyze`
Analyze uploaded resume
- Parameters:
  - `resume` (file): PDF or DOCX file
  - `job_description` (string, optional): Target job description
- Response: Complete analysis with parsed data and AI insights

### `POST /api/score`
Score resume text
- Body: `{"resume_text": "...", "job_description": "..."}`
- Response: Multi-dimensional scores

### `POST /api/suggestions`
Get improvement suggestions
- Body: `{"resume_text": "...", "job_description": "..."}`
- Response: List of actionable suggestions

## 🎨 Customization

### Adjust AI Model
Edit `ai_analyzer.py`:
```python
self.model = "gpt-3.5-turbo"  # Cheaper, faster
# or
self.model = "gpt-4"  # More accurate, slower
```

### Change Skills Database
Edit `resume_parser.py` in the `_extract_skills` method to add more skills relevant to your industry.

### Modify Scoring Criteria
Edit `ai_analyzer.py` in the `score_resume` method to adjust scoring parameters.

## 🔐 Security Notes

- ⚠️ Never commit your `.env` file with real API keys
- Uploaded resumes are automatically deleted after processing
- Use HTTPS in production
- Implement rate limiting for public deployments

## 💰 Cost Considerations

- OpenAI API charges based on token usage
- Estimated cost per resume analysis: $0.01 - $0.05
- Use GPT-3.5-turbo for lower costs
- Monitor usage in OpenAI dashboard

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
- Check `.env` file exists
- Verify API key is correct
- Ensure no extra spaces around the key

### Port already in use
Edit `.env` and change:
```
PORT=5001
```

### Resume parsing fails
- Ensure file is valid PDF or DOCX
- Check file is not password-protected
- Verify file size is under 16MB

## 📊 Features Roadmap

- [ ] Support for more file formats (TXT, RTF)
- [ ] Batch processing for multiple resumes
- [ ] Export analysis reports (PDF)
- [ ] Resume builder/editor
- [ ] ATS (Applicant Tracking System) optimization
- [ ] Multi-language support
- [ ] User accounts and history
- [ ] Integration with job boards

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT API
- Flask framework
- PyPDF2 and python-docx libraries

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review OpenAI API documentation
3. Create an issue in the repository

## 🔄 Updates

To update the project:
```bash
git pull
pip install -r requirements.txt --upgrade
```

---
**🌟 Star this project if you find it helpful!**

