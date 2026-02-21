import re
import os
import sys

def load_dict(dict_path):
    """Загружает словарь замен из файла"""
    replacements = {}
    try:
        with open(dict_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '→' not in line:
                    continue
                old, new = line.split('→', 1)
                # Убираем кавычки и лишние пробелы
                old = old.strip().strip('"\'')
                new = new.strip().strip('"\'')
                if old:
                    replacements[old] = new
    except FileNotFoundError:
        print(f"Ошибка: файл словаря {dict_path} не найден")
        sys.exit(1)
    return replacements

def replace_in_file(filepath, replacements):
    """Заменяет слова в файле согласно словарю"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Сортируем ключи по убыванию длины для правильной заменки составных слов
        sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b')

        new_content = pattern.sub(lambda m: replacements[m.group(1)], content)

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except UnicodeDecodeError:
        print(f"Пропускаем бинарный файл: {filepath}")
        return False

def process_directory(dir_path, replacements):
    """Обрабатывает все файлы в директории"""
    changed_count = 0
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if replace_in_file(filepath, replacements):
                changed_count += 1
                print(f"Изменен: {filepath}")

    print(f"\nЗавершено. Изменено файлов: {changed_count}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <путь_к_словарю> <путь_к_директории>")
        sys.exit(1)

    dict_path = sys.argv[1]
    dir_path = sys.argv[2]

    if not os.path.isdir(dir_path):
        print(f"Ошибка: директория {dir_path} не существует")
        sys.exit(1)

    replacements = load_dict(dict_path)
    if not replacements:
        print("Словарь замен пуст")
        sys.exit(0)

    print(f"Загружено замен: {len(replacements)}")
    process_directory(dir_path, replacements)