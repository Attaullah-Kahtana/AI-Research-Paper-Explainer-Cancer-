# Cancer Research Paper Explainer - Deployment Guide

## 🌐 Deploy Your Application Online

### Backend Deployment (Render)

1. **Create a GitHub Repository:**
   ```bash
   cd "d:\A F\code\app.py"
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub:**
   - Create a new repository on GitHub
   - Follow GitHub's instructions to push your code

3. **Deploy on Render:**
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** `cancer-paper-explainer-api`
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
     - **Add Environment Variable:** 
       - Key: `GROQ_API_KEY`
       - Value: `your_groq_api_key_here`
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL (e.g., `https://cancer-paper-explainer-api.onrender.com`)

### Frontend Deployment (Netlify)

1. **Update API URL in script.js:**
   - Replace `http://localhost:8000/summarize` with your Render URL
   - Example: `https://cancer-paper-explainer-api.onrender.com/summarize`

2. **Deploy on Netlify:**
   - Go to [netlify.com](https://netlify.com) and sign up
   - Drag and drop these files into Netlify:
     - `index.html`
     - `style.css`
     - `script.js`
   - OR use Netlify CLI:
     ```bash
     npm install -g netlify-cli
     netlify deploy --prod
     ```

3. **Your app is live!**
   - Netlify will give you a URL like: `https://your-app.netlify.app`

---

## 🚀 Alternative: Quick Deploy with Railway

1. Go to [railway.app](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Add environment variable `GROQ_API_KEY`
5. Railway will auto-detect and deploy your FastAPI app
6. Deploy frontend files separately on Netlify/Vercel

---

## ⚡ Important Notes

- **Free Tier Limits:** Render's free tier may sleep after 15 minutes of inactivity
- **API Key Security:** Never commit API keys to public repositories
- **CORS:** Already configured to allow all origins
