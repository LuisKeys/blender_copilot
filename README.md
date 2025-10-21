# Blender Copilot

A Blender add-on that translates natural language commands into safe Blender operations using AI (Ollama).

## 🎯 Overview

Blender Copilot allows you to describe what you want to create in plain English, and it generates a safe JSON plan that executes Blender operators to accomplish your request. The add-on uses Ollama's local AI models to interpret commands while maintaining strict safety through operator whitelisting.

## ✨ Features

- **Natural Language Interface**: Describe 3D operations in plain English
- **AI-Powered Planning**: Uses Ollama (Gemma 3 12B) for intelligent command interpretation  
- **Safety First**: Whitelisted operators prevent dangerous operations
- **Real-time Feedback**: Console logging shows detailed execution steps
- **Debug Support**: VS Code remote debugging integration
- **Modular Architecture**: Clean, maintainable codebase

## 🛠️ Supported Operations

### Primitive Creation
- `mesh.primitive_cube_add` - Create cubes
- `mesh.primitive_uv_sphere_add` - Create UV spheres
- `mesh.primitive_cylinder_add` - Create cylinders
- `mesh.primitive_plane_add` - Create planes
- `mesh.primitive_cone_add` - Create cones
- `mesh.primitive_torus_add` - Create torus

### Object Operations
- `object.modifier_add` - Add modifiers
- `object.modifier_apply` - Apply modifiers
- `object.shade_smooth` - Apply smooth shading
- `object.duplicate` - Duplicate objects
- `object.delete` - Delete objects

### Transformations
- `transform.translate` - Move objects
- `transform.rotate` - Rotate objects
- `transform.resize` - Scale objects

## 📋 Prerequisites

1. **Blender 4.5+** - The add-on is designed for modern Blender versions
2. **Ollama** - Local AI service running on `localhost:11434`
   - Install from [https://ollama.ai](https://ollama.ai)
   - Pull the Gemma 3 12B model: `ollama pull gemma3:12b`
3. **Python debugpy** (optional) - For VS Code debugging
   - Install in Blender's Python: `pip install debugpy`

## 🚀 Installation

1. **Download or clone** this repository
2. **Copy the `blender_copilot` folder** to your Blender add-ons directory:
   - **Linux**: `~/.config/blender/[version]/scripts/addons/`
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/[version]/scripts/addons/`
3. **Enable the add-on**:
   - Open Blender → Edit → Preferences → Add-ons
   - Search for "Blender Copilot"
   - Check the box to enable it

## 🎮 Usage

### Basic Workflow
1. **Start Ollama**: Ensure Ollama is running with `ollama serve`
2. **Open Blender**: The add-on panel appears in 3D Viewport → Sidebar → "Blender Copilot" tab
3. **Enter Command**: Type your request in natural language
4. **Execute**: Click "Run" to generate and execute the plan

### Example Commands
- `"Create a 2 m cube centered on the origin, and shade smooth"`
- `"Add a sphere with radius 1.5 meters"`
- `"Create a cylinder and move it 2 units up"`
- `"Make a plane and scale it to half size"`

### Console Debugging
Launch Blender from terminal to see detailed execution logs:
```bash
blender
```

## 🏗️ Project Structure

```
blender_copilot/
├── __init__.py                 # Main add-on entry point
├── README.md                   # This file
└── src/
    ├── __init__.py            # Source package marker
    ├── debug.py               # VS Code debugging setup
    ├── executor.py            # Blender operator execution
    ├── ollama_client.py       # Ollama API communication
    ├── prompts.py             # AI prompt templates
    └── ui.py                  # Blender UI panels and operators
```

### Module Responsibilities

- **`__init__.py`**: Add-on registration and orchestration
- **`debug.py`**: Remote debugging server for VS Code integration
- **`executor.py`**: Safe execution of whitelisted Blender operators with context validation
- **`ollama_client.py`**: HTTP communication with Ollama API service
- **`prompts.py`**: AI prompt engineering and templates
- **`ui.py`**: Blender user interface panels and operators

## 🔧 Development

### VS Code Debugging Setup

1. **Install debugpy** in Blender's Python environment
2. **Create launch configuration** in VS Code:
```json
{
    "name": "Python: Attach to Blender",
    "type": "debugpy",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678
    },
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "."
        }
    ]
}
```
3. **Launch Blender** with the add-on enabled
4. **Attach debugger** in VS Code and set breakpoints

### Architecture Principles

- **Safety**: All operations go through whitelisted operator validation
- **Modularity**: Each module has a single responsibility
- **Extensibility**: Easy to add new operators or AI models
- **Debugging**: Comprehensive logging and debug support
- **Error Handling**: Graceful failure with user feedback

## ⚙️ Configuration

### Ollama Settings
```python
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:12b"
```

### Supported Arguments
The AI generates JSON with these argument patterns:
- **Vectors**: `{"value": [x, y, z]}` for transforms
- **Scalars**: `{"size": 2.0}` for primitive sizing
- **Context**: Operations requiring active objects are validated

## 🐛 Troubleshooting

### Common Issues

**"Object created but not visible"**
- Check viewport shading mode (Solid vs Wireframe)
- Press `Home` to frame all objects
- Verify object isn't behind camera or clipping planes

**"Connection refused to Ollama"**
- Ensure Ollama is running: `ollama serve`
- Check if port 11434 is accessible
- Verify Gemma 3 model is installed: `ollama list`

**"Operator requires active object"**
- Select an object before running transforms/modifiers
- Create a primitive first, then apply operations

### Debug Output
Enable console logging by launching Blender from terminal. Look for:
```
Blender Copilot: User prompt: [your command]
Blender Copilot: Sending request to Ollama...
Blender Copilot: Executing step 0: mesh.primitive_cube_add...
```

## 🚨 Safety & Limitations

### Safety Features
- **Operator Whitelisting**: Only approved Blender operators can execute
- **Argument Validation**: Parameters are filtered and type-checked  
- **Context Checking**: Operations requiring selections are validated
- **Local AI**: No data sent to external services

### Current Limitations
- Limited to whitelisted operators (no arbitrary Python execution)
- Requires active internet connection for initial Ollama model download
- Single-step operations (no complex multi-object workflows yet)
- English language prompts only

## 🔮 Future Enhancements

- **Material Operations**: Support for material and texture commands
- **Animation Support**: Keyframe and animation operator integration
- **Custom Templates**: User-defined operation templates
- **Multi-Language**: Support for non-English prompts
- **Batch Operations**: Complex multi-step workflows
- **Model Choice**: Support for different AI models beyond Gemma

## 📄 License

This project is open source. Please check the specific license file for details.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional operator support
- Better prompt engineering
- UI/UX enhancements
- Documentation improvements
- Test coverage

## 📞 Support

For issues, questions, or feature requests, please create an issue in the project repository.

---

**Made with ❤️ for the Blender community**