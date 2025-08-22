# Тема 28: ИИ видео-копирайтер

## Основы видео-копирайтинга с ИИ

### Специфика видеоконтента
- **Сценарии**: Структура и драматургия видео
- **Тайминг**: Управление длительностью и ритмом
- **Визуальное повествование**: Связь текста и изображения
- **Call-to-Action**: Призывы к действию в видео
- **Эмоциональное воздействие**: Создание нужной атмосферы

### Архитектура ИИ-копирайтера для видео
```python
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
import json

class VideoType(Enum):
    PROMOTIONAL = "promotional"
    EDUCATIONAL = "educational"
    ENTERTAINMENT = "entertainment"
    DOCUMENTARY = "documentary"
    COMMERCIAL = "commercial"
    SOCIAL_MEDIA = "social_media"
    EXPLAINER = "explainer"

class VideoFormat(Enum):
    SHORT_FORM = "short_form"  # До 60 секунд
    MEDIUM_FORM = "medium_form"  # 1-10 минут
    LONG_FORM = "long_form"  # Более 10 минут

@dataclass
class VideoSpec:
    """Спецификация видео"""
    type: VideoType
    format: VideoFormat
    duration: int  # В секундах
    target_audience: str
    platform: str  # YouTube, TikTok, Instagram, etc.
    tone: str  # Casual, professional, humorous, etc.
    language: str
    budget: Optional[str] = None
    special_requirements: Optional[List[str]] = None

@dataclass
class SceneDescription:
    """Описание сцены"""
    scene_number: int
    duration: int  # В секундах
    visual_description: str
    audio_description: str
    text_overlay: Optional[str] = None
    voiceover: Optional[str] = None
    music_style: Optional[str] = None
    transitions: Optional[str] = None

@dataclass
class VideoScript:
    """Сценарий видео"""
    title: str
    description: str
    total_duration: int
    scenes: List[SceneDescription]
    metadata: Dict[str, Any]
    hooks: List[str]  # Зацепки для аудитории
    cta: str  # Call to action

class VideoCopywriterAI:
    """ИИ-копирайтер для видеоконтента"""
    
    def __init__(self):
        self.platform_constraints = {
            'youtube': {
                'max_title_length': 100,
                'max_description_length': 5000,
                'optimal_duration_ranges': {
                    'short': (0, 60),
                    'medium': (60, 600),
                    'long': (600, 3600)
                }
            },
            'tiktok': {
                'max_title_length': 150,
                'max_description_length': 2200,
                'optimal_duration_ranges': {
                    'short': (15, 60),
                    'medium': (60, 180)
                }
            },
            'instagram': {
                'max_title_length': 125,
                'max_description_length': 2200,
                'optimal_duration_ranges': {
                    'reels': (15, 90),
                    'igtv': (60, 3600),
                    'stories': (1, 15)
                }
            }
        }
        
        self.tone_templates = {
            'casual': {
                'intro_phrases': ['Привет!', 'Что's up!', 'Давайте разберемся'],
                'transitions': ['Кстати', 'А еще', 'И вот что интересно'],
                'outros': ['Увидимся!', 'До встречи!', 'Пока!']
            },
            'professional': {
                'intro_phrases': ['Добро пожаловать', 'Сегодня мы рассмотрим', 'В этом видео'],
                'transitions': ['Далее', 'Кроме того', 'Важно отметить'],
                'outros': ['Спасибо за внимание', 'До свидания', 'Увидимся в следующем видео']
            },
            'humorous': {
                'intro_phrases': ['Ну что, поехали!', 'Готовы к веселью?', 'Сейчас будет смешно'],
                'transitions': ['А вот это уже интереснее', 'Но подождите, это еще не все', 'И тут начинается самое веселое'],
                'outros': ['Было весело!', 'Смейтесь на здоровье!', 'До новых приколов!']
            }
        }
    
    def generate_video_script(self, brief: Dict[str, Any], spec: VideoSpec) -> VideoScript:
        """Генерация сценария видео"""
        
        # Анализируем бриф
        topic = brief.get('topic', 'Общая тема')
        key_points = brief.get('key_points', [])
        target_action = brief.get('target_action', 'Подписаться на канал')
        
        # Создаем структуру видео
        scenes = self._create_video_structure(spec, key_points)
        
        # Генерируем контент для каждой сцены
        detailed_scenes = []
        for scene_template in scenes:
            detailed_scene = self._generate_scene_content(
                scene_template, brief, spec
            )
            detailed_scenes.append(detailed_scene)
        
        # Создаем хуки и CTA
        hooks = self._generate_hooks(topic, spec)
        cta = self._generate_cta(target_action, spec)
        
        # Создаем заголовок и описание
        title = self._generate_title(topic, spec)
        description = self._generate_description(brief, spec)
        
        return VideoScript(
            title=title,
            description=description,
            total_duration=spec.duration,
            scenes=detailed_scenes,
            metadata={
                'platform': spec.platform,
                'type': spec.type.value,
                'format': spec.format.value,
                'tone': spec.tone,
                'audience': spec.target_audience
            },
            hooks=hooks,
            cta=cta
        )
    
    def _create_video_structure(self, spec: VideoSpec, key_points: List[str]) -> List[Dict]:
        """Создание базовой структуры видео"""
        
        if spec.format == VideoFormat.SHORT_FORM:
            return self._create_short_form_structure(spec, key_points)
        elif spec.format == VideoFormat.MEDIUM_FORM:
            return self._create_medium_form_structure(spec, key_points)
        else:
            return self._create_long_form_structure(spec, key_points)
    
    def _create_short_form_structure(self, spec: VideoSpec, key_points: List[str]) -> List[Dict]:
        """Структура для коротких видео (до 60 сек)"""
        total_duration = spec.duration
        
        structure = [
            {
                'type': 'hook',
                'duration': min(5, total_duration * 0.1),
                'purpose': 'Захватить внимание в первые секунды'
            },
            {
                'type': 'main_content',
                'duration': total_duration * 0.7,
                'purpose': 'Основное содержание'
            },
            {
                'type': 'cta',
                'duration': max(5, total_duration * 0.2),
                'purpose': 'Призыв к действию'
            }
        ]
        
        return structure
    
    def _create_medium_form_structure(self, spec: VideoSpec, key_points: List[str]) -> List[Dict]:
        """Структура для средних видео (1-10 мин)"""
        total_duration = spec.duration
        
        structure = [
            {
                'type': 'intro',
                'duration': min(15, total_duration * 0.1),
                'purpose': 'Представление и анонс содержания'
            },
            {
                'type': 'hook',
                'duration': min(10, total_duration * 0.05),
                'purpose': 'Зацепка для удержания аудитории'
            }
        ]
        
        # Основные блоки по ключевым точкам
        main_content_duration = total_duration * 0.7
        if key_points:
            point_duration = main_content_duration / len(key_points)
            for i, point in enumerate(key_points):
                structure.append({
                    'type': 'content_block',
                    'duration': point_duration,
                    'purpose': f'Раскрытие темы: {point}',
                    'content': point
                })
        else:
            structure.append({
                'type': 'main_content',
                'duration': main_content_duration,
                'purpose': 'Основное содержание'
            })
        
        structure.extend([
            {
                'type': 'summary',
                'duration': total_duration * 0.1,
                'purpose': 'Подведение итогов'
            },
            {
                'type': 'cta',
                'duration': total_duration * 0.05,
                'purpose': 'Призыв к действию'
            }
        ])
        
        return structure
    
    def _create_long_form_structure(self, spec: VideoSpec, key_points: List[str]) -> List[Dict]:
        """Структура для длинных видео (более 10 мин)"""
        # Аналогично medium, но с дополнительными элементами
        structure = self._create_medium_form_structure(spec, key_points)
        
        # Добавляем промежуточные хуки и переходы
        enhanced_structure = []
        for i, segment in enumerate(structure):
            enhanced_structure.append(segment)
            
            # Добавляем промежуточные элементы
            if segment['type'] == 'content_block' and i < len(structure) - 2:
                enhanced_structure.append({
                    'type': 'transition',
                    'duration': 5,
                    'purpose': 'Переход к следующему блоку'
                })
        
        return enhanced_structure
    
    def _generate_scene_content(self, scene_template: Dict, brief: Dict, spec: VideoSpec) -> SceneDescription:
        """Генерация контента для сцены"""
        scene_type = scene_template['type']
        duration = int(scene_template['duration'])
        
        # Получаем шаблоны для тона
        tone_data = self.tone_templates.get(spec.tone, self.tone_templates['professional'])
        
        visual_description = ""
        voiceover = ""
        text_overlay = None
        music_style = "background"
        
        if scene_type == 'hook':
            visual_description = "Крупный план, динамичные кадры, яркие цвета"
            voiceover = self._generate_hook_voiceover(brief, tone_data)
            text_overlay = "ВНИМАНИЕ!" if spec.platform.lower() == 'tiktok' else None
            music_style = "энергичная"
            
        elif scene_type == 'intro':
            visual_description = "Заставка, логотип, ведущий в кадре"
            voiceover = self._generate_intro_voiceover(brief, tone_data)
            text_overlay = brief.get('topic', 'Тема видео')
            
        elif scene_type == 'main_content' or scene_type == 'content_block':
            content = scene_template.get('content', brief.get('topic', ''))
            visual_description = f"Иллюстрации по теме: {content}"
            voiceover = self._generate_content_voiceover(content, tone_data)
            
        elif scene_type == 'cta':
            visual_description = "Кнопки подписки, ссылки, контактная информация"
            voiceover = self._generate_cta_voiceover(brief.get('target_action', ''), tone_data)
            text_overlay = "ПОДПИШИСЬ!"
            
        elif scene_type == 'summary':
            visual_description = "Коллаж из ключевых моментов видео"
            voiceover = self._generate_summary_voiceover(brief, tone_data)
            
        return SceneDescription(
            scene_number=len([s for s in [] if hasattr(s, 'scene_number')]) + 1,
            duration=duration,
            visual_description=visual_description,
            audio_description="Четкий звук без шумов",
            text_overlay=text_overlay,
            voiceover=voiceover,
            music_style=music_style,
            transitions="Плавный переход"
        )
    
    def _generate_hook_voiceover(self, brief: Dict, tone_data: Dict) -> str:
        """Генерация голосового сопровождения для хука"""
        topic = brief.get('topic', '')
        intro_phrase = tone_data['intro_phrases'][0]
        
        hooks = [
            f"{intro_phrase} Знаете ли вы, что {topic.lower()}?",
            f"За {brief.get('duration', 60)} секунд вы узнаете все о {topic.lower()}!",
            f"{intro_phrase} Сейчас я расскажу, как {topic.lower()} изменит вашу жизнь!"
        ]
        
        return hooks[0]  # В реальности выбирали бы лучший вариант
    
    def _generate_intro_voiceover(self, brief: Dict, tone_data: Dict) -> str:
        """Генерация интро"""
        intro_phrase = tone_data['intro_phrases'][0]
        topic = brief.get('topic', '')
        
        return f"{intro_phrase} в новом выпуске! Сегодня мы подробно разберем {topic.lower()}. Оставайтесь с нами!"
    
    def _generate_content_voiceover(self, content: str, tone_data: Dict) -> str:
        """Генерация основного контента"""
        transition = tone_data['transitions'][0]
        
        return f"{transition}, давайте рассмотрим {content.lower()}. Это очень важная тема, которая поможет вам..."
    
    def _generate_cta_voiceover(self, target_action: str, tone_data: Dict) -> str:
        """Генерация призыва к действию"""
        outro = tone_data['outros'][0]
        
        return f"Если видео было полезным, обязательно {target_action.lower()}! {outro}"
    
    def _generate_summary_voiceover(self, brief: Dict, tone_data: Dict) -> str:
        """Генерация заключения"""
        return "Итак, сегодня мы узнали много нового. Главное помните..."
    
    def _generate_hooks(self, topic: str, spec: VideoSpec) -> List[str]:
        """Генерация зацепок для аудитории"""
        hooks = [
            f"Секрет {topic.lower()}, о котором не знают 90% людей",
            f"3 ошибки в {topic.lower()}, которые совершает каждый",
            f"Как {topic.lower()} изменил мою жизнь за 30 дней",
            f"То, чего вам не расскажут про {topic.lower()}",
            f"Простой способ освоить {topic.lower()} за неделю"
        ]
        
        return hooks[:3]  # Возвращаем топ-3 хука
    
    def _generate_cta(self, target_action: str, spec: VideoSpec) -> str:
        """Генерация призыва к действию"""
        platform_specific_ctas = {
            'youtube': "Подпишитесь на канал и нажмите колокольчик",
            'tiktok': "Ставьте лайк и подписывайтесь",
            'instagram': "Сохраните пост и поделитесь в Stories"
        }
        
        base_cta = platform_specific_ctas.get(spec.platform.lower(), target_action)
        
        return f"{base_cta}! Также напишите в комментариях ваше мнение по теме."
    
    def _generate_title(self, topic: str, spec: VideoSpec) -> str:
        """Генерация заголовка"""
        platform_constraints = self.platform_constraints.get(spec.platform.lower(), {})
        max_length = platform_constraints.get('max_title_length', 100)
        
        title_templates = [
            f"Как {topic.upper()} изменит вашу жизнь",
            f"ВСЯ ПРАВДА про {topic.upper()}",
            f"{topic.upper()}: Полное руководство 2024",
            f"5 секретов {topic.upper()}, которые нужно знать",
            f"{topic.upper()} для начинающих: пошаговая инструкция"
        ]
        
        # Выбираем заголовок, который помещается в лимит
        for title in title_templates:
            if len(title) <= max_length:
                return title
        
        # Если все заголовки слишком длинные, обрезаем
        return title_templates[0][:max_length-3] + "..."
    
    def _generate_description(self, brief: Dict, spec: VideoSpec) -> str:
        """Генерация описания видео"""
        platform_constraints = self.platform_constraints.get(spec.platform.lower(), {})
        max_length = platform_constraints.get('max_description_length', 2000)
        
        description_parts = [
            f"🎯 В этом видео: {brief.get('topic', 'интересная тема')}",
            "",
            "📌 Что вы узнаете:",
        ]
        
        # Добавляем ключевые пункты
        key_points = brief.get('key_points', [])
        for i, point in enumerate(key_points[:5], 1):
            description_parts.append(f"{i}. {point}")
        
        description_parts.extend([
            "",
            "💡 Полезные ссылки:",
            "• Наш сайт: example.com",
            "• Telegram канал: @example",
            "",
            f"🏷️ Теги: #{brief.get('topic', 'тема').replace(' ', '')} #полезное #обучение",
            "",
            "⏰ Таймкоды:",
            "00:00 - Введение",
            f"00:30 - Основная часть",
            f"{spec.duration//60:02d}:{spec.duration%60:02d} - Заключение"
        ])
        
        full_description = "\n".join(description_parts)
        
        # Обрезаем если нужно
        if len(full_description) > max_length:
            return full_description[:max_length-3] + "..."
        
        return full_description

# Демонстрация работы ИИ-копирайтера
copywriter = VideoCopywriterAI()

# Создаем бриф для видео
video_brief = {
    'topic': 'Искусственный интеллект в маркетинге',
    'key_points': [
        'Автоматизация рекламных кампаний',
        'Персонализация контента',
        'Анализ поведения клиентов',
        'Прогнозирование трендов'
    ],
    'target_action': 'подписаться на канал',
    'duration': 300  # 5 минут
}

# Создаем спецификацию
video_spec = VideoSpec(
    type=VideoType.EDUCATIONAL,
    format=VideoFormat.MEDIUM_FORM,
    duration=300,
    target_audience='маркетологи и предприниматели',
    platform='YouTube',
    tone='professional',
    language='ru'
)

# Генерируем сценарий
script = copywriter.generate_video_script(video_brief, video_spec)

print("=== СЦЕНАРИЙ ВИДЕО ===")
print(f"Заголовок: {script.title}")
print(f"Общая длительность: {script.total_duration} сек")
print(f"Количество сцен: {len(script.scenes)}")
print()

print("=== СТРУКТУРА ВИДЕО ===")
for i, scene in enumerate(script.scenes[:3], 1):  # Показываем первые 3 сцены
    print(f"Сцена {i} ({scene.duration} сек):")
    print(f"  Визуал: {scene.visual_description}")
    print(f"  Голос: {scene.voiceover}")
    if scene.text_overlay:
        print(f"  Текст: {scene.text_overlay}")
    print()

print("=== ПРИЗЫВ К ДЕЙСТВИЮ ===")
print(script.cta)
print()

print("=== ОПИСАНИЕ ===")
print(script.description[:300] + "...")
```

## Адаптация под платформы

### Оптимизация для разных платформ
```python
class PlatformOptimizer:
    """Оптимизация контента под различные платформы"""
    
    def __init__(self):
        self.platform_specs = {
            'youtube': {
                'video_formats': ['16:9'],
                'optimal_durations': {
                    'shorts': (15, 60),
                    'standard': (300, 1200),
                    'long_form': (1200, 3600)
                },
                'engagement_factors': ['retention_rate', 'watch_time', 'comments'],
                'algorithm_preferences': ['consistency', 'watch_time', 'clickthrough_rate']
            },
            'tiktok': {
                'video_formats': ['9:16'],
                'optimal_durations': {
                    'short': (15, 30),
                    'medium': (30, 60),
                    'extended': (60, 180)
                },
                'engagement_factors': ['completion_rate', 'shares', 'comments'],
                'algorithm_preferences': ['virality', 'trending_sounds', 'participation']
            },
            'instagram': {
                'video_formats': ['1:1', '4:5', '9:16'],
                'optimal_durations': {
                    'reels': (15, 90),
                    'igtv': (60, 3600),
                    'stories': (1, 15)
                },
                'engagement_factors': ['likes', 'shares', 'saves'],
                'algorithm_preferences': ['recent_posts', 'relationships', 'interest']
            },
            'linkedin': {
                'video_formats': ['16:9', '1:1'],
                'optimal_durations': {
                    'native': (30, 300),
                    'professional': (60, 600)
                },
                'engagement_factors': ['professional_relevance', 'comments', 'shares'],
                'algorithm_preferences': ['professional_content', 'network_engagement']
            }
        }
    
    def optimize_script_for_platform(self, script: VideoScript, 
                                   platform: str) -> VideoScript:
        """Оптимизация сценария под платформу"""
        
        if platform.lower() not in self.platform_specs:
            return script
        
        platform_data = self.platform_specs[platform.lower()]
        
        # Клонируем сценарий для модификации
        optimized_script = self._clone_script(script)
        
        # Адаптируем под алгоритм платформы
        if platform.lower() == 'tiktok':
            optimized_script = self._optimize_for_tiktok(optimized_script)
        elif platform.lower() == 'youtube':
            optimized_script = self._optimize_for_youtube(optimized_script)
        elif platform.lower() == 'instagram':
            optimized_script = self._optimize_for_instagram(optimized_script)
        elif platform.lower() == 'linkedin':
            optimized_script = self._optimize_for_linkedin(optimized_script)
        
        return optimized_script
    
    def _optimize_for_tiktok(self, script: VideoScript) -> VideoScript:
        """Оптимизация для TikTok"""
        
        # TikTok любит быстрый темп и зацепки
        for scene in script.scenes:
            if scene.scene_number == 1:  # Первая сцена критична
                # Делаем хук более агрессивным
                scene.voiceover = self._add_tiktok_energy(scene.voiceover)
                scene.text_overlay = "СМОТРИ ДО КОНЦА!"
                scene.music_style = "трендовая музыка"
            
            # Сокращаем длинные сцены
            if scene.duration > 15:
                scene.duration = min(scene.duration, 15)
                scene.voiceover = self._compress_voiceover(scene.voiceover, 0.7)
        
        # Добавляем TikTok-специфичные элементы
        script.metadata['hashtags'] = self._generate_tiktok_hashtags(script.title)
        script.metadata['trending_sounds'] = True
        
        return script
    
    def _optimize_for_youtube(self, script: VideoScript) -> VideoScript:
        """Оптимизация для YouTube"""
        
        # YouTube ценит удержание аудитории
        for i, scene in enumerate(script.scenes):
            if i == 0:  # Intro должно обещать ценность
                scene.voiceover = self._add_value_promise(scene.voiceover)
            
            # Добавляем элементы удержания
            if i > 0 and i % 3 == 0:  # Каждая 3-я сцена
                retention_phrase = self._get_retention_phrase()
                scene.voiceover = f"{retention_phrase} {scene.voiceover}"
        
        # Добавляем элементы для алгоритма YouTube
        script.metadata['chapters'] = self._generate_chapters(script.scenes)
        script.metadata['end_screen'] = True
        
        return script
    
    def _optimize_for_instagram(self, script: VideoScript) -> VideoScript:
        """Оптимизация для Instagram"""
        
        # Instagram любит визуальность и эстетику
        for scene in script.scenes:
            scene.visual_description = self._enhance_visual_appeal(scene.visual_description)
            
            # Добавляем элементы для сохранений
            if 'полезн' in scene.voiceover.lower():
                scene.text_overlay = "СОХРАНИ ПОСТ"
        
        script.metadata['aesthetic_style'] = 'minimalist'
        script.metadata['story_format'] = True
        
        return script
    
    def _optimize_for_linkedin(self, script: VideoScript) -> VideoScript:
        """Оптимизация для LinkedIn"""
        
        # LinkedIn требует профессионального тона
        for scene in script.scenes:
            scene.voiceover = self._professionalize_tone(scene.voiceover)
            scene.visual_description = self._add_professional_context(scene.visual_description)
        
        script.metadata['professional_insights'] = True
        script.metadata['business_value'] = True
        
        return script
    
    def _add_tiktok_energy(self, voiceover: str) -> str:
        """Добавление энергии для TikTok"""
        energetic_phrases = [
            "ВНИМАНИЕ!",
            "Это невероятно!",
            "Вы не поверите!",
            "СЕКРЕТ раскрыт!"
        ]
        
        return f"{energetic_phrases[0]} {voiceover}"
    
    def _compress_voiceover(self, voiceover: str, factor: float) -> str:
        """Сжатие текста голосового сопровождения"""
        words = voiceover.split()
        target_length = int(len(words) * factor)
        
        # Простое сжатие - берем самые важные слова
        important_words = [w for w in words if len(w) > 3 and w.lower() not in ['который', 'также', 'очень', 'самый']]
        
        if len(important_words) <= target_length:
            return ' '.join(important_words)
        
        return ' '.join(important_words[:target_length])
    
    def _add_value_promise(self, voiceover: str) -> str:
        """Добавление обещания ценности"""
        value_promises = [
            "За 5 минут вы узнаете то, что изменит ваш подход к работе.",
            "В этом видео я покажу простой способ увеличить эффективность в 2 раза.",
            "Сегодня делюсь секретом, который сэкономит вам часы времени."
        ]
        
        return f"{value_promises[0]} {voiceover}"
    
    def _get_retention_phrase(self) -> str:
        """Получение фразы для удержания аудитории"""
        phrases = [
            "А вот что еще важнее -",
            "Но подождите, это еще не все!",
            "Самое интересное будет дальше.",
            "И вот главный секрет:"
        ]
        
        import random
        return random.choice(phrases)
    
    def _generate_tiktok_hashtags(self, title: str) -> List[str]:
        """Генерация хештегов для TikTok"""
        base_hashtags = ['#рекомендации', '#полезное', '#лайфхак', '#топ']
        
        # Извлекаем ключевые слова из заголовка
        words = re.findall(r'\b[а-яё]+\b', title.lower())
        topic_hashtags = [f'#{word}' for word in words if len(word) > 4]
        
        return base_hashtags + topic_hashtags[:3]
    
    def _generate_chapters(self, scenes: List[SceneDescription]) -> List[Dict]:
        """Генерация глав для YouTube"""
        chapters = []
        current_time = 0
        
        for scene in scenes:
            if scene.duration > 30:  # Только для длинных сцен
                chapter = {
                    'time': f"{current_time//60:02d}:{current_time%60:02d}",
                    'title': scene.visual_description[:30] + "..."
                }
                chapters.append(chapter)
            
            current_time += scene.duration
        
        return chapters
    
    def _enhance_visual_appeal(self, visual_desc: str) -> str:
        """Улучшение визуальной привлекательности"""
        enhancements = [
            "с красивым фоном",
            "в эстетичных тонах",
            "со стильным оформлением",
            "с минималистичным дизайном"
        ]
        
        return f"{visual_desc} {enhancements[0]}"
    
    def _professionalize_tone(self, voiceover: str) -> str:
        """Профессионализация тона"""
        casual_to_formal = {
            'привет': 'добро пожаловать',
            'классно': 'эффективно',
            'круто': 'впечатляюще',
            'супер': 'отлично'
        }
        
        result = voiceover
        for casual, formal in casual_to_formal.items():
            result = re.sub(rf'\b{casual}\b', formal, result, flags=re.IGNORECASE)
        
        return result
    
    def _add_professional_context(self, visual_desc: str) -> str:
        """Добавление профессионального контекста"""
        return f"{visual_desc} в офисной среде с деловой атмосферой"
    
    def _clone_script(self, script: VideoScript) -> VideoScript:
        """Клонирование сценария"""
        import copy
        return copy.deepcopy(script)

# Демонстрация платформенной оптимизации
optimizer = PlatformOptimizer()

# Берем оригинальный сценарий и адаптируем под TikTok
tiktok_script = optimizer.optimize_script_for_platform(script, 'tiktok')

print("=== АДАПТАЦИЯ ДЛЯ TIKTOK ===")
print(f"Оригинальная первая сцена: {script.scenes[0].voiceover}")
print(f"TikTok версия: {tiktok_script.scenes[0].voiceover}")
print(f"Хештеги: {tiktok_script.metadata.get('hashtags', [])}")
print()

# Адаптация для YouTube
youtube_script = optimizer.optimize_script_for_platform(script, 'youtube')

print("=== АДАПТАЦИЯ ДЛЯ YOUTUBE ===")
print(f"YouTube версия первой сцены: {youtube_script.scenes[0].voiceover}")
print(f"Главы: {youtube_script.metadata.get('chapters', [])[:2]}")
```

## Анализ эффективности и оптимизация

### Метрики видеоконтента
```python
from datetime import datetime, timedelta
import statistics

@dataclass
class VideoMetrics:
    """Метрики видео"""
    video_id: str
    views: int
    likes: int
    dislikes: int
    comments: int
    shares: int
    watch_time_seconds: int
    avg_view_duration: float
    click_through_rate: float
    subscriber_conversion: float
    engagement_rate: float
    publish_date: datetime

class VideoAnalytics:
    """Аналитика видеоконтента"""
    
    def __init__(self):
        self.metrics_history = []
        self.benchmarks = {
            'youtube': {
                'good_retention': 0.5,  # 50% retention считается хорошим
                'good_ctr': 0.05,       # 5% CTR
                'good_engagement': 0.03  # 3% engagement rate
            },
            'tiktok': {
                'good_retention': 0.7,   # 70% completion rate
                'good_engagement': 0.06  # 6% engagement rate
            },
            'instagram': {
                'good_retention': 0.6,
                'good_engagement': 0.04
            }
        }
    
    def analyze_video_performance(self, metrics: VideoMetrics, 
                                platform: str) -> Dict[str, Any]:
        """Анализ производительности видео"""
        
        analysis = {
            'video_id': metrics.video_id,
            'platform': platform,
            'overall_score': 0,
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        # Анализ удержания аудитории
        retention_rate = metrics.avg_view_duration
        benchmark_retention = self.benchmarks[platform]['good_retention']
        
        if retention_rate >= benchmark_retention:
            analysis['strengths'].append(f"Отличное удержание аудитории ({retention_rate:.1%})")
            analysis['overall_score'] += 30
        else:
            analysis['weaknesses'].append(f"Низкое удержание аудитории ({retention_rate:.1%})")
            analysis['recommendations'].append("Улучшить хук в первые 5 секунд")
            analysis['recommendations'].append("Добавить больше визуальных переходов")
        
        # Анализ вовлеченности
        if metrics.views > 0:
            engagement_rate = (metrics.likes + metrics.comments + metrics.shares) / metrics.views
            benchmark_engagement = self.benchmarks[platform]['good_engagement']
            
            if engagement_rate >= benchmark_engagement:
                analysis['strengths'].append(f"Высокая вовлеченность ({engagement_rate:.1%})")
                analysis['overall_score'] += 25
            else:
                analysis['weaknesses'].append(f"Низкая вовлеченность ({engagement_rate:.1%})")
                analysis['recommendations'].append("Добавить больше призывов к взаимодействию")
                analysis['recommendations'].append("Улучшить эмоциональную составляющую")
        
        # Анализ CTR (для YouTube)
        if platform == 'youtube' and hasattr(metrics, 'click_through_rate'):
            benchmark_ctr = self.benchmarks[platform]['good_ctr']
            
            if metrics.click_through_rate >= benchmark_ctr:
                analysis['strengths'].append(f"Хороший CTR ({metrics.click_through_rate:.1%})")
                analysis['overall_score'] += 20
            else:
                analysis['weaknesses'].append(f"Низкий CTR ({metrics.click_through_rate:.1%})")
                analysis['recommendations'].append("Улучшить превью и заголовок")
                analysis['recommendations'].append("Протестировать разные обложки")
        
        # Анализ времени просмотра
        total_watch_time_hours = metrics.watch_time_seconds / 3600
        if total_watch_time_hours > 100:  # Более 100 часов общего времени просмотра
            analysis['strengths'].append(f"Большое время просмотра ({total_watch_time_hours:.1f} ч)")
            analysis['overall_score'] += 25
        
        # Нормализуем общий счет
        analysis['overall_score'] = min(analysis['overall_score'], 100)
        
        # Определяем общую оценку
        if analysis['overall_score'] >= 80:
            analysis['rating'] = 'Отлично'
        elif analysis['overall_score'] >= 60:
            analysis['rating'] = 'Хорошо'
        elif analysis['overall_score'] >= 40:
            analysis['rating'] = 'Удовлетворительно'
        else:
            analysis['rating'] = 'Требует улучшения'
        
        return analysis
    
    def compare_with_history(self, current_metrics: VideoMetrics,
                           platform: str) -> Dict[str, Any]:
        """Сравнение с историческими данными"""
        
        # Фильтруем метрики той же платформы
        platform_history = [m for m in self.metrics_history 
                          if hasattr(m, 'platform') and m.platform == platform]
        
        if not platform_history:
            return {'comparison': 'Недостаточно данных для сравнения'}
        
        comparison = {}
        
        # Сравниваем ключевые метрики
        historical_views = [m.views for m in platform_history]
        historical_engagement = [(m.likes + m.comments + m.shares) / max(m.views, 1) 
                               for m in platform_history]
        historical_retention = [m.avg_view_duration for m in platform_history]
        
        avg_views = statistics.mean(historical_views)
        avg_engagement = statistics.mean(historical_engagement)
        avg_retention = statistics.mean(historical_retention)
        
        current_engagement = (current_metrics.likes + current_metrics.comments + 
                            current_metrics.shares) / max(current_metrics.views, 1)
        
        # Вычисляем изменения в процентах
        views_change = ((current_metrics.views - avg_views) / avg_views) * 100 if avg_views > 0 else 0
        engagement_change = ((current_engagement - avg_engagement) / avg_engagement) * 100 if avg_engagement > 0 else 0
        retention_change = ((current_metrics.avg_view_duration - avg_retention) / avg_retention) * 100 if avg_retention > 0 else 0
        
        comparison = {
            'views_change_percent': views_change,
            'engagement_change_percent': engagement_change,
            'retention_change_percent': retention_change,
            'trend_analysis': self._analyze_trends(platform_history)
        }
        
        return comparison
    
    def _analyze_trends(self, metrics_history: List[VideoMetrics]) -> Dict[str, str]:
        """Анализ трендов"""
        if len(metrics_history) < 3:
            return {'trend': 'Недостаточно данных'}
        
        # Сортируем по дате
        sorted_metrics = sorted(metrics_history, key=lambda x: x.publish_date)
        
        # Анализируем тренд просмотров
        recent_views = [m.views for m in sorted_metrics[-3:]]
        earlier_views = [m.views for m in sorted_metrics[-6:-3]] if len(sorted_metrics) >= 6 else recent_views
        
        recent_avg = statistics.mean(recent_views)
        earlier_avg = statistics.mean(earlier_views)
        
        if recent_avg > earlier_avg * 1.2:
            views_trend = 'Рост'
        elif recent_avg < earlier_avg * 0.8:
            views_trend = 'Снижение'
        else:
            views_trend = 'Стабильность'
        
        return {
            'views_trend': views_trend,
            'last_updated': sorted_metrics[-1].publish_date.strftime('%Y-%m-%d')
        }
    
    def generate_optimization_suggestions(self, analysis: Dict[str, Any],
                                        script: VideoScript) -> List[str]:
        """Генерация рекомендаций по оптимизации"""
        
        suggestions = []
        
        # Рекомендации на основе слабых мест
        weaknesses = analysis.get('weaknesses', [])
        
        for weakness in weaknesses:
            if 'удержание' in weakness.lower():
                suggestions.extend([
                    "Сократить intro до 5 секунд",
                    "Добавить preview ключевых моментов в начало",
                    "Использовать динамичные переходы между сценами",
                    "Добавить паттерн-интерапт каждые 15 секунд"
                ])
            
            if 'вовлеченность' in weakness.lower():
                suggestions.extend([
                    "Добавить больше вопросов к аудитории",
                    "Включить интерактивные элементы",
                    "Усилить эмоциональную составляющую",
                    "Добавить контроверсиальные моменты для обсуждения"
                ])
            
            if 'ctr' in weakness.lower():
                suggestions.extend([
                    "Протестировать A/B варианты превью",
                    "Использовать более яркие цвета в обложке",
                    "Добавить интригующие элементы в заголовок",
                    "Включить числа и конкретику в название"
                ])
        
        # Рекомендации на основе типа контента
        if script.metadata.get('type') == 'educational':
            suggestions.append("Добавить практические примеры и кейсы")
            suggestions.append("Структурировать материал по принципу 'проблема-решение'")
        
        if script.metadata.get('format') == 'short_form':
            suggestions.append("Максимально сконцентрировать ценность в начале")
            suggestions.append("Использовать быстрые нарезки и переходы")
        
        # Убираем дубликаты
        return list(set(suggestions))

# Демонстрация аналитики
analytics = VideoAnalytics()

# Создаем тестовые метрики
test_metrics = VideoMetrics(
    video_id="test_video_001",
    views=10000,
    likes=500,
    dislikes=50,
    comments=150,
    shares=75,
    watch_time_seconds=25000,
    avg_view_duration=0.45,  # 45% retention
    click_through_rate=0.03,  # 3% CTR
    subscriber_conversion=0.02,
    engagement_rate=0.0725,
    publish_date=datetime.now()
)

# Анализируем производительность
performance_analysis = analytics.analyze_video_performance(test_metrics, 'youtube')

print("=== АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ===")
print(f"Общая оценка: {performance_analysis['overall_score']}/100 ({performance_analysis['rating']})")
print()

print("Сильные стороны:")
for strength in performance_analysis['strengths']:
    print(f"  ✅ {strength}")

print("\nСлабые стороны:")
for weakness in performance_analysis['weaknesses']:
    print(f"  ❌ {weakness}")

print("\nРекомендации:")
for recommendation in performance_analysis['recommendations']:
    print(f"  💡 {recommendation}")

# Генерируем рекомендации по оптимизации
optimization_suggestions = analytics.generate_optimization_suggestions(
    performance_analysis, script
)

print("\n=== РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ ===")
for suggestion in optimization_suggestions[:5]:
    print(f"  🔧 {suggestion}")
```

## Ключевые моменты для экзамена

### Основы видео-копирайтинга
1. **Структура видео**: Hook, intro, main content, CTA
2. **Тайминг**: Критичность первых 5-15 секунд
3. **Платформенные особенности**: YouTube, TikTok, Instagram, LinkedIn
4. **Адаптация контента**: Под алгоритмы и аудиторию

### Техническая реализация
- Автоматическая генерация сценариев на основе брифа
- Оптимизация под ограничения платформ
- Адаптивные призывы к действию
- Интеграция с аналитикой и метриками

### Оптимизация производительности
- **Retention rate**: Процент досмотра видео
- **Click-through rate**: Эффективность превью и заголовков
- **Engagement rate**: Лайки, комментарии, репосты
- **Watch time**: Общее время просмотра

### Платформенная специфика
- **YouTube**: Акцент на watch time и retention
- **TikTok**: Быстрые хуки и трендовые элементы
- **Instagram**: Визуальная эстетика и сторителлинг
- **LinkedIn**: Профессиональная ценность и экспертность

### Практические навыки
- Создание эффективных хуков
- Структурирование контента по аудитории
- A/B тестирование элементов видео
- Анализ метрик и оптимизация стратегии