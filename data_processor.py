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
            
            # Process and clean all data
            self.processed_data = self._process_all_data()
            
            logger.info("All data loaded and processed successfully")
            return self.processed_data
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
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
    
    def _process_all_data(self) -> Dict[str, Any]:
        """
        Process all loaded data and create comprehensive analysis
        
        Returns:
            Dictionary containing processed and analyzed data
        """
        logger.info("Processing all data...")
        
        processed_data = {
            'streaming_history': self.streaming_history,
            'sound_capsule': self.sound_capsule,
            'library': self.library,
            'analysis': self._analyze_data(),
            'duplicates': self._detect_duplicates(),
            'summary': self._generate_summary()
        }
        
        return processed_data
    
    def _analyze_data(self) -> Dict[str, Any]:
        """
        Analyze the loaded data for patterns and insights
        
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'time_periods': self._analyze_time_periods(),
            'top_artists': self._analyze_top_artists(),
            'top_tracks': self._analyze_top_tracks(),
            'genres': self._analyze_genres(),
            'listening_patterns': self._analyze_listening_patterns(),
            'engagement_metrics': self._analyze_engagement()
        }
        
        return analysis
    
    def _analyze_time_periods(self) -> Dict[str, Any]:
        """
        Analyze listening patterns across different time periods
        
        Returns:
            Time period analysis
        """
        if not self.streaming_history:
            return {}
        
        # Group by month
        monthly_stats = defaultdict(lambda: {
            'count': 0,
            'total_seconds': 0,
            'artists': Counter(),
            'tracks': Counter(),
            'avg_session_length': 0
        })
        
        for record in self.streaming_history:
            month_key = record['timestamp'].strftime("%Y-%m")
            monthly_stats[month_key]['count'] += 1
            monthly_stats[month_key]['total_seconds'] += record['secondsPlayed']
            monthly_stats[month_key]['artists'][record['artistName']] += 1
            monthly_stats[month_key]['tracks'][record['trackName']] += 1
        
        # Calculate averages
        for month in monthly_stats:
            count = monthly_stats[month]['count']
            if count > 0:
                monthly_stats[month]['avg_session_length'] = monthly_stats[month]['total_seconds'] / count
        
        return dict(monthly_stats)
    
    def _analyze_top_artists(self) -> Dict[str, Any]:
        """
        Analyze top artists across all data sources
        
        Returns:
            Top artists analysis
        """
        artist_stats = defaultdict(lambda: {
            'stream_count': 0,
            'total_seconds': 0,
            'tracks': set(),
            'avg_engagement': 0
        })
        
        # From streaming history
        for record in self.streaming_history:
            artist = record['artistName']
            artist_stats[artist]['stream_count'] += 1
            artist_stats[artist]['total_seconds'] += record['secondsPlayed']
            artist_stats[artist]['tracks'].add(record['trackName'])
        
        # From sound capsule
        for stat in self.sound_capsule.get('stats', []):
            for artist in stat.get('topArtists', []):
                artist_name = artist['name']
                artist_stats[artist_name]['stream_count'] += artist.get('streamCount', 0)
                artist_stats[artist_name]['total_seconds'] += artist.get('secondsPlayed', 0)
        
        # Calculate engagement metrics
        for artist in artist_stats:
            if artist_stats[artist]['stream_count'] > 0:
                artist_stats[artist]['avg_engagement'] = artist_stats[artist]['total_seconds'] / artist_stats[artist]['stream_count']
                artist_stats[artist]['tracks'] = list(artist_stats[artist]['tracks'])
        
        # Sort by total seconds
        sorted_artists = sorted(artist_stats.items(), key=lambda x: x[1]['total_seconds'], reverse=True)
        
        return {
            'by_total_time': sorted_artists[:50],
            'by_stream_count': sorted(artist_stats.items(), key=lambda x: x[1]['stream_count'], reverse=True)[:50],
            'by_engagement': sorted(artist_stats.items(), key=lambda x: x[1]['avg_engagement'], reverse=True)[:50]
        }
    
    def _analyze_top_tracks(self) -> Dict[str, Any]:
        """
        Analyze top tracks across all data sources
        
        Returns:
            Top tracks analysis
        """
        track_stats = defaultdict(lambda: {
            'stream_count': 0,
            'total_seconds': 0,
            'artists': set(),
            'avg_engagement': 0
        })
        
        # From streaming history
        for record in self.streaming_history:
            track = record['trackName']
            track_stats[track]['stream_count'] += 1
            track_stats[track]['total_seconds'] += record['secondsPlayed']
            track_stats[track]['artists'].add(record['artistName'])
        
        # From sound capsule
        for stat in self.sound_capsule.get('stats', []):
            for track in stat.get('topTracks', []):
                track_name = track['name']
                track_stats[track_name]['stream_count'] += track.get('streamCount', 0)
                track_stats[track_name]['total_seconds'] += track.get('secondsPlayed', 0)
        
        # Calculate engagement metrics
        for track in track_stats:
            if track_stats[track]['stream_count'] > 0:
                track_stats[track]['avg_engagement'] = track_stats[track]['total_seconds'] / track_stats[track]['stream_count']
                track_stats[track]['artists'] = list(track_stats[track]['artists'])
        
        # Sort by total seconds
        sorted_tracks = sorted(track_stats.items(), key=lambda x: x[1]['total_seconds'], reverse=True)
        
        return {
            'by_total_time': sorted_tracks[:50],
            'by_stream_count': sorted(track_stats.items(), key=lambda x: x[1]['stream_count'], reverse=True)[:50],
            'by_engagement': sorted(track_stats.items(), key=lambda x: x[1]['avg_engagement'], reverse=True)[:50]
        }
    
    def _analyze_genres(self) -> Dict[str, Any]:
        """
        Analyze genre preferences from sound capsule data
        
        Returns:
            Genre analysis
        """
        genre_stats = defaultdict(lambda: {
            'stream_count': 0,
            'total_seconds': 0,
            'months_active': set()
        })
        
        # From sound capsule
        for stat in self.sound_capsule.get('stats', []):
            month = stat.get('date', '')
            for genre in stat.get('topGenres', []):
                genre_name = genre['name']
                genre_stats[genre_name]['stream_count'] += genre.get('streamCount', 0)
                genre_stats[genre_name]['total_seconds'] += genre.get('secondsPlayed', 0)
                if month:
                    genre_stats[genre_name]['months_active'].add(month)
        
        # Convert sets to lists for JSON serialization
        for genre in genre_stats:
            genre_stats[genre]['months_active'] = list(genre_stats[genre]['months_active'])
        
        # Sort by total seconds
        sorted_genres = sorted(genre_stats.items(), key=lambda x: x[1]['total_seconds'], reverse=True)
        
        return {
            'by_total_time': sorted_genres[:20],
            'by_stream_count': sorted(genre_stats.items(), key=lambda x: x[1]['stream_count'], reverse=True)[:20],
            'by_consistency': sorted(genre_stats.items(), key=lambda x: len(x[1]['months_active']), reverse=True)[:20]
        }
    
    def _analyze_listening_patterns(self) -> Dict[str, Any]:
        """
        Analyze listening patterns and behaviors
        
        Returns:
            Listening patterns analysis
        """
        if not self.streaming_history:
            return {}
        
        patterns = {
            'time_of_day': defaultdict(int),
            'day_of_week': defaultdict(int),
            'session_lengths': [],
            'skip_rates': defaultdict(int)
        }
        
        for record in self.streaming_history:
            timestamp = record['timestamp']
            
            # Time of day analysis
            hour = timestamp.hour
            if 6 <= hour < 12:
                patterns['time_of_day']['morning'] += 1
            elif 12 <= hour < 17:
                patterns['time_of_day']['afternoon'] += 1
            elif 17 <= hour < 22:
                patterns['time_of_day']['evening'] += 1
            else:
                patterns['time_of_day']['night'] += 1
            
            # Day of week analysis
            day_name = timestamp.strftime('%A').lower()
            patterns['day_of_week'][day_name] += 1
            
            # Session length analysis
            patterns['session_lengths'].append(record['secondsPlayed'])
            
            # Skip rate analysis (tracks played for less than 30 seconds)
            if record['secondsPlayed'] < 30:
                patterns['skip_rates'][record['artistName']] += 1
        
        # Calculate averages
        if patterns['session_lengths']:
            patterns['avg_session_length'] = sum(patterns['session_lengths']) / len(patterns['session_lengths'])
        
        return dict(patterns)
    
    def _analyze_engagement(self) -> Dict[str, Any]:
        """
        Analyze user engagement metrics
        
        Returns:
            Engagement analysis
        """
        if not self.streaming_history:
            return {}
        
        engagement = {
            'total_streams': len(self.streaming_history),
            'total_seconds': sum(record['secondsPlayed'] for record in self.streaming_history),
            'unique_artists': len(set(record['artistName'] for record in self.streaming_history)),
            'unique_tracks': len(set(record['trackName'] for record in self.streaming_history)),
            'avg_stream_length': 0,
            'completion_rates': {}
        }
        
        # Calculate average stream length
        if engagement['total_streams'] > 0:
            engagement['avg_stream_length'] = engagement['total_seconds'] / engagement['total_streams']
        
        # Calculate completion rates by artist
        artist_completions = defaultdict(lambda: {'total': 0, 'completed': 0})
        
        for record in self.streaming_history:
            artist = record['artistName']
            artist_completions[artist]['total'] += 1
            # Consider a track "completed" if played for more than 60% of typical length (3 minutes)
            if record['secondsPlayed'] > 180:
                artist_completions[artist]['completed'] += 1
        
        for artist, stats in artist_completions.items():
            if stats['total'] > 0:
                engagement['completion_rates'][artist] = stats['completed'] / stats['total']
        
        return engagement
    
    def _detect_duplicates(self) -> Dict[str, Any]:
        """
        Detect and analyze duplicate entries across data sources
        
        Returns:
            Duplicate analysis
        """
        duplicates = {
            'streaming_history': self._find_streaming_duplicates(),
            'cross_source': self._find_cross_source_duplicates()
        }
        
        return duplicates
    
    def _find_streaming_duplicates(self) -> Dict[str, Any]:
        """
        Find duplicate entries within streaming history
        
        Returns:
            Duplicate analysis for streaming history
        """
        if not self.streaming_history:
            return {}
        
        # Group by artist + track
        track_groups = defaultdict(list)
        for i, record in enumerate(self.streaming_history):
            key = f"{record['artistName']} - {record['trackName']}"
            track_groups[key].append(i)
        
        # Find duplicates
        duplicates = {
            'exact_duplicates': [],
            'similar_tracks': [],
            'repeated_listens': []
        }
        
        for key, indices in track_groups.items():
            if len(indices) > 1:
                # Check for exact duplicates (same timestamp and duration)
                exact_dups = []
                for i in indices:
                    for j in indices:
                        if i != j:
                            record1 = self.streaming_history[i]
                            record2 = self.streaming_history[j]
                            if (record1['endTime'] == record2['endTime'] and 
                                record1['msPlayed'] == record2['msPlayed']):
                                exact_dups.append((i, j))
                
                if exact_dups:
                    duplicates['exact_duplicates'].extend(exact_dups)
                else:
                    duplicates['repeated_listens'].append({
                        'track': key,
                        'count': len(indices),
                        'indices': indices
                    })
        
        return duplicates
    
    def _find_cross_source_duplicates(self) -> Dict[str, Any]:
        """
        Find duplicate entries across different data sources
        
        Returns:
            Cross-source duplicate analysis
        """
        cross_duplicates = {
            'streaming_vs_capsule': [],
            'streaming_vs_library': [],
            'capsule_vs_library': []
        }
        
        # Compare streaming history vs sound capsule
        streaming_tracks = set()
        for record in self.streaming_history:
            streaming_tracks.add(f"{record['artistName']} - {record['trackName']}")
        
        capsule_tracks = set()
        for stat in self.sound_capsule.get('stats', []):
            for track in stat.get('topTracks', []):
                capsule_tracks.add(track['name'])
        
        # Find overlaps
        for track in streaming_tracks:
            track_name = track.split(' - ', 1)[1] if ' - ' in track else track
            if track_name in capsule_tracks:
                cross_duplicates['streaming_vs_capsule'].append(track)
        
        # Compare with library
        library_tracks = set()
        for track in self.library.get('tracks', []):
            library_tracks.add(f"{track['artist']} - {track['track']}")
        
        for track in streaming_tracks:
            if track in library_tracks:
                cross_duplicates['streaming_vs_library'].append(track)
        
        return cross_duplicates
    
    def _generate_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of all data
        
        Returns:
            Data summary
        """
        summary = {
            'data_sources': {
                'streaming_history': {
                    'records': len(self.streaming_history),
                    'time_span': self._get_time_span(self.streaming_history),
                    'unique_artists': len(set(record['artistName'] for record in self.streaming_history)) if self.streaming_history else 0,
                    'unique_tracks': len(set(record['trackName'] for record in self.streaming_history)) if self.streaming_history else 0
                },
                'sound_capsule': {
                    'months': len(self.sound_capsule.get('stats', [])),
                    'highlights': len(self.sound_capsule.get('highlights', []))
                },
                'library': {
                    'tracks': len(self.library.get('tracks', [])),
                    'albums': len(self.library.get('albums', [])),
                    'shows': len(self.library.get('shows', [])),
                    'episodes': len(self.library.get('episodes', []))
                }
            },
            'total_listening_time': sum(record['secondsPlayed'] for record in self.streaming_history) if self.streaming_history else 0,
            'processing_timestamp': datetime.now().isoformat()
        }
        
        return summary
    
    def _get_time_span(self, records: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Get the time span of streaming history records
        
        Args:
            records: List of streaming records
            
        Returns:
            Dictionary with start and end dates
        """
        if not records:
            return {}
        
        timestamps = [record['timestamp'] for record in records]
        return {
            'start': min(timestamps).strftime("%Y-%m-%d"),
            'end': max(timestamps).strftime("%Y-%m-%d")
        }
    
    def get_processed_data(self) -> Dict[str, Any]:
        """
        Get the processed data
        
        Returns:
            Processed data dictionary
        """
        return self.processed_data
    
    def export_analysis(self, output_file: str = "data_analysis.json") -> None:
        """
        Export the processed data and analysis to a JSON file
        
        Args:
            output_file: Output file path
        """
        try:
            # Convert sets to lists for JSON serialization
            export_data = self._prepare_for_export(self.processed_data)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Analysis exported to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting analysis: {e}")
            raise
    
    def _prepare_for_export(self, data: Any) -> Any:
        """
        Prepare data for JSON export by converting non-serializable types
        
        Args:
            data: Data to prepare
            
        Returns:
            JSON-serializable data
        """
        if isinstance(data, dict):
            return {k: self._prepare_for_export(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._prepare_for_export(item) for item in data]
        elif isinstance(data, set):
            return list(data)
        elif isinstance(data, datetime):
            return data.isoformat()
        else:
            return data


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
    
    # Load and process data
    processor = DataProcessor()
    data = processor.load_all_data()
    
    # Print summary
    summary = data['summary']
    print(f"\n📊 Data Processing Summary:")
    print(f"Streaming History: {summary['data_sources']['streaming_history']['records']} records")
    print(f"Sound Capsule: {summary['data_sources']['sound_capsule']['months']} months")
    print(f"Library: {summary['data_sources']['library']['tracks']} tracks, {summary['data_sources']['library']['albums']} albums")
    print(f"Total Listening Time: {summary['total_listening_time'] / 3600:.1f} hours")
    
    # Export analysis
    processor.export_analysis()
