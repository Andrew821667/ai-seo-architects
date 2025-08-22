# Тема 22: Парсинг данных для ИИ систем

## Основы парсинга

### Типы парсинга данных
- **HTML/XML парсинг**: Извлечение данных из веб-страниц
- **JSON парсинг**: Обработка структурированных данных API
- **CSV парсинг**: Табличные данные и отчеты
- **PDF парсинг**: Извлечение текста из документов
- **Парсинг естественного языка**: NLP обработка текстов

### Инструменты и библиотеки
```python
# Основные библиотеки для парсинга
import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import re
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict, Optional

# Настройка сессии для веб-скрепинга
class WebScraper:
    def __init__(self, delay: float = 1.0):
        self.session = requests.Session()
        self.delay = delay
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Безопасное получение и парсинг страницы"""
        try:
            time.sleep(self.delay)  # Уважение к серверу
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'html.parser')
        
        except requests.RequestException as e:
            print(f"Ошибка при получении {url}: {e}")
            return None
    
    def extract_text_content(self, soup: BeautifulSoup, 
                           remove_tags: List[str] = None) -> str:
        """Извлечение чистого текста"""
        if remove_tags:
            for tag in remove_tags:
                for element in soup.find_all(tag):
                    element.decompose()
        
        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        # Очистка текста
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text

# Пример использования
scraper = WebScraper(delay=1.0)
```

## HTML/XML парсинг

### Извлечение структурированных данных
```python
class HTMLDataExtractor:
    def __init__(self, scraper: WebScraper):
        self.scraper = scraper
    
    def extract_articles(self, url: str) -> List[Dict]:
        """Извлечение статей с новостного сайта"""
        soup = self.scraper.get_page(url)
        if not soup:
            return []
        
        articles = []
        
        # Поиск статей по различным селекторам
        article_selectors = [
            'article',
            '.article',
            '.news-item',
            '.post',
            '[itemtype*="Article"]'
        ]
        
        for selector in article_selectors:
            elements = soup.select(selector)
            if elements:
                break
        
        for element in elements:
            article_data = self._extract_article_data(element)
            if article_data:
                articles.append(article_data)
        
        return articles
    
    def _extract_article_data(self, element) -> Optional[Dict]:
        """Извлечение данных одной статьи"""
        try:
            # Заголовок
            title_selectors = ['h1', 'h2', 'h3', '.title', '.headline']
            title = self._find_text_by_selectors(element, title_selectors)
            
            # Описание/аннотация
            desc_selectors = ['.description', '.excerpt', '.summary', 'p']
            description = self._find_text_by_selectors(element, desc_selectors)
            
            # Ссылка
            link_element = element.find('a')
            link = link_element.get('href') if link_element else None
            
            # Дата
            date_selectors = ['.date', '.published', 'time', '[datetime]']
            date = self._find_text_by_selectors(element, date_selectors)
            
            # Автор
            author_selectors = ['.author', '.by', '.writer']
            author = self._find_text_by_selectors(element, author_selectors)
            
            if title:  # Минимальное требование
                return {
                    'title': title.strip(),
                    'description': description.strip() if description else '',
                    'link': link,
                    'date': date.strip() if date else '',
                    'author': author.strip() if author else '',
                    'content': element.get_text().strip()
                }
        
        except Exception as e:
            print(f"Ошибка извлечения данных статьи: {e}")
        
        return None
    
    def _find_text_by_selectors(self, element, selectors: List[str]) -> Optional[str]:
        """Поиск текста по списку селекторов"""
        for selector in selectors:
            found = element.select_one(selector)
            if found:
                return found.get_text()
        return None
    
    def extract_product_info(self, url: str) -> Dict:
        """Извлечение информации о товаре с e-commerce сайта"""
        soup = self.scraper.get_page(url)
        if not soup:
            return {}
        
        product_info = {}
        
        # Название товара
        name_selectors = ['h1', '.product-title', '.item-name', '#product-name']
        product_info['name'] = self._find_text_by_selectors(soup, name_selectors)
        
        # Цена
        price_selectors = ['.price', '.cost', '.amount', '[data-price]']
        price_text = self._find_text_by_selectors(soup, price_selectors)
        if price_text:
            # Извлекаем число из текста цены
            price_match = re.search(r'[\d\s,]+', price_text.replace(' ', ''))
            if price_match:
                product_info['price'] = price_match.group().replace(',', '.')
        
        # Описание
        desc_selectors = ['.description', '.product-desc', '.details']
        product_info['description'] = self._find_text_by_selectors(soup, desc_selectors)
        
        # Изображения
        img_elements = soup.find_all('img')
        images = []
        for img in img_elements:
            src = img.get('src') or img.get('data-src')
            if src and ('product' in src.lower() or 'item' in src.lower()):
                images.append(urljoin(url, src))
        product_info['images'] = images[:5]  # Первые 5 изображений
        
        # Характеристики
        specs = {}
        
        # Поиск таблиц характеристик
        spec_tables = soup.find_all('table', class_=re.compile(r'spec|attr|prop'))
        for table in spec_tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) == 2:
                    key = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    specs[key] = value
        
        # Поиск списков характеристик
        spec_lists = soup.find_all(['dl', 'ul'], class_=re.compile(r'spec|attr|prop'))
        for spec_list in spec_lists:
            if spec_list.name == 'dl':
                dts = spec_list.find_all('dt')
                dds = spec_list.find_all('dd')
                for dt, dd in zip(dts, dds):
                    specs[dt.get_text().strip()] = dd.get_text().strip()
        
        product_info['specifications'] = specs
        
        return product_info

# Пример использования
extractor = HTMLDataExtractor(scraper)

# Извлечение статей
# articles = extractor.extract_articles("https://example-news.com")
# print(f"Найдено {len(articles)} статей")

# Извлечение информации о товаре
# product = extractor.extract_product_info("https://example-shop.com/product/123")
# print(f"Товар: {product.get('name', 'N/A')}")
```

### Работа с формами и динамическим контентом
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class DynamicContentScraper:
    def __init__(self, headless: bool = True):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = None
    
    def __enter__(self):
        self.driver = webdriver.Chrome(options=self.options)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
    
    def scrape_spa_content(self, url: str, wait_element: str) -> BeautifulSoup:
        """Скрепинг SPA приложений с ожиданием загрузки"""
        self.driver.get(url)
        
        # Ждем загрузки контента
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, wait_element))
            )
        except Exception as e:
            print(f"Элемент {wait_element} не найден: {e}")
        
        # Получаем HTML после выполнения JavaScript
        html = self.driver.page_source
        return BeautifulSoup(html, 'html.parser')
    
    def fill_search_form(self, url: str, search_params: Dict) -> BeautifulSoup:
        """Заполнение поисковой формы и получение результатов"""
        self.driver.get(url)
        
        # Заполняем форму
        for field_name, value in search_params.items():
            try:
                # Пробуем разные способы поиска поля
                field_selectors = [
                    f'input[name="{field_name}"]',
                    f'input[id="{field_name}"]',
                    f'#{field_name}',
                    f'.{field_name}'
                ]
                
                field_element = None
                for selector in field_selectors:
                    try:
                        field_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if field_element:
                    field_element.clear()
                    field_element.send_keys(value)
                
            except Exception as e:
                print(f"Не удалось заполнить поле {field_name}: {e}")
        
        # Отправляем форму
        submit_selectors = [
            'input[type="submit"]',
            'button[type="submit"]',
            '.submit-btn',
            '#submit',
            'button:contains("Search")'
        ]
        
        for selector in submit_selectors:
            try:
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                submit_btn.click()
                break
            except:
                continue
        
        # Ждем загрузки результатов
        time.sleep(3)
        
        return BeautifulSoup(self.driver.page_source, 'html.parser')

# Пример использования Selenium
def scrape_dynamic_site():
    with DynamicContentScraper() as scraper:
        # Скрепинг SPA
        soup = scraper.scrape_spa_content(
            "https://example-spa.com", 
            ".content-loaded"
        )
        
        # Поиск через форму
        search_results = scraper.fill_search_form(
            "https://example-search.com",
            {"query": "машинное обучение", "category": "ai"}
        )
        
        return soup, search_results
```

## Парсинг API и JSON данных

### Работа с REST API
```python
import requests
from typing import Iterator, Union
import json
import time

class APIParser:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def paginated_request(self, endpoint: str, params: Dict = None, 
                         page_param: str = 'page') -> Iterator[Dict]:
        """Получение данных с пагинацией"""
        page = 1
        params = params or {}
        
        while True:
            params[page_param] = page
            
            try:
                response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Разные форматы ответов
                if isinstance(data, list):
                    items = data
                elif 'data' in data:
                    items = data['data']
                elif 'results' in data:
                    items = data['results']
                else:
                    items = [data]
                
                if not items:
                    break
                
                for item in items:
                    yield item
                
                # Проверка наличия следующей страницы
                if 'next' not in data and len(items) < params.get('per_page', 100):
                    break
                
                page += 1
                time.sleep(0.5)  # Ограничение скорости запросов
                
            except requests.RequestException as e:
                print(f"Ошибка API запроса: {e}")
                break
    
    def batch_request(self, endpoints: List[str]) -> Dict[str, Dict]:
        """Пакетные запросы к API"""
        results = {}
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{self.base_url}/{endpoint}")
                response.raise_for_status()
                results[endpoint] = response.json()
                
            except requests.RequestException as e:
                print(f"Ошибка запроса {endpoint}: {e}")
                results[endpoint] = None
            
            time.sleep(0.2)  # Небольшая задержка
        
        return results
    
    def extract_nested_data(self, data: Union[Dict, List], 
                           path: str) -> List[any]:
        """Извлечение вложенных данных по пути"""
        def get_nested_value(obj, keys):
            for key in keys:
                if isinstance(obj, dict) and key in obj:
                    obj = obj[key]
                elif isinstance(obj, list) and key.isdigit():
                    try:
                        obj = obj[int(key)]
                    except (IndexError, ValueError):
                        return None
                else:
                    return None
            return obj
        
        keys = path.split('.')
        
        if isinstance(data, list):
            results = []
            for item in data:
                value = get_nested_value(item, keys)
                if value is not None:
                    results.append(value)
            return results
        else:
            value = get_nested_value(data, keys)
            return [value] if value is not None else []

# Пример работы с различными API
class NewsAPIParser(APIParser):
    def __init__(self, api_key: str):
        super().__init__("https://newsapi.org/v2", api_key)
    
    def get_headlines(self, country: str = 'ru', category: str = None) -> List[Dict]:
        """Получение новостных заголовков"""
        params = {'country': country}
        if category:
            params['category'] = category
        
        articles = []
        for article in self.paginated_request('top-headlines', params):
            cleaned_article = {
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'published_at': article.get('publishedAt'),
                'source': article.get('source', {}).get('name'),
                'content_preview': article.get('content', '')[:200]
            }
            articles.append(cleaned_article)
        
        return articles

class GitHubAPIParser(APIParser):
    def __init__(self, token: str = None):
        super().__init__("https://api.github.com", token)
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """Получение информации о репозитории"""
        try:
            response = self.session.get(f"{self.base_url}/repos/{owner}/{repo}")
            response.raise_for_status()
            
            repo_data = response.json()
            
            return {
                'name': repo_data.get('name'),
                'description': repo_data.get('description'),
                'stars': repo_data.get('stargazers_count'),
                'forks': repo_data.get('forks_count'),
                'language': repo_data.get('language'),
                'created_at': repo_data.get('created_at'),
                'updated_at': repo_data.get('updated_at'),
                'topics': repo_data.get('topics', []),
                'size': repo_data.get('size'),
                'open_issues': repo_data.get('open_issues_count')
            }
        
        except requests.RequestException as e:
            print(f"Ошибка получения данных репозитория: {e}")
            return {}

# Пример использования
# news_parser = NewsAPIParser("your-api-key")
# headlines = news_parser.get_headlines(country='us', category='technology')

# github_parser = GitHubAPIParser("your-github-token")
# repo_info = github_parser.get_repo_info("microsoft", "vscode")
```

## Обработка файлов и документов

### Парсинг CSV и Excel файлов
```python
import pandas as pd
from typing import Generator, Dict, List
import chardet

class FileParser:
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """Определение кодировки файла"""
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    
    @staticmethod
    def parse_csv_chunked(file_path: str, chunk_size: int = 1000) -> Generator[pd.DataFrame, None, None]:
        """Парсинг больших CSV файлов по частям"""
        encoding = FileParser.detect_encoding(file_path)
        
        try:
            for chunk in pd.read_csv(file_path, encoding=encoding, chunksize=chunk_size):
                # Очистка данных
                chunk = chunk.dropna(how='all')  # Удаляем полностью пустые строки
                chunk = chunk.fillna('')  # Заполняем пустые ячейки
                
                yield chunk
                
        except Exception as e:
            print(f"Ошибка парсинга CSV: {e}")
    
    @staticmethod
    def parse_excel_sheets(file_path: str) -> Dict[str, pd.DataFrame]:
        """Парсинг всех листов Excel файла"""
        try:
            # Получаем список всех листов
            xl_file = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet_name in xl_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Базовая очистка
                df = df.dropna(how='all')
                df.columns = df.columns.astype(str)  # Преобразуем названия колонок в строки
                
                sheets_data[sheet_name] = df
            
            return sheets_data
            
        except Exception as e:
            print(f"Ошибка парсинга Excel: {e}")
            return {}
    
    @staticmethod
    def extract_structured_data(df: pd.DataFrame, 
                              column_mapping: Dict[str, str] = None) -> List[Dict]:
        """Извлечение структурированных данных из DataFrame"""
        if column_mapping:
            # Переименование колонок согласно маппингу
            df = df.rename(columns=column_mapping)
        
        # Преобразование в список словарей
        records = []
        for _, row in df.iterrows():
            record = {}
            for col in df.columns:
                value = row[col]
                
                # Обработка различных типов данных
                if pd.isna(value):
                    record[col] = None
                elif isinstance(value, (int, float)):
                    record[col] = value
                else:
                    record[col] = str(value).strip()
            
            records.append(record)
        
        return records

# Пример использования
def process_sales_data():
    parser = FileParser()
    
    # Парсинг CSV по частям
    total_sales = 0
    product_counts = {}
    
    for chunk in parser.parse_csv_chunked('sales_data.csv', chunk_size=5000):
        # Обработка каждого чанка
        if 'amount' in chunk.columns:
            total_sales += chunk['amount'].sum()
        
        if 'product' in chunk.columns:
            for product in chunk['product'].value_counts().items():
                product_counts[product[0]] = product_counts.get(product[0], 0) + product[1]
    
    print(f"Общие продажи: {total_sales}")
    print(f"Топ товары: {sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]}")
    
    # Парсинг Excel
    excel_data = parser.parse_excel_sheets('report.xlsx')
    for sheet_name, df in excel_data.items():
        print(f"Лист '{sheet_name}': {len(df)} строк, {len(df.columns)} колонок")
```

### Парсинг PDF документов
```python
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
from typing import Dict, List, Tuple

class PDFParser:
    @staticmethod
    def extract_text_pypdf2(pdf_path: str) -> str:
        """Простое извлечение текста с помощью PyPDF2"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        
        except Exception as e:
            print(f"Ошибка PyPDF2: {e}")
        
        return text
    
    @staticmethod
    def extract_structured_content(pdf_path: str) -> Dict:
        """Извлечение структурированного контента с помощью pdfplumber"""
        content = {
            'text': '',
            'tables': [],
            'metadata': {},
            'pages': []
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                content['metadata'] = pdf.metadata
                
                for page_num, page in enumerate(pdf.pages):
                    page_content = {
                        'page_number': page_num + 1,
                        'text': '',
                        'tables': []
                    }
                    
                    # Извлечение текста
                    page_text = page.extract_text()
                    if page_text:
                        page_content['text'] = page_text
                        content['text'] += page_text + "\n"
                    
                    # Извлечение таблиц
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            # Преобразуем таблицу в более удобный формат
                            table_data = []
                            headers = table[0] if table else []
                            
                            for row in table[1:]:
                                row_dict = {}
                                for i, cell in enumerate(row):
                                    header = headers[i] if i < len(headers) else f'column_{i}'
                                    row_dict[header] = cell
                                table_data.append(row_dict)
                            
                            page_content['tables'].append(table_data)
                            content['tables'].extend(table_data)
                    
                    content['pages'].append(page_content)
        
        except Exception as e:
            print(f"Ошибка pdfplumber: {e}")
        
        return content
    
    @staticmethod
    def extract_with_layout(pdf_path: str) -> Dict:
        """Извлечение с сохранением макета с помощью PyMuPDF"""
        content = {
            'text_blocks': [],
            'images': [],
            'annotations': [],
            'fonts': set()
        }
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Извлечение текстовых блоков с форматированием
                blocks = page.get_text("dict")
                
                for block in blocks["blocks"]:
                    if "lines" in block:  # Текстовый блок
                        for line in block["lines"]:
                            for span in line["spans"]:
                                content['text_blocks'].append({
                                    'page': page_num + 1,
                                    'text': span["text"],
                                    'font': span["font"],
                                    'size': span["size"],
                                    'bbox': span["bbox"]
                                })
                                content['fonts'].add(span["font"])
                
                # Извлечение изображений
                image_list = page.get_images()
                for img_index, img in enumerate(image_list):
                    content['images'].append({
                        'page': page_num + 1,
                        'index': img_index,
                        'xref': img[0]
                    })
                
                # Извлечение аннотаций
                annotations = page.annots()
                for annot in annotations:
                    content['annotations'].append({
                        'page': page_num + 1,
                        'type': annot.type[1],
                        'content': annot.content,
                        'rect': annot.rect
                    })
            
            doc.close()
            
        except Exception as e:
            print(f"Ошибка PyMuPDF: {e}")
        
        content['fonts'] = list(content['fonts'])
        return content

# Пример анализа PDF документа
def analyze_pdf_document(pdf_path: str) -> Dict:
    """Комплексный анализ PDF документа"""
    parser = PDFParser()
    
    # Извлекаем структурированный контент
    structured_content = parser.extract_structured_content(pdf_path)
    
    # Извлекаем контент с макетом
    layout_content = parser.extract_with_layout(pdf_path)
    
    # Анализируем содержание
    analysis = {
        'total_pages': len(structured_content['pages']),
        'total_text_length': len(structured_content['text']),
        'total_tables': len(structured_content['tables']),
        'metadata': structured_content['metadata'],
        'fonts_used': layout_content['fonts'],
        'images_count': len(layout_content['images']),
        'annotations_count': len(layout_content['annotations'])
    }
    
    # Анализ текста по страницам
    page_analysis = []
    for page in structured_content['pages']:
        page_stats = {
            'page_number': page['page_number'],
            'text_length': len(page['text']),
            'tables_count': len(page['tables']),
            'has_content': bool(page['text'] or page['tables'])
        }
        page_analysis.append(page_stats)
    
    analysis['page_analysis'] = page_analysis
    
    return analysis

# Пример использования
# pdf_analysis = analyze_pdf_document('document.pdf')
# print(f"Документ содержит {pdf_analysis['total_pages']} страниц")
# print(f"Общая длина текста: {pdf_analysis['total_text_length']} символов")
# print(f"Найдено таблиц: {pdf_analysis['total_tables']}")
```

## Ключевые моменты для экзамена

### Основные инструменты парсинга
1. **BeautifulSoup**: HTML/XML парсинг
2. **Selenium**: Динамический контент и формы
3. **Requests**: HTTP запросы и API
4. **Pandas**: Структурированные данные (CSV/Excel)
5. **PyPDF2/pdfplumber**: PDF документы

### Стратегии парсинга
- **Respectful scraping**: Задержки, robots.txt, rate limiting
- **Error handling**: Обработка сетевых ошибок и исключений  
- **Data validation**: Проверка и очистка извлеченных данных
- **Scalability**: Пагинация, chunking, параллельная обработка

### Практические техники
- Использование селекторов CSS и XPath
- Обработка различных кодировок
- Извлечение метаданных и структурированных данных
- Работа с формами и AJAX запросами
- Кэширование и оптимизация запросов

### Этические и правовые аспекты
- Соблюдение robots.txt и Terms of Service
- Ограничение скорости запросов
- Уважение к серверным ресурсам
- Получение разрешений при необходимости