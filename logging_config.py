#!/usr/bin/env python3
"""
Spotify Agent - Logging Configuration
Centralized logging setup for the entire application
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logging(log_level=logging.INFO):
    """
    Set up comprehensive logging for the Spotify Agent application
    
    Args:
        log_level: Logging level (default: INFO)
        
    Returns:
        tuple: (logger, log_file_path)
    """
    
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Generate log file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file_path = os.path.join(logs_dir, f"spotify_agent_{timestamp}.log")
    
    # Create simple text formatter
    log_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # File handler with rotation (max 10MB, keep 5 files)
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    
    # Console handler for important messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
    console_formatter = logging.Formatter(
        fmt='%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Reduce verbosity of external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('spotipy').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    
    # Create application-specific logger
    app_logger = logging.getLogger('spotify_agent')
    
    # Log startup information
    app_logger.info("=" * 80)
    app_logger.info("SPOTIFY AGENT APPLICATION STARTED")
    app_logger.info("=" * 80)
    app_logger.info(f"Log file: {log_file_path}")
    app_logger.info(f"Log level: {logging.getLevelName(log_level)}")
    app_logger.info(f"Python version: {os.sys.version}")
    app_logger.info(f"Working directory: {os.getcwd()}")
    app_logger.info("Logging system initialized successfully")
    
    return app_logger, log_file_path


def get_logger(name):
    """
    Get a logger instance for a specific module
    
    Args:
        name (str): Logger name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(f'spotify_agent.{name}')


def log_function_entry(logger, func_name, **kwargs):
    """
    Log function entry with parameters
    
    Args:
        logger: Logger instance
        func_name (str): Function name
        **kwargs: Function parameters to log
    """
    params = ", ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else "no parameters"
    logger.debug(f"ENTERING {func_name}({params})")


def log_function_exit(logger, func_name, result=None, success=True):
    """
    Log function exit with result
    
    Args:
        logger: Logger instance
        func_name (str): Function name
        result: Function result to log
        success (bool): Whether function completed successfully
    """
    status = "SUCCESS" if success else "FAILED"
    result_str = f" -> {result}" if result is not None else ""
    logger.debug(f"EXITING {func_name} [{status}]{result_str}")


def log_api_call(logger, api_name, endpoint, method="GET", params=None, response_status=None):
    """
    Log API call details
    
    Args:
        logger: Logger instance
        api_name (str): Name of the API (e.g., "Spotify", "OpenAI")
        endpoint (str): API endpoint
        method (str): HTTP method
        params: Request parameters
        response_status: Response status code
    """
    params_str = f" with params: {params}" if params else ""
    status_str = f" -> Status: {response_status}" if response_status else ""
    logger.info(f"API CALL [{api_name}] {method} {endpoint}{params_str}{status_str}")


def log_user_interaction(logger, action, details=None):
    """
    Log user interaction events
    
    Args:
        logger: Logger instance
        action (str): User action description
        details: Additional details about the interaction
    """
    details_str = f" - {details}" if details else ""
    logger.info(f"USER ACTION: {action}{details_str}")


def log_error_with_context(logger, error, context=None, function=None):
    """
    Log error with contextual information
    
    Args:
        logger: Logger instance
        error: Exception or error message
        context (dict): Additional context information
        function (str): Function where error occurred
    """
    function_str = f" in {function}" if function else ""
    context_str = f" | Context: {context}" if context else ""
    logger.error(f"ERROR{function_str}: {error}{context_str}")


def log_performance_metric(logger, operation, duration, details=None):
    """
    Log performance metrics
    
    Args:
        logger: Logger instance
        operation (str): Operation description
        duration (float): Duration in seconds
        details: Additional performance details
    """
    details_str = f" | {details}" if details else ""
    logger.info(f"PERFORMANCE: {operation} completed in {duration:.3f}s{details_str}")


def log_data_summary(logger, data_type, count, sample=None):
    """
    Log data summary information
    
    Args:
        logger: Logger instance
        data_type (str): Type of data (e.g., "tracks", "artists")
        count (int): Number of items
        sample: Sample of the data for logging
    """
    sample_str = f" | Sample: {sample}" if sample else ""
    logger.info(f"DATA SUMMARY: Retrieved {count} {data_type}{sample_str}")


class SpotifyAgentLoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter for Spotify Agent with additional context
    """
    
    def process(self, msg, kwargs):
        """Add session context to log messages"""
        session_id = self.extra.get('session_id', 'unknown')
        user_id = self.extra.get('user_id', 'unknown')
        return f"[Session:{session_id}|User:{user_id}] {msg}", kwargs


if __name__ == "__main__":
    # Test the logging system
    logger, log_file = setup_logging(logging.DEBUG)
    
    logger.info("Testing logging system...")
    log_function_entry(logger, "test_function", param1="value1", param2=42)
    log_api_call(logger, "Spotify", "/me", "GET", {"limit": 10}, 200)
    log_user_interaction(logger, "Started chat session", "User requested music recommendations")
    log_performance_metric(logger, "Spotify data fetch", 2.345, "10 tracks, 5 artists")
    log_data_summary(logger, "tracks", 10, ["Track 1", "Track 2"])
    log_function_exit(logger, "test_function", "success", True)
    
    print(f"Logging test completed. Check log file: {log_file}")
