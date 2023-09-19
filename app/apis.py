import os
import json
import asyncio
import signal
from datetime import datetime
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn

# Define the custom exception class HTTPNotImplemented
class HTTPNotImplemented(HTTPException):
    def __init__(self, detail: str = "Not Implemented", status_code: int = 501):
        super().__init__(detail=detail, status_code=status_code)

app = FastAPI()
folder_path = "C:\\Users\\zeesh\\Desktop\\Kambi\\files"
valid_file_types = ["txt", "jpg", "png", "pdf"]

# Create an asyncio event loop
loop = asyncio.get_event_loop()

# Variable to track whether the server is shutting down
shutdown_flag = False

async def list_files_async(folder_name: str, count: int, filename: Optional[str] = None) -> Dict:
    """
    Asynchronously list files in the specified folder.

    Args:
        folder_name (str): Name of the folder to list files from.
        count (int): Index of the file to return.
        filename (str, optional): Filter files by name prefix.

    Returns:
        Dict: A dictionary containing folder_name and files.
    """
    try:
        await asyncio.sleep(5)  # Simulate a blocking call
        if shutdown_flag:
            return {"error": "Server is shutting down"}

        image_folder = folder_path

        if not os.path.exists(image_folder):
            raise HTTPException(status_code=404, detail=f"Folder '{folder_name}' does not exist")
        elif not os.access(image_folder, os.R_OK):
            raise HTTPException(status_code=403, detail="You do not have permission to read this folder")

        file_list = []
        for file_name in os.listdir(image_folder):
            if filename and not file_name.startswith(filename):
                continue

            file_path = os.path.join(image_folder, file_name)
            file_stat = os.stat(file_path)
            is_directory = "Directory" if os.path.isdir(file_path) else "File"
            file_size = file_stat.st_size / 1024
            file_type = os.path.splitext(file_name)[1]

            modification_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            file_info = {
                "name": file_name,
                "date": modification_time,
                "type": is_directory,
                "size": file_size,
                "file_type": file_type
            }
            file_list.append(file_info)

        if count < 0 or count >= len(file_list):
            return {"error": "Invalid count parameter"}

        if count == 0:
            response_data = {
                "folder_name": folder_name,
                "files": file_list
            }
        else:
            response_data = {
                "folder_name": folder_name,
                "files": file_list[:count]
            }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.on_event("shutdown")
async def on_shutdown():
    global shutdown_flag
    shutdown_flag = True
    await asyncio.gather(*asyncio.all_tasks())

@app.get('/list_files/{folder_name}', response_model=Dict)
async def list_files(folder_name: str, count: int = Query(default=0, description='Index of the file to return')) -> Dict:
    """
    List files in the specified folder.

    Args:
        folder_name (str): Name of the folder to list files from.
        count (int): Index of the file to return.

    Returns:
        Dict: A dictionary containing folder_name and files.
    """
    try:
        if not isinstance(count, int) or count < 0:
            raise HTTPException(status_code=400, detail="Invalid count parameter: Count must be a non-negative integer.")

        result = await list_files_async(folder_name, count)

        return result

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

@app.get('/filter_files/{folder_name}/{filename}', response_model=Dict)
async def filter_files_by_name(folder_name: str, filename: str) -> Dict:
    """
    Filter files in the specified folder by name prefix.

    Args:
        folder_name (str): Name of the folder to filter files from.
        filename (str): The filename prefix to filter by.

    Returns:
        Dict: A dictionary containing folder_name and filtered files.
    """
    try:
        await asyncio.sleep(5)  # Simulate a blocking call
        result = await list_files_async(folder_name, 0)

        filtered_files = [file for file in result["files"] if file["name"].startswith(filename)]

        response_data = {
            "folder_name": folder_name,
            "files": filtered_files
        }

        return response_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

@app.get('/order_files_by_size/{folder_name}', response_model=Dict)
async def order_files_by_size(folder_name: str) -> Dict:
    """
    Order files in the specified folder by size in ascending order.

    Args:
        folder_name (str): Name of the folder to order files from.

    Returns:
        Dict: A dictionary containing folder_name and ordered files.
    """
    try:
        await asyncio.sleep(5)  # Simulate a blocking call
        result = await list_files_async(folder_name, 0)

        sorted_files = sorted(result["files"], key=lambda x: x["size"])

        response_data = {
            "folder_name": folder_name,
            "files": sorted_files
        }

        return response_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

@app.get('/filter_files_by_type/{folder_name}/{file_type}', response_model=Dict)
async def filter_files_by_type(folder_name: str, file_type: str) -> Dict:
    """
    Filter files in the specified folder by file type (extension).

    Args:
        folder_name (str): Name of the folder to filter files from.
        file_type (str): The file type (extension) to filter by.

    Returns:
        Dict: A dictionary containing folder_name and filtered files.
    """
    try:
        await asyncio.sleep(5)  # Simulate a blocking call
        result = await list_files_async(folder_name, 0)

        if file_type.lower() not in valid_file_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file_type}")

        filtered_files = [file for file in result["files"] if file["file_type"].lower() == f".{file_type.lower()}"]

        response_data = {
            "folder_name": folder_name,
            "files": filtered_files
        }

        return response_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

@app.exception_handler(HTTPNotImplemented)
async def handle_not_implemented_exception(request, exc):
    return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)

if __name__ == '__main__':
    def handle_sigint(signum, frame):
        loop.stop()
    signal.signal(signal.SIGINT, handle_sigint)

    uvicorn.run(app, host="0.0.0.0", port=8000, loop=loop)
