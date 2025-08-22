# Тема 27: Обработка речи в ИИ системах

## Основы обработки речи

### Компоненты речевых технологий
- **Speech-to-Text (STT)**: Распознавание речи в текст
- **Text-to-Speech (TTS)**: Синтез речи из текста
- **Speech Enhancement**: Улучшение качества аудио
- **Speaker Recognition**: Идентификация говорящего
- **Emotion Recognition**: Распознавание эмоций в речи

### Архитектура систем обработки речи
```python
import os
import wave
import json
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np

class AudioFormat(Enum):
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"

@dataclass
class AudioMetadata:
    """Метаданные аудиофайла"""
    duration: float
    sample_rate: int
    channels: int
    format: AudioFormat
    size_bytes: int
    bitrate: Optional[int] = None

@dataclass
class SpeechResult:
    """Результат обработки речи"""
    text: str
    confidence: float
    timestamps: List[Tuple[float, float, str]]  # start, end, word
    language: str
    speaker_id: Optional[str] = None
    emotion: Optional[str] = None

class AudioProcessor:
    """Базовый класс для обработки аудио"""
    
    def __init__(self):
        self.supported_formats = [AudioFormat.WAV, AudioFormat.MP3, AudioFormat.FLAC]
        self.default_sample_rate = 16000
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, AudioMetadata]:
        """Загрузка аудиофайла"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Аудиофайл не найден: {file_path}")
        
        # Определяем формат по расширению
        ext = os.path.splitext(file_path)[1][1:].lower()
        audio_format = AudioFormat(ext) if ext in [f.value for f in AudioFormat] else AudioFormat.WAV
        
        # Простая загрузка WAV файла
        if audio_format == AudioFormat.WAV:
            return self._load_wav(file_path)
        else:
            # Для других форматов потребуются дополнительные библиотеки
            raise NotImplementedError(f"Формат {audio_format} пока не поддерживается")
    
    def _load_wav(self, file_path: str) -> Tuple[np.ndarray, AudioMetadata]:
        """Загрузка WAV файла"""
        with wave.open(file_path, 'rb') as wav_file:
            frames = wav_file.readframes(-1)
            sample_rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            
            # Конвертация в numpy array
            if sample_width == 1:
                audio_data = np.frombuffer(frames, dtype=np.uint8)
            elif sample_width == 2:
                audio_data = np.frombuffer(frames, dtype=np.int16)
            else:
                audio_data = np.frombuffer(frames, dtype=np.int32)
            
            # Нормализация
            audio_data = audio_data.astype(np.float32)
            if sample_width == 1:
                audio_data = (audio_data - 128) / 128.0
            elif sample_width == 2:
                audio_data = audio_data / 32768.0
            else:
                audio_data = audio_data / 2147483648.0
            
            # Метаданные
            duration = len(audio_data) / sample_rate
            size_bytes = os.path.getsize(file_path)
            
            metadata = AudioMetadata(
                duration=duration,
                sample_rate=sample_rate,
                channels=channels,
                format=AudioFormat.WAV,
                size_bytes=size_bytes
            )
            
            return audio_data, metadata
    
    def preprocess_audio(self, audio_data: np.ndarray, 
                        target_sample_rate: int = None) -> np.ndarray:
        """Предобработка аудио"""
        if target_sample_rate is None:
            target_sample_rate = self.default_sample_rate
        
        # Здесь могли бы быть:
        # - Ресэмплинг
        # - Нормализация громкости
        # - Шумоподавление
        # - Удаление тишины
        
        # Простая нормализация
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val
        
        return audio_data
    
    def detect_silence(self, audio_data: np.ndarray, 
                      threshold: float = 0.01, 
                      min_duration: float = 0.5) -> List[Tuple[float, float]]:
        """Определение участков тишины"""
        sample_rate = self.default_sample_rate
        min_samples = int(min_duration * sample_rate)
        
        # Определяем уровень сигнала
        is_silence = np.abs(audio_data) < threshold
        
        silence_segments = []
        start = None
        
        for i, silent in enumerate(is_silence):
            if silent and start is None:
                start = i
            elif not silent and start is not None:
                if i - start >= min_samples:
                    start_time = start / sample_rate
                    end_time = i / sample_rate
                    silence_segments.append((start_time, end_time))
                start = None
        
        # Проверяем последний сегмент
        if start is not None and len(is_silence) - start >= min_samples:
            start_time = start / sample_rate
            end_time = len(is_silence) / sample_rate
            silence_segments.append((start_time, end_time))
        
        return silence_segments
    
    def split_by_silence(self, audio_data: np.ndarray, 
                        silence_threshold: float = 0.01) -> List[np.ndarray]:
        """Разделение аудио по участкам тишины"""
        silence_segments = self.detect_silence(audio_data, silence_threshold)
        
        if not silence_segments:
            return [audio_data]
        
        sample_rate = self.default_sample_rate
        audio_segments = []
        
        start_idx = 0
        for silence_start, silence_end in silence_segments:
            # Сегмент до тишины
            end_idx = int(silence_start * sample_rate)
            if end_idx > start_idx:
                segment = audio_data[start_idx:end_idx]
                if len(segment) > sample_rate * 0.1:  # Минимум 0.1 секунды
                    audio_segments.append(segment)
            
            start_idx = int(silence_end * sample_rate)
        
        # Последний сегмент
        if start_idx < len(audio_data):
            segment = audio_data[start_idx:]
            if len(segment) > sample_rate * 0.1:
                audio_segments.append(segment)
        
        return audio_segments

# Пример использования базового процессора
processor = AudioProcessor()

# Имитация аудиоданных
sample_rate = 16000
duration = 5.0  # секунд
t = np.linspace(0, duration, int(sample_rate * duration))
# Синусоида с периодами тишины
audio_signal = np.sin(2 * np.pi * 440 * t)  # 440 Hz тон
audio_signal[int(1*sample_rate):int(2*sample_rate)] = 0  # тишина с 1 до 2 сек
audio_signal[int(3.5*sample_rate):int(4*sample_rate)] = 0  # тишина с 3.5 до 4 сек

print("Анализ аудио:")
print(f"Длительность: {duration} сек")
print(f"Частота дискретизации: {sample_rate} Гц")

# Поиск тишины
silence_segments = processor.detect_silence(audio_signal, threshold=0.1)
print(f"Найдено {len(silence_segments)} участков тишины:")
for i, (start, end) in enumerate(silence_segments):
    print(f"  {i+1}: {start:.2f}с - {end:.2f}с")

# Разделение по тишине
audio_parts = processor.split_by_silence(audio_signal)
print(f"Аудио разделено на {len(audio_parts)} частей")
```

## Speech-to-Text (Распознавание речи)

### Интеграция с внешними API
```python
import aiohttp
import base64
from typing import Dict, Optional

class SpeechToTextEngine:
    """Движок распознавания речи"""
    
    def __init__(self, api_type: str = "mock"):
        self.api_type = api_type
        self.config = {
            'language': 'ru-RU',
            'model': 'latest_short',
            'enable_word_time_offsets': True,
            'enable_automatic_punctuation': True
        }
    
    async def transcribe_audio(self, audio_data: np.ndarray, 
                             sample_rate: int = 16000,
                             language: str = None) -> SpeechResult:
        """Транскрибация аудио в текст"""
        if language:
            self.config['language'] = language
        
        if self.api_type == "google":
            return await self._transcribe_google(audio_data, sample_rate)
        elif self.api_type == "yandex":
            return await self._transcribe_yandex(audio_data, sample_rate)
        elif self.api_type == "whisper":
            return await self._transcribe_whisper(audio_data, sample_rate)
        else:
            return self._mock_transcribe(audio_data, sample_rate)
    
    async def _transcribe_google(self, audio_data: np.ndarray, 
                               sample_rate: int) -> SpeechResult:
        """Транскрибация через Google Speech-to-Text API"""
        # Конвертация аудио в формат для API
        audio_bytes = self._audio_to_bytes(audio_data, sample_rate)
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        request_data = {
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": sample_rate,
                "languageCode": self.config['language'],
                "enableWordTimeOffsets": self.config['enable_word_time_offsets'],
                "enableAutomaticPunctuation": self.config['enable_automatic_punctuation']
            },
            "audio": {
                "content": audio_base64
            }
        }
        
        # Здесь был бы реальный HTTP запрос к Google API
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(google_api_url, json=request_data) as response:
        #         result = await response.json()
        
        # Мок ответа
        mock_result = {
            "results": [{
                "alternatives": [{
                    "transcript": "Привет, как дела? Это тестовое сообщение.",
                    "confidence": 0.95,
                    "words": [
                        {"word": "Привет", "startTime": "0s", "endTime": "0.5s"},
                        {"word": "как", "startTime": "0.5s", "endTime": "0.7s"},
                        {"word": "дела", "startTime": "0.7s", "endTime": "1.2s"}
                    ]
                }]
            }]
        }
        
        return self._parse_google_response(mock_result)
    
    async def _transcribe_yandex(self, audio_data: np.ndarray, 
                               sample_rate: int) -> SpeechResult:
        """Транскрибация через Yandex SpeechKit"""
        # Аналогично Google, но с форматом Yandex API
        return SpeechResult(
            text="Результат от Yandex SpeechKit",
            confidence=0.88,
            timestamps=[(0.0, 1.0, "результат"), (1.0, 2.5, "от"), (2.5, 4.0, "яндекс")],
            language="ru-RU"
        )
    
    async def _transcribe_whisper(self, audio_data: np.ndarray, 
                                sample_rate: int) -> SpeechResult:
        """Транскрибация через OpenAI Whisper"""
        # Здесь была бы интеграция с Whisper API или локальной моделью
        return SpeechResult(
            text="Результат от OpenAI Whisper модели",
            confidence=0.92,
            timestamps=[(0.0, 2.0, "результат"), (2.0, 3.5, "от"), (3.5, 5.0, "whisper")],
            language="ru"
        )
    
    def _mock_transcribe(self, audio_data: np.ndarray, 
                        sample_rate: int) -> SpeechResult:
        """Мок транскрибации для тестирования"""
        duration = len(audio_data) / sample_rate
        
        # Имитируем распознавание
        words = ["тестовое", "аудио", "сообщение", "длительностью", f"{duration:.1f}", "секунд"]
        word_duration = duration / len(words)
        
        timestamps = []
        for i, word in enumerate(words):
            start_time = i * word_duration
            end_time = (i + 1) * word_duration
            timestamps.append((start_time, end_time, word))
        
        return SpeechResult(
            text=" ".join(words),
            confidence=0.85,
            timestamps=timestamps,
            language="ru"
        )
    
    def _audio_to_bytes(self, audio_data: np.ndarray, sample_rate: int) -> bytes:
        """Конвертация аудио в байты для API"""
        # Конвертируем в 16-bit PCM
        audio_int16 = (audio_data * 32767).astype(np.int16)
        return audio_int16.tobytes()
    
    def _parse_google_response(self, response: Dict) -> SpeechResult:
        """Парсинг ответа Google Speech API"""
        if not response.get('results'):
            return SpeechResult("", 0.0, [], "unknown")
        
        result = response['results'][0]
        alternative = result['alternatives'][0]
        
        text = alternative['transcript']
        confidence = alternative.get('confidence', 0.0)
        
        timestamps = []
        if 'words' in alternative:
            for word_info in alternative['words']:
                word = word_info['word']
                start_time = float(word_info['startTime'].rstrip('s'))
                end_time = float(word_info['endTime'].rstrip('s'))
                timestamps.append((start_time, end_time, word))
        
        return SpeechResult(
            text=text,
            confidence=confidence,
            timestamps=timestamps,
            language=self.config['language']
        )

# Демонстрация распознавания речи
async def demo_speech_recognition():
    stt_engine = SpeechToTextEngine("mock")
    
    # Создаем тестовое аудио
    processor = AudioProcessor()
    sample_rate = 16000
    duration = 3.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    test_audio = np.sin(2 * np.pi * 440 * t) * 0.1  # Тихий тон
    
    # Распознаем речь
    result = await stt_engine.transcribe_audio(test_audio, sample_rate)
    
    print("Результат распознавания речи:")
    print(f"Текст: {result.text}")
    print(f"Уверенность: {result.confidence:.2f}")
    print(f"Язык: {result.language}")
    print("Временные метки:")
    for start, end, word in result.timestamps[:3]:  # Первые 3 слова
        print(f"  {word}: {start:.2f}с - {end:.2f}с")

# asyncio.run(demo_speech_recognition())
```

### Пост-обработка результатов распознавания
```python
import re
from typing import Set

class SpeechPostProcessor:
    """Пост-обработка результатов распознавания речи"""
    
    def __init__(self):
        self.punctuation_model = PunctuationModel()
        self.spell_checker = SpellChecker()
        self.profanity_filter = ProfanityFilter()
    
    def process_transcription(self, result: SpeechResult, 
                            enable_spell_check: bool = True,
                            enable_punctuation: bool = True,
                            enable_profanity_filter: bool = False) -> SpeechResult:
        """Комплексная пост-обработка транскрипции"""
        processed_text = result.text
        
        # Очистка и нормализация
        processed_text = self._normalize_text(processed_text)
        
        # Проверка орфографии
        if enable_spell_check:
            processed_text = self.spell_checker.correct_text(processed_text)
        
        # Расстановка знаков препинания
        if enable_punctuation:
            processed_text = self.punctuation_model.add_punctuation(processed_text)
        
        # Фильтрация нецензурных слов
        if enable_profanity_filter:
            processed_text = self.profanity_filter.filter_text(processed_text)
        
        # Создаем обновленный результат
        return SpeechResult(
            text=processed_text,
            confidence=result.confidence,
            timestamps=result.timestamps,
            language=result.language,
            speaker_id=result.speaker_id,
            emotion=result.emotion
        )
    
    def _normalize_text(self, text: str) -> str:
        """Нормализация текста"""
        # Удаление лишних пробелов
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Нормализация чисел
        text = self._normalize_numbers(text)
        
        # Приведение к нижнему регистру первых букв (кроме имен собственных)
        words = text.split()
        normalized_words = []
        
        for i, word in enumerate(words):
            if i == 0 or word in self._get_proper_nouns():
                # Первое слово или имя собственное
                normalized_words.append(word.capitalize())
            else:
                normalized_words.append(word.lower())
        
        return ' '.join(normalized_words)
    
    def _normalize_numbers(self, text: str) -> str:
        """Нормализация числительных"""
        number_words = {
            'ноль': '0', 'один': '1', 'два': '2', 'три': '3', 'четыре': '4',
            'пять': '5', 'шесть': '6', 'семь': '7', 'восемь': '8', 'девять': '9',
            'десять': '10', 'одиннадцать': '11', 'двенадцать': '12',
            'тринадцать': '13', 'четырнадцать': '14', 'пятнадцать': '15',
            'шестнадцать': '16', 'семнадцать': '17', 'восемнадцать': '18',
            'девятнадцать': '19', 'двадцать': '20', 'тридцать': '30',
            'сорок': '40', 'пятьдесят': '50', 'шестьдесят': '60',
            'семьдесят': '70', 'восемьдесят': '80', 'девяносто': '90',
            'сто': '100', 'тысяча': '1000', 'миллион': '1000000'
        }
        
        for word_num, digit_num in number_words.items():
            text = re.sub(rf'\b{word_num}\b', digit_num, text, flags=re.IGNORECASE)
        
        return text
    
    def _get_proper_nouns(self) -> Set[str]:
        """Получение списка имен собственных"""
        return {
            'москва', 'петербург', 'россия', 'александр', 'анна', 'иван',
            'мария', 'пётр', 'елена', 'михаил', 'ольга', 'сергей'
        }

class PunctuationModel:
    """Модель для расстановки знаков препинания"""
    
    def add_punctuation(self, text: str) -> str:
        """Добавление знаков препинания"""
        # Простая эвристическая модель
        
        # Разбиваем на предложения по паузам (упрощенно)
        sentences = re.split(r'\s+(?=\b(?:и|а|но|или|что|где|когда|как)\b)', text)
        
        processed_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Добавляем запятые перед союзами
            sentence = re.sub(r'\s+(и|а|но)\s+', r', \1 ', sentence)
            
            # Добавляем запятые после вводных слов
            intro_words = ['конечно', 'наверное', 'возможно', 'кстати', 'например']
            for word in intro_words:
                sentence = re.sub(rf'\b{word}\b', f'{word},', sentence, flags=re.IGNORECASE)
            
            # Добавляем точку в конце, если её нет
            if not sentence.endswith(('.', '!', '?')):
                sentence += '.'
            
            processed_sentences.append(sentence)
        
        return ' '.join(processed_sentences)

class SpellChecker:
    """Проверка и исправление орфографии"""
    
    def __init__(self):
        self.common_mistakes = {
            'чё': 'что',
            'щас': 'сейчас',
            'токо': 'только',
            'ваще': 'вообще',
            'прям': 'прямо',
            'типа': 'как бы',
            'короче': 'в общем'
        }
    
    def correct_text(self, text: str) -> str:
        """Исправление орфографии"""
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Убираем знаки препинания для проверки
            clean_word = re.sub(r'[^\w]', '', word.lower())
            
            if clean_word in self.common_mistakes:
                # Заменяем слово, сохраняя регистр и знаки препинания
                corrected = self.common_mistakes[clean_word]
                if word[0].isupper():
                    corrected = corrected.capitalize()
                
                # Восстанавливаем знаки препинания
                punctuation = re.findall(r'[^\w]', word)
                if punctuation:
                    corrected += ''.join(punctuation)
                
                corrected_words.append(corrected)
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words)

class ProfanityFilter:
    """Фильтр нецензурных слов"""
    
    def __init__(self):
        # В реальности это был бы более полный список
        self.profanity_words = {'плохое_слово1', 'плохое_слово2'}
        self.replacement = '***'
    
    def filter_text(self, text: str) -> str:
        """Фильтрация нецензурных слов"""
        words = text.split()
        filtered_words = []
        
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            
            if clean_word in self.profanity_words:
                # Заменяем на звездочки, сохраняя длину
                replacement = self.replacement * (len(clean_word) // len(self.replacement) + 1)
                replacement = replacement[:len(clean_word)]
                
                # Восстанавливаем знаки препинания
                punctuation = re.findall(r'[^\w]', word)
                if punctuation:
                    replacement += ''.join(punctuation)
                
                filtered_words.append(replacement)
            else:
                filtered_words.append(word)
        
        return ' '.join(filtered_words)

# Демонстрация пост-обработки
post_processor = SpeechPostProcessor()

# Тестовый результат распознавания с ошибками
test_result = SpeechResult(
    text="привет токо щас прилетел как дела чё делаешь",
    confidence=0.8,
    timestamps=[(0, 1, "привет"), (1, 2, "токо"), (2, 3, "щас")],
    language="ru"
)

print("Исходная транскрипция:")
print(test_result.text)

processed_result = post_processor.process_transcription(
    test_result,
    enable_spell_check=True,
    enable_punctuation=True,
    enable_profanity_filter=True
)

print("\nОбработанная транскрипция:")
print(processed_result.text)
```

## Text-to-Speech (Синтез речи)

### Генерация речи из текста
```python
class TextToSpeechEngine:
    """Движок синтеза речи"""
    
    def __init__(self, api_type: str = "mock"):
        self.api_type = api_type
        self.config = {
            'language': 'ru-RU',
            'voice': 'female',
            'speed': 1.0,
            'pitch': 0.0,
            'volume': 0.8,
            'sample_rate': 22050
        }
        self.available_voices = {
            'ru-RU': {
                'female': ['alena', 'oksana', 'jane'],
                'male': ['omazh', 'zahar', 'ermil']
            },
            'en-US': {
                'female': ['alloy', 'nova', 'shimmer'],
                'male': ['echo', 'fable', 'onyx']
            }
        }
    
    async def synthesize_speech(self, text: str, 
                              voice: str = None,
                              speed: float = None,
                              output_format: str = "wav") -> bytes:
        """Синтез речи из текста"""
        
        # Обновляем параметры
        if voice:
            self.config['voice'] = voice
        if speed:
            self.config['speed'] = speed
        
        # Предобработка текста
        processed_text = self._preprocess_text(text)
        
        if self.api_type == "openai":
            return await self._synthesize_openai(processed_text, output_format)
        elif self.api_type == "yandex":
            return await self._synthesize_yandex(processed_text, output_format)
        elif self.api_type == "elevenlabs":
            return await self._synthesize_elevenlabs(processed_text, output_format)
        else:
            return self._mock_synthesize(processed_text, output_format)
    
    def _preprocess_text(self, text: str) -> str:
        """Предобработка текста для синтеза"""
        # Нормализация чисел и аббревиатур
        text = self._expand_abbreviations(text)
        text = self._normalize_numbers_for_speech(text)
        
        # Разметка SSML для управления произношением
        text = self._add_pronunciation_hints(text)
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Раскрытие аббревиатур"""
        abbreviations = {
            'ИИ': 'искусственный интеллект',
            'МО': 'машинное обучение',
            'НС': 'нейронная сеть',
            'API': 'эй-пи-ай',
            'HTTP': 'эйч-ти-ти-пи',
            'URL': 'ю-ар-эл',
            'GPS': 'джи-пи-эс',
            'USB': 'ю-эс-би'
        }
        
        for abbr, expansion in abbreviations.items():
            text = re.sub(rf'\b{abbr}\b', expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _normalize_numbers_for_speech(self, text: str) -> str:
        """Нормализация чисел для произношения"""
        # Преобразование цифр в слова
        def number_to_words(match):
            num = int(match.group())
            
            ones = ['', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
            teens = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 
                    'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать']
            tens = ['', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 
                   'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']
            
            if num == 0:
                return 'ноль'
            elif num < 10:
                return ones[num]
            elif num < 20:
                return teens[num - 10]
            elif num < 100:
                return tens[num // 10] + (' ' + ones[num % 10] if num % 10 != 0 else '')
            else:
                return str(num)  # Для больших чисел оставляем как есть
        
        # Заменяем числа от 0 до 99
        text = re.sub(r'\b\d{1,2}\b', number_to_words, text)
        
        return text
    
    def _add_pronunciation_hints(self, text: str) -> str:
        """Добавление подсказок произношения"""
        # Паузы между предложениями
        text = re.sub(r'\.(\s+)', r'.<break time="0.5s"/>\1', text)
        
        # Ударения в сложных словах
        stress_words = {
            'программирование': 'программи́рование',
            'администрирование': 'администри́рование',
            'тестирование': 'тести́рование'
        }
        
        for word, stressed in stress_words.items():
            text = re.sub(rf'\b{word}\b', stressed, text, flags=re.IGNORECASE)
        
        return text
    
    async def _synthesize_openai(self, text: str, output_format: str) -> bytes:
        """Синтез через OpenAI TTS"""
        request_data = {
            "model": "tts-1",
            "input": text,
            "voice": self.config['voice'],
            "response_format": output_format,
            "speed": self.config['speed']
        }
        
        # Здесь был бы реальный запрос к OpenAI API
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(openai_tts_url, json=request_data) as response:
        #         return await response.read()
        
        return self._mock_synthesize(text, output_format)
    
    async def _synthesize_yandex(self, text: str, output_format: str) -> bytes:
        """Синтез через Yandex SpeechKit"""
        return self._mock_synthesize(text, output_format)
    
    async def _synthesize_elevenlabs(self, text: str, output_format: str) -> bytes:
        """Синтез через ElevenLabs"""
        return self._mock_synthesize(text, output_format)
    
    def _mock_synthesize(self, text: str, output_format: str) -> bytes:
        """Мок синтеза для тестирования"""
        # Генерируем простой аудиосигнал на основе текста
        sample_rate = self.config['sample_rate']
        duration = len(text) * 0.1  # 0.1 секунды на символ
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Создаем синусоиду с изменяющейся частотой (имитация речи)
        frequency = 200 + (hash(text) % 200)  # Частота зависит от текста
        audio_signal = np.sin(2 * np.pi * frequency * t) * self.config['volume']
        
        # Добавляем модуляцию для естественности
        modulation = 1 + 0.3 * np.sin(2 * np.pi * 5 * t)
        audio_signal *= modulation
        
        # Конвертируем в байты
        audio_int16 = (audio_signal * 32767).astype(np.int16)
        return audio_int16.tobytes()
    
    def get_available_voices(self, language: str = None) -> Dict:
        """Получение доступных голосов"""
        if language:
            return self.available_voices.get(language, {})
        return self.available_voices
    
    def set_voice_parameters(self, **kwargs):
        """Настройка параметров голоса"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value

# Демонстрация синтеза речи
async def demo_text_to_speech():
    tts_engine = TextToSpeechEngine("mock")
    
    # Настройка голоса
    tts_engine.set_voice_parameters(
        voice='female',
        speed=1.2,
        pitch=0.1,
        volume=0.9
    )
    
    # Тестовый текст
    test_text = """
    Привет! Это демонстрация синтеза речи. 
    Система может произносить числа: 25, 100, 999.
    А также аббревиатуры: ИИ, API, HTTP.
    Скорость и тон голоса можно настраивать.
    """
    
    print("Синтез речи...")
    print(f"Исходный текст: {test_text.strip()}")
    
    # Получаем доступные голоса
    voices = tts_engine.get_available_voices('ru-RU')
    print(f"Доступные голоса: {voices}")
    
    # Синтезируем речь
    audio_bytes = await tts_engine.synthesize_speech(test_text)
    
    print(f"Сгенерировано {len(audio_bytes)} байт аудио")
    print(f"Настройки: {tts_engine.config}")

# asyncio.run(demo_text_to_speech())
```

### Управление параметрами голоса
```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class VoiceProfile:
    """Профиль голоса"""
    name: str
    language: str
    gender: str
    age_group: str  # child, adult, elderly
    style: str  # neutral, cheerful, serious, calm
    speed_range: Tuple[float, float]  # min, max speed
    pitch_range: Tuple[float, float]  # min, max pitch
    supported_emotions: List[str]

class VoiceManager:
    """Менеджер голосов и их параметров"""
    
    def __init__(self):
        self.voice_profiles = {}
        self.current_profile = None
        self._initialize_default_profiles()
    
    def _initialize_default_profiles(self):
        """Инициализация профилей по умолчанию"""
        profiles = [
            VoiceProfile(
                name="alena",
                language="ru-RU",
                gender="female",
                age_group="adult",
                style="neutral",
                speed_range=(0.5, 2.0),
                pitch_range(-0.5, 0.5),
                supported_emotions=["neutral", "happy", "sad", "angry"]
            ),
            VoiceProfile(
                name="zahar",
                language="ru-RU", 
                gender="male",
                age_group="adult",
                style="serious",
                speed_range=(0.7, 1.8),
                pitch_range=(-0.3, 0.3),
                supported_emotions=["neutral", "serious", "confident"]
            ),
            VoiceProfile(
                name="nova",
                language="en-US",
                gender="female",
                age_group="adult",
                style="cheerful",
                speed_range=(0.8, 2.2),
                pitch_range=(-0.2, 0.8),
                supported_emotions=["neutral", "happy", "excited", "calm"]
            )
        ]
        
        for profile in profiles:
            self.voice_profiles[profile.name] = profile
    
    def select_voice(self, criteria: Dict[str, str]) -> Optional[str]:
        """Выбор голоса по критериям"""
        matching_voices = []
        
        for name, profile in self.voice_profiles.items():
            match_score = 0
            total_criteria = len(criteria)
            
            if criteria.get('language') == profile.language:
                match_score += 1
            if criteria.get('gender') == profile.gender:
                match_score += 1
            if criteria.get('age_group') == profile.age_group:
                match_score += 1
            if criteria.get('style') == profile.style:
                match_score += 1
            
            if match_score > 0:
                matching_voices.append((name, match_score / total_criteria))
        
        if matching_voices:
            # Возвращаем голос с лучшим соответствием
            best_match = max(matching_voices, key=lambda x: x[1])
            return best_match[0]
        
        return None
    
    def get_optimal_parameters(self, voice_name: str, context: Dict) -> Dict[str, float]:
        """Получение оптимальных параметров для контекста"""
        if voice_name not in self.voice_profiles:
            return {}
        
        profile = self.voice_profiles[voice_name]
        params = {}
        
        # Базовые параметры
        params['speed'] = (profile.speed_range[0] + profile.speed_range[1]) / 2
        params['pitch'] = (profile.pitch_range[0] + profile.pitch_range[1]) / 2
        
        # Адаптация под контекст
        content_type = context.get('content_type', 'general')
        emotion = context.get('emotion', 'neutral')
        audience = context.get('audience', 'adult')
        
        # Корректировка скорости по типу контента
        if content_type == 'news':
            params['speed'] = min(params['speed'] * 1.1, profile.speed_range[1])
        elif content_type == 'audiobook':
            params['speed'] = max(params['speed'] * 0.9, profile.speed_range[0])
        elif content_type == 'advertisement':
            params['speed'] = min(params['speed'] * 1.3, profile.speed_range[1])
        
        # Корректировка под эмоцию
        if emotion in profile.supported_emotions:
            if emotion == 'happy':
                params['pitch'] = min(params['pitch'] + 0.2, profile.pitch_range[1])
                params['speed'] = min(params['speed'] * 1.1, profile.speed_range[1])
            elif emotion == 'sad':
                params['pitch'] = max(params['pitch'] - 0.2, profile.pitch_range[0])
                params['speed'] = max(params['speed'] * 0.8, profile.speed_range[0])
            elif emotion == 'angry':
                params['pitch'] = min(params['pitch'] + 0.1, profile.pitch_range[1])
                params['speed'] = min(params['speed'] * 1.2, profile.speed_range[1])
        
        # Корректировка под аудиторию
        if audience == 'children':
            params['pitch'] = min(params['pitch'] + 0.3, profile.pitch_range[1])
            params['speed'] = max(params['speed'] * 0.9, profile.speed_range[0])
        elif audience == 'elderly':
            params['speed'] = max(params['speed'] * 0.8, profile.speed_range[0])
        
        return params
    
    def create_custom_profile(self, name: str, base_profile: str, 
                            modifications: Dict) -> bool:
        """Создание кастомного профиля на основе существующего"""
        if base_profile not in self.voice_profiles:
            return False
        
        base = self.voice_profiles[base_profile]
        
        # Копируем базовый профиль
        custom_profile = VoiceProfile(
            name=name,
            language=modifications.get('language', base.language),
            gender=modifications.get('gender', base.gender),
            age_group=modifications.get('age_group', base.age_group),
            style=modifications.get('style', base.style),
            speed_range=modifications.get('speed_range', base.speed_range),
            pitch_range=modifications.get('pitch_range', base.pitch_range),
            supported_emotions=modifications.get('supported_emotions', base.supported_emotions)
        )
        
        self.voice_profiles[name] = custom_profile
        return True

# Демонстрация управления голосами
voice_manager = VoiceManager()

# Поиск голоса по критериям
criteria = {
    'language': 'ru-RU',
    'gender': 'female',
    'style': 'neutral'
}

selected_voice = voice_manager.select_voice(criteria)
print(f"Выбранный голос: {selected_voice}")

if selected_voice:
    # Получение оптимальных параметров для контекста
    context = {
        'content_type': 'audiobook',
        'emotion': 'calm',
        'audience': 'adult'
    }
    
    optimal_params = voice_manager.get_optimal_parameters(selected_voice, context)
    print(f"Оптимальные параметры: {optimal_params}")
    
    # Создание кастомного профиля
    modifications = {
        'style': 'calm',
        'speed_range': (0.6, 1.5),
        'supported_emotions': ['neutral', 'calm', 'peaceful']
    }
    
    success = voice_manager.create_custom_profile('alena_calm', selected_voice, modifications)
    print(f"Создан кастомный профиль: {success}")
```

## Ключевые моменты для экзамена

### Основные компоненты обработки речи
1. **Speech-to-Text**: Преобразование речи в текст с временными метками
2. **Text-to-Speech**: Синтез естественно звучащей речи из текста
3. **Audio Processing**: Предобработка, нормализация, фильтрация аудио
4. **Post-processing**: Улучшение результатов через орфографию и пунктуацию

### Технические аспекты
- **Форматы аудио**: WAV, MP3, FLAC и их особенности
- **Частота дискретизации**: 16kHz для речи, 44.1kHz для музыки
- **Обработка в реальном времени**: Streaming и chunking
- **Качество и точность**: Metrics для оценки производительности

### API и интеграции
- Google Speech-to-Text и Text-to-Speech
- Yandex SpeechKit для русского языка
- OpenAI Whisper для распознавания
- ElevenLabs для качественного синтеза

### Оптимизация и настройка
- Выбор голосов и их параметризация
- Адаптация под контекст и аудиторию
- Управление эмоциональной окраской
- Нормализация и предобработка текста

### Практические применения
- Голосовые помощники и чат-боты
- Аудиокниги и подкасты
- Системы IVR и автоответчики
- Доступность для людей с ограниченными возможностями
- Мультиязычные приложения