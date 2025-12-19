from .nodes import LoadGGUFPath, LoadGGUFMPROJPath, LoadGGUFDraftPath

NODE_CLASS_MAPPINGS = {
    "LoadGGUFPath": LoadGGUFPath,
    "LoadGGUFMPROJPath": LoadGGUFMPROJPath,
    "LoadGGUFDraftPath": LoadGGUFDraftPath,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadGGUFPath": "Load GGUF Path",
    "LoadGGUFMPROJPath": "Load GGUF MPROJ Path",
    "LoadGGUFDraftPath": "Load GGUF DRAFT Path",
}
