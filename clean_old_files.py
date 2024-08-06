import os
import time


def clean_old_files(directory: str, days_old: int):
    now = time.time()
    cutoff = now - (days_old * 86400)  # 86400 секунд в дне

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and os.path.getmtime(file_path) < cutoff:
            os.remove(file_path)
            print(f"Deleted {file_path}")

if __name__ == "__main__":
    directory = "./uploads"  # Замените на вашу директорию
    days_old = 30  # Замените на нужное количество дней
    clean_old_files(directory, days_old)
