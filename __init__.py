
from .nodes import LoadGGUFPath, LoadGGUFMPROJPath, LoadGGUFDraftPath, WaitForPassthrough, CallRemoteUrl, WaitForMilliseconds

NODE_CLASS_MAPPINGS = {
    "LoadGGUFPath": LoadGGUFPath,
    "LoadGGUFMPROJPath": LoadGGUFMPROJPath,
    "LoadGGUFDraftPath": LoadGGUFDraftPath,
    "WaitForPassthrough": WaitForPassthrough,
    "WaitForMilliseconds": WaitForMilliseconds,
    "CallRemoteUrl": CallRemoteUrl,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadGGUFPath": "Load GGUF Path",
    "LoadGGUFMPROJPath": "Load GGUF MPROJ Path",
    "LoadGGUFDraftPath": "Load GGUF DRAFT Path",
    "WaitForPassthrough": "Wait For Passthrough",
    "WaitForMilliseconds": "Wait For Milliseconds",
    "CallRemoteUrl": "Call Remote URL",
}
