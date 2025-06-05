# Valkyrie Client

A Python client library for connecting to and interacting with the Valkyrie key-value database server.

## Features

- **TCP Connection Management**: Reliable connection handling with automatic cleanup
- **Authentication**: Password-based authentication with retry mechanism
- **Data Types Support**: 
  - Primitives: bool, int, float, string, blob (bytes)
  - Composite: arrays and maps (dictionaries)
- **Operations**:
  - **Primitive Operations**: get, set, remove, length, append, increment, decrement
  - **Array Operations**: slice, insert, remove, length
  - **Map Operations**: get, set, remove, contains, keys, values
- **Error Handling**: Comprehensive exception hierarchy for different error types

## Installation

```bash
git clone git@github.com:valkyriedb/valkyrie_sdk.git
cd valkyrie-client

# Install dependencies
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- pytest (for testing)

## Quick Start

### Basic Usage


```python
from src.client import ValkyrieClient

with ValkyrieClient(host='localhost', port=8080, password='your_password') as client:
    # All operations here
    client.set('greeting', 'Hello from Valkyrie!')
    greeting = client.get('greeting')
    print(greeting)
# Connection automatically closed
```

## API Reference

```

#### Connection Methods
- `connect()`: Establish connection to the server
- `disconnect()`: Close connection
- `is_connected`: Property to check connection status

#### Primitive Operations
- `get(key: str)`: Get value by key
- `set(key: str, value)`: Set key-value pair
- `remove(key: str)`: Remove key
- `length(key: str)`: Get length of string/blob value
- `append(key: str, value: str)`: Append to string value
- `increment(key: str)`: Increment numeric value
- `decrement(key: str)`: Decrement numeric value

#### Array Operations (client.arrays)
- `slice(key: str, start: int, end: int)`: Get array slice
- `insert(key: str, index: int, values: list)`: Insert values at index
- `remove(key: str, start: int, end: int)`: Remove elements in range
- `length(key: str)`: Get array length

#### Map Operations (client.maps)
- `get(key: str, map_key: str)`: Get value from map
- `set(key: str, map_key: str, value)`: Set key-value in map
- `remove(key: str, map_key: str)`: Remove key from map
- `contains(key: str, map_key: str)`: Check if key exists in map
- `keys(key: str)`: Get all keys from map
- `values(key: str)`: Get all values from map

## Data Types

### Supported Primitive Types
- `bool`: Boolean values
- `int`: 64-bit signed integers
- `float`: 64-bit double precision floats
- `str`: UTF-8 encoded strings
- `bytes`: Binary data (blobs)

### Composite Types
- `list`: Arrays of mixed types
- `dict`: Key-value maps



## Protocol Details

The client communicates with the Valkyrie server using a custom binary protocol:

- **Encoding**: Little-endian byte order
- **Message Format**: Length-prefixed messages
- **Authentication**: Password-based with retry mechanism (max 3 attempts)
- **Status Codes**: Comprehensive error reporting

## Testing

### Prerequisites
```bash
pip install pytest
```

### Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run specific test categories:
```bash
# Test connection functionality
pytest tests/connection/ -v

# Test operations
pytest tests/operations/ -v

# Test protocol functionality
pytest tests/protocol/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

