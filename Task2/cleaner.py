import sys
import os
from html.parser import HTMLParser
import re

class TextExtractor(HTMLParser):
    """Парсер для извлечения текста из HTML с удалением тегов"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.ignore_tags = {'script', 'style', 'noscript', 'meta'}
        self.in_ignore_tag = False

    def handle_starttag(self, tag, attrs):
        # Флаги для игнорирования содержимого определенных тегов
        if tag in self.ignore_tags:
            self.in_ignore_tag = True

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            self.in_ignore_tag = False
        # Добавляем пробелы после блоковых элементов для читаемости
        if tag in {'p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            self.text.append(' ')

    def handle_data(self, data):
        if not self.in_ignore_tag and data.strip():
            self.text.append(data)

    def get_text(self):
        # Объединяем текст и очищаем от лишних пробелов
        full_text = ''.join(self.text)
        # Заменяем множественные пробелы и переносы на одинарные
        cleaned = re.sub(r'\s+', ' ', full_text)
        return cleaned.strip()

def read_html_file(filepath):
    """Читает HTML из файла"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка чтения файла {filepath}: {e}")
        return None

def extract_main_text(html):
    """Извлекает основной текст из HTML"""
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()

def process_html_files(directory_path):
    """Обрабатывает HTML файлы в указанной директории"""
    if not os.path.exists(directory_path):
        print(f"Директория {directory_path} не найдена")
        return
    
    if not os.path.isdir(directory_path):
        print(f"{directory_path} не является директорией")
        return
    
    # Получаем список всех HTML файлов в директории
    html_files = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.html', '.htm')):
            html_files.append(os.path.join(directory_path, filename))
    
    if not html_files:
        print(f"В директории {directory_path} не найдено HTML файлов")
        return
    
    print(f"Найдено {len(html_files)} HTML файлов для обработки")
    
    for html_file in html_files:
        print(f"Обработка: {html_file}")
        
        html = read_html_file(html_file)
        if not html:
            continue
        
        text = extract_main_text(html)
        
        # Создаем имя для выходного файла
        base_name = os.path.splitext(os.path.basename(html_file))[0]
        output_file = os.path.join(directory_path, f"{base_name}.txt")
        
        # Сохраняем результат
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  Сохранено в: {output_file}")
        except Exception as e:
            print(f"  Ошибка сохранения: {e}")

def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <директория_с_html_файлами>")
        print("Скрипт обработает все HTML файлы в указанной директории")
        print("и сохранит извлеченный текст в текстовые файлы с тем же именем")
        sys.exit(1)

    directory_path = sys.argv[1]
    process_html_files(directory_path)

if __name__ == "__main__":
    main()