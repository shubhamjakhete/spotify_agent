Software Requirements Document (SRD)
Spotify Agent - Smart Music Recommendation System

1. Introduction

1.1 Purpose
This document specifies the functional and non-functional requirements for the Spotify Agent system. The purpose of this system is to build a smart assistant that can access a user's Spotify account, analyze listening habits, and generate personalized music recommendations.

1.2 Scope
The Spotify Agent will be a command-line interface (CLI) application that integrates with Spotify's API to provide intelligent music recommendations based on user listening patterns, preferences, and contextual factors through an interactive terminal-based chat interface.

 1.3 Definitions and Acronyms
- SRD: Software Requirements Document
- API: Application Programming Interface
- OAuth: Open Authorization protocol
- JWT: JSON Web Token
- REST: Representational State Transfer
- UI/UX: User Interface/User Experience

 2. System Overview

 2.1 System Description
The Spotify Agent is an intelligent music recommendation system that leverages OpenAI's advanced AI models, TensorFlow, and PyTorch for machine learning algorithms to analyze user listening behavior and provide personalized music suggestions. The system will integrate with Spotify's API through Spotipy to access user data and use OpenAI's API for intelligent recommendation generation through an interactive command-line interface with chat-based interactions.

 2.2 System Context
- Primary Users: Spotify Premium and Free users
- Integration: Spotify Web API (via Spotipy), Spotify OAuth 2.0, OpenAI API
- Platform: Command-line interface (CLI) application
- Deployment: Local installation on user's machine
- AI Engine: OpenAI GPT models, TensorFlow, and PyTorch for intelligent recommendation generation
- Interface: Interactive terminal-based chat interface
- Technology Stack: Python, Spotipy, TensorFlow, PyTorch

 3. Functional Requirements

 3.1 User Authentication and Authorization
FR-001: User Authentication
- The system shall allow users to authenticate using Spotify OAuth 2.0
- The system shall request appropriate permissions to access user's Spotify data
- The system shall securely store and manage user authentication tokens
- The system shall handle token refresh automatically

FR-002: User Profile Management
- The system shall display user's Spotify profile information
- The system shall allow users to view their current subscription status
- The system shall provide logout functionality

 3.2 Data Collection and Analysis
FR-003: Listening History Analysis
- The system shall collect user's recent listening history (last 50 tracks)
- The system shall analyze listening patterns and preferences
- The system shall identify favorite artists, genres, and tracks
- The system shall track listening frequency and time patterns

FR-004: Playlist Analysis
- The system shall analyze user's created and followed playlists
- The system shall identify playlist themes and moods
- The system shall extract common characteristics from playlist contents

FR-005: AI-Enhanced Audio Features Analysis
- The system shall analyze audio features of listened tracks (tempo, energy, danceability, etc.) using Spotipy
- The system shall use OpenAI, TensorFlow, and PyTorch to create intelligent user preference profiles based on audio characteristics
- The system shall employ machine learning models to identify complex patterns in audio feature preferences
- The system shall use AI to correlate audio features with user behavior and preferences

 3.6 Recommendation Engine
FR-006: AI-Powered Personalized Recommendations
- The system shall use OpenAI API, TensorFlow, and PyTorch to generate personalized track recommendations based on listening history
- The system shall leverage GPT models and machine learning algorithms to provide intelligent artist recommendations based on user preferences
- The system shall use AI analysis and ML models to suggest new genres or sub-genres to explore
- The system shall employ OpenAI and ML frameworks to offer smart playlist recommendations

FR-007: AI-Enhanced Contextual Recommendations
- The system shall use OpenAI, TensorFlow, and PyTorch to consider time of day, mood, and context for recommendations
- The system shall factor in user's current mood (if provided) using AI sentiment analysis and ML models
- The system shall provide AI-powered recommendations based on activity context (workout, study, party, etc.)
- The system shall use natural language processing and machine learning to understand user preferences and context

FR-008: AI-Driven Discovery Features
- The system shall use OpenAI, TensorFlow, and PyTorch to suggest "Discover Weekly" style recommendations with enhanced intelligence
- The system shall provide AI-powered "Release Radar" for new releases from favorite artists using ML models
- The system shall offer "Similar Artists" suggestions using OpenAI's understanding and ML-based similarity analysis
- The system shall generate personalized music insights and trends using AI analysis and machine learning algorithms

 3.9 Command-Line Interface
FR-009: Interactive Chat Interface
- The system shall provide an interactive chat-based interface in the terminal
- The system shall display user's music profile and statistics through text-based output
- The system shall show recent recommendations and their performance in a readable format

FR-010: Terminal-Based Recommendation Display
- The system shall display recommendations in an organized, text-based format suitable for terminal
- The system shall provide track preview information through terminal output
- The system shall allow users to save recommendations to playlists via command inputs
- The system shall provide play functionality for recommendations through terminal commands

FR-011: Command-Based Search and Filter
- The system shall allow users to search through recommendations using text commands
- The system shall provide filtering options by genre, mood, energy level, etc. through command parameters
- The system shall allow users to sort recommendations using command-line arguments

 3.13 Playlist Management
FR-012: Command-Based Playlist Creation
- The system shall allow users to create new playlists from recommendations using terminal commands
- The system shall provide smart playlist generation based on criteria through command-line interface
- The system shall allow users to modify existing playlists via terminal commands

FR-013: Terminal-Based Playlist Operations
- The system shall allow users to share generated playlists through terminal commands
- The system shall provide playlist export functionality via command-line interface
- The system shall display playlist information in a terminal-friendly format

 4. Non-Functional Requirements

 4.1 Performance Requirements
NFR-001: Response Time
- The system shall respond to user requests within 2 seconds
- AI-powered recommendation generation shall complete within 8 seconds (including OpenAI API calls)
- Page load times shall be under 3 seconds
- OpenAI API calls shall be optimized to minimize latency

NFR-002: Scalability
- The system shall support up to 10,000 concurrent users
- The system shall handle up to 100,000 API requests per hour (combined Spotify and OpenAI)
- The system shall be horizontally scalable
- The system shall implement OpenAI API rate limiting and cost optimization

 4.2 Security Requirements
NFR-003: Data Security
- All user data shall be encrypted in transit using HTTPS
- User authentication tokens shall be stored securely
- The system shall comply with GDPR and data privacy regulations
- The system shall implement proper session management

NFR-004: API Security
- The system shall implement rate limiting for API calls (both Spotify and OpenAI)
- The system shall validate all input data
- The system shall implement proper error handling without exposing sensitive information
- The system shall securely manage OpenAI API keys and credentials
- The system shall implement request caching to optimize OpenAI API usage

 4.3 Reliability Requirements
NFR-005: Availability
- The system shall maintain 99.5% uptime
- The system shall implement graceful degradation when Spotify API is unavailable
- The system shall implement graceful degradation when OpenAI API is unavailable
- The system shall provide backup and recovery mechanisms
- The system shall cache AI recommendations to reduce dependency on OpenAI API availability

NFR-006: Data Integrity
- The system shall maintain data consistency across all operations
- The system shall implement proper error handling and logging
- The system shall provide data validation and sanitization

 4.4 Usability Requirements
NFR-007: Terminal User Experience
- The system shall provide an intuitive and responsive command-line interface
- The system shall be accessible on desktop and laptop terminals
- The system shall support keyboard navigation and command history
- The system shall provide clear error messages and user feedback in terminal format

NFR-008: Terminal Accessibility
- The system shall provide clear, readable text output in terminal
- The system shall support terminal color schemes and formatting
- The system shall be compatible with terminal screen readers
- The system shall provide keyboard shortcuts for common operations

 4.5 Compatibility Requirements
NFR-009: Terminal Compatibility
- The system shall work on Unix-based terminals (Linux, macOS)
- The system shall be compatible with Windows Command Prompt and PowerShell
- The system shall support various terminal emulators and color schemes
- The system shall work with different terminal window sizes

NFR-010: API Compatibility
- The system shall be compatible with Spotify Web API v1
- The system shall handle API version changes gracefully
- The system shall implement proper API error handling

 4.6 Maintainability Requirements
NFR-011: Code Quality
- The system shall follow Python coding standards and best practices (PEP 8)
- The system shall include comprehensive documentation
- The system shall implement proper logging and monitoring
- The system shall be modular and easily maintainable
- The system shall use Python virtual environments for dependency management

NFR-012: Testing
- The system shall have unit test coverage of at least 80% using Python testing frameworks (pytest)
- The system shall include integration tests for API interactions (Spotify and OpenAI)
- The system shall include end-to-end testing for critical user flows
- The system shall include ML model testing and validation

 5. System Constraints

 5.1 Technical Constraints
- Must integrate with Spotify Web API using Spotipy library
- Must integrate with OpenAI API for AI-powered recommendations
- Must use TensorFlow and PyTorch for machine learning components
- Must comply with Spotify's API usage limits and terms of service
- Must comply with OpenAI's API usage limits and terms of service
- Must use OAuth 2.0 for authentication
- Must be a Python-based command-line interface application
- Must be installable and runnable on user's local machine
- Must manage Python dependencies and ML model requirements

 5.2 Business Constraints
- Must be developed within budget and timeline constraints
- Must comply with data protection regulations
- Must not violate Spotify's terms of service
- Must be monetizable (future consideration)

 5.3 Regulatory Constraints
- Must comply with GDPR for EU users
- Must comply with CCPA for California users
- Must implement proper data retention policies
- Must provide user data export and deletion capabilities

 6. External Interfaces

 6.1 User Interfaces
- Command-line interface with interactive chat functionality
- Terminal-based text output and input
- Command history and auto-completion features

 6.2 Hardware Interfaces
- User's local machine (desktop/laptop)
- Terminal/command prompt interface
- Local storage for configuration and cache

 6.3 Software Interfaces
- Spotify Web API
- OpenAI API (GPT models for recommendation engine)
- Local database/file system for configuration
- Python-based command-line application
- Spotipy library for Spotify API integration
- TensorFlow and PyTorch for machine learning components
- Terminal interface libraries (rich, click, typer)

 6.4 Communication Interfaces
- HTTPS for secure API communication
- Local file system for data persistence
- Terminal input/output for user interaction

 7. Quality Attributes

 7.1 Performance
- Fast recommendation generation
- Efficient data processing
- Optimized API usage

 7.2 Security
- Secure authentication
- Data encryption
- Privacy protection

 7.3 Usability
- Intuitive command-line interface
- Responsive terminal interactions
- Terminal accessibility features

 7.4 Reliability
- High availability
- Error handling
- Data backup

 8. Black Box Testing

 8.1 Testing Methodology
Black box testing was conducted to verify the functionality of the Spotify Agent system without knowledge of its internal implementation. Testing focused on user interactions, API integrations, and system responses.

 8.2 Test Environment
- **Operating System**: macOS (darwin 24.5.0)
- **Python Version**: 3.x
- **Virtual Environment**: spotify_agent_env
- **Terminal**: zsh shell
- **Dependencies**: spotipy, python-dotenv, openai>=1.0.0

 8.3 Test Cases and Results

 #### 8.3.1 Environment Setup Testing

 **Test Case 1: Virtual Environment Creation**
- Input: python3 -m venv spotify_agent_env
- Expected Result: Virtual environment created
- Actual Result: Virtual environment created successfully
- Status: ✅ PASS

 **Test Case 2: Environment Activation**
- Input: source venv/bin/activate
- Expected Result: Environment activated
- Actual Result: Environment activated successfully
- Status: ✅ PASS

 **Test Case 3: Dependency Installation**
- Input: pip install "openai>=1.0.0"
- Expected Result: Dependencies installed
- Actual Result: Dependencies installed successfully
- Status: ✅ PASS

 **Test Case 4: Environment File Setup**
- Input: mv env_template.txt .env
- Expected Result: Environment file created
- Actual Result: Environment file created successfully
- Status: ✅ PASS

 #### 8.3.2 Spotify Client Testing

 **Test Case 1: Spotify OAuth Authentication**
- Input: Run python spotify_client.py
- Expected Result: User authentication successful
- Actual Result: Authentication successful, user info displayed
- Status: ✅ PASS

 **Test Case 2: User Information Display**
- Input: Automatic after authentication
- Expected Result: Display name and email shown
- Actual Result: User profile information displayed correctly
- Status: ✅ PASS

 **Test Case 3: Recent Tracks Retrieval**
- Input: get_recent_tracks(limit=5)
- Expected Result: 5 recent tracks returned
- Actual Result: Recent tracks retrieved successfully
- Status: ✅ PASS

 **Test Case 4: Top Artists Retrieval**
- Input: get_top_artists(limit=5)
- Expected Result: 5 top artists returned
- Actual Result: Top artists retrieved successfully
- Status: ✅ PASS

 **Test Case 5: OAuth Scope Validation**
- Input: Check required scopes
- Expected Result: All required scopes granted
- Actual Result: Initially failed with 403 error, resolved after scope update
- Status: ⚠️ FIXED

 #### 8.3.3 OpenAI Client Testing

 **Test Case 1: OpenAI API Connection**
- Input: Run python openai_client.py
- Expected Result: Connection successful
- Actual Result: Connection successful
- Status: ✅ PASS

 **Test Case 2: Model Configuration**
- Input: GPT-3.5-turbo
- Expected Result: Model responds correctly
- Actual Result: Model responds correctly
- Status: ✅ PASS

 **Test Case 3: Basic Chat Function**
- Input: "Hello"
- Expected Result: Response received
- Actual Result: Response received successfully
- Status: ✅ PASS

 **Test Case 4: Music Recommendation Test**
- Input: "I like Avicii, Find me 5 similar ones"
- Expected Result: 5 music recommendations
- Actual Result: 5 relevant recommendations provided
- Status: ✅ PASS

 **Test Case 5: File Naming Conflict**
- Input: openai.py file name
- Expected Result: Import error
- Actual Result: ImportError: cannot import name 'OpenAI'
- Status: ❌ FAIL

 **Test Case 6: File Rename Resolution**
- Input: Rename to openai_client.py
- Expected Result: No import conflicts
- Actual Result: No import conflicts
- Status: ✅ PASS

 #### 8.3.4 Music Recommendation Testing

 **Test Case 1: Avicii Recommendation**
- Input: "I like Avicii, Find me 5 similar ones"
- Expected Result: EDM artists recommended
- Actual Result: Zedd, David Guetta, Calvin Harris recommended
- Status: ✅ PASS

 **Test Case 2: Coldplay Recommendation**
- Input: "I like Colplay, Find me 5 Coldplay songs"
- Expected Result: Coldplay songs recommended
- Actual Result: Coldplay songs recommended
- Status: ✅ PASS

 **Test Case 3: Pritam & Arijit Singh Test**
- Input: "I like Pritam and Arijit Singh, Find me 5 similar ones"
- Expected Result: Mix of composers and singers
- Actual Result: Only Arijit Singh songs recommended, Pritam ignored
- Status: ⚠️ PARTIAL

 **Test Case 4: AI Composer Understanding**
- Input: Test composer vs singer distinction
- Expected Result: Proper distinction made
- Actual Result: AI confused composers with singers
- Status: ❌ FAIL

 #### 8.3.5 Error Handling Testing

 **Test Case 1: Missing API Keys**
- Input: No .env file
- Expected Result: Clear error message
- Actual Result: "Missing OpenAI API key" error displayed
- Status: ✅ PASS

 **Test Case 2: Invalid API Keys**
- Input: Wrong API keys
- Expected Result: Authentication failure
- Actual Result: Authentication failure handled gracefully
- Status: ✅ PASS

 **Test Case 3: Network Connectivity**
- Input: No internet connection
- Expected Result: Connection error
- Actual Result: Connection error handled
- Status: ✅ PASS

 **Test Case 4: Rate Limiting**
- Input: Multiple rapid requests
- Expected Result: Rate limit handling
- Actual Result: Rate limit handling implemented
- Status: ✅ PASS

 #### 8.3.6 Code Quality Testing

 **Test Case 1: Syntax Validation**
- Input: Python syntax check
- Expected Result: No syntax errors
- Actual Result: Syntax errors in function calls fixed
- Status: ✅ PASS

 **Test Case 2: Import Validation**
- Input: Import statements
- Expected Result: All imports successful
- Actual Result: Import conflicts resolved
- Status: ✅ PASS

 **Test Case 3: Function Cleanup**
- Input: Comment unused functions
- Expected Result: Clean codebase
- Actual Result: Unused functions commented out
- Status: ✅ PASS

 **Test Case 4: Documentation**
- Input: Code documentation
- Expected Result: Well-documented code
- Actual Result: Functions properly documented
- Status: ✅ PASS

 8.4 Test Results Summary

 #### 8.4.1 Overall Test Results
- **Total Test Cases**: 24
- **Passed**: 20 (83.3%)
- **Failed**: 2 (8.3%)
- **Fixed**: 2 (8.3%)

 #### 8.4.2 Key Findings
1. **Authentication Systems**: Both Spotify OAuth and OpenAI API authentication work correctly
2. **Music Recommendations**: Basic recommendations work well, but AI struggles with composer/singer distinction
3. **Error Handling**: Comprehensive error handling implemented and tested
4. **Code Quality**: Clean, well-documented code with proper syntax
5. **Integration**: Successful integration between Spotify and OpenAI APIs

 #### 8.4.3 Issues Identified and Resolved
1. **OAuth Scope Issues**: Initially failed due to insufficient scopes, resolved by updating scope permissions
2. **File Naming Conflicts**: `openai.py` conflicted with library import, resolved by renaming to `openai_client.py`
3. **Shell Interpretation**: `>=` characters interpreted as redirection, resolved by using quotes
4. **Syntax Errors**: Multiple mood parameters in function calls, resolved by proper list formatting

 #### 8.4.4 Recommendations for Future Testing
1. **AI Model Training**: Improve composer vs singer distinction in AI responses
2. **Comprehensive Integration Testing**: Test full workflow from Spotify data to OpenAI recommendations
3. **Performance Testing**: Test with larger datasets and multiple users
4. **Security Testing**: Penetration testing for API key security
5. **User Acceptance Testing**: Real user testing with various music preferences

 8.5 Test Documentation
- **Test Environment Setup**: Documented in prompt.txt
- **Test Cases**: All test cases documented with inputs and results
- **Issues Log**: Complete log of issues encountered and resolutions
- **Code Changes**: All modifications tracked and documented

 9. Appendices

 8.1 Glossary
- API: Application Programming Interface
- CLI: Command-Line Interface
- OAuth: Open Authorization protocol
- JWT: JSON Web Token
- GPT: Generative Pre-trained Transformer (OpenAI's language model)
- AI: Artificial Intelligence
- NLP: Natural Language Processing
- ML: Machine Learning
- Spotipy: Python library for Spotify Web API
- TensorFlow: Open-source machine learning framework
- PyTorch: Open-source machine learning framework
- GDPR: General Data Protection Regulation
- CCPA: California Consumer Privacy Act

 8.2 References
- Spotify Web API Documentation
- Spotipy Library Documentation
- OpenAI API Documentation
- TensorFlow Documentation
- PyTorch Documentation
- OAuth 2.0 Specification
- GDPR Compliance Guidelines
- Python PEP 8 Style Guide




Prompt test method:
1. when specifically asked "recommend me something i like most often" -> it is recommending only one song

2. it is ignoring the message like "already listened", "heard before"

3. Quantity of recommended songs not detected

4. 