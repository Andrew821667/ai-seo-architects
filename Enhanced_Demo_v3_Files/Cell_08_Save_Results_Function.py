# ЯЧЕЙКА 8: Функция сохранения детальных результатов

print('💾 ОПРЕДЕЛЕНИЕ ФУНКЦИИ СОХРАНЕНИЯ РЕЗУЛЬТАТОВ')
print('=' * 60)

def save_detailed_results(results, token_tracker):
    """Сохраняет полные результаты в JSON и markdown файлы"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Детальные результаты в JSON
    detailed_data = {
        "timestamp": datetime.now().isoformat(),
        "demo_results": results,
        "token_usage": {
            "by_level": token_tracker.usage_by_level,
            "by_agent": token_tracker.agent_details,
            "total_cost": token_tracker.get_total_cost(),
            "total_tokens": token_tracker.get_total_tokens()
        },
        "pricing_model": {
            "gpt-4": {"input": 0.01, "output": 0.03},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006}
        }
    }
    
    with open(f'demo_results_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(detailed_data, f, ensure_ascii=False, indent=2)
    
    # 2. Executive summary в Markdown
    with open(f'executive_summary_{timestamp}.md', 'w', encoding='utf-8') as f:
        f.write('# 📊 AI SEO Architects - Executive Summary\\n\\n')
        f.write(f'**Дата тестирования:** {datetime.now().strftime("%d.%m.%Y %H:%M")}\\n\\n')
        
        f.write('## 🎯 Результаты тестирования\\n\\n')
        for level in ['executive', 'management', 'operational']:
            level_data = results.get(level)
            if level_data and level_data.get('success'):
                stats = level_data['stats']
                model_type = 'GPT-4' if level == 'executive' else 'GPT-4o-mini'
                
                f.write(f'### {level.capitalize()} Level ({model_type})\\n')
                f.write(f'- **Агентов протестировано:** {stats["successful_tests"]}/{stats["total_tests"]}\\n')
                f.write(f'- **Success Rate:** {stats["success_rate"]:.1f}%\\n')
                f.write(f'- **Среднее качество:** {stats["avg_quality_score"]:.1f}/100\\n')
                f.write(f'- **Среднее время ответа:** {stats["avg_processing_time"]:.2f}с\\n\\n')
        
        f.write('## 💰 Стоимость и токены\\n\\n')
        total_cost = token_tracker.get_total_cost()
        total_tokens = token_tracker.get_total_tokens()
        
        f.write(f'- **Общая стоимость:** ${total_cost:.4f}\\n')
        f.write(f'- **Всего токенов:** {total_tokens:,}\\n')
        f.write(f'- **Стоимость за токен:** ${total_cost/max(1, total_tokens):.8f}\\n\\n')
        
        f.write('### Детализация по уровням:\\n\\n')
        for level, usage in token_tracker.usage_by_level.items():
            if usage['requests'] > 0:
                model_type = 'GPT-4' if level == 'executive' else 'GPT-4o-mini'
                f.write(f'**{level.capitalize()} ({model_type}):**\\n')
                f.write(f'- Input токены: {usage["input"]:,}\\n')
                f.write(f'- Output токены: {usage["output"]:,}\\n')
                f.write(f'- Стоимость: ${usage["cost"]:.4f}\\n')
                f.write(f'- Запросы: {usage["requests"]}\\n\\n')
    
    # 3. Billing summary для бухгалтерии
    with open(f'billing_summary_{timestamp}.csv', 'w', encoding='utf-8') as f:
        f.write('Level,Model,Input_Tokens,Output_Tokens,Cost_USD,Requests\\n')
        for level, usage in token_tracker.usage_by_level.items():
            if usage['requests'] > 0:
                model_type = 'GPT-4' if level == 'executive' else 'GPT-4o-mini'
                f.write(f'{level},{model_type},{usage["input"]},{usage["output"]},{usage["cost"]:.6f},{usage["requests"]}\\n')
    
    print(f'📁 Файлы сохранены:')
    print(f'├─ demo_results_{timestamp}.json - детальные данные')
    print(f'├─ executive_summary_{timestamp}.md - краткий отчет')
    print(f'└─ billing_summary_{timestamp}.csv - данные для бухгалтерии')

print('✅ Функция save_detailed_results определена!')
print('🎯 Переходите к следующей ячейке!')