# import os
# def save_file(filename: str, content: bytes) -> str:
#     upload_dir = "./uploads"
#     if not os.path.exists(upload_dir):
#         os.makedirs(upload_dir)
#
#     file_path = os.path.join(upload_dir, filename)
#     with open(file_path, 'wb') as f:
#         f.write(content)
#
#     return file_path
import os

def save_file(filename: str, content: bytes) -> str:
    directory = "./uploads"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, 'wb') as f:
        f.write(content)
    return file_path