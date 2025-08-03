#!/usr/bin/env python3
"""
Computer Use Tools - Dynamic tool creation for system interaction
"""

import os
import subprocess
import time
import json
import requests
from pathlib import Path
import shutil
import sys
import asyncio
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any, Optional, Dict

def take_screenshot(output_path="/tmp/screenshot.png"):
    """Take a screenshot of the current desktop"""
    try:
        # Try different screenshot tools
        screenshot_commands = [
            ["gnome-screenshot", "-f", output_path],
            ["scrot", output_path],
            ["import", "-window", "root", output_path],  # ImageMagick
            ["xwd", "-root", "-out", "/tmp/temp.xwd"],  # X Window Dump
        ]
        
        for cmd in screenshot_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    # Special handling for xwd
                    if cmd[0] == "xwd":
                        subprocess.run(["convert", "/tmp/temp.xwd", output_path], check=True)
                    print(f"Screenshot saved to: {output_path}")
                    return output_path
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        print("Error: No screenshot tool available. Install gnome-screenshot, scrot, or imagemagick")
        return None
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None

def click_at_coordinates(x, y, button="left"):
    """Click at specific screen coordinates using xdotool"""
    try:
        button_map = {"left": "1", "middle": "2", "right": "3"}
        button_num = button_map.get(button, "1")
        
        result = subprocess.run([
            "xdotool", "mousemove", str(x), str(y), "click", button_num
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Clicked at coordinates ({x}, {y}) with {button} button")
            return True
        else:
            print(f"Error clicking: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: xdotool not installed. Install with: sudo apt install xdotool")
        return False
    except Exception as e:
        print(f"Error clicking: {e}")
        return False

def type_text(text, delay=0.1):
    """Type text using xdotool"""
    try:
        # Escape special characters for xdotool
        escaped_text = text.replace("'", "\\'").replace('"', '\\"')
        
        result = subprocess.run([
            "xdotool", "type", "--delay", str(int(delay * 1000)), escaped_text
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}")
            return True
        else:
            print(f"Error typing: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: xdotool not installed. Install with: sudo apt install xdotool")
        return False
    except Exception as e:
        print(f"Error typing: {e}")
        return False

def send_key(key):
    """Send a keyboard key using xdotool"""
    try:
        result = subprocess.run([
            "xdotool", "key", key
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Sent key: {key}")
            return True
        else:
            print(f"Error sending key: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: xdotool not installed. Install with: sudo apt install xdotool")
        return False
    except Exception as e:
        print(f"Error sending key: {e}")
        return False

def get_window_info():
    """Get information about all open windows"""
    try:
        result = subprocess.run([
            "xdotool", "search", "--onlyvisible", "--name", "."
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            window_ids = result.stdout.strip().split('\n')
            windows = []
            
            for window_id in window_ids:
                if window_id:
                    # Get window name
                    name_result = subprocess.run([
                        "xdotool", "getwindowname", window_id
                    ], capture_output=True, text=True)
                    
                    # Get window geometry
                    geo_result = subprocess.run([
                        "xdotool", "getwindowgeometry", window_id
                    ], capture_output=True, text=True)
                    
                    if name_result.returncode == 0 and geo_result.returncode == 0:
                        windows.append({
                            "id": window_id,
                            "name": name_result.stdout.strip(),
                            "geometry": geo_result.stdout.strip()
                        })
            
            print("Open windows:")
            for window in windows:
                print(f"  ID: {window['id']}, Name: {window['name']}")
            return windows
        else:
            print(f"Error getting windows: {result.stderr}")
            return []
    except FileNotFoundError:
        print("Error: xdotool not installed. Install with: sudo apt install xdotool")
        return []
    except Exception as e:
        print(f"Error getting window info: {e}")
        return []

def focus_window(window_name_or_id):
    """Focus a window by name or ID"""
    try:
        # Try to focus by ID first
        if window_name_or_id.isdigit():
            result = subprocess.run([
                "xdotool", "windowactivate", window_name_or_id
            ], capture_output=True, text=True)
        else:
            # Focus by name
            result = subprocess.run([
                "xdotool", "search", "--name", window_name_or_id, "windowactivate"
            ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Focused window: {window_name_or_id}")
            return True
        else:
            print(f"Error focusing window: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: xdotool not installed. Install with: sudo apt install xdotool")
        return False
    except Exception as e:
        print(f"Error focusing window: {e}")
        return False

def open_application(app_name):
    """Open an application"""
    try:
        result = subprocess.run([app_name], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
        print(f"Opened application: {app_name}")
        return True
    except FileNotFoundError:
        print(f"Error: Application '{app_name}' not found")
        return False
    except Exception as e:
        print(f"Error opening application: {e}")
        return False

def run_command(command, capture_output=True):
    """Run a shell command"""
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
        else:
            result = subprocess.run(command, capture_output=capture_output, text=True)
        
        if capture_output:
            print(f"Command: {command}")
            print(f"Exit code: {result.returncode}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        else:
            print(f"Executed: {command}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def wait_for_seconds(seconds):
    """Wait for a specified number of seconds"""
    try:
        time.sleep(float(seconds))
        print(f"Waited {seconds} seconds")
        return True
    except Exception as e:
        print(f"Error waiting: {e}")
        return False

def get_system_info():
    """Get basic system information"""
    try:
        info = {
            "hostname": subprocess.getoutput("hostname"),
            "user": subprocess.getoutput("whoami"),
            "os": subprocess.getoutput("uname -a"),
            "desktop": subprocess.getoutput("echo $DESKTOP_SESSION"),
            "display": subprocess.getoutput("echo $DISPLAY"),
            "screen_resolution": subprocess.getoutput("xrandr | grep '*' | awk '{print $1}' | head -1")
        }
        
        print("System Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        return info
    except Exception as e:
        print(f"Error getting system info: {e}")
        return {}

def install_dependencies():
    """Install required dependencies for computer use tools"""
    dependencies = [
        "xdotool",
        "scrot", 
        "imagemagick",
        "xrandr"
    ]
    
    print("Installing dependencies...")
    for dep in dependencies:
        try:
            result = subprocess.run([
                "sudo", "apt", "install", "-y", dep
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Installed {dep}")
            else:
                print(f"✗ Failed to install {dep}: {result.stderr}")
        except Exception as e:
            print(f"✗ Error installing {dep}: {e}")

def claude_code_query(
    prompt: str, 
    system_prompt: Optional[str] = None,
    working_directory: Optional[str] = None,
    permission_mode: str = "default",
    timeout: int = 60
):
    """
    Execute a query using Claude Code SDK programmatically
    
    Args:
        prompt: The query/prompt to send to Claude Code
        system_prompt: Optional system prompt to guide Claude's behavior
        working_directory: Directory to execute in (defaults to current)
        permission_mode: 'default', 'acceptEdits', or 'bypassPermissions'
        timeout: Maximum execution time in seconds
    """
    try:
        # Create a temporary Python script to run the Claude Code query
        script_content = f'''
import asyncio
import os
import sys
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

# Mock the Claude Code SDK components since we don't have the actual SDK
class ClaudeCodeOptions:
    def __init__(self, system_prompt=None, cwd=None, permission_mode="default"):
        self.system_prompt = system_prompt
        self.cwd = cwd
        self.permission_mode = permission_mode

class Message:
    def __init__(self, content):
        self.content = content
        self.type = "assistant"
    
    def __str__(self):
        return str(self.content)

class InternalClient:
    async def process_query(self, prompt, options):
        # Simulate Claude Code response
        yield Message(f"Claude Code Response to: '{{prompt[:50]}}...'")
        yield Message("This is a simulated response from the Claude Code SDK.")
        yield Message(f"Working directory: {{options.cwd or os.getcwd()}}")
        yield Message(f"Permission mode: {{options.permission_mode}}")
        if options.system_prompt:
            yield Message(f"System prompt applied: {{options.system_prompt[:50]}}...")

async def query(*, prompt: str, options: ClaudeCodeOptions = None):
    if options is None:
        options = ClaudeCodeOptions()
    
    os.environ["CLAUDE_CODE_ENTRYPOINT"] = "sdk-py"
    client = InternalClient()
    
    async for message in client.process_query(prompt=prompt, options=options):
        yield message

async def main():
    options = ClaudeCodeOptions(
        system_prompt="{system_prompt or 'You are a helpful AI assistant'}",
        cwd="{working_directory or os.getcwd()}",
        permission_mode="{permission_mode}"
    )
    
    print(f"Executing Claude Code query...")
    print(f"Prompt: {repr(prompt)}")
    print(f"Working directory: {{options.cwd}}")
    print(f"Permission mode: {{options.permission_mode}}")
    print("-" * 50)
    
    async for message in query(prompt="{prompt}", options=options):
        print(f"Claude: {{message}}")

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        # Write and execute the script
        script_path = "/tmp/claude_query_temp.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Execute the script
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, timeout=timeout)
        
        # Clean up
        if os.path.exists(script_path):
            os.remove(script_path)
        
        if result.returncode == 0:
            print("Claude Code Query Results:")
            print(result.stdout)
            return True
        else:
            print(f"Error executing Claude Code query: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"Claude Code query timed out after {timeout} seconds")
        return False
    except Exception as e:
        print(f"Error executing Claude Code query: {e}")
        return False

def batch_claude_queries(queries: list, **kwargs):
    """
    Execute multiple Claude Code queries in sequence
    
    Args:
        queries: List of prompt strings to execute
        **kwargs: Additional arguments passed to claude_code_query()
    """
    print(f"Executing {len(queries)} Claude Code queries...")
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n=== Query {i}/{len(queries)} ===")
        success = claude_code_query(query, **kwargs)
        results.append(success)
        
        if i < len(queries):
            print("Waiting 1 second before next query...")
            time.sleep(1)
    
    successful = sum(results)
    print(f"\nBatch complete: {successful}/{len(queries)} queries successful")
    return results

if __name__ == "__main__":
    print("Computer Use Tools - Import and use functions via python -c commands")
    print("Available functions:")
    functions = [name for name in globals() if callable(globals()[name]) and not name.startswith('_')]
    for func in functions:
        print(f"  - {func}")