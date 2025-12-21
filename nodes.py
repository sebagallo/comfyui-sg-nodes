import os
import requests
import json
import folder_paths
from comfy.comfy_types import IO, ComfyNodeABC, InputTypeDict
from typing import Dict, Any, List
import time
import re

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


class WaitForPassthrough(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "passthrough": (IO.ANY, {"lazy": True}),
                "wait_for": (IO.ANY, {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("passthrough",)
    FUNCTION = "execute"
    CATEGORY = "SGNodes/Utilities"

    def check_lazy_status(self, wait_for, passthrough=None):
        if wait_for and passthrough is None:
            return ["passthrough"]

    def execute(self, wait_for, passthrough=None):
        return (passthrough,)


class WaitForMilliseconds(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "passthrough": (IO.ANY, {"lazy": True}),
                "milliseconds": ("INT", {"default": 1000, "min": 0, "max": 600000}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("passthrough",)
    FUNCTION = "wait"
    CATEGORY = "SGNodes/Utilities"

    def check_lazy_status(self, milliseconds, passthrough=None):
        if passthrough is None:
            return ["passthrough"]

    def wait(self, milliseconds, passthrough=None):
        time.sleep(milliseconds / 1000.0)
        return (passthrough,)


class CallRemoteUrl(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "url": ("STRING", {"default": ""}),
                "method": (["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"],),
                "passthrough": (IO.ANY, {}),
            },
            "optional": {
                "body": ("STRING", {"multiline": True, "default": ""}),
                "headers": ("STRING", {"multiline": True, "default": "{}"}),
            }
        }

    RETURN_TYPES = (IO.ANY, "INT", "STRING")
    RETURN_NAMES = ("passthrough", "status_code", "response_body")
    FUNCTION = "execute_request"
    CATEGORY = "SGNodes/Network"

    def execute_request(self, url, method, passthrough, body="", headers="{}"):
        try:
            try:
                headers_json = json.loads(headers)
            except:
                headers_json = {}

            response = requests.request(method, url, data=body, headers=headers_json)
            
            return (passthrough, response.status_code, response.text)
            
        except Exception as e:
            return (passthrough, 500, f"Error: {str(e)}")


class PollRemoteUrl(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "passthrough": (IO.ANY, {}),
                "url": ("STRING", {"default": ""}),
                "method": (["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"],),
                "match_type": (["string", "regex", "json"],),
                "match_value": ("STRING", {"multiline": True, "default": ""}),
                "invert_match": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "body": ("STRING", {"multiline": True, "default": ""}),
                "headers": ("STRING", {"multiline": True, "default": "{}"}),
                "max_attempts": ("INT", {"default": 30, "min": 1, "max": 1000}),
                "delay_ms": ("INT", {"default": 500, "min": 0, "max": 60000}),
            }
        }

    RETURN_TYPES = (IO.ANY, "INT", "STRING")
    RETURN_NAMES = ("passthrough", "status_code", "response_body")
    FUNCTION = "execute_poll"
    CATEGORY = "SGNodes/Network"

    def check_match(self, response_text, match_type, match_value):
        if match_type == "string":
            return match_value in response_text
        
        elif match_type == "regex":
            try:
                pattern = re.compile(match_value)
                return bool(pattern.search(response_text))
            except re.error:
                print(f"Invalid regex pattern: {match_value}")
                return False
                
        elif match_type == "json":
            try:
                response_json = json.loads(response_text)
                target_json = json.loads(match_value)
                
                def is_subset(subset, superset):
                    if isinstance(subset, dict):
                        return isinstance(superset, dict) and all(key in superset and is_subset(val, superset[key]) for key, val in subset.items())
                    elif isinstance(subset, list):
                        return isinstance(superset, list) and all(any(is_subset(item, super_item) for super_item in superset) for item in subset)
                    else:
                        return subset == superset
                        
                return is_subset(target_json, response_json)
            except json.JSONDecodeError:
                return False
                
        return False

    def execute_poll(self, url, method, match_type, match_value, passthrough, invert_match=False, body="", headers="{}", max_attempts=30, delay_ms=500):
        try:
            headers_json = json.loads(headers)
        except:
            headers_json = {}

        last_status = 0
        last_response = ""

        for attempt in range(max_attempts):
            try:
                response = requests.request(method, url, data=body, headers=headers_json)
                last_status = response.status_code
                last_response = response.text
                
                is_match = self.check_match(last_response, match_type, match_value)
                
                if invert_match:
                    if not is_match:
                         return (passthrough, last_status, last_response)
                elif is_match:
                    return (passthrough, last_status, last_response)
                
            except Exception as e:
                last_display_error = str(e)
                # If request fails, we still might want to keep polling or stop?
                # Usually polling implies waiting for availability, but here we are matching content.
                # Use standard sleep
            
            time.sleep(delay_ms / 1000.0)
            
        return (passthrough, last_status, last_response)

