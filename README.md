# ComfyUI SG Nodes

A collection of custom nodes for ComfyUI.

## Nodes

### Load GGUF Path
Loads the full path to a general GGUF model file.

- **Category**: SGNodes/GGUF Loaders
- **Input**: Model name from dropdown
- **Output**: Full file path as string

### Load GGUF MPROJ Path
Loads the full path to a GGUF multi-modal projector model file.

- **Category**: SGNodes/GGUF Loaders
- **Input**: Model name from dropdown
- **Output**: Full file path as string

### Load GGUF DRAFT Path
Loads the full path to a GGUF draft model file.

- **Category**: SGNodes/GGUF Loaders
- **Input**: Model name from dropdown
- **Output**: Full file path as string

### Wait For Passthrough
A utility node that waits for one input to be ready before passing through another input.

- **Category**: SGNodes/Utilities
- **Inputs**:
  - `passthrough`: Any type, lazy input that will be returned
  - `wait_for`: Any type, required input that triggers execution
- **Output**: The `passthrough` input value
- **Behavior**: Executes when `wait_for` is ready, then requests the `passthrough` value if not already available

## Configuration

Create a `config.json` file in the same directory as this package to specify additional model folders to scan:

```json
{
  "model_folders": [
    "C:\\Users\\YourUsername\\models",
    "D:\\AI\\LLM\\models",
    "/home/user/models"
  ]
}
```

The nodes will automatically scan:
- ComfyUI's `text_encoders` folder
- Any folders specified in `config.json`

## Installation

1. Place this folder in your ComfyUI `custom_nodes` directory
2. Restart ComfyUI
3. The nodes will appear in the "SGNodes" category

## Requirements

- ComfyUI
