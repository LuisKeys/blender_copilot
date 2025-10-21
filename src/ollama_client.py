"""
Ollama API client for Blender Copilot
Handles communication with the Ollama API service
"""

import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:12b"


def ollama_generate(prompt_text, url=OLLAMA_URL, model=OLLAMA_MODEL, temperature=0.0):
    """Generate a response from Ollama API."""
    print(f"Blender Copilot: Sending request to Ollama at {url} with model {model}")
    payload = {
        "model": model,
        "prompt": prompt_text,
        "stream": False,
        "options": {"temperature": temperature},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            obj = json.loads(body)
            response = obj.get("response", "").strip()
            print(
                f"Blender Copilot: Received response from Ollama: {response[:100]}..."
            )
            return response
    except urllib.error.URLError as e:
        print(f"Blender Copilot: URLError in Ollama request: {e}")
        return f"__ERROR__: URLError {e}"
    except json.JSONDecodeError as e:
        print(f"Blender Copilot: JSON decode error in Ollama response: {e}")
        return f"__ERROR__: Invalid JSON response from Ollama: {e}"
    except Exception as e:
        print(f"Blender Copilot: Unexpected error in Ollama request: {e}")
        return f"__ERROR__: {e}"
