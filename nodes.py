import os
import json
import folder_paths
from comfy.comfy_types import IO, ComfyNodeABC, InputTypeDict
from typing import Dict, Any, List

# Config file path
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config() -> Dict[str, Any]:
    """Load config from config.json, return empty dict if not found or invalid."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_user_model_folders() -> List[str]:
    """Get user-specified model folders from config."""
    config = load_config()
    return config.get('model_folders', [])

def get_merged_model_folders() -> List[str]:
    """Merge ComfyUI text_encoders folders with user folders."""
    try:
        comfy_folders = folder_paths.get_folder_paths("text_encoders")
    except:
        comfy_folders = []
    user_folders = get_user_model_folders()
    all_folders = comfy_folders + user_folders
    # Filter out non-existent paths
    return [f for f in all_folders if os.path.exists(f)]

def scan_gguf_models_in_folders() -> List[str]:
    """Scan merged folders for GGUF model files."""
    folders = get_merged_model_folders()
    model_list = []
    for folder in folders:
        try:
            files = os.listdir(folder)
            model_list.extend([f for f in files if f.lower().endswith('.gguf')])
        except:
            pass  # Skip inaccessible folders
    return model_list

def find_model_path(model_name: str) -> str:
    """Find full path to model in merged folders."""
    folders = get_merged_model_folders()
    for folder in folders:
        path = os.path.join(folder, model_name)
        if os.path.exists(path):
            return path
    return None


class LoadGGUFPath(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        model_list = scan_gguf_models_in_folders()

        # Filter for general GGUF models (exclude mmproj and draft)
        general_models = [f for f in model_list if 'mmproj' not in f.lower() and 'draft' not in f.lower()]

        return {
            "required": {
                "model_name": (general_models if general_models else ["No GGUF models found"], {"tooltip": "Select GGUF model file"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)
    FUNCTION = "load_path"
    CATEGORY = "SGNodes/GGUF Loaders"

    def load_path(self, model_name: str) -> tuple:
        try:
            model_path = find_model_path(model_name)

            if model_path is None:
                raise FileNotFoundError(f"Model file not found: {model_name}")

            if not model_name.lower().endswith('.gguf'):
                raise ValueError(f"Selected file is not a GGUF model: {model_name}")

            return (model_path,)

        except Exception as e:
            raise RuntimeError(f"Failed to load model path: {str(e)}")


class LoadGGUFMPROJPath(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        model_list = scan_gguf_models_in_folders()

        # Filter for mmproj models
        mmproj_models = [f for f in model_list if 'mmproj' in f.lower()]

        return {
            "required": {
                "model_name": (mmproj_models if mmproj_models else ["No GGUF mmproj models found"], {"tooltip": "Select GGUF mmproj model file"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("mmproj_path",)
    FUNCTION = "load_path"
    CATEGORY = "SGNodes/GGUF Loaders"

    def load_path(self, model_name: str) -> tuple:
        try:
            model_path = find_model_path(model_name)

            if model_path is None:
                raise FileNotFoundError(f"Model file not found: {model_name}")

            if not model_name.lower().endswith('.gguf'):
                raise ValueError(f"Selected file is not a GGUF model: {model_name}")

            return (model_path,)

        except Exception as e:
            raise RuntimeError(f"Failed to load model path: {str(e)}")


class LoadGGUFDraftPath(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        model_list = scan_gguf_models_in_folders()

        # Filter for draft models
        draft_models = [f for f in model_list if 'draft' in f.lower()]

        return {
            "required": {
                "model_name": (draft_models if draft_models else ["No GGUF draft models found"], {"tooltip": "Select GGUF draft model file"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("draft_path",)
    FUNCTION = "load_path"
    CATEGORY = "SGNodes/GGUF Loaders"

    def load_path(self, model_name: str) -> tuple:
        try:
            model_path = find_model_path(model_name)

            if model_path is None:
                raise FileNotFoundError(f"Model file not found: {model_name}")

            if not model_name.lower().endswith('.gguf'):
                raise ValueError(f"Selected file is not a GGUF model: {model_name}")

            return (model_path,)

        except Exception as e:
            raise RuntimeError(f"Failed to load model path: {str(e)}")
