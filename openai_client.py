#!/usr/bin/env python3
"""
OpenAI Client for Spotify Agent
Handles OpenAI API interactions for music recommendations
"""

import os
import sys
import time
from typing import Optional, Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv
from logging_config import (
    get_logger,
    log_function_entry,
    log_function_exit,
    log_api_call,
    log_error_with_context,
    log_performance_metric,
    log_user_interaction
)

# Get configured logger
logger = get_logger('openai_client')


class OpenAIClient:
    """
    OpenAI client class for handling API interactions
    """
    
    def __init__(self):
        """Initialize the OpenAI client"""
        # Load environment variables
        load_dotenv()
        
        # Get OpenAI credentials from environment
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        self.org_id = os.getenv('OPENAI_ORG_ID')
        
        # Validate required environment variables
        if not self.api_key:
            raise ValueError(
                "Missing OpenAI API key. Please set OPENAI_API_KEY in your .env file"
            )
        
        # Initialize OpenAI client
        self.client = self._initialize_openai_client()
        
    def _initialize_openai_client(self) -> OpenAI:
        """
        Initialize OpenAI client
        
        Returns:
            OpenAI: Initialized OpenAI client
        """
        try:
            # Create OpenAI client
            client = OpenAI(
                api_key=self.api_key,
                organization=self.org_id if self.org_id else None
            )
            
            # Test the connection with a simple request
            self._test_connection(client)
            
            logger.info(f"Successfully initialized OpenAI client with model: {self.model}")
            return client
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def _test_connection(self, client: OpenAI) -> None:
        """
        Test the OpenAI connection with a simple request
        
        Args:
            client: OpenAI client instance
        """
        try:
            # Simple test request
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
                temperature=0
            )
            
            if response.choices and response.choices[0].message.content:
                logger.info("OpenAI connection test successful")
            else:
                raise Exception("No response received from OpenAI")
                
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            raise
    
    def chat(self, prompt: str) -> str:
        """
        Send a user prompt to GPT and return the response
        
        Args:
            prompt (str): User's input prompt
            
        Returns:
            str: GPT's response
        """
        try:
            logger.info(f"Processing prompt: {prompt[:50]}...")
            
            # Create the conversation context
            messages = [
                {
                    "role": "system",
                    "content": """You are a music recommendation expert. You help users discover new music based on their preferences. 
                    When suggesting songs, provide:
                    1. Song name
                    2. Artist name
                    3. Brief reason why they might like it
                    
                    Be enthusiastic and helpful in your recommendations. Use emojis to make responses engaging."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract the response
            if response.choices and response.choices[0].message.content:
                gpt_response = response.choices[0].message.content.strip()
                logger.info(f"Generated response for prompt: {prompt[:50]}...")
                return gpt_response
            else:
                error_msg = "No response content received from OpenAI"
                logger.error(error_msg)
                return f"Sorry, I encountered an error: {error_msg}"
                
        except Exception as e:
            logger.error(f"Failed to get response from OpenAI: {e}")
            return f"Sorry, I encountered an error while processing your request: {str(e)}"
    
    # def get_music_recommendations(self, artists: List[str], genres: Optional[List[str]] = None, 
    #                              mood: Optional[str] = None, count: int = 5) -> str:
    #     """
    #     Get music recommendations based on artists and preferences
    #     
    #     Args:
    #         artists (List[str]): List of favorite artists
    #         genres (Optional[List[str]]): Preferred genres
    #         mood (Optional[str]): Desired mood
    #         count (int): Number of recommendations to generate
    #         
    #     Returns:
    #         str: Formatted recommendations
    #     """
    #     try:
    #         # Build the recommendation prompt
    #         prompt_parts = [f"I like {', '.join(artists)}"]
    #         
    #         if genres:
    #             prompt_parts.append(f"I enjoy {', '.join(genres)} music")
    #         
    #         if mood:
    #             prompt_parts.append(f"I'm looking for {mood} music")
    #         
    #         prompt_parts.append(f"Can you suggest {count} similar artists or songs I might like?")
    #         
    #         prompt = ". ".join(prompt_parts) + "."
    #         
    #         # Get recommendations
    #         return self.chat(prompt)
    #         
    #     except Exception as e:
    #         logger.error(f"Failed to get music recommendations: {e}")
    #         return f"Sorry, I couldn't generate recommendations: {str(e)}"
    
    # def analyze_listening_patterns(self, recent_tracks: List[Dict[str, Any]], 
    #                              top_artists: List[Dict[str, Any]]) -> str:
    #     """
    #     Analyze user's listening patterns and provide insights
    #     
    #     Args:
    #         recent_tracks (List[Dict]): User's recently played tracks
    #         top_artists (List[Dict]): User's top artists
    #         
    #     Returns:
    #         str: Analysis and insights
    #     """
    #     try:
    #         # Build analysis prompt
    #         tracks_info = "\n".join([
    #             f"- {track['name']} by {track['artist']}" 
    #             for track in recent_tracks[:10]
    #         ])
    #         
    #         artists_info = "\n".join([
    #             f"- {artist['name']} ({', '.join(artist['genres'][:3])})" 
    #             for artist in top_artists[:10]
    #         ])
    #         
    #         prompt = f"""Based on my listening patterns, can you analyze my music taste?
    # 
    # Recent tracks I've been listening to:
    # {tracks_info}
    # 
    # My top artists:
    # {artists_info}
    # 
    # Please provide:
    # 1. Analysis of my music preferences
    # 2. Genres I seem to enjoy most
    # 3. 5 new artists I should check out
    # 4. Any patterns you notice in my listening habits"""
    # 
    #         return self.chat(prompt)
    #         
    #     except Exception as e:
    #         logger.error(f"Failed to analyze listening patterns: {e}")
    #         return f"Sorry, I couldn't analyze your listening patterns: {str(e)}"
    
    def test_connection(self) -> bool:
        """
        Test the OpenAI connection
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10,
                temperature=0
            )
            
            if response.choices and response.choices[0].message.content:
                logger.info("OpenAI connection test successful")
                return True
            else:
                logger.error("OpenAI connection test failed - no response")
                return False
                
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False


def main():
    """Main function to test OpenAI client"""
    try:
        print("🤖 Initializing OpenAI Client...")
        
        # Create OpenAI client
        client = OpenAIClient()
        
        # Test connection
        if client.test_connection():
            print("✅ OpenAI connection successful!")
            
            # Test the sample prompt
            print("\n" + "="*60)
            print("🎵 MUSIC RECOMMENDATION TEST")
            print("="*60)
            
            sample_prompt = "I like Colplay, Find me 5 Coldplay songs"
            print(f"User: {sample_prompt}")
            
            response = client.chat(sample_prompt)
            print(f"GPT: {response}")
            
            # Test music recommendations method
            #print("\n" + "="*60)
            #print("🎤 STRUCTURED RECOMMENDATIONS TEST")
            #print("="*60)
            
            #recommendations = client.get_music_recommendations(
            #    artists=["Coldplay"],
            #    genres=["EDM","pop"],
            #    mood=["romantic","energetic","sad","happy","angry","relaxed","upbeat","chill","party","dance"],
            #    count=5
            #    )
            #print(recommendations)
            
        else:
            print("❌ Failed to connect to OpenAI")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease ensure your .env file contains:")
        print("  - OPENAI_API_KEY")
        print("  - OPENAI_MODEL (optional, defaults to gpt-3.5-turbo)")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        logger.error(f"Unexpected error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 