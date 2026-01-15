#!/usr/bin/env python3
"""
Скрипт для дополнения файла сгенерированными именами с помощью библиотеки Faker.
Формат файла: каждая строка содержит имя и стрелку → (без кавычек в примере).
Скрипт дополняет строки сгенерированными именами после стрелки.
"""

import sys
from faker import Faker


def process_file(file_path):
    """
    Читает файл, дополняет каждую строку сгенерированным именем и сохраняет изменения.

    Args:
        file_path (str): Путь к обрабатываемому файлу
    """
    fake = Faker()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified_lines = []
        for line in lines:
            line = line.strip()
            if '→' in line:
                # Дополняем строку сгенерированным именем в кавычках
                modified_line = f'{line} "{fake.first_name()}"'
            else:
                # Если нет стрелки, оставляем строку как есть
                modified_line = line
            modified_lines.append(modified_line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(modified_lines))

        print(f"Файл успешно обработан: {file_path}")

    except FileNotFoundError:
        print(f"Ошибка: файл не найден - {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь_к_файлу>")
        print('Пример: python script.py "data.txt"')
        sys.exit(1)

    process_file(sys.argv[1])