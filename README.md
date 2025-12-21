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

### Wait For Milliseconds
Pauses execution for a specified number of milliseconds.

- **Category**: SGNodes/Utilities
- **Inputs**:
  - `passthrough`: Any type, lazy input that will be returned
  - `milliseconds`: Integer, number of milliseconds to wait (default: 1000)
- **Output**: The `passthrough` input value

### Call Remote URL
Performs a server-side HTTP request to a remote URL. Useful for integrating with external APIs.

- **Category**: SGNodes/Network
- **Inputs**:
  - `url`: Target URL string
  - `method`: HTTP method (GET, POST, etc.)
  - `passthrough`: Any type (IO.ANY), passed through to output. Useful for execution ordering.
  - `body` (Optional): Request body string
  - `headers` (Optional): JSON string of request headers
- **Outputs**:
  - `passthrough`: The input `passthrough` value
  - `status_code`: HTTP status code (INT)
  - `response_body`: Response content (STRING)

### Poll Remote URL
Polls a remote URL until a matching condition is met or maximum attempts are reached.

- **Category**: SGNodes/Network
- **Inputs**:
  - `passthrough`: Any type (IO.ANY), passed through to output.
  - `url`: Target URL string.
  - `method`: HTTP method (GET, POST, etc.).
  - `match_type`: Type of matching to perform (`string`, `regex`, `json`).
    - `string`: Checks if `match_value` is a substring of the response.
    - `regex`: Checks if `match_value` regex pattern matches the response.
    - `json`: Checks if `match_value` (as JSON) is a subset of the response JSON. *Note: The match is partial but structural. To match `{"status": "ok"}` inside `{"data": {"status": "ok"}}`, your match value must include the full path: `{"data": {"status": "ok"}}`.*
  - `match_value`: The value to match against.
  - `invert_match`: (Boolean) If True, waits until the match condition is **FALSE** (e.g. wait for something to disappear).
  - `body` (Optional): Request body string.
  - `headers` (Optional): JSON string of request headers.
  - `max_attempts` (Optional): Maximum number of polling attempts (default: 30).
  - `delay_ms` (Optional): Delay between attempts in milliseconds (default: 500).
- **Outputs**:
  - `passthrough`: The input `passthrough` value.
  - `status_code`: Last HTTP status code (INT).
  - `response_body`: Last response content (STRING).

### Map JSON To Property
Extracts a property from a JSON object string.

- **Category**: SGNodes/JSON
- **Inputs**:
  - `json_string`: JSON object string (e.g., `{"a": 1}`).
  - `property_name`: Name of the property to extract. Supports dot notation for nested keys (e.g., `data.user.id`).
- **Output**: The value of the property as a string. If the value is an object or array, it returns a JSON string.

### Map JSON Array
Maps a property from each object in a JSON array.

- **Category**: SGNodes/JSON
- **Inputs**:
  - `json_array`: JSON array string (e.g., `[{"id": 1}, {"id": 2}]`).
  - `property_name`: Name of the property to extract from each item. Supports dot notation (e.g., `user.name`).
- **Output**: A JSON array string of the extracted values (e.g., `["User1", "User2"]`).

### Find JSON Element
Finds the first element in a JSON array that matches a key-value pair.

- **Category**: SGNodes/JSON
- **Inputs**:
  - `json_array`: JSON array string.
  - `match_key`: The key to check in each element. Supports dot notation (e.g., `status.code`).
  - `match_value`: The value to match against (compared as string).
- **Output**: The matching element as a JSON string. Returns empty string if not found.

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
