"""
Data Processor for Spotify Agent
Handles JSON file loading, parsing, data cleaning, and normalization
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import logging

# Set up logging
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Handles loading, cleaning, and processing of Spotify JSON data files
    """
    
    def __init__(self, data_folder: str = "data"):
        """
        Initialize the data processor
        
        Args:
            data_folder: Path to the folder containing JSON data files
        """
        self.data_folder = data_folder
        self.streaming_history = []
        self.sound_capsule = {}
        self.library = {}
        self.processed_data = {}
    
    def load_all_data(self) -> Dict[str, Any]:
        """
        Load all JSON files from the data folder
        
        Returns:
            Dictionary containing all loaded and processed data
        """
        logger.info("Loading all JSON data files...")
        
        try:
            # Load streaming history
            self.streaming_history = self._load_streaming_history()
            logger.info(f"Loaded {len(self.streaming_history)} streaming history records")
            
            # Load sound capsule
            self.sound_capsule = self._load_sound_capsule()
            logger.info(f"Loaded sound capsule with {len(self.sound_capsule.get('stats', []))} monthly stats")
            
            # Load library
            self.library = self._load_library()
            logger.info(f"Loaded library with {len(self.library.get('tracks', []))} tracks and {len(self.library.get('albums', []))} albums")
            
            logger.info("All data loaded successfully")
            return {
                'streaming_history': self.streaming_history,
                'sound_capsule': self.sound_capsule,
                'library': self.library
            }
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def load_2024_chunk(self, limit: int = 30) -> Dict[str, str]:
        """
        Load and format 2024 listening data for GPT processing.
        Only includes essential data: track names, artist names, and genres.
        
        Args:
            limit: Maximum number of items to include per category
            
        Returns:
            Dictionary with formatted strings for recent tracks, top artists, and genres
        """
        logger.info("Loading 2024 chunk for GPT processing...")
        
        try:
            # Get 2024 data
            data_2024 = self._get_2024_essential_data()
            
            # Format each component
            formatted_data = {
                'recent_tracks': self._format_2024_tracks_simple(data_2024['tracks'], limit),
                'top_artists': self._format_2024_artists_simple(data_2024['artists'], limit),
                'top_genres': self._format_2024_genres_simple(data_2024['genres'], limit)
            }
            
            return formatted_data
            
        except Exception as e:
            logger.error(f"Error loading 2024 chunk: {e}")
            return {'recent_tracks': '', 'top_artists': '', 'top_genres': ''}
    
    def _get_2024_essential_data(self) -> Dict[str, List[str]]:
        """
        Extract essential 2024 data from all sources
        """
        data_2024 = {
            'tracks': [],
            'artists': [],
            'genres': []
        }
        
        # Get tracks and artists from streaming history
        if self.streaming_history:
            logger.info(f"Processing {len(self.streaming_history)} streaming history records")
            records_2024 = 0
            for record in self.streaming_history:
                if record['timestamp'].year == 2024:
                    records_2024 += 1
                    track_str = f"{record['trackName']} by {record['artistName']}"
                    if track_str not in data_2024['tracks']:
                        data_2024['tracks'].append(track_str)
                    if record['artistName'] not in data_2024['artists']:
                        data_2024['artists'].append(record['artistName'])
            logger.info(f"Found {records_2024} records from 2024")
        
        # Get genres from sound capsule
        if self.sound_capsule.get('stats'):
            logger.info(f"Processing {len(self.sound_capsule['stats'])} monthly stats")
            months_2024 = 0
            for stat in self.sound_capsule['stats']:
                # Assuming date format is YYYY-MM
                if stat.get('date', '').startswith('2024'):
                    months_2024 += 1
                    for genre in stat.get('topGenres', []):
                        genre_name = genre['name']
                        if genre_name not in data_2024['genres']:
                            data_2024['genres'].append(genre_name)
            logger.info(f"Found {months_2024} months from 2024")
        
        logger.info(f"Extracted {len(data_2024['tracks'])} unique tracks, {len(data_2024['artists'])} unique artists, and {len(data_2024['genres'])} unique genres from 2024")
        return data_2024
    
    def _format_2024_tracks_simple(self, tracks: List[str], limit: int) -> str:
        """Format tracks as comma-separated string"""
        top_tracks = tracks[:limit] if limit > 0 else tracks
        return ", ".join(top_tracks)
    
    def _format_2024_artists_simple(self, artists: List[str], limit: int) -> str:
        """Format artists as comma-separated string"""
        top_artists = artists[:limit] if limit > 0 else artists
        return ", ".join(top_artists)
    
    def _format_2024_genres_simple(self, genres: List[str], limit: int) -> str:
        """Format genres as comma-separated string"""
        top_genres = genres[:limit] if limit > 0 else genres
        return ", ".join(top_genres)
    
    def _load_streaming_history(self) -> List[Dict[str, Any]]:
        """
        Load streaming history from JSON file
        
        Returns:
            List of streaming history records
        """
        file_path = os.path.join(self.data_folder, "StreamingHistory_music_0.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Streaming history file not found: {file_path}")
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clean and validate each record
            cleaned_data = []
            for record in data:
                cleaned_record = self._clean_streaming_record(record)
                if cleaned_record:
                    cleaned_data.append(cleaned_record)
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error loading streaming history: {e}")
            return []
    
    def _load_sound_capsule(self) -> Dict[str, Any]:
        """
        Load sound capsule data from JSON file
        
        Returns:
            Sound capsule data dictionary
        """
        file_path = os.path.join(self.data_folder, "YourSoundCapsule.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Sound capsule file not found: {file_path}")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clean and validate the data
            return self._clean_sound_capsule(data)
            
        except Exception as e:
            logger.error(f"Error loading sound capsule: {e}")
            return {}
    
    def _load_library(self) -> Dict[str, Any]:
        """
        Load library data from JSON file
        
        Returns:
            Library data dictionary
        """
        file_path = os.path.join(self.data_folder, "YourLibrary.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Library file not found: {file_path}")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clean and validate the data
            return self._clean_library(data)
            
        except Exception as e:
            logger.error(f"Error loading library: {e}")
            return {}
    
    def _clean_streaming_record(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Clean and validate a streaming history record
        
        Args:
            record: Raw streaming record
            
        Returns:
            Cleaned record or None if invalid
        """
        try:
            # Extract and validate required fields
            end_time = record.get('endTime')
            artist_name = record.get('artistName', '').strip()
            track_name = record.get('trackName', '').strip()
            ms_played = record.get('msPlayed', 0)
            
            # Skip records with missing essential data
            if not end_time or not artist_name or not track_name:
                return None
            
            # Parse and validate timestamp
            try:
                timestamp = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            except ValueError:
                logger.warning(f"Invalid timestamp format: {end_time}")
                return None
            
            # Clean artist and track names
            artist_name = self._normalize_artist_name(artist_name)
            track_name = self._normalize_track_name(track_name)
            
            # Skip if names are too short after cleaning
            if len(artist_name) < 1 or len(track_name) < 1:
                return None
            
            return {
                'endTime': end_time,
                'timestamp': timestamp,
                'artistName': artist_name,
                'trackName': track_name,
                'msPlayed': ms_played,
                'secondsPlayed': ms_played / 1000 if ms_played > 0 else 0
            }
            
        except Exception as e:
            logger.warning(f"Error cleaning streaming record: {e}")
            return None
    
    def _clean_sound_capsule(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and validate sound capsule data
        
        Args:
            data: Raw sound capsule data
            
        Returns:
            Cleaned sound capsule data
        """
        cleaned_data = {
            'stats': [],
            'highlights': data.get('highlights', [])
        }
        
        # Clean monthly stats
        for stat in data.get('stats', []):
            cleaned_stat = self._clean_monthly_stat(stat)
            if cleaned_stat:
                cleaned_data['stats'].append(cleaned_stat)
        
        return cleaned_data
    
    def _clean_monthly_stat(self, stat: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Clean a monthly stat record
        
        Args:
            stat: Raw monthly stat
            
        Returns:
            Cleaned monthly stat or None if invalid
        """
        try:
            # Validate required fields
            date = stat.get('date')
            if not date:
                return None
            
            cleaned_stat = {
                'date': date,
                'streamCount': stat.get('streamCount', 0),
                'secondsPlayed': stat.get('secondsPlayed', 0),
                'topTracks': [],
                'topArtists': [],
                'topGenres': [],
                'timeOfDayStats': stat.get('timeOfDayStats', [])
            }
            
            # Clean top tracks
            for track in stat.get('topTracks', []):
                cleaned_track = self._clean_top_track(track)
                if cleaned_track:
                    cleaned_stat['topTracks'].append(cleaned_track)
            
            # Clean top artists
            for artist in stat.get('topArtists', []):
                cleaned_artist = self._clean_top_artist(artist)
                if cleaned_artist:
                    cleaned_stat['topArtists'].append(cleaned_artist)
            
            # Clean top genres
            for genre in stat.get('topGenres', []):
                cleaned_genre = self._clean_top_genre(genre)
                if cleaned_genre:
                    cleaned_stat['topGenres'].append(cleaned_genre)
            
            return cleaned_stat
            
        except Exception as e:
            logger.warning(f"Error cleaning monthly stat: {e}")
            return None
    
    def _clean_top_track(self, track: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Clean a top track record
        
        Args:
            track: Raw top track data
            
        Returns:
            Cleaned top track or None if invalid
        """
        try:
            name = track.get('name', '').strip()
            if not name:
                return None
            
            return {
                'name': self._normalize_track_name(name),
                'streamCount': track.get('streamCount', 0),
                'secondsPlayed': track.get('secondsPlayed', 0)
            }
        except Exception as e:
            logger.warning(f"Error cleaning top track: {e}")
            return None
    
    def _clean_top_artist(self, artist: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Clean a top artist record
        
        Args:
            artist: Raw top artist data
            
        Returns:
            Cleaned top artist or None if invalid
        """
        try:
            name = artist.get('name', '').strip()
            if not name:
                return None
            
            return {
                'name': self._normalize_artist_name(name),
                'streamCount': artist.get('streamCount', 0),
                'secondsPlayed': artist.get('secondsPlayed', 0)
            }
        except Exception as e:
            logger.warning(f"Error cleaning top artist: {e}")
            return None
    
    def _clean_top_genre(self, genre: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Clean a top genre record
        
        Args:
            genre: Raw top genre data
            
        Returns:
            Cleaned top genre or None if invalid
        """
        try:
            name = genre.get('name', '').strip().lower()
            if not name:
                return None
            
            return {
                'name': name,
                'streamCount': genre.get('streamCount', 0),
                'secondsPlayed': genre.get('secondsPlayed', 0)
            }
        except Exception as e:
            logger.warning(f"Error cleaning top genre: {e}")
            return None
    
    def _clean_library(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and validate library data
        
        Args:
            data: Raw library data
            
        Returns:
            Cleaned library data
        """
        cleaned_data = {
            'tracks': [],
            'albums': [],
            'shows': data.get('shows', []),
            'episodes': data.get('episodes', [])
        }
        
        # Clean tracks
        for track in data.get('tracks', []):
            cleaned_track = self._clean_library_track(track)
            if cleaned_track:
                cleaned_data['tracks'].append(cleaned_track)
        
        # Clean albums
        for album in data.get('albums', []):
            cleaned_album = self._clean_library_album(album)
            if cleaned_album:
                cleaned_data['albums'].append(cleaned_album)
        
        return cleaned_data
    
    def _clean_library_track(self, track: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Clean a library track record
        
        Args:
            track: Raw library track data
            
        Returns:
            Cleaned library track or None if invalid
        """
        try:
            artist = track.get('artist', '').strip()
            album = track.get('album', '').strip()
            track_name = track.get('track', '').strip()
            uri = track.get('uri', '').strip()
            
            if not artist or not track_name:
                return None
            
            return {
                'artist': self._normalize_artist_name(artist),
                'album': self._normalize_album_name(album),
                'track': self._normalize_track_name(track_name),
                'uri': uri
            }
        except Exception as e:
            logger.warning(f"Error cleaning library track: {e}")
            return None
    
    def _clean_library_album(self, album: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Clean a library album record
        
        Args:
            album: Raw library album data
            
        Returns:
            Cleaned library album or None if invalid
        """
        try:
            artist = album.get('artist', '').strip()
            album_name = album.get('album', '').strip()
            uri = album.get('uri', '').strip()
            
            if not artist or not album_name:
                return None
            
            return {
                'artist': self._normalize_artist_name(artist),
                'album': self._normalize_album_name(album_name),
                'uri': uri
            }
        except Exception as e:
            logger.warning(f"Error cleaning library album: {e}")
            return None
    
    def _normalize_artist_name(self, name: str) -> str:
        """
        Normalize artist name by removing common artifacts
        
        Args:
            name: Raw artist name
            
        Returns:
            Normalized artist name
        """
        if not name:
            return ""
        
        # Remove common prefixes/suffixes
        name = re.sub(r'^\s*feat\.?\s*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'^\s*ft\.?\s*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'^\s*featuring\s*', '', name, flags=re.IGNORECASE)
        
        # Remove parentheses content
        name = re.sub(r'\s*\([^)]*\)\s*', ' ', name)
        
        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def _normalize_track_name(self, name: str) -> str:
        """
        Normalize track name by removing common artifacts
        
        Args:
            name: Raw track name
            
        Returns:
            Normalized track name
        """
        if not name:
            return ""
        
        # Remove common suffixes
        name = re.sub(r'\s*\([^)]*\)\s*$', '', name)  # Remove trailing parentheses
        name = re.sub(r'\s*-\s*Remix\s*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*-\s*Mix\s*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*\([^)]*Mix[^)]*\)\s*', '', name, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def _normalize_album_name(self, name: str) -> str:
        """
        Normalize album name by removing common artifacts
        
        Args:
            name: Raw album name
            
        Returns:
            Normalized album name
        """
        if not name:
            return ""
        
        # Remove common suffixes
        name = re.sub(r'\s*-\s*Single\s*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*\([^)]*\)\s*$', '', name)  # Remove trailing parentheses
        
        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name


# Convenience function for quick data loading
def load_spotify_data(data_folder: str = "data") -> Dict[str, Any]:
    """
    Convenience function to quickly load and process all Spotify data
    
    Args:
        data_folder: Path to the data folder
        
    Returns:
        Processed data dictionary
    """
    processor = DataProcessor(data_folder)
    return processor.load_all_data()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Test the 2024 data loading
    processor = DataProcessor()
    processor.load_all_data()
    
    # First get all data without limits to see total counts
    all_data = processor.load_2024_chunk(limit=0)
    
    # Count total items
    track_count = len(all_data['recent_tracks'].split(", ")) if all_data['recent_tracks'] else 0
    artist_count = len(all_data['top_artists'].split(", ")) if all_data['top_artists'] else 0
    genre_count = len(all_data['top_genres'].split(", ")) if all_data['top_genres'] else 0
    
    print("\n📊 Total Available 2024 Data:")
    print(f"Total Unique Tracks: {track_count}")
    print(f"Total Unique Artists: {artist_count}")
    print(f"Total Unique Genres: {genre_count}")
    
    # Now get data with higher limit
    data_2024 = processor.load_2024_chunk(limit=30)
    
    print("\n🎵 2024 Listening Data for GPT (Top 30 each):")
    print(f"\nRecent Tracks:")
    tracks = data_2024['recent_tracks'].split(", ")
    for i, track in enumerate(tracks, 1):
        print(f"{i}. {track}")
    
    print(f"\nTop Artists:")
    artists = data_2024['top_artists'].split(", ")
    for i, artist in enumerate(artists, 1):
        print(f"{i}. {artist}")
    
    print(f"\nTop Genres:")
    genres = data_2024['top_genres'].split(", ")
    for i, genre in enumerate(genres, 1):
        print(f"{i}. {genre}")