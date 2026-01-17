
from .nodes import (
    LoadGGUFPath, LoadGGUFMPROJPath, LoadGGUFDraftPath, 
    WaitForPassthrough, CallRemoteUrl, WaitForMilliseconds, 
    PollRemoteUrl, MapJsonToProperty, MapJsonArray, 
    FindJsonElement, SelectFileFromFolder, SelectFromList, MakeJsonList, 
    AnyAdapter, AnyLazyAdapter
)

NODE_CLASS_MAPPINGS = {
    "LoadGGUFPath": LoadGGUFPath,
    "LoadGGUFMPROJPath": LoadGGUFMPROJPath,
    "LoadGGUFDraftPath": LoadGGUFDraftPath,
    "WaitForPassthrough": WaitForPassthrough,
    "WaitForMilliseconds": WaitForMilliseconds,
    "CallRemoteUrl": CallRemoteUrl,
    "PollRemoteUrl": PollRemoteUrl,
    "MapJsonToProperty": MapJsonToProperty,
    "MapJsonArray": MapJsonArray,
    "FindJsonElement": FindJsonElement,
    "SelectFileFromFolder": SelectFileFromFolder,
    "SelectFromList": SelectFromList,
    "MakeJsonList": MakeJsonList,
    "AnyAdapter": AnyAdapter,
    "AnyLazyAdapter": AnyLazyAdapter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadGGUFPath": "Load GGUF Path",
    "LoadGGUFMPROJPath": "Load GGUF MPROJ Path",
    "LoadGGUFDraftPath": "Load GGUF DRAFT Path",
    "WaitForPassthrough": "Wait For Passthrough",
    "WaitForMilliseconds": "Wait For Milliseconds",
    "CallRemoteUrl": "Call Remote URL",
    "PollRemoteUrl": "Poll Remote URL",
    "MapJsonToProperty": "Map JSON To Property",
    "MapJsonArray": "Map JSON Array",
    "FindJsonElement": "Find JSON Element",
    "SelectFileFromFolder": "Select File From Directory",
    "SelectFromList": "Select From List",
    "MakeJsonList": "Make JSON List",
    "AnyAdapter": "Any Adapter",
    "AnyLazyAdapter": "Any Lazy Adapter",
}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]