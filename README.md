# 🎵 Spotify Agent - AI-Powered Music Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 🎯 Project Goal

Spotify Agent is an intelligent music recommendation system that transforms how you discover music. By combining the power of Spotify's vast music library with OpenAI's advanced AI models, it creates a personalized music discovery experience through an interactive chat interface.

### 🌟 What Makes It Special?

- **🤖 AI-Powered Intelligence**: Uses OpenAI GPT models to understand your music taste and provide intelligent recommendations
- **🎵 Spotify Integration**: Seamlessly connects to your Spotify account to analyze your listening patterns
- **💬 Natural Conversations**: Chat naturally about your music preferences - no complex commands needed
- **🎯 Personalized Experience**: Learns from your listening history to suggest music you'll actually love
- **🔒 Privacy First**: Your data stays on your machine - no external storage of personal information

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Spotify account (Free or Premium)
- OpenAI API key

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shubhamjakhete/spotify_agent.git
   cd spotify_agent
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install spotipy openai python-dotenv
   ```

4. **Configure API Keys**
   ```bash
   cp env_template.txt .env
   # Edit .env file with your API keys
   ```

### Get Your API Keys

#### Spotify API Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Copy your `CLIENT_ID` and `CLIENT_SECRET`
4. Set redirect URI to `http://localhost:8888/callback`

#### OpenAI API Setup
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

### Running the Application

```bash
python main.py
```

That's it! The application will guide you through the setup process.

## 💬 How to Use

Once the application starts, simply chat with it naturally:

```
🎵 You: I'm feeling energetic, recommend some upbeat songs
🎵 You: What are my top artists?
🎵 You: Suggest songs similar to Coldplay
🎵 You: I want to discover new genres
🎵 You: Create a workout playlist
```

### Example Session

```
🎵 Spotify Agent - Starting Chat Interface...
==================================================

🎵 Initializing Spotify Agent...
🤖 Connecting to OpenAI... ✅
📡 Connecting to Spotify... ✅

📊 Loading your Spotify profile...
✅ Spotify context loaded!
📋 Found 50 recent tracks and 50 top artists

🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵
  SPOTIFY AGENT - CHAT INTERFACE
🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵🎵

🎤 Welcome to your AI Music Assistant!
💬 Chat with me about music and get personalized recommendations!

🎵 You: I'm feeling energetic, recommend some upbeat songs

🤔 Thinking...

🎯 AI Assistant: Absolutely! I've got just the thing to lift your spirits! 🎶

Here are some energetic and upbeat songs that will get you moving:

1. **"Uptown Funk" by Mark Ronson ft. Bruno Mars** - A high-energy funk-pop anthem!
2. **"Can't Stop the Feeling!" by Justin Timberlake** - Pure joy and energy!
3. **"Shake It Off" by Taylor Swift** - An empowering anthem!
4. **"Happy" by Pharrell Williams** - The ultimate mood-lifter!
5. **"Dynamite" by BTS** - A K-pop explosion of energy!

These tracks are perfect for working out, cleaning, or just boosting your mood! ✨
```

## 🛠️ Features

### 🎵 Music Discovery
- **Personalized Recommendations**: Based on your actual listening history
- **Artist Discovery**: Find new artists similar to your favorites
- **Genre Exploration**: Discover new genres and sub-genres
- **Mood-Based Suggestions**: Get recommendations based on your current mood
- **Playlist Analysis**: Intelligent analysis of your music taste

### 🤖 AI Capabilities
- **Natural Language Processing**: Chat naturally about music
- **Context Awareness**: Remembers your conversation history
- **Intelligent Analysis**: AI-powered music taste analysis
- **Adaptive Learning**: Improves recommendations over time

### 🔒 Security & Privacy
- **OAuth 2.0 Authentication**: Secure Spotify connection
- **Local Data Storage**: Your data stays on your machine
- **API Key Protection**: Secure handling of credentials
- **Privacy Compliant**: GDPR and CCPA compliant

## 📁 Project Structure

```
spotify_agent/
├── main.py                 # 🚀 Application entry point
├── chat_cli.py            # 💬 Interactive CLI interface
├── spotify_client.py      # 🎵 Spotify API integration
├── openai_client.py       # 🤖 OpenAI API integration
├── logging_config.py      # 📝 Logging system
├── view_logs.py           # 🔍 Log viewing utility
├── env_template.txt       # ⚙️ Environment template
├── SOFTWARE_REQUIREMENTS.md # 📋 Detailed requirements
├── README.md              # 📖 This file
└── logs/                  # 📊 Application logs
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your API keys:

```bash
# Spotify Configuration
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
```

## 🐛 Troubleshooting

### Common Issues

**Spotify Authentication Failed?**
- Verify your client ID and secret
- Check redirect URI configuration
- Ensure proper scopes are set

**OpenAI API Errors?**
- Verify your API key
- Check API usage limits
- Ensure proper model configuration

**Import Errors?**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`

### Debug Mode

Enable debug logging:
```bash
LOG_LEVEL=DEBUG python main.py
```

### View Logs

```bash
python view_logs.py
```

## 🧪 Testing

Run the test suite:
```bash
pip install pytest
pytest
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 Python style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Spotify**: For the comprehensive music API
- **OpenAI**: For the powerful GPT models
- **Spotipy**: For the excellent Python Spotify library
- **Python Community**: For the amazing ecosystem

## 📞 Support

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/shubhamjakhete/spotify_agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shubhamjakhete/spotify_agent/discussions)
- **Documentation**: Check [SOFTWARE_REQUIREMENTS.md](SOFTWARE_REQUIREMENTS.md) for detailed requirements

---

## 👨‍💻 Author & Developer

**Developed by Shubham Jakhete**

- **GitHub**: [@shubhamjakhete](https://github.com/shubhamjakhete)
- **Repository**: [https://github.com/shubhamjakhete/spotify_agent](https://github.com/shubhamjakhete/spotify_agent)

### About the Developer

Shubham Jakhete is a passionate developer who loves creating innovative solutions that combine cutting-edge AI technology with practical applications. This Spotify Agent project demonstrates the power of AI in enhancing everyday experiences like music discovery.

---

**🎵 Made with ❤️ for music lovers everywhere**

*Last updated: August 8, 2025*
