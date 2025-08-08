#!/usr/bin/env python3
"""
Spotify Agent - Interactive Chat CLI
A chat-based command line interface for music recommendations using GPT
"""

import sys
import time
from datetime import datetime
from typing import List, Dict, Any
from spotify_client import SpotifyClient
from openai_client import OpenAIClient
from logging_config import (
    get_logger,
    log_function_entry,
    log_function_exit,
    log_user_interaction,
    log_error_with_context,
    log_performance_metric
)

# Get configured logger
logger = get_logger('chat_cli')


class SpotifyAgentCLI:
    """
    Interactive CLI for Spotify Agent with conversation context
    """
    
    def __init__(self):
        """Initialize the CLI with clients and conversation history"""
        self.spotify_client = None
        self.openai_client = None
        self.conversation_history = []
        self.exit_commands = ['exit', 'quit', 'bye', 'goodbye']
        self.session_start_time = datetime.now()
        
    def initialize_clients(self):
        """Initialize Spotify and OpenAI clients"""
        try:
            print("🎵 Initializing Spotify Agent...")
            print("=" * 50)
            
            # Initialize OpenAI Client (required)
            print("🤖 Connecting to OpenAI...")
            self.openai_client = OpenAIClient()
            
            if not self.openai_client.test_connection():
                print("❌ Failed to connect to OpenAI")
                return False
            
            print("✅ OpenAI connection successful!")
            
            # Initialize Spotify Client (optional)
            print("📡 Connecting to Spotify...")
            try:
                self.spotify_client = SpotifyClient()
                if self.spotify_client.test_connection():
                    print("✅ Spotify connection successful!")
                    self._load_spotify_context()
                else:
                    print("⚠️  Spotify connection failed - continuing without Spotify data")
                    self.spotify_client = None
            except Exception as e:
                print(f"⚠️  Spotify unavailable: {e}")
                print("🎵 Continuing with OpenAI only...")
                self.spotify_client = None
            
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            logger.error(f"Failed to initialize clients: {e}")
            return False
    
    def _load_spotify_context(self):
        """Load user's Spotify context at session start"""
        try:
            if not self.spotify_client:
                return
            
            print("\n📊 Loading your Spotify profile...")
            
            # Get recent tracks and top artists
            recent_tracks = self.spotify_client.get_recent_tracks(limit=50)
            top_artists = self.spotify_client.get_top_artists(limit=50)
            
            if recent_tracks or top_artists:
                context_prompt = self._format_spotify_context(recent_tracks, top_artists)
                
                # Add Spotify context to conversation history
                self.conversation_history.append({
                    "role": "system",
                    "content": f"User's Spotify Context: {context_prompt}"
                })
                
                print("✅ Spotify context loaded!")
                print(f"📋 Found {len(recent_tracks)} recent tracks and {len(top_artists)} top artists")
            else:
                print("⚠️  No Spotify data available")
                
        except Exception as e:
            logger.error(f"Failed to load Spotify context: {e}")
            print("⚠️  Could not load Spotify context - continuing without it")
    
    def _format_spotify_context(self, recent_tracks: List[Dict], top_artists: List[Dict]) -> str:
        """Format Spotify data for context"""
        context_parts = []
        
        #if recent_tracks:
        #    tracks_text = ", ".join([f"{track['name']} by {track['artist']}" for track in recent_tracks])
        #    context_parts.append(f"Recent tracks: {tracks_text}")
        
        if recent_tracks:
        # Create a dictionary to track unique tracks using track+artist as key
            unique_tracks = {}
            for track in recent_tracks:
                track_key = f"{track['name']} by {track['artist']}"
                if track_key not in unique_tracks:
                    unique_tracks[track_key] = track
        
        # Join only the unique tracks
            tracks_text = ", ".join(unique_tracks.keys())
            context_parts.append(f"Recent tracks: {tracks_text}")

        if top_artists:
            artists_text = ", ".join([artist['name'] for artist in top_artists])
            context_parts.append(f"Top artists: {artists_text}")
        
        return ". ".join(context_parts)
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "🎵" * 20)
        print("  SPOTIFY AGENT - CHAT INTERFACE")
        print("🎵" * 20)
        print("\n🎤 Welcome to your AI Music Assistant!")
        print("💬 Chat with me about music and get personalized recommendations!")
        print("\n📝 How to use:")
        print("   • Ask for music recommendations")
        print("   • Describe your mood or activity")
        print("   • Ask about artists or genres")
        print("   • Type 'exit', 'quit', or 'bye' to end")
        print("\n" + "=" * 50)
        
        if self.spotify_client:
            print("🎯 I have access to your Spotify listening history for better recommendations!")
        else:
            print("🎯 I'll help you discover music based on your preferences!")
        
        print("=" * 50 + "\n")
    
    def display_conversation_stats(self):
        """Display conversation statistics"""
        user_messages = len([msg for msg in self.conversation_history if msg['role'] == 'user'])
        assistant_messages = len([msg for msg in self.conversation_history if msg['role'] == 'assistant'])
        session_duration = datetime.now() - self.session_start_time
        
        print(f"\n📊 Session Stats:")
        print(f"   • Duration: {session_duration}")
        print(f"   • Your messages: {user_messages}")
        print(f"   • AI responses: {assistant_messages}")
        print(f"   • Total exchanges: {user_messages}")
    
    def get_user_input(self) -> str:
        """Get user input with prompt"""
        try:
            user_input = input("🎵 You: ").strip()
            return user_input
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for chatting about music!")
            return "exit"
        except EOFError:
            return "exit"
    
    def is_exit_command(self, user_input: str) -> bool:
        """Check if user wants to exit"""
        return user_input.lower() in self.exit_commands
    
    def validate_input(self, user_input: str) -> bool:
        """Validate user input"""
        if not user_input:
            print("⚠️  Please enter a message or type 'exit' to quit.")
            return False
        
        if len(user_input.strip()) < 2:
            print("⚠️  Please enter a more detailed message.")
            return False
        
        return True
    
    def process_user_message(self, user_input: str) -> str:
        """Process user message and get GPT response"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Create context-aware prompt
            full_prompt = self._build_context_prompt(user_input)
            print("Debug: About to send the following to GPT:")
            # Print the full context being sent to GPT
            print("\n📝 Full Context being sent to GPT:")
            print("=" * 50)
            print(full_prompt)
            print("=" * 50)
            print()
            
            # Get response from OpenAI
            logger.info(f"User input: {user_input[:100]}...")
            gpt_response = self.openai_client.chat(full_prompt)
            
            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": gpt_response
            })
            
            logger.info(f"GPT response: {gpt_response[:100]}...")
            return gpt_response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            logger.error(f"Error processing message: {e}")
            return error_msg
    
    def _build_context_prompt(self, current_input: str) -> str:
        """Build context-aware prompt with conversation history"""
        # Get recent conversation context (last 6 messages to avoid token limits)
        recent_history = self.conversation_history[-6:] if len(self.conversation_history) > 6 else self.conversation_history
        
        context_parts = []
        
        # Add conversation context
        if recent_history:
            context_parts.append("Previous conversation:")
            for msg in recent_history:
                if msg['role'] == 'user':
                    context_parts.append(f"User: {msg['content']}")
                elif msg['role'] == 'assistant':
                    context_parts.append(f"Assistant: {msg['content'][:200]}...")  # Truncate long responses
                elif msg['role'] == 'system':
                    context_parts.append(f"System: {msg['content']}")
                # Skip system messages in context to save tokens
        
        # Add current input
        context_parts.append(f"Current request: {current_input}")
        
        return "\n".join(context_parts)
    
    def display_response(self, response: str):
        """Display GPT response with formatting"""
        print(f"\n🎯 AI Assistant: {response}\n")
        print("-" * 50)
    
    def run_chat_loop(self):
        """Main chat loop"""
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                # Check for exit command
                if self.is_exit_command(user_input):
                    print("\n👋 Thanks for chatting! Hope you discover some great music!")
                    self.display_conversation_stats()
                    logger.info("Chat session ended by user")
                    break
                
                # Validate input
                if not self.validate_input(user_input):
                    continue
                
                # Process message and get response
                print("\n🤔 Thinking...")
                response = self.process_user_message(user_input)
                
                # Display response
                self.display_response(response)
                
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                logger.error(f"Unexpected error in chat loop: {e}")
                print("Please try again or type 'exit' to quit.\n")
    
    def start_session(self):
        """Start the chat session"""
        try:
            # Initialize clients
            if not self.initialize_clients():
                print("❌ Failed to initialize. Please check your configuration.")
                sys.exit(1)
            
            # Display welcome
            self.display_welcome()
            
            # Log session start
            logger.info("=== NEW CHAT SESSION STARTED ===")
            logger.info(f"Session start time: {self.session_start_time}")
            logger.info(f"Spotify available: {self.spotify_client is not None}")
            
            # Start chat loop
            self.run_chat_loop()
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
        except Exception as e:
            print(f"\n❌ Session error: {e}")
            logger.error(f"Session error: {e}")
        finally:
            logger.info("=== CHAT SESSION ENDED ===")


def main():
    """Main function to start the chat CLI"""
    cli = SpotifyAgentCLI()
    cli.start_session()


if __name__ == "__main__":
    main()
