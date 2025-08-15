# ЯЧЕЙКА 6: Функция отображения бизнес-истории пайплайна

print('📊 ОПРЕДЕЛЕНИЕ ФУНКЦИИ БИЗНЕС-ИСТОРИИ ПАЙПЛАЙНА')
print('=' * 60)

import time
import json
import asyncio
from datetime import datetime

def show_business_pipeline_story(pipeline_results):
    """Показывает бизнес-историю пайплайна в удобочитаемом формате"""
    
    print('\n🎯 БИЗНЕС-ИСТОРИЯ ПАЙПЛАЙНА:')
    print('═' * 80)
    
    if not pipeline_results or not pipeline_results.get('success'):
        print('❌ Пайплайн не выполнен или содержит ошибки')
        return
    
    pipelines = pipeline_results.get('pipelines', [])
    
    for i, pipeline in enumerate(pipelines, 1):
        pipeline_name = pipeline.get('name', f'Пайплайн {i}')
        print(f'\n🚀 {pipeline_name.upper()}')
        print('─' * 60)
        
        steps = pipeline.get('steps', [])
        for step_num, step in enumerate(steps, 1):
            agent_name = step.get('agent_name', 'Unknown Agent')
            business_action = step.get('business_action', 'Обработка данных')
            result_summary = step.get('result_summary', 'Результат получен')
            next_action = step.get('next_action', 'Переход к следующему этапу')
            
            # Иконки для разных типов агентов
            if 'qualification' in agent_name.lower():
                icon = '🔍'
            elif 'conversation' in agent_name.lower() or 'sales' in agent_name.lower():
                icon = '💬'
            elif 'proposal' in agent_name.lower():
                icon = '💰'
            elif 'seo' in agent_name.lower():
                icon = '🎯'
            else:
                icon = '⚙️'
            
            print(f'{icon} ЭТАП {step_num}: {business_action.upper()}')
            print(f'├─ {result_summary}')
            print(f'└─ NEXT: {next_action}')
            print()
        
        # Итоговый результат пайплайна
        final_result = pipeline.get('final_result', {})
        success_rate = final_result.get('success_rate', 0)
        business_value = final_result.get('business_value', 'Не определено')
        
        print(f'🎯 ИТОГОВЫЙ РЕЗУЛЬТАТ:')
        print(f'├─ Успешность: {success_rate}%')
        print(f'└─ Бизнес-ценность: {business_value}')
        print('═' * 60)

print('✅ Функция show_business_pipeline_story определена!')
print('🎯 Переходите к следующей ячейке!')