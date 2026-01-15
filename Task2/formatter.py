#!/usr/bin/env python3
"""
Скрипт для форматирования текстовых файлов:
расставляет переносы строк, не разрывая слова.
Максимальная длина строки - 120 символов.
"""

import os
import sys
import re

def format_line(text, max_length=120):
    """Форматирует одну строку, не разрывая слова"""
    if len(text) <= max_length:
        return text

    result = []
    current_line = []
    current_length = 0

    for word in text.split():
        word_len = len(word)

        # Если текущее слово помещается в строку
        if current_length + word_len + (1 if current_line else 0) <= max_length:
            current_line.append(word)
            current_length += word_len + (1 if current_line else 0)
        else:
            # Сохраняем текущую строку и начинаем новую
            if current_line:
                result.append(' '.join(current_line))
            current_line = [word]
            current_length = word_len

    # Добавляем последнюю строку
    if current_line:
        result.append(' '.join(current_line))

    return '\n'.join(result)

def process_file(filepath):
    """Обрабатывает один файл"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Разбиваем на абзацы (сохраняем пустые строки)
        paragraphs = re.split(r'(\n\s*\n)', content)
        formatted_paragraphs = []

        for para in paragraphs:
            if para.strip():  # Непустой абзац
                formatted_para = format_line(para.strip())
                formatted_paragraphs.append(formatted_para)
            else:  # Пустая строка/разделитель
                formatted_paragraphs.append(para)

        # Собираем обратно
        new_content = ''.join(formatted_paragraphs)

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False

    except (UnicodeDecodeError, PermissionError, OSError) as e:
        print(f"  Пропуск {filepath}: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <директория>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Ошибка: {directory} не является директорией")
        sys.exit(1)

    processed = 0
    skipped = 0

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            print(f"Обработка: {filepath}")

            if process_file(filepath):
                processed += 1
                print(f"  ✓ Отформатирован")
            else:
                skipped += 1
                print(f"  ○ Без изменений")

    print(f"\nИтог: обработано {processed} файлов, пропущено {skipped}")

if __name__ == "__main__":
    main()