#!/usr/bin/env python3
"""
Spotify Agent - Chat Interface
A chat-based CLI for music recommendations using Spotify and OpenAI
"""

import sys
import time
from spotify_client import SpotifyClient
from openai_client import OpenAIClient
from chat_cli import SpotifyAgentCLI
from logging_config import (
    setup_logging, 
    get_logger,
    log_user_interaction
)

# Initialize logging system
app_logger, log_file_path = setup_logging()
logger = get_logger('main')


def main():
    """Main function - directly starts the chat interface"""
    try:
        logger.info("Starting Spotify Agent")
        
        print("🎵 Spotify Agent - Starting Chat Interface...")
        print("=" * 50)
        print(f"📋 Logs: {log_file_path}")
        print("=" * 50)
        
        log_user_interaction(logger, "Application started", "User initiated main.py")
        
        # Create and start chat CLI
        cli = SpotifyAgentCLI()
        cli.start_session()
        
        logger.info("Application completed successfully")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all required files are in the same directory:")
        print("  - spotify_client.py")
        print("  - openai_client.py") 
        print("  - chat_cli.py")
        print("  - logging_config.py")
        logger.error(f"Import error: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!")
        logger.info("Application interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 