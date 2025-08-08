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
            self.scopes = os.getenv('SPOTIFY_SCOPES', 'user-read-private user-read-email user-read-recently-played user-top-read playlist-modify-public playlist-modify-private')
            
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
    
    def create_recommendation_playlist_from_text(self, gpt_text: str) -> Dict[str, Any]:
        """
        Create a Spotify playlist from GPT recommendation text
        
        Args:
            gpt_text (str): GPT response containing song and artist recommendations
            
        Returns:
            Dict[str, Any]: Playlist metadata including name, URL, and track count
        """
        import re
        from datetime import datetime
        
        try:
            log_function_entry(logger, "create_recommendation_playlist_from_text")
            logger.info(f"Creating playlist from GPT text: {gpt_text[:100]}...")
            
            # Parse track information from GPT text
            tracks_info = self._parse_tracks_from_text(gpt_text)
            if not tracks_info:
                logger.warning("No tracks found in GPT text")
                return {
                    'success': False,
                    'error': 'No tracks found in the recommendation text',
                    'tracks_added': 0
                }
            
            logger.info(f"Parsed {len(tracks_info)} tracks from text")
            
            # Get current user info
            user = self.sp.current_user()
            user_id = user['id']
            
            # Create playlist name with current date
            playlist_name = f"AI Recommendations - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Create the playlist
            playlist = self.sp.user_playlist_create(
                user=user_id,
                name=playlist_name,
                public=False,  # Private by default
                description="AI-generated music recommendations from Spotify Agent"
            )
            
            logger.info(f"Created playlist: {playlist_name} (ID: {playlist['id']})")
            
            # Search for tracks and collect URIs
            track_uris = []
            successful_tracks = []
            failed_tracks = []
            
            for track_info in tracks_info:
                try:
                    # Search for the track
                    query = f"track:{track_info['track']} artist:{track_info['artist']}"
                    results = self.sp.search(q=query, type='track', limit=1)
                    
                    if results['tracks']['items']:
                        track = results['tracks']['items'][0]
                        track_uris.append(track['uri'])
                        successful_tracks.append({
                            'searched': f"{track_info['track']} by {track_info['artist']}",
                            'found': f"{track['name']} by {track['artists'][0]['name']}"
                        })
                        logger.debug(f"Found track: {track['name']} by {track['artists'][0]['name']}")
                    else:
                        failed_tracks.append(f"{track_info['track']} by {track_info['artist']}")
                        logger.warning(f"Track not found: {track_info['track']} by {track_info['artist']}")
                        
                except Exception as e:
                    failed_tracks.append(f"{track_info['track']} by {track_info['artist']}")
                    logger.error(f"Error searching for track {track_info['track']}: {e}")
            
            # Add tracks to playlist
            if track_uris:
                # Spotify allows max 100 tracks per request
                for i in range(0, len(track_uris), 100):
                    batch = track_uris[i:i+100]
                    self.sp.playlist_add_items(playlist['id'], batch)
                
                logger.info(f"Added {len(track_uris)} tracks to playlist {playlist_name}")
            
            # Log results
            log_data_summary(logger, "playlist_creation", {
                'total_tracks_parsed': len(tracks_info),
                'successful_tracks': len(successful_tracks),
                'failed_tracks': len(failed_tracks),
                'playlist_id': playlist['id']
            })
            
            result = {
                'success': True,
                'playlist_name': playlist_name,
                'playlist_url': playlist['external_urls']['spotify'],
                'playlist_id': playlist['id'],
                'tracks_added': len(track_uris),
                'total_tracks_parsed': len(tracks_info),
                'successful_tracks': successful_tracks,
                'failed_tracks': failed_tracks
            }
            
            log_function_exit(logger, "create_recommendation_playlist_from_text", 
                            f"Created playlist with {len(track_uris)} tracks", True)
            return result
            
        except Exception as e:
            log_error_with_context(logger, e, {
                'gpt_text_length': len(gpt_text) if gpt_text else 0
            }, "create_recommendation_playlist_from_text")
            log_function_exit(logger, "create_recommendation_playlist_from_text", None, False)
            return {
                'success': False,
                'error': str(e),
                'tracks_added': 0
            }
    
    def _parse_tracks_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Parse track and artist information from GPT recommendation text
        
        Args:
            text (str): Text containing track recommendations
            
        Returns:
            List[Dict[str, str]]: List of dictionaries with 'track' and 'artist' keys
        """
        import re
        
        tracks = []
        
        # Pattern to match various formats:
        # 1. "Song Name" by Artist Name
        # 2. **"Song Name" by Artist Name**
        # 3. 1. Song Name - Artist Name
        # 4. • Song Name by Artist Name
        patterns = [
            # Pattern 1: "Song Name" by Artist Name or **"Song Name" by Artist Name**
            r'(?:\*\*)?["\'""]([^"\'""]+)["\'""](?:\*\*)?\s+by\s+([^\n\-–—•*]+?)(?:\s*[\-–—]|\n|$)',
            # Pattern 2: Number. Song Name - Artist Name or • Song Name - Artist Name  
            r'(?:\d+\.|\•|\*)\s*([^-–—\n]+?)\s*[\-–—]\s*([^\n•*]+?)(?:\s*[\-–—]|\n|$)',
            # Pattern 3: Number. Song Name by Artist Name
            r'(?:\d+\.|\•|\*)\s*([^-–—\n]+?)\s+by\s+([^\n•*]+?)(?:\s*[\-–—]|\n|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                track_name = match[0].strip().strip('*').strip()
                artist_name = match[1].strip().strip('*').strip()
                
                # Clean up common artifacts
                track_name = re.sub(r'^[\d\.\)\]\}\-–—\s]+', '', track_name).strip()
                artist_name = re.sub(r'[\-–—\s]*\([^)]*\).*$', '', artist_name).strip()
                
                if track_name and artist_name and len(track_name) > 1 and len(artist_name) > 1:
                    # Avoid duplicates
                    track_key = f"{track_name.lower()}|{artist_name.lower()}"
                    if not any(f"{t['track'].lower()}|{t['artist'].lower()}" == track_key for t in tracks):
                        tracks.append({
                            'track': track_name,
                            'artist': artist_name
                        })
                        logger.debug(f"Parsed track: {track_name} by {artist_name}")
        
        logger.info(f"Parsed {len(tracks)} unique tracks from text")
        return tracks


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