#!/usr/bin/env python3
"""
Spotify Client for Spotify Agent
Handles OAuth authentication and basic user information retrieval
"""

import os
import sys
import time
from typing import Optional, Dict, Any, List
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from logging_config import (
    get_logger,
    log_function_entry,
    log_function_exit,
    log_api_call,
    log_error_with_context,
    log_performance_metric,
    log_data_summary
)

# Get configured logger
logger = get_logger('spotify_client')


class SpotifyClient:
    """
    Spotify client class for handling authentication and API interactions
    """
    
    def __init__(self):
        """Initialize the Spotify client with OAuth authentication"""
        log_function_entry(logger, "__init__")
        start_time = time.time()
        
        try:
            # Load environment variables
            logger.info("Loading environment variables for Spotify client")
            load_dotenv()
            
            # Get Spotify credentials from environment
            self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
            self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
            self.scopes = os.getenv('SPOTIFY_SCOPES', 'user-read-private user-read-email')
            
            logger.debug(f"Loaded credentials - Client ID: {'*' * len(self.client_id) if self.client_id else 'None'}")
            logger.debug(f"Redirect URI: {self.redirect_uri}")
            logger.debug(f"Scopes: {self.scopes}")
            
            # Validate required environment variables
            if not self.client_id or not self.client_secret:
                missing_creds = []
                if not self.client_id: missing_creds.append("SPOTIFY_CLIENT_ID")
                if not self.client_secret: missing_creds.append("SPOTIFY_CLIENT_SECRET")
                
                error_msg = f"Missing Spotify credentials: {', '.join(missing_creds)}"
                log_error_with_context(logger, error_msg, 
                                     {"missing_credentials": missing_creds}, "__init__")
                raise ValueError(
                    "Missing Spotify credentials. Please set SPOTIFY_CLIENT_ID and "
                    "SPOTIFY_CLIENT_SECRET in your .env file"
                )
            
            logger.info("Spotify credentials validated successfully")
            
            # Initialize Spotify client with OAuth
            self.sp = self._initialize_spotify_client()
            
            duration = time.time() - start_time
            log_performance_metric(logger, "spotify_client_initialization", duration, "OAuth setup completed")
            log_function_exit(logger, "__init__", "SpotifyClient initialized", True)
            
        except Exception as e:
            log_error_with_context(logger, e, {"stage": "initialization"}, "__init__")
            log_function_exit(logger, "__init__", None, False)
            raise
        
    def _initialize_spotify_client(self) -> spotipy.Spotify:
        """
        Initialize Spotify client with OAuth authentication
        
        Returns:
            spotipy.Spotify: Authenticated Spotify client
        """
        try:
            # Create OAuth manager
            oauth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scopes,
                cache_path='.spotify_cache'  # Cache tokens locally
            )
            
            # Create Spotify client
            sp = spotipy.Spotify(auth_manager=oauth_manager)
            
            # Test the connection
            sp.current_user()
            
            logger.info("Successfully authenticated with Spotify")
            return sp
            
        except Exception as e:
            logger.error(f"Failed to initialize Spotify client: {e}")
            raise
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get current user's information
        
        Returns:
            Dict[str, Any]: User information including display name, email, etc.
        """
        try:
            user = self.sp.current_user()
            
            user_info = {
                'id': user.get('id'),
                'display_name': user.get('display_name'),
                'email': user.get('email'),
                'country': user.get('country'),
                'product': user.get('product'),  # premium, free, etc.
                'followers': user.get('followers', {}).get('total', 0),
                'images': user.get('images', [])
            }
            
            logger.info(f"Retrieved user info for: {user_info['display_name']}")
            return user_info
            
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            raise
    
    def print_user_info(self) -> None:
        """Print user information in a formatted way"""
        try:
            user_info = self.get_user_info()
            
            print("\n" + "="*50)
            print("🎵 SPOTIFY CONNECTION SUCCESSFUL 🎵")
            print("="*50)
            print(f"👤 Display Name: {user_info['display_name']}")
            print(f"📧 Email: {user_info['email']}")
            print(f"🌍 Country: {user_info['country']}")
            print(f"💎 Subscription: {user_info['product'].title()}")
            print(f"👥 Followers: {user_info['followers']}")
            
            if user_info['images']:
                print(f"🖼️  Profile Image: {user_info['images'][0]['url']}")
            
            print("="*50)
            print("✅ Ready to provide music recommendations!")
            print("="*50 + "\n")
            
        except Exception as e:
            logger.error(f"Failed to print user info: {e}")
            print(f"❌ Error displaying user information: {e}")
    
    def test_connection(self) -> bool:
        """
        Test the Spotify connection
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            # Try to get current user
            user = self.sp.current_user()
            if user and user.get('id'):
                logger.info("Spotify connection test successful")
                return True
            else:
                logger.error("Spotify connection test failed - no user data")
                return False
                
        except Exception as e:
            logger.error(f"Spotify connection test failed: {e}")
            return False
    
    def get_recent_tracks(self, limit: int = 10) -> list:
        """
        Get user's recently played tracks
        
        Args:
            limit (int): Number of tracks to retrieve (max 50)
            
        Returns:
            list: List of recently played tracks
        """
        try:
            # Validate limit
            if limit > 50:
                logger.warning("Limiting recent tracks to maximum of 50")
                limit = 50
            
            # Get tracks from Spotify
            recent_tracks = self.sp.current_user_recently_played(limit=limit)
            tracks = []
            
            # Process tracks
            for item in recent_tracks['items']:
                track = item['track']
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'played_at': item['played_at']
                })
            
            logger.info(f"Retrieved {len(tracks)} recent tracks")
            return tracks
            
        except Exception as e:
            logger.error(f"Failed to get recent tracks: {e}")
            return []
    
    def get_top_artists(self, limit: int = 10, time_range: str = 'medium_term') -> list:
        """
        Get user's top artists
        
        Args:
            limit (int): Number of artists to retrieve (max 50)
            time_range (str): Time range ('short_term', 'medium_term', 'long_term')
            
        Returns:
            list: List of top artists
        """
        try:
            top_artists = self.sp.current_user_top_artists(
                limit=limit, 
                time_range=time_range
            )
            
            artists = []
            for artist in top_artists['items']:
                artists.append({
                    'name': artist['name'],
                    'genres': artist['genres'],
                    'popularity': artist['popularity'],
                    'followers': artist['followers']['total']
                })
            
            logger.info(f"Retrieved {len(artists)} top artists")
            return artists
            
        except Exception as e:
            logger.error(f"Failed to get top artists: {e}")
            return []


def main():
    """Main function to test Spotify client"""
    try:
        print("🎵 Initializing Spotify Agent...")
        
        # Create Spotify client
        client = SpotifyClient()
        
        # Test connection
        if client.test_connection():
            # Print user information
            client.print_user_info()
            
            # Show some recent tracks
            print("📊 Recent Listening Activity:")
            recent_tracks = client.get_recent_tracks(limit=10)
            for i, track in enumerate(recent_tracks, 1):
                print(f"  {i}. {track['name']} - {track['artist']}")
            
            print("\n🎤 Top Artists (Last 6 months):")
            top_artists = client.get_top_artists(limit=10, time_range='medium_term')
            for i, artist in enumerate(top_artists, 1):
                print(f"  {i}. {artist['name']} ({', '.join(artist['genres'][:2])})")
            
        else:
            print("❌ Failed to connect to Spotify")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease ensure your .env file contains:")
        print("  - SPOTIFY_CLIENT_ID")
        print("  - SPOTIFY_CLIENT_SECRET")
        print("  - SPOTIFY_REDIRECT_URI (optional)")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        logger.error(f"Unexpected error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 