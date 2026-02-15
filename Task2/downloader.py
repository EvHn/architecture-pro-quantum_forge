import sys
import urllib.request
import time
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

def fetch_html(url):
    """Загружает HTML по URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return None

def extract_main_text(html):
    """Извлекает основной текст из HTML"""
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()

def process_urls(input_file):
    """Обрабатывает файл с URL и сохраняет тексты"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Файл {input_file} не найден")
        return

    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            print(f"Пропуск строки (неверный формат): {line}")
            continue

        url = parts[0]
        filename = parts[1]

        print(f"Обработка: {url}")

        html = fetch_html(url)
        if not html:
            continue

        text = extract_main_text(html)

        # Сохраняем результат
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            print(f"  Ошибка сохранения: {e}")

        time.sleep(5)

def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <файл_с_url>")
        print("Формат файла: каждая строка: URL имя_файла.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    process_urls(input_file)

if __name__ == "__main__":
    main()