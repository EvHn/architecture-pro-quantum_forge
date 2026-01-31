import os
import sys

def rename_files(directory):
    # Получаем список файлов в директории (исключая поддиректории)
    try:
        files = [f for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print(f"Директория '{directory}' не найдена")
        sys.exit(1)

    # Сортируем для предсказуемого порядка нумерации
    files.sort()

    for i, filename in enumerate(files, 1):
        # Формируем новое имя
        new_name = f"file-{i}.txt"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)

        # Переименовываем файл
        os.rename(old_path, new_path)
        print(f"{filename} -> {new_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python script.py <директория>")
        sys.exit(1)

    rename_files(sys.argv[1])