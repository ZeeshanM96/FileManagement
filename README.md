# kambi_assignment

# FastAPI File Management API

This is a FastAPI-based web application that provides RESTful endpoints for managing files in a specified folder asynchronously. You can use this API to list, filter, and order files based on various criteria.

## Features

- List files in a folder.
- List specific number of files in a folder.
- Filter files by name prefix.
- Order files by size in ascending order.
- Filter files by file type (extension).

## Prerequisites

Before running this application, make sure you have the following prerequisites installed on your system:

- Python 3.7+
- FastAPI
- Uvicorn

## Getting Started
Follow these steps to run the FastAPI application:

- Clone the repository:
```bash
git clone https://github.com/ZeeshanM96/kambi_assignment.git
cd kambi_assignment
```

- create a virual env

```bash
cd path\to\your\desired\directory
```
```bash
python -m venv myenv
```
```bash
.\myenv\Scripts\Activate
```
```bash
myenv\Scripts\Activate
```

- You can install FastAPI and Uvicorn using pip:

```bash
pip install fastapi uvicorn
```

- Run the application
```bash
python -m uvicorn apis:app --host 0.0.0.0 --port 8000
  ```

This will start the FastAPI server on http://localhost:8000.

- Access the API using a web browser or a tool like curl or Postman.
## Endpoints

# List Files
- Endpoint: /list_files/{folder_name}
- Method: GET
- Parameters:
  - folder_name (str): Name of the folder to list files from.
  - count (int, optional): Index of the file to return (default is 0 for all files).
Example Request:
```bash
GET http://localhost:8000/list_files/files?count=3
```
# Filter Files by Name
- Endpoint: /filter_files/{folder_name}/{filename}/{characters}
- Method: GET
- Parameters:
  - folder_name (str): Name of the folder to filter files from.
  - filename (str): The filename prefix to filter by.
Example Request:
```bash
GET http://localhost:8000/list_files/files/e
```

# Shutdown
The server can be gracefully shut down by sending a SIGINT signal (Ctrl+C).

# Test cases:
There's few test cases that oyou can run. 
-  Install pytest
```bash
pip install pytest
```
-  Run the test cases
```bash
pytest test_cases.py
```


# Contributing
Feel free to contribute to this project by opening issues or creating pull requests. I welcome your suggestions and improvements.






















