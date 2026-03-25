# 🎙 Emotion Voice AI

<div align="center">

![Emotion Voice AI](https://img.shields.io/badge/Emotion-Voice%20AI-8B7CF6?style=for-the-badge&logo=brain&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.1-F55036?style=for-the-badge&logo=groq&logoColor=white)
![Murf](https://img.shields.io/badge/Murf-Falcon%20TTS-4DD9C0?style=for-the-badge&logoColor=white)

**An AI-powered emotional wellness assistant that detects your emotions and responds with empathy — powered by Groq LLaMA 3.1 and Murf Falcon TTS.**

[🚀 Getting Started](#-getting-started) • [✨ Features](#-features) • [🛠 Tech Stack](#-tech-stack) • [📁 Project Structure](#-project-structure) • [🎯 How It Works](#-how-it-works)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Emotion Detection** | Detects 9 emotions — happy, sad, angry, anxious, curious, fearful, disgusted, surprised, neutral |
| 🤖 **AI Chat** | Groq LLaMA 3.1 responds with tone matched to your detected emotion |
| 🔊 **Murf Falcon TTS** | AI voice changes style automatically — Sad, Promo, Angry, Conversational |
| 🎤 **Voice Input** | Speak your message using browser Speech Recognition |
| ⚖️ **BMI Calculator** | Calculate BMI + get AI-powered health recommendations |
| 📊 **Emotion History** | Track your emotional journey and conversation patterns over time |
| 🔐 **User Auth** | Signup/Login system with localStorage — no backend database needed |
| 💬 **Chat History** | Remembers last 10 conversations for context-aware responses |

---

## 🎯 How It Works

```
You type a message
        ↓
Groq detects your emotion (happy/sad/angry/anxious...)
        ↓
AI responds with tone matched to your emotion
        ↓
Murf Falcon speaks the reply in emotion-matched voice style
        ↓
Emotion + conversation saved to your history
```

### Emotion → Voice Style Mapping

| Emotion | Murf Falcon Style | Feel |
|---|---|---|
| 😊 Happy | Promo | Energetic, upbeat |
| 😢 Sad | Sad | Gentle, soft |
| 😠 Angry | Angry | Firm, intense |
| 😮 Surprised | Promo | Expressive, punchy |
| 😰 Anxious | Conversational | Calm, steady |
| 🤔 Curious | Conversational | Natural, engaged |
| 😐 Neutral | Conversational | Relaxed, balanced |

---

## 🛠 Tech Stack

### Backend
- **Python 3.11** — Core language
- **Flask** — Web framework
- **Groq API** — LLaMA 3.1 for AI chat + emotion detection
- **Murf API** — Falcon voice TTS
- **Flask-CORS** — Cross-origin support
- **python-dotenv** — Environment variables

### Frontend
- **HTML5 / CSS3 / Vanilla JS** — No framework needed
- **Web Speech API** — Browser TTS (fallback) + mic input
- **Orbitron + Outfit fonts** — Futuristic UI typography
- **CSS animations** — 3D particle background, glowing effects

---

## 📁 Project Structure

```
EMOTION-VOICE-AI/
│
├── 📄 .env                          # API keys (never commit this!)
│
├── 📁 backend/
│   ├── 🐍 app.py                    # Flask entry point
│   ├── 🐍 chat_routes.py            # /api/chat, /api/status
│   ├── 🐍 emotion_engine.py         # Groq emotion detection
│   ├── 🐍 murf_tts.py               # Murf Falcon TTS integration
│   ├── 🐍 bmi_calculator.py         # /api/bmi
│   ├── 🐍 recommendations.py        # /api/recommendations
│   └── 📄 requirements.txt          # Python dependencies
│
└── 📁 frontend/
    ├── 🌐 login.html                 # Login page
    ├── 🌐 signup.html                # Signup page
    ├── 🌐 dashboard.html             # Main dashboard
    ├── 🌐 chat.html                  # Emotion chat
    ├── 🌐 bmi.html                   # BMI calculator
    ├── 🌐 history.html               # Emotion history
    ├── 🎨 style.css                  # Shared styles (dark 3D UI)
    └── ⚙️ app.js                     # Shared JS (Auth, TTS, particles)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Chrome or Edge browser
- Groq API key (free) → [console.groq.com](https://console.groq.com)
- Murf API key (optional) → [murf.ai](https://murf.ai)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/emotion-voice-ai.git
cd emotion-voice-ai
```

**2. Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**3. Setup environment variables**

Create `.env` file in root folder:
```env
GROQ_API_KEY=gsk_your_groq_key_here
GROQ_MODEL=llama-3.1-8b-instant
MURF_API_KEY=your_murf_key_here
SECRET_KEY=your_random_secret_key
```

**4. Run the application**
```bash
py -3.11 app.py
```

**5. Open in browser**
```
http://localhost:5000
```

---

## 🌐 Pages

| Page | URL | Description |
|---|---|---|
| Login | `/login.html` | Sign in to your account |
| Signup | `/signup.html` | Create new account |
| Dashboard | `/dashboard.html` | Overview + navigation |
| Chat | `/chat.html` | Emotion AI chat |
| BMI | `/bmi.html` | BMI + health recs |
| History | `/history.html` | Emotion analytics |

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Send message, get AI reply + emotion |
| `POST` | `/api/chat/clear` | Clear chat session history |
| `GET` | `/api/status` | Check API connection status |
| `POST` | `/api/bmi` | Calculate BMI |
| `POST` | `/api/recommendations` | Get AI health recommendations |

---

## 📸 Screenshots

### Login Page
> Dark 3D glassmorphism design with animated particle background and glowing logo

### Dashboard
> Welcome banner with emotion stats, 3 feature cards, emotion summary chart

### Emotion Chat
> Real-time chat with emotion badges, Murf Falcon voice, waveform animations

### BMI & Health
> BMI calculator with animated meter + AI-generated health recommendations

---

## ⚙️ Configuration

### Available Groq Models
```env
GROQ_MODEL=llama-3.1-8b-instant     # Fast, recommended
GROQ_MODEL=llama-3.1-70b-versatile  # More capable, slower
GROQ_MODEL=mixtral-8x7b-32768       # Alternative
```

### Voice Settings (in chat UI)
- **Rate** — Speech speed (0.6 to 1.6)
- **Pitch** — Voice pitch (0.5 to 1.8)
- **Voice** — Select from available browser voices

---

## 🔒 Security Notes

- Never commit your `.env` file
- Add `.env` to `.gitignore`
- `SECRET_KEY` should be a random string in production
- User passwords are encoded with `btoa()` in localStorage

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Priya**

---

<div align="center">

Made with ❤️ and a lot of emotions 🎙

**⭐ Star this repo if you found it helpful!**

</div>
