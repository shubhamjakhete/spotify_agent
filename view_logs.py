#!/usr/bin/env python3
"""
Log Viewer for Spotify Agent
Simple utility to view and filter application logs
"""

import os
import sys
import argparse
from datetime import datetime
import glob


def list_log_files():
    """List all available log files"""
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        print("❌ No logs directory found")
        return []
    
    pattern = os.path.join(logs_dir, "spotify_agent_*.log")
    log_files = glob.glob(pattern)
    
    if not log_files:
        print("❌ No log files found")
        return []
    
    # Sort by modification time (newest first)
    log_files.sort(key=os.path.getmtime, reverse=True)
    
    print("📋 Available log files:")
    for i, log_file in enumerate(log_files, 1):
        mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
        size = os.path.getsize(log_file)
        print(f"  {i}. {log_file} ({size} bytes, modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    return log_files


def filter_logs(log_file, level=None, component=None, function=None, search_term=None):
    """Filter and display logs based on criteria"""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        filtered_lines = []
        
        for line in lines:
            # Apply filters
            if level and f"| {level.upper()}" not in line:
                continue
            
            if component and f"spotify_agent.{component}" not in line:
                continue
            
            if function and f"| {function}" not in line:
                continue
            
            if search_term and search_term.lower() not in line.lower():
                continue
            
            filtered_lines.append(line)
        
        return filtered_lines
        
    except Exception as e:
        print(f"❌ Error reading log file: {e}")
        return []


def display_logs(lines, tail=None):
    """Display log lines with optional tail functionality"""
    if not lines:
        print("\nNo log entries found")
        return
    
    # Apply tail if specified
    if tail:
        lines = lines[-tail:]
    
    print(f"\nShowing {len(lines)} log entries:\n")
    
    for line in lines:
        print(line.strip())
    
    print("")


def show_log_summary(log_file):
    """Show a summary of log entries by level and component"""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Count by level
        level_counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
        
        # Count by component
        component_counts = {}
        
        # Count by function
        function_counts = {}
        
        for line in lines:
            # Count levels
            for level in level_counts:
                if f"| {level}" in line:
                    level_counts[level] += 1
                    break
            
            # Count components
            if "spotify_agent." in line:
                parts = line.split("spotify_agent.")
                if len(parts) > 1:
                    component = parts[1].split()[0].split("|")[0].strip()
                    component_counts[component] = component_counts.get(component, 0) + 1
            
            # Count functions (API calls, USER actions, etc.)
            if "API CALL" in line:
                function_counts["API Calls"] = function_counts.get("API Calls", 0) + 1
            elif "USER ACTION" in line:
                function_counts["User Actions"] = function_counts.get("User Actions", 0) + 1
            elif "PERFORMANCE" in line:
                function_counts["Performance Metrics"] = function_counts.get("Performance Metrics", 0) + 1
            elif "ERROR" in line:
                function_counts["Errors"] = function_counts.get("Errors", 0) + 1
        
        print(f"\n📊 Log Summary for {log_file}")
        print("=" * 50)
        
        print("\n🎯 Log Levels:")
        for level, count in level_counts.items():
            if count > 0:
                print(f"  {level}: {count}")
        
        print("\n🧩 Components:")
        for component, count in sorted(component_counts.items()):
            if count > 0:
                print(f"  {component}: {count}")
        
        print("\n⚡ Activity Types:")
        for activity, count in sorted(function_counts.items()):
            if count > 0:
                print(f"  {activity}: {count}")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error analyzing log file: {e}")


def main():
    """Main function for log viewer"""
    parser = argparse.ArgumentParser(description="Spotify Agent Log Viewer")
    parser.add_argument("--level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       help="Filter by log level")
    parser.add_argument("--component", choices=["main", "spotify_client", "openai_client", "chat_cli"],
                       help="Filter by component")
    parser.add_argument("--function", help="Filter by function name")
    parser.add_argument("--search", help="Search for specific text")
    parser.add_argument("--tail", type=int, help="Show last N lines")
    parser.add_argument("--summary", action="store_true", help="Show log summary")
    parser.add_argument("--list", action="store_true", help="List available log files")
    parser.add_argument("--file", help="Specific log file to view")
    
    args = parser.parse_args()
    
    # List files if requested
    if args.list:
        list_log_files()
        return
    
    # Get log files
    log_files = list_log_files()
    if not log_files:
        return
    
    # Select log file
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ Log file not found: {args.file}")
            return
        selected_file = args.file
    else:
        # Use most recent log file
        selected_file = log_files[0]
        print(f"\n🎯 Using most recent log file: {selected_file}")
    
    # Show summary if requested
    if args.summary:
        show_log_summary(selected_file)
        return
    
    # Filter and display logs
    filtered_lines = filter_logs(
        selected_file,
        level=args.level,
        component=args.component,
        function=args.function,
        search_term=args.search
    )
    
    display_logs(filtered_lines, tail=args.tail)


if __name__ == "__main__":
    main()
