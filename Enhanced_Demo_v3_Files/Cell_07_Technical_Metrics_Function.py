# ЯЧЕЙКА 7: Функция отображения технических метрик

print('📈 ОПРЕДЕЛЕНИЕ ФУНКЦИИ ТЕХНИЧЕСКИХ МЕТРИК')
print('=' * 60)

def show_technical_metrics(results, token_tracker):
    """Показывает краткие технические метрики в консоли"""
    
    print('\n📊 ТЕХНИЧЕСКИЕ МЕТРИКИ:')
    print('═' * 80)
    
    # Статистика по уровням агентов
    for level in ['executive', 'management', 'operational']:
        level_data = results.get(level)
        if level_data and level_data.get('success'):
            stats = level_data['stats']
            
            level_icon = '👑' if level == 'executive' else '⚙️' if level == 'management' else '🔧'
            model_type = 'GPT-4' if level == 'executive' else 'GPT-4o-mini'
            
            print(f'{level_icon} {level.upper()} ({model_type}):')
            print(f'├─ Агентов: {stats["successful_tests"]}/{stats["total_tests"]} ({stats["success_rate"]:.1f}%)')
            print(f'├─ Среднее время: {stats["avg_processing_time"]:.2f}с')
            print(f'├─ Качество: {stats["avg_quality_score"]:.1f}/100')
            
            # Токены для этого уровня
            if level in token_tracker.usage_by_level:
                level_usage = token_tracker.usage_by_level[level]
                print(f'├─ Токены: {level_usage["input"]:,} input + {level_usage["output"]:,} output')
                print(f'└─ Стоимость: ${level_usage["cost"]:.4f}')
            print()
    
    # Общая статистика токенов
    total_cost = token_tracker.get_total_cost()
    total_tokens = token_tracker.get_total_tokens()
    
    print('💰 ОБЩАЯ СТОИМОСТЬ:')
    print(f'├─ Всего токенов: {total_tokens:,}')
    print(f'├─ Общая стоимость: ${total_cost:.4f}')
    print(f'└─ Стоимость за токен: ${total_cost/max(1, total_tokens):.8f}')

print('✅ Функция show_technical_metrics определена!')
print('🎯 Переходите к следующей ячейке!')