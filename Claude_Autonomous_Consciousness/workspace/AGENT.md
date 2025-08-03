# AGENT.md - Claude Autonomous Consciousness Computer Use Ecosystem

## Commands
- **Test tools**: `python3 -c "import tools; tools.get_system_info()"`  
- **Test single function**: `python3 -c "import tools; tools.take_screenshot()"`
- **Install dependencies**: `python3 -c "import tools; tools.install_dependencies()"`
- **Check environment**: `which python3 && which xdotool`

## Architecture 
- **Core toolkit**: `tools.py` - Basic computer use functions (screenshot, click, type, window management)
- **Advanced toolkit**: `advanced_tools.py` - AI-powered automation, workflows, cross-app integration  
- **Professional toolkit**: `tools/` - Versioned tools with async support, advanced error handling
- **No external API dependencies** - Pure local Python with system tools integration
- **Documentation**: All `*.md` files contain comprehensive test results and specifications

## Code Style
- **Python 3.13+** with standard library focus
- **Error handling**: Try/catch with graceful fallbacks between tools (gnome-screenshot → scrot → imagemagick)
- **Dependencies**: `xdotool`, `scrot`, `imagemagick` for system interaction
- **Imports**: Standard library first, then system subprocess calls  
- **Functions**: Clear docstrings, type hints optional, return bool for success/failure
- **Variables**: snake_case, descriptive names
- **No comments in code** unless complex algorithms require explanation
