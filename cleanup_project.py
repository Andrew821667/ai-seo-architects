#!/usr/bin/env python3
"""
Скрипт для очистки проекта AI SEO Architects от временных и лишних файлов
Анализирует структуру проекта и предлагает файлы для удаления
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import re

class ProjectCleaner:
    """Класс для анализа и очистки проекта"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.files_to_remove = []
        self.directories_to_remove = []
        self.analysis_results = {}
    
    def analyze_project(self):
        """Анализируем проект на предмет лишних файлов"""
        print("🔍 АНАЛИЗ ПРОЕКТА НА ПРЕДМЕТ ЛИШНИХ ФАЙЛОВ")
        print("=" * 60)
        
        # Категории файлов для анализа
        self.analyze_temporary_files()
        self.analyze_test_result_files()
        self.analyze_duplicate_vector_stores()
        self.analyze_backup_files()
        self.analyze_development_files()
        self.analyze_empty_directories()
        
        self.generate_cleanup_report()
    
    def analyze_temporary_files(self):
        """Анализируем временные файлы"""
        print("\n📁 Анализ временных файлов...")
        
        temp_patterns = [
            r'.*_\d{8}_\d{6}\.md$',  # Файлы с timestamp
            r'.*\.tmp$',
            r'.*\.temp$',
            r'.*~$',
            r'__pycache__',
            r'\.pyc$',
            r'\.DS_Store$'
        ]
        
        temp_files = []
        
        for pattern in temp_patterns:
            for file_path in self.project_root.rglob('*'):
                if re.search(pattern, str(file_path)):
                    temp_files.append(file_path)
        
        # Специфичные временные файлы
        specific_temp_files = [
            'AGENT_TEST_RESULTS_20250805_210750.md',
            'AGENT_TEST_RESULTS_20250805_210913.md', 
            'AGENT_TEST_RESULTS_20250805_211014.md',
            'COMPREHENSIVE_AGENT_ANALYSIS_20250805_212658.md',
            'COMPREHENSIVE_AGENT_ANALYSIS_20250805_212748.md',
            'COMPREHENSIVE_AGENT_ANALYSIS_20250805_212939.md',
            'COMPREHENSIVE_AGENT_ANALYSIS_20250805_213029.md',
            'DEMO_RESULTS_20250805_211112.md',
            'DEMO_RESULTS_20250805_211649.md',
            'DEMO_RESULTS_20250805_211902.md',
            'DEMO_RESULTS_20250805_211934.md',
            'DEMO_RESULTS_20250805_212024.md',
            'DEMO_RESULTS_20250805_212105.md',
            'TESTING_BREAKTHROUGH_RESULTS.md'
        ]
        
        for filename in specific_temp_files:
            file_path = self.project_root / filename
            if file_path.exists():
                temp_files.append(file_path)
        
        self.analysis_results['temporary_files'] = temp_files
        print(f"   Найдено временных файлов: {len(temp_files)}")
    
    def analyze_test_result_files(self):
        """Анализируем файлы результатов тестирования"""
        print("\n🧪 Анализ файлов результатов тестирования...")
        
        test_result_files = []
        
        # Паттерны для тестовых файлов
        test_patterns = [
            r'test_.*\.py$',
            r'.*_test\.py$'
        ]
        
        # Сохраняем основные тестовые файлы, но проверяем дубликаты
        main_test_files = [
            'test_agents_integration.py',
            'test_api_endpoints.py', 
            'test_faiss_integration.py',
            'test_mcp_integration.py'
        ]
        
        # Файлы которые можно удалить (дубликаты или устаревшие)
        redundant_test_files = [
            'test_enhanced_integration.py',  # Дубликат
            'test_rag_integration.py',       # Устарел
            'test_real_data_demo.py',        # Демо версия
            'quick_demo_test.py',            # Быстрый демо тест
            'comprehensive_agent_test.py',   # Устарел
            'analyze_knowledge_quality.py', # Временный анализ
            'test_russian_agents_integration.py',  # Специфичный тест - можно оставить
            'test_all_agents_vectorization.py',    # Специфичный тест - можно оставить  
            'update_vectorization.py'       # Утилита - можно оставить после использования
        ]
        
        for filename in redundant_test_files[:-3]:  # Исключаем последние 3
            file_path = self.project_root / filename
            if file_path.exists():
                test_result_files.append(file_path)
        
        self.analysis_results['test_files'] = test_result_files
        print(f"   Найдено избыточных тестовых файлов: {len(test_result_files)}")
    
    def analyze_duplicate_vector_stores(self):
        """Анализируем дублированные векторные хранилища"""
        print("\n🗂️ Анализ дублированных векторных хранилищ...")
        
        vector_stores_path = self.project_root / 'data' / 'vector_stores'
        duplicate_stores = []
        
        if vector_stores_path.exists():
            # Ищем дубликаты с суффиксом _agent
            for item in vector_stores_path.iterdir():
                if item.is_dir() and item.name.endswith('_agent'):
                    base_name = item.name[:-6]  # Убираем _agent
                    base_dir = vector_stores_path / base_name
                    
                    if base_dir.exists():
                        # Есть дубликат - можем удалить версию с _agent
                        duplicate_stores.append(item)
                        print(f"   Дубликат найден: {item.name} -> {base_name}")
        
        self.analysis_results['duplicate_vectors'] = duplicate_stores
        print(f"   Найдено дублированных векторных хранилищ: {len(duplicate_stores)}")
    
    def analyze_backup_files(self):
        """Анализируем backup файлы"""
        print("\n💾 Анализ backup файлов...")
        
        backup_dirs = []
        data_path = self.project_root / 'data'
        
        if data_path.exists():
            for item in data_path.iterdir():
                if item.is_dir() and 'backup' in item.name:
                    backup_dirs.append(item)
        
        self.analysis_results['backup_dirs'] = backup_dirs
        print(f"   Найдено backup директорий: {len(backup_dirs)}")
        
        # Можем оставить самый свежий backup и удалить старые
        if backup_dirs:
            sorted_backups = sorted(backup_dirs, key=lambda x: x.stat().st_mtime, reverse=True)
            old_backups = sorted_backups[1:]  # Все кроме самого свежего
            
            self.analysis_results['old_backups'] = old_backups
            print(f"   Старых backup'ов для удаления: {len(old_backups)}")
    
    def analyze_development_files(self):
        """Анализируем файлы разработки"""
        print("\n🔧 Анализ файлов разработки...")
        
        dev_files = []
        
        # Файлы которые были созданы в процессе разработки
        potential_dev_files = [
            'setup_seo_ai_models.py',  # Устарел если интеграция не нужна
            '1.md',                    # Временный файл правил
        ]
        
        # Проверяем какие из них существуют
        for filename in potential_dev_files:
            file_path = self.project_root / filename
            if file_path.exists():
                # Проверяем содержимое 1.md
                if filename == '1.md':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if len(content.strip()) < 100:  # Если файл почти пустой
                            dev_files.append(file_path)
                else:
                    dev_files.append(file_path)
        
        self.analysis_results['dev_files'] = dev_files
        print(f"   Найдено файлов разработки: {len(dev_files)}")
    
    def analyze_empty_directories(self):
        """Анализируем пустые директории"""
        print("\n📁 Анализ пустых директорий...")
        
        empty_dirs = []
        
        for root, dirs, files in os.walk(self.project_root):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                
                # Проверяем что директория пустая или содержит только __init__.py
                try:
                    contents = list(dir_path.iterdir())
                    if not contents:
                        empty_dirs.append(dir_path)
                    elif len(contents) == 1 and contents[0].name == '__init__.py':
                        # Проверяем что __init__.py пустой
                        init_file = contents[0]
                        if init_file.stat().st_size < 50:  # Меньше 50 байт
                            empty_dirs.append(dir_path)
                except PermissionError:
                    continue
        
        # Исключаем системные директории
        system_dirs = ['__pycache__', '.git', '.pytest_cache', 'chroma_db']
        empty_dirs = [d for d in empty_dirs if d.name not in system_dirs]
        
        self.analysis_results['empty_dirs'] = empty_dirs
        print(f"   Найдено потенциально пустых директорий: {len(empty_dirs)}")
    
    def generate_cleanup_report(self):
        """Генерируем отчет по очистке"""
        print("\n" + "=" * 60)
        print("📋 ОТЧЕТ ПО ОЧИСТКЕ ПРОЕКТА")
        print("=" * 60)
        
        total_files = 0
        total_size = 0
        
        # Подсчитываем общую статистику
        for category, files in self.analysis_results.items():
            if files:
                category_size = 0
                for file_path in files:
                    if file_path.exists():
                        if file_path.is_file():
                            size = file_path.stat().st_size
                            category_size += size
                        elif file_path.is_dir():
                            # Подсчитываем размер директории
                            for root, dirs, filenames in os.walk(file_path):
                                for filename in filenames:
                                    fp = Path(root) / filename
                                    if fp.exists():
                                        category_size += fp.stat().st_size
                
                total_files += len(files)
                total_size += category_size
                
                print(f"\n📂 {category.upper().replace('_', ' ')}:")
                print(f"   Файлов/директорий: {len(files)}")
                print(f"   Размер: {self.format_size(category_size)}")
                
                # Показываем первые несколько файлов
                for i, file_path in enumerate(files[:3]):
                    rel_path = file_path.relative_to(self.project_root)
                    print(f"   • {rel_path}")
                
                if len(files) > 3:
                    print(f"   ... и еще {len(files) - 3} файлов")
        
        print(f"\n🎯 ОБЩАЯ СТАТИСТИКА:")
        print(f"   Всего файлов для удаления: {total_files}")
        print(f"   Общий размер: {self.format_size(total_size)}")
        
        return total_files > 0
    
    def format_size(self, size_bytes: int) -> str:
        """Форматируем размер файла"""
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB']
        size = float(size_bytes)
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.1f} {units[unit_index]}"
    
    def confirm_cleanup(self) -> bool:
        """Запрашиваем подтверждение на удаление"""
        print("\n" + "=" * 60)
        print("⚠️  ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ")
        print("=" * 60)
        
        print("🔥 ВНИМАНИЕ! Следующие файлы и директории будут УДАЛЕНЫ:")
        
        for category, files in self.analysis_results.items():
            if files:
                print(f"\n📂 {category.upper().replace('_', ' ')}:")
                for file_path in files:
                    rel_path = file_path.relative_to(self.project_root)
                    print(f"   🗑️  {rel_path}")
        
        print(f"\n❓ Продолжить удаление? (yes/no): ", end="")
        response = input().strip().lower()
        
        return response in ['yes', 'y', 'да', 'д']
    
    def perform_cleanup(self):
        """Выполняем очистку"""
        print("\n🧹 ВЫПОЛНЕНИЕ ОЧИСТКИ...")
        print("-" * 40)
        
        removed_count = 0
        errors = []
        
        for category, files in self.analysis_results.items():
            if files:
                print(f"\n📂 Очистка {category.replace('_', ' ')}...")
                
                for file_path in files:
                    try:
                        if file_path.exists():
                            if file_path.is_file():
                                file_path.unlink()
                                print(f"   ✅ Удален файл: {file_path.name}")
                            elif file_path.is_dir():
                                shutil.rmtree(file_path)
                                print(f"   ✅ Удалена директория: {file_path.name}")
                            
                            removed_count += 1
                        
                    except Exception as e:
                        error_msg = f"Ошибка удаления {file_path}: {e}"
                        errors.append(error_msg)
                        print(f"   ❌ {error_msg}")
        
        print(f"\n🎉 ОЧИСТКА ЗАВЕРШЕНА!")
        print(f"   ✅ Удалено: {removed_count} элементов")
        
        if errors:
            print(f"   ⚠️ Ошибок: {len(errors)}")
            for error in errors:
                print(f"      • {error}")
        else:
            print(f"   🏆 Без ошибок!")


def main():
    """Основная функция"""
    print("🚀 СИСТЕМА ОЧИСТКИ ПРОЕКТА AI SEO ARCHITECTS")
    print(f"🕒 Время запуска: {datetime.now().isoformat()}")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    cleaner = ProjectCleaner(project_root)
    
    try:
        # Анализируем проект
        cleaner.analyze_project()
        
        # Проверяем есть ли что удалять
        has_files_to_remove = any(files for files in cleaner.analysis_results.values())
        
        if not has_files_to_remove:
            print("\n✨ ПРОЕКТ УЖЕ ЧИСТЫЙ!")
            print("   Лишних файлов не найдено")
            return
        
        # Запрашиваем подтверждение
        if cleaner.confirm_cleanup():
            cleaner.perform_cleanup()
        else:
            print("\n👋 Очистка отменена пользователем")
    
    except KeyboardInterrupt:
        print("\n👋 Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()