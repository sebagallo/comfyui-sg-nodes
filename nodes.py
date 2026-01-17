import os
import requests
import json
import folder_paths
from comfy.comfy_types import IO, ComfyNodeABC, InputTypeDict
from typing import Dict, Any, List
import time
import re
from server import PromptServer
from aiohttp import web

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


def get_nested_value(data, path, default=None):
    """Retrieve a value from a nested dictionary using dot notation."""
    try:
        keys = path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, default)
            elif isinstance(current, list):
                # Optional: support list indexing via integers?
                try:
                    index = int(key)
                    if 0 <= index < len(current):
                         current = current[index]
                    else:
                        return default
                except ValueError:
                     return default
            else:
                return default
                
            if current is None:
                return default
                
        return current
    except Exception:
        return default

class MapJsonToProperty(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "json_string": ("STRING", {"multiline": True, "default": "{}"}),
                "property_name": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_value",)
    FUNCTION = "map_to_property"
    CATEGORY = "SGNodes/JSON"

    def map_to_property(self, json_string, property_name):
        try:
            data = json.loads(json_string)
            if not isinstance(data, (dict, list)): # Allow list as root for index access
                 return ("",)

            value = get_nested_value(data, property_name)
            
            if value is None:
                return ("",)

            if isinstance(value, (dict, list)):
                return (json.dumps(value),)
            
            return (str(value),)
            
        except json.JSONDecodeError:
            return ("",)
        except Exception as e:
            return (str(e),)

class MapJsonArray(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "json_array": ("STRING", {"multiline": True, "default": "[]"}),
                "property_name": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("mapped_array",)
    FUNCTION = "map_array"
    CATEGORY = "SGNodes/JSON"

    def map_array(self, json_array, property_name):
        try:
            data = json.loads(json_array)
            if not isinstance(data, list):
                return ("[]",)

            result = []
            for item in data:
                 value = get_nested_value(item, property_name)
                 if value is not None:
                     result.append(value)
            
            return (json.dumps(result),)
            
        except json.JSONDecodeError:
            return ("[]",)
        except Exception as e:
            return (f"Error: {str(e)}",)

class FindJsonElement(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "json_array": ("STRING", {"multiline": True, "default": "[]"}),
                "match_key": ("STRING", {"default": ""}),
                "match_value": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("found_element",)
    FUNCTION = "find_element"
    CATEGORY = "SGNodes/JSON"

    def find_element(self, json_array, match_key, match_value):
        try:
            data = json.loads(json_array)
            if not isinstance(data, list):
                 return ("",)

            for item in data:
                val = get_nested_value(item, match_key)
                if val is not None:
                    # Compare as strings to be robust
                    if str(val) == str(match_value):
                        return (json.dumps(item),)
                            
            return ("",)

        except json.JSONDecodeError:
            return ("",)
        except Exception as e:
            return (f"Error: {str(e)}",)

@PromptServer.instance.routes.get("/sg-nodes/list_files")
async def list_files_endpoint(request):
    try:
        folder_path = request.rel_url.query.get("path", "")
        extensions = request.rel_url.query.get("extensions", "").strip()
        filter_type = request.rel_url.query.get("filter_type", "none")
        filter_text = request.rel_url.query.get("filter_text", "")
        
        if not folder_path or not os.path.isdir(folder_path):
            return web.json_response({"files": []})
        
        # Parse extensions
        ext_list = []
        if extensions:
            ext_list = [e.strip().lower() for e in extensions.split(",") if e.strip()]
            # Ensure they start with dot
            ext_list = [e if e.startswith(".") else f".{e}" for e in ext_list]

        files_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Create relative path from the base folder
                rel_path = os.path.relpath(os.path.join(root, file), folder_path)
                # Normalize to forward slashes for consistency
                rel_path = rel_path.replace("\\", "/")
                
                # Apply extension filter
                if ext_list:
                    if not any(file.lower().endswith(ext) for ext in ext_list):
                        continue

                # Apply additional filters
                include = True
                if filter_type == "contains" and filter_text:
                    if filter_text.lower() not in rel_path.lower():
                        include = False
                elif filter_type == "regex" and filter_text:
                    try:
                        if not re.search(filter_text, rel_path, re.IGNORECASE):
                            include = False
                    except:
                        pass # Invalid regex
                
                if include:
                    files_list.append(rel_path)
        
        files_list.sort()
        return web.json_response({"files": files_list})
    except Exception as e:
        print(f"Error listing files: {e}")
        return web.json_response({"files": []}, status=500)

class SelectFileFromFolder(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "folder_path": ("STRING", {"default": "", "multiline": False}),
                "extensions": ("STRING", {"default": "*", "multiline": False}),
                "filter_type": (["none", "contains", "regex"],),
                "filter_text": ("STRING", {"default": "", "multiline": False}),
                "file_name": ([""], {}), 
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("full_path", "relative_path", "file_name")
    FUNCTION = "get_full_path"
    CATEGORY = "SGNodes/Utilities"

    def get_full_path(self, folder_path, extensions, filter_type, filter_text, file_name):
        if not folder_path or not file_name:
             return ("", "", "")
        
        # input file_name is the relative path from the UI list
        relative_path = file_name
        base_name = os.path.basename(file_name)
        full_path = os.path.join(folder_path, relative_path)
        
        # Normalize slashes
        full_path = full_path.replace("\\", "/")
        relative_path = relative_path.replace("\\", "/")
        
        return (full_path, relative_path, base_name)


class SelectFromList(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "list_data": ("STRING", {"multiline": True, "default": ""}),
                "input_mode": (["auto", "delimiter", "json"], {"default": "auto"}),
                "delimiter": ("STRING", {"default": "\\n"}),
                "selected_value": ([""], {}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("selected_item",)
    FUNCTION = "select_item"
    CATEGORY = "SGNodes/Utilities"

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    def select_item(self, list_data, input_mode, delimiter, selected_value):
        if not list_data:
            return (None,)
        
        items = []
        
        def parse_json(data):
            try:
                parsed = json.loads(data)
                if isinstance(parsed, list):
                    return parsed
                return [parsed]
            except:
                return None

        def parse_delimited(data, delim):
            # Handle escape sequences
            if delim == "\\n":
                delim = "\n"
            elif delim == "\\t":
                delim = "\t"
            elif delim == "\\r":
                delim = "\r"
            
            if not delim:
                return [data]
                
            return [part.strip() for part in data.split(delim) if part.strip()]

        if input_mode == "json":
            items = parse_json(list_data) or []
        elif input_mode == "delimiter":
            items = parse_delimited(list_data, delimiter)
        else: # auto
            items = parse_json(list_data)
            if items is None:
                items = parse_delimited(list_data, delimiter)

        if not items:
            return (None,)

        # Final selection check
        if selected_value in items:
            return (selected_value,)
        
        for item in items:
            if str(item) == selected_value:
                return (item,)

        return (selected_value,)


class MakeJsonList(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {},
            "optional": {}
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_string",)
    FUNCTION = "make_json_list"
    CATEGORY = "SGNodes/JSON"

    def make_json_list(self, **kwargs):
        # inputs will be in kwargs like "input_1", "input_2", etc.
        # We need to sort them to maintain order
        
        # Filter only our dynamic inputs
        input_keys = [k for k in kwargs.keys() if k.startswith("input_")]
        
        # Sort by the number suffix
        try:
            input_keys.sort(key=lambda k: int(k.split("_")[1]))
        except ValueError:
            # Fallback for unexpected naming, just alphabetical
            input_keys.sort()
            
        result_list = [kwargs[k] for k in input_keys]
        
        try:
            json_output = json.dumps(result_list)
        except Exception as e:
            json_output = json.dumps([str(x) for x in result_list])
            
        return (json_output,)





class AnyAdapter(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "any_input": (IO.ANY, {"tooltip": "Connect any type here."}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("any_output",)
    FUNCTION = "adapt"
    CATEGORY = "SGNodes/Utilities"

    def adapt(self, any_input: Any) -> tuple:
        return (any_input,)


class AnyLazyAdapter(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "any_input": (IO.ANY, {"lazy": True, "tooltip": "Connect any type here. Evaluation is lazy."}),
            }
        }

    RETURN_TYPES = (IO.ANY,)
    RETURN_NAMES = ("any_output",)
    FUNCTION = "adapt"
    CATEGORY = "SGNodes/Utilities"

    def check_lazy_status(self, any_input=None):
        if any_input is None:
            return ["any_input"]

    def adapt(self, any_input: Any = None) -> tuple:
        return (any_input,)
