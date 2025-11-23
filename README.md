# Cancer Research Paper Explainer

An AI-powered tool that makes complex cancer research papers understandable for patients, caregivers, and the general public.

## 🚀 Quick Start (Local Development)

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. **Run the Server:**
   ```bash
   python app.py
   ```

4. **Open the Frontend:**
   - Open `index.html` in your browser
   - Or visit: `file:///path/to/index.html`

## 🌐 Deploy Online

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Render and Netlify.

## 📝 Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

Get your API key from: https://console.groq.com/

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python
- **Frontend:** HTML, CSS, JavaScript
- **AI:** Groq (LLaMA 3.3 70B)
- **PDF Processing:** PyMuPDF
