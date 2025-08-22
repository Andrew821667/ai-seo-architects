# Тема 30: AI-HR - Искусственный интеллект в HR

## Основы AI-HR систем

### Применение ИИ в HR процессах
- **Рекрутинг**: Автоматизация подбора персонала
- **Скрининг резюме**: Анализ и ранжирование кандидатов  
- **Интервью**: ИИ-ассистенты для проведения собеседований
- **Оценка персонала**: Анализ производительности сотрудников
- **Обучение**: Персонализированные программы развития
- **Retention**: Прогнозирование текучести кадров

### Архитектура AI-HR системы
```python
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import re
import json
import statistics

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class JobLevel(Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"

@dataclass
class Skill:
    """Навык кандидата или требование вакансии"""
    name: str
    level: SkillLevel
    years_experience: Optional[int] = None
    verified: bool = False
    certifications: List[str] = field(default_factory=list)

@dataclass
class Candidate:
    """Кандидат"""
    id: str
    name: str
    email: str
    phone: str
    skills: List[Skill]
    experience_years: int
    education: List[str]
    previous_companies: List[str]
    salary_expectation: Optional[int] = None
    availability: Optional[str] = None
    resume_text: str = ""
    interview_scores: Dict[str, float] = field(default_factory=dict)

@dataclass
class JobRequirement:
    """Требования к вакансии"""
    position: str
    level: JobLevel
    required_skills: List[Skill]
    preferred_skills: List[Skill]
    min_experience: int
    salary_range: Tuple[int, int]
    location: str
    remote_ok: bool
    description: str

@dataclass
class MatchResult:
    """Результат сопоставления кандидата и вакансии"""
    candidate_id: str
    job_id: str
    overall_score: float
    skill_match_score: float
    experience_match_score: float
    cultural_fit_score: float
    details: Dict[str, Any]
    recommendations: List[str]

class ResumeParser:
    """Парсер резюме"""
    
    def __init__(self):
        self.skill_patterns = self._initialize_skill_patterns()
        self.experience_patterns = self._initialize_experience_patterns()
    
    def _initialize_skill_patterns(self) -> Dict[str, List[str]]:
        """Инициализация паттернов для поиска навыков"""
        return {
            'programming': [
                r'\bpython\b', r'\bjava\b', r'\bjavascript\b', r'\bc\+\+\b',
                r'\bc#\b', r'\bruby\b', r'\bphp\b', r'\bgo\b', r'\brust\b'
            ],
            'databases': [
                r'\bmysql\b', r'\bpostgresql\b', r'\bmongodb\b', r'\boracle\b',
                r'\bredis\b', r'\belasticsearch\b', r'\bcassandra\b'
            ],
            'frameworks': [
                r'\bdjango\b', r'\bflask\b', r'\breact\b', r'\bvue\b',
                r'\bangular\b', r'\bspring\b', r'\b\.net\b'
            ],
            'ai_ml': [
                r'\bmachine learning\b', r'\bdeep learning\b', r'\btensorflow\b',
                r'\bpytorch\b', r'\bscikit-learn\b', r'\bnlp\b', r'\bcomputer vision\b'
            ],
            'tools': [
                r'\bgit\b', r'\bdocker\b', r'\bkubernetes\b', r'\baws\b',
                r'\bazure\b', r'\bgcp\b', r'\bjenkins\b', r'\bansible\b'
            ]
        }
    
    def _initialize_experience_patterns(self) -> List[str]:
        """Паттерны для поиска опыта работы"""
        return [
            r'(\d+)\s*(?:года?|лет|years?)\s*опыта',
            r'опыт\s*(\d+)\s*(?:года?|лет|years?)',
            r'(\d+)\+?\s*(?:года?|лет|years?)\s*в',
            r'более\s*(\d+)\s*(?:лет|года?)'
        ]
    
    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """Парсинг резюме"""
        
        parsed_data = {
            'skills': self._extract_skills(resume_text),
            'experience': self._extract_experience(resume_text),
            'education': self._extract_education(resume_text),
            'contact_info': self._extract_contact_info(resume_text),
            'companies': self._extract_companies(resume_text),
            'summary': self._extract_summary(resume_text)
        }
        
        return parsed_data
    
    def _extract_skills(self, text: str) -> List[Skill]:
        """Извлечение навыков из текста"""
        found_skills = []
        text_lower = text.lower()
        
        for category, patterns in self.skill_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                
                for match in matches:
                    # Определяем уровень навыка по контексту
                    skill_level = self._determine_skill_level(text, match)
                    
                    skill = Skill(
                        name=match,
                        level=skill_level,
                        years_experience=self._extract_skill_experience(text, match)
                    )
                    
                    found_skills.append(skill)
        
        # Удаляем дубликаты
        unique_skills = []
        seen_skills = set()
        
        for skill in found_skills:
            if skill.name not in seen_skills:
                unique_skills.append(skill)
                seen_skills.add(skill.name)
        
        return unique_skills
    
    def _determine_skill_level(self, text: str, skill_name: str) -> SkillLevel:
        """Определение уровня навыка по контексту"""
        skill_context = self._get_skill_context(text, skill_name)
        
        # Ключевые слова для определения уровня
        expert_keywords = ['эксперт', 'expert', 'архитект', 'лид', 'senior', 'advanced']
        intermediate_keywords = ['опытный', 'experienced', 'middle', 'intermediate']
        beginner_keywords = ['базовый', 'basic', 'начальный', 'junior', 'beginner']
        
        context_lower = skill_context.lower()
        
        for keyword in expert_keywords:
            if keyword in context_lower:
                return SkillLevel.EXPERT
        
        for keyword in intermediate_keywords:
            if keyword in context_lower:
                return SkillLevel.INTERMEDIATE
        
        for keyword in beginner_keywords:
            if keyword in context_lower:
                return SkillLevel.BEGINNER
        
        return SkillLevel.INTERMEDIATE  # По умолчанию
    
    def _get_skill_context(self, text: str, skill_name: str, 
                          context_window: int = 50) -> str:
        """Получение контекста вокруг упоминания навыка"""
        skill_index = text.lower().find(skill_name.lower())
        
        if skill_index == -1:
            return ""
        
        start_index = max(0, skill_index - context_window)
        end_index = min(len(text), skill_index + len(skill_name) + context_window)
        
        return text[start_index:end_index]
    
    def _extract_skill_experience(self, text: str, skill_name: str) -> Optional[int]:
        """Извлечение количества лет опыта с навыком"""
        context = self._get_skill_context(text, skill_name, 100)
        
        for pattern in self.experience_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _extract_experience(self, text: str) -> int:
        """Извлечение общего опыта работы"""
        total_experience = 0
        
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                try:
                    years = int(match) if isinstance(match, str) else int(match[0])
                    total_experience = max(total_experience, years)
                except (ValueError, TypeError):
                    continue
        
        return total_experience
    
    def _extract_education(self, text: str) -> List[str]:
        """Извлечение информации об образовании"""
        education_keywords = [
            'университет', 'институт', 'академия', 'колледж',
            'бакалавр', 'магистр', 'кандидат наук', 'доктор наук',
            'диплом', 'степень', 'образование'
        ]
        
        education_info = []
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                education_info.append(line.strip())
        
        return education_info[:5]  # Максимум 5 записей
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Извлечение контактной информации"""
        contact_info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Телефон
        phone_patterns = [
            r'\+7\s*\(\d{3}\)\s*\d{3}-\d{2}-\d{2}',
            r'\+7\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2}',
            r'8\s*\(\d{3}\)\s*\d{3}-\d{2}-\d{2}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                contact_info['phone'] = phones[0]
                break
        
        return contact_info
    
    def _extract_companies(self, text: str) -> List[str]:
        """Извлечение названий компаний"""
        # Простая эвристика: слова после "в", "работал в", "компания"
        company_patterns = [
            r'(?:в\s+|работал\s+в\s+|компани[яи]\s+)([А-ЯA-Z][а-яa-z\s&\.]+?)(?:\s|,|\.|\n)',
            r'([А-ЯA-Z][а-яa-z\s&\.]{3,})\s*(?:ООО|ОАО|ЗАО|Ltd|Inc|Corp)',
        ]
        
        companies = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.extend([match.strip() for match in matches])
        
        return list(set(companies))[:10]  # Уникальные, максимум 10
    
    def _extract_summary(self, text: str) -> str:
        """Извлечение краткой сводки о кандидате"""
        lines = text.split('\n')
        
        # Ищем секцию "О себе", "Резюме", "Summary"
        summary_keywords = ['о себе', 'резюме', 'summary', 'обо мне', 'краткая информация']
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in summary_keywords):
                # Берем следующие несколько строк как summary
                summary_lines = []
                for j in range(i + 1, min(i + 6, len(lines))):
                    if lines[j].strip() and not any(kw in lines[j].lower() for kw in ['опыт работы', 'образование', 'навыки']):
                        summary_lines.append(lines[j].strip())
                    else:
                        break
                
                if summary_lines:
                    return ' '.join(summary_lines)
        
        # Если специальной секции нет, берем первые несколько предложений
        sentences = text.split('.')[:3]
        return '. '.join(sentence.strip() for sentence in sentences if sentence.strip())

class CandidateMatcher:
    """Система сопоставления кандидатов и вакансий"""
    
    def __init__(self):
        self.skill_weights = {
            'exact_match': 1.0,
            'similar_skill': 0.7,
            'related_skill': 0.4,
            'transferable_skill': 0.3
        }
        
        self.skill_synonyms = {
            'python': ['питон', 'пайтон'],
            'javascript': ['js', 'джаваскрипт'],
            'machine learning': ['ml', 'машинное обучение', 'мл'],
            'artificial intelligence': ['ai', 'искусственный интеллект', 'ии']
        }
    
    def calculate_match_score(self, candidate: Candidate, 
                            job_req: JobRequirement) -> MatchResult:
        """Расчет соответствия кандидата вакансии"""
        
        # Оценка навыков
        skill_score = self._calculate_skill_match(candidate.skills, job_req.required_skills)
        
        # Оценка опыта
        experience_score = self._calculate_experience_match(
            candidate.experience_years, job_req.min_experience
        )
        
        # Оценка культурного соответствия (упрощенная)
        cultural_score = self._calculate_cultural_fit(candidate, job_req)
        
        # Общий балл (взвешенная сумма)
        overall_score = (
            skill_score * 0.5 +
            experience_score * 0.3 +
            cultural_score * 0.2
        )
        
        # Генерация рекомендаций
        recommendations = self._generate_recommendations(
            candidate, job_req, skill_score, experience_score
        )
        
        return MatchResult(
            candidate_id=candidate.id,
            job_id=f"{job_req.position}_{job_req.level.value}",
            overall_score=overall_score,
            skill_match_score=skill_score,
            experience_match_score=experience_score,
            cultural_fit_score=cultural_score,
            details={
                'matched_skills': self._get_matched_skills(candidate.skills, job_req.required_skills),
                'missing_skills': self._get_missing_skills(candidate.skills, job_req.required_skills),
                'experience_gap': max(0, job_req.min_experience - candidate.experience_years)
            },
            recommendations=recommendations
        )
    
    def _calculate_skill_match(self, candidate_skills: List[Skill], 
                             required_skills: List[Skill]) -> float:
        """Расчет соответствия навыков"""
        
        if not required_skills:
            return 1.0
        
        total_weight = 0
        matched_weight = 0
        
        for req_skill in required_skills:
            skill_weight = self._get_skill_importance_weight(req_skill)
            total_weight += skill_weight
            
            # Ищем соответствующий навык у кандидата
            best_match_score = 0
            
            for candidate_skill in candidate_skills:
                match_score = self._compare_skills(candidate_skill, req_skill)
                best_match_score = max(best_match_score, match_score)
            
            matched_weight += best_match_score * skill_weight
        
        return matched_weight / total_weight if total_weight > 0 else 0.0
    
    def _compare_skills(self, candidate_skill: Skill, required_skill: Skill) -> float:
        """Сравнение двух навыков"""
        
        # Точное совпадение названия
        if candidate_skill.name.lower() == required_skill.name.lower():
            level_score = self._compare_skill_levels(candidate_skill.level, required_skill.level)
            return level_score * self.skill_weights['exact_match']
        
        # Поиск в синонимах
        for main_skill, synonyms in self.skill_synonyms.items():
            if (candidate_skill.name.lower() in synonyms and 
                required_skill.name.lower() == main_skill) or \
               (required_skill.name.lower() in synonyms and 
                candidate_skill.name.lower() == main_skill):
                level_score = self._compare_skill_levels(candidate_skill.level, required_skill.level)
                return level_score * self.skill_weights['similar_skill']
        
        # Частичное совпадение (например, "React" vs "React Native")
        if (candidate_skill.name.lower() in required_skill.name.lower() or
            required_skill.name.lower() in candidate_skill.name.lower()):
            level_score = self._compare_skill_levels(candidate_skill.level, required_skill.level)
            return level_score * self.skill_weights['related_skill']
        
        return 0.0
    
    def _compare_skill_levels(self, candidate_level: SkillLevel, 
                            required_level: SkillLevel) -> float:
        """Сравнение уровней навыков"""
        level_mapping = {
            SkillLevel.BEGINNER: 1,
            SkillLevel.INTERMEDIATE: 2,
            SkillLevel.ADVANCED: 3,
            SkillLevel.EXPERT: 4
        }
        
        candidate_numeric = level_mapping[candidate_level]
        required_numeric = level_mapping[required_level]
        
        if candidate_numeric >= required_numeric:
            return 1.0
        elif candidate_numeric == required_numeric - 1:
            return 0.8  # Один уровень ниже
        elif candidate_numeric == required_numeric - 2:
            return 0.5  # Два уровня ниже
        else:
            return 0.2  # Значительно ниже
    
    def _get_skill_importance_weight(self, skill: Skill) -> float:
        """Получение веса важности навыка"""
        # В реальной системе это могло бы определяться на основе:
        # - Частоты упоминания в описании вакансии
        # - Критичности для позиции
        # - Рыночной востребованности
        
        core_skills = ['python', 'javascript', 'machine learning', 'sql']
        
        if skill.name.lower() in core_skills:
            return 1.5  # Повышенный вес для ключевых навыков
        
        return 1.0
    
    def _calculate_experience_match(self, candidate_exp: int, 
                                  required_exp: int) -> float:
        """Расчет соответствия опыта"""
        
        if candidate_exp >= required_exp:
            # Бонус за дополнительный опыт, но с убывающей отдачей
            bonus = min((candidate_exp - required_exp) * 0.1, 0.3)
            return min(1.0 + bonus, 1.0)
        else:
            # Штраф за недостаток опыта
            gap = required_exp - candidate_exp
            penalty = gap * 0.2
            return max(0.0, 1.0 - penalty)
    
    def _calculate_cultural_fit(self, candidate: Candidate, 
                              job_req: JobRequirement) -> float:
        """Расчет культурного соответствия (упрощенный)"""
        
        # Анализ предыдущих компаний
        company_size_match = 0.7  # Базовое значение
        
        # Анализ локации
        location_match = 1.0 if job_req.remote_ok else 0.8
        
        # Анализ зарплатных ожиданий
        salary_match = 1.0
        if candidate.salary_expectation and job_req.salary_range:
            min_salary, max_salary = job_req.salary_range
            
            if min_salary <= candidate.salary_expectation <= max_salary:
                salary_match = 1.0
            elif candidate.salary_expectation < min_salary:
                # Кандидат готов на меньшую зарплату
                salary_match = 0.9
            else:
                # Завышенные ожидания
                overpay_ratio = candidate.salary_expectation / max_salary
                salary_match = max(0.3, 1.0 - (overpay_ratio - 1.0))
        
        return statistics.mean([company_size_match, location_match, salary_match])
    
    def _get_matched_skills(self, candidate_skills: List[Skill], 
                          required_skills: List[Skill]) -> List[str]:
        """Получение списка совпавших навыков"""
        matched = []
        
        for req_skill in required_skills:
            for cand_skill in candidate_skills:
                if self._compare_skills(cand_skill, req_skill) > 0.7:
                    matched.append(req_skill.name)
                    break
        
        return matched
    
    def _get_missing_skills(self, candidate_skills: List[Skill], 
                          required_skills: List[Skill]) -> List[str]:
        """Получение списка недостающих навыков"""
        missing = []
        
        for req_skill in required_skills:
            has_skill = False
            
            for cand_skill in candidate_skills:
                if self._compare_skills(cand_skill, req_skill) > 0.7:
                    has_skill = True
                    break
            
            if not has_skill:
                missing.append(req_skill.name)
        
        return missing
    
    def _generate_recommendations(self, candidate: Candidate, job_req: JobRequirement,
                                skill_score: float, experience_score: float) -> List[str]:
        """Генерация рекомендаций"""
        recommendations = []
        
        if skill_score < 0.7:
            missing_skills = self._get_missing_skills(candidate.skills, job_req.required_skills)
            if missing_skills:
                recommendations.append(f"Изучить недостающие навыки: {', '.join(missing_skills[:3])}")
        
        if experience_score < 0.8:
            exp_gap = job_req.min_experience - candidate.experience_years
            if exp_gap > 0:
                recommendations.append(f"Получить дополнительный опыт: {exp_gap} лет")
        
        if skill_score > 0.8 and experience_score > 0.8:
            recommendations.append("Отличное соответствие! Рекомендуется к интервью")
        elif skill_score > 0.6 and experience_score > 0.6:
            recommendations.append("Хорошее соответствие, рассмотреть для интервью")
        else:
            recommendations.append("Слабое соответствие, рассмотреть для других позиций")
        
        return recommendations

# Демонстрация AI-HR системы
print("=== ДЕМОНСТРАЦИЯ AI-HR СИСТЕМЫ ===")

# Создаем парсер резюме
parser = ResumeParser()

# Пример резюме
sample_resume = """
Иван Петров
Senior Python Developer

Email: ivan.petrov@example.com
Телефон: +7 (495) 123-45-67

О себе:
Опытный разработчик с 5+ годами опыта в Python и машинном обучении.
Специализируюсь на создании ИИ-систем и анализе данных.

Навыки:
- Python (экспертный уровень) - 5 лет
- Machine Learning (TensorFlow, PyTorch) - 3 года  
- SQL, PostgreSQL - 4 года
- Docker, Kubernetes - 2 года
- Git, CI/CD - 4 года

Опыт работы:
- Яндекс (Senior Developer) - 2 года
- Mail.ru Group (Middle Developer) - 3 года

Образование:
МФТИ, Магистр прикладной математики и физики

Зарплатные ожидания: 300,000 руб/мес
"""

# Парсим резюме
parsed_resume = parser.parse_resume(sample_resume)

print("Результат парсинга резюме:")
print(f"Найдено навыков: {len(parsed_resume['skills'])}")
print(f"Опыт работы: {parsed_resume['experience']} лет")
print(f"Контакты: {parsed_resume['contact_info']}")
print(f"Компании: {parsed_resume['companies']}")

# Создаем кандидата
candidate = Candidate(
    id="cand_001",
    name="Иван Петров",
    email="ivan.petrov@example.com",
    phone="+7 (495) 123-45-67",
    skills=parsed_resume['skills'],
    experience_years=parsed_resume['experience'],
    education=parsed_resume['education'],
    previous_companies=parsed_resume['companies'],
    salary_expectation=300000,
    resume_text=sample_resume
)

# Создаем требования вакансии
job_requirement = JobRequirement(
    position="AI Engineer",
    level=JobLevel.SENIOR,
    required_skills=[
        Skill("python", SkillLevel.ADVANCED),
        Skill("machine learning", SkillLevel.INTERMEDIATE),
        Skill("sql", SkillLevel.INTERMEDIATE)
    ],
    preferred_skills=[
        Skill("docker", SkillLevel.INTERMEDIATE),
        Skill("kubernetes", SkillLevel.BEGINNER)
    ],
    min_experience=4,
    salary_range=(280000, 350000),
    location="Москва",
    remote_ok=True,
    description="Разработка ИИ-систем для анализа данных"
)

# Проводим сопоставление
matcher = CandidateMatcher()
match_result = matcher.calculate_match_score(candidate, job_requirement)

print(f"\n=== РЕЗУЛЬТАТ СОПОСТАВЛЕНИЯ ===")
print(f"Общий балл: {match_result.overall_score:.2f}")
print(f"Соответствие навыков: {match_result.skill_match_score:.2f}")
print(f"Соответствие опыта: {match_result.experience_match_score:.2f}")
print(f"Культурное соответствие: {match_result.cultural_fit_score:.2f}")

print(f"\nСовпавшие навыки: {match_result.details['matched_skills']}")
print(f"Недостающие навыки: {match_result.details['missing_skills']}")

print(f"\nРекомендации:")
for recommendation in match_result.recommendations:
    print(f"  💡 {recommendation}")
```

## Автоматизация HR процессов

### Система интервью с ИИ
```python
class AIInterviewer:
    """ИИ-интервьюер"""
    
    def __init__(self):
        self.question_bank = self._initialize_question_bank()
        self.evaluation_criteria = self._initialize_evaluation_criteria()
        self.interview_flow = {}
    
    def _initialize_question_bank(self) -> Dict[str, List[Dict]]:
        """Инициализация банка вопросов"""
        return {
            'technical': [
                {
                    'question': 'Объясните разницу между списком и кортежем в Python',
                    'difficulty': 'junior',
                    'expected_keywords': ['изменяемый', 'неизменяемый', 'mutable', 'immutable'],
                    'evaluation_time': 300  # секунд
                },
                {
                    'question': 'Как работает механизм сборки мусора в Python?',
                    'difficulty': 'senior',
                    'expected_keywords': ['reference counting', 'циклические ссылки', 'gc'],
                    'evaluation_time': 600
                },
                {
                    'question': 'Опишите архитектуру микросервисов',
                    'difficulty': 'middle',
                    'expected_keywords': ['API', 'независимость', 'масштабируемость'],
                    'evaluation_time': 450
                }
            ],
            'behavioral': [
                {
                    'question': 'Расскажите о сложной проблеме, которую вам пришлось решать',
                    'difficulty': 'universal',
                    'evaluation_criteria': ['структурированность', 'конкретность', 'результат'],
                    'evaluation_time': 420
                },
                {
                    'question': 'Как вы работаете в команде?',
                    'difficulty': 'universal',
                    'evaluation_criteria': ['коммуникация', 'сотрудничество', 'конфликты'],
                    'evaluation_time': 300
                }
            ],
            'situational': [
                {
                    'question': 'Ваш код не прошел код-ревью. Как будете действовать?',
                    'difficulty': 'middle',
                    'evaluation_criteria': ['принятие критики', 'готовность учиться', 'профессионализм'],
                    'evaluation_time': 360
                }
            ]
        }
    
    def _initialize_evaluation_criteria(self) -> Dict[str, Dict]:
        """Критерии оценки ответов"""
        return {
            'technical': {
                'accuracy': 0.4,      # Техническая корректность
                'completeness': 0.3,  # Полнота ответа
                'clarity': 0.2,       # Ясность изложения
                'depth': 0.1          # Глубина понимания
            },
            'behavioral': {
                'structure': 0.25,    # Структурированность ответа
                'examples': 0.25,     # Наличие конкретных примеров
                'self_awareness': 0.25, # Самосознание
                'communication': 0.25  # Коммуникативные навыки
            },
            'situational': {
                'problem_solving': 0.3, # Навыки решения проблем
                'decision_making': 0.3, # Принятие решений
                'leadership': 0.2,      # Лидерские качества
                'adaptability': 0.2     # Адаптивность
            }
        }
    
    def generate_interview_plan(self, candidate: Candidate, 
                              job_req: JobRequirement,
                              interview_duration: int = 3600) -> Dict[str, Any]:
        """Генерация плана интервью"""
        
        plan = {
            'candidate_id': candidate.id,
            'job_position': job_req.position,
            'total_duration': interview_duration,
            'questions': [],
            'time_allocation': {},
            'focus_areas': []
        }
        
        # Определяем фокусные области на основе вакансии
        if job_req.level in [JobLevel.SENIOR, JobLevel.LEAD]:
            plan['focus_areas'] = ['technical', 'behavioral', 'situational']
            plan['time_allocation'] = {'technical': 0.5, 'behavioral': 0.3, 'situational': 0.2}
        else:
            plan['focus_areas'] = ['technical', 'behavioral']
            plan['time_allocation'] = {'technical': 0.7, 'behavioral': 0.3}
        
        # Выбираем вопросы для каждой области
        for area in plan['focus_areas']:
            area_duration = interview_duration * plan['time_allocation'][area]
            area_questions = self._select_questions_for_area(area, job_req.level, area_duration)
            
            plan['questions'].extend(area_questions)
        
        return plan
    
    def _select_questions_for_area(self, area: str, job_level: JobLevel, 
                                 duration: int) -> List[Dict]:
        """Выбор вопросов для области"""
        
        available_questions = self.question_bank.get(area, [])
        
        # Фильтруем по уровню сложности
        level_mapping = {
            JobLevel.JUNIOR: ['junior', 'universal'],
            JobLevel.MIDDLE: ['junior', 'middle', 'universal'],
            JobLevel.SENIOR: ['middle', 'senior', 'universal'],
            JobLevel.LEAD: ['senior', 'universal'],
            JobLevel.PRINCIPAL: ['senior', 'universal']
        }
        
        suitable_difficulties = level_mapping.get(job_level, ['universal'])
        
        filtered_questions = [q for q in available_questions 
                            if q.get('difficulty') in suitable_difficulties]
        
        # Выбираем вопросы в пределах времени
        selected_questions = []
        used_time = 0
        
        for question in filtered_questions:
            question_time = question.get('evaluation_time', 300)
            
            if used_time + question_time <= duration:
                selected_questions.append({
                    **question,
                    'area': area,
                    'allocated_time': question_time
                })
                used_time += question_time
            
            if used_time >= duration * 0.9:  # Используем 90% времени
                break
        
        return selected_questions
    
    def evaluate_answer(self, question: Dict, answer: str) -> Dict[str, Any]:
        """Оценка ответа кандидата"""
        
        area = question['area']
        criteria = self.evaluation_criteria[area]
        
        scores = {}
        
        if area == 'technical':
            scores = self._evaluate_technical_answer(question, answer)
        elif area == 'behavioral':
            scores = self._evaluate_behavioral_answer(question, answer)
        elif area == 'situational':
            scores = self._evaluate_situational_answer(question, answer)
        
        # Вычисляем взвешенную оценку
        weighted_score = sum(scores[criterion] * weight 
                           for criterion, weight in criteria.items() 
                           if criterion in scores)
        
        return {
            'overall_score': weighted_score,
            'detailed_scores': scores,
            'evaluation_criteria': criteria,
            'feedback': self._generate_feedback(scores, criteria)
        }
    
    def _evaluate_technical_answer(self, question: Dict, answer: str) -> Dict[str, float]:
        """Оценка технического ответа"""
        
        # Проверка наличия ожидаемых ключевых слов
        expected_keywords = question.get('expected_keywords', [])
        found_keywords = sum(1 for keyword in expected_keywords 
                           if keyword.lower() in answer.lower())
        
        accuracy = found_keywords / max(len(expected_keywords), 1)
        
        # Оценка полноты (по длине и структуре)
        words_count = len(answer.split())
        completeness = min(words_count / 50, 1.0)  # Ожидаем ~50 слов для полного ответа
        
        # Оценка ясности (отсутствие филлеров и структурированность)
        filler_words = ['ну', 'вот', 'как бы', 'типа', 'в принципе']
        filler_count = sum(1 for filler in filler_words if filler in answer.lower())
        clarity = max(0, 1.0 - filler_count / max(words_count, 1) * 10)
        
        # Оценка глубины (наличие примеров и деталей)
        depth_indicators = ['пример', 'например', 'то есть', 'конкретно', 'детально']
        depth_score = sum(1 for indicator in depth_indicators if indicator in answer.lower())
        depth = min(depth_score / 3, 1.0)
        
        return {
            'accuracy': accuracy,
            'completeness': completeness,
            'clarity': clarity,
            'depth': depth
        }
    
    def _evaluate_behavioral_answer(self, question: Dict, answer: str) -> Dict[str, float]:
        """Оценка поведенческого ответа"""
        
        # STAR структура (Situation, Task, Action, Result)
        star_keywords = {
            'situation': ['ситуация', 'было', 'произошло', 'случилось'],
            'task': ['задача', 'нужно было', 'требовалось', 'цель'],
            'action': ['сделал', 'предпринял', 'решил', 'действие'],
            'result': ['результат', 'итог', 'получилось', 'завершилось']
        }
        
        structure_score = 0
        for component, keywords in star_keywords.items():
            if any(keyword in answer.lower() for keyword in keywords):
                structure_score += 0.25
        
        # Наличие конкретных примеров
        example_indicators = ['когда я', 'однажды', 'в проекте', 'в компании', 'например']
        examples_score = min(
            sum(1 for indicator in example_indicators if indicator in answer.lower()) / 2,
            1.0
        )
        
        # Самосознание (рефлексия и выводы)
        self_awareness_indicators = ['понял', 'осознал', 'вывод', 'урок', 'научился']
        self_awareness = min(
            sum(1 for indicator in self_awareness_indicators if indicator in answer.lower()) / 2,
            1.0
        )
        
        # Коммуникативные навыки (связность и логичность)
        sentences = answer.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        communication = 1.0 - max(0, (avg_sentence_length - 20) / 30)  # Оптимально ~20 слов
        
        return {
            'structure': structure_score,
            'examples': examples_score,
            'self_awareness': self_awareness,
            'communication': max(0.3, communication)  # Минимум 0.3
        }
    
    def _evaluate_situational_answer(self, question: Dict, answer: str) -> Dict[str, float]:
        """Оценка ситуационного ответа"""
        
        # Навыки решения проблем
        problem_solving_words = ['анализ', 'причина', 'решение', 'подход', 'метод']
        problem_solving = min(
            sum(1 for word in problem_solving_words if word in answer.lower()) / 3,
            1.0
        )
        
        # Принятие решений
        decision_words = ['решил', 'выбрал', 'определил', 'принял решение', 'решение']
        decision_making = min(
            sum(1 for word in decision_words if word in answer.lower()) / 2,
            1.0
        )
        
        # Лидерские качества
        leadership_words = ['команда', 'руководил', 'координировал', 'организовал', 'делегировал']
        leadership = min(
            sum(1 for word in leadership_words if word in answer.lower()) / 2,
            1.0
        )
        
        # Адаптивность
        adaptability_words = ['изменил', 'адаптировал', 'скорректировал', 'гибкость', 'приспособился']
        adaptability = min(
            sum(1 for word in adaptability_words if word in answer.lower()) / 2,
            1.0
        )
        
        return {
            'problem_solving': problem_solving,
            'decision_making': decision_making,
            'leadership': leadership,
            'adaptability': adaptability
        }
    
    def _generate_feedback(self, scores: Dict[str, float], 
                          criteria: Dict[str, float]) -> List[str]:
        """Генерация обратной связи"""
        feedback = []
        
        for criterion, score in scores.items():
            weight = criteria.get(criterion, 0)
            
            if score >= 0.8:
                feedback.append(f"✅ Отлично по критерию '{criterion}': {score:.2f}")
            elif score >= 0.6:
                feedback.append(f"✨ Хорошо по критерию '{criterion}': {score:.2f}")
            elif score >= 0.4:
                feedback.append(f"⚠️ Удовлетворительно по '{criterion}': {score:.2f}")
            else:
                feedback.append(f"❌ Требует улучшения '{criterion}': {score:.2f}")
        
        return feedback

# Демонстрация ИИ-интервьюера
interviewer = AIInterviewer()

# Генерируем план интервью
interview_plan = interviewer.generate_interview_plan(candidate, job_requirement, 3600)

print(f"\n=== ПЛАН ИНТЕРВЬЮ ===")
print(f"Кандидат: {candidate.name}")
print(f"Позиция: {job_requirement.position}")
print(f"Длительность: {interview_plan['total_duration']//60} минут")

print(f"\nФокусные области: {interview_plan['focus_areas']}")
print(f"Распределение времени: {interview_plan['time_allocation']}")

print(f"\nВопросы ({len(interview_plan['questions'])}):")
for i, question in enumerate(interview_plan['questions'][:3], 1):  # Первые 3
    print(f"  {i}. [{question['area']}] {question['question']}")
    print(f"     Время: {question['allocated_time']//60} мин, Сложность: {question['difficulty']}")

# Симуляция оценки ответа
sample_answer = """
В Python список (list) является изменяемым типом данных, то есть мы можем добавлять, 
удалять и изменять элементы после создания. Например, my_list = [1, 2, 3] и я могу 
сделать my_list.append(4). А кортеж (tuple) неизменяемый - после создания нельзя 
изменить содержимое. Например, my_tuple = (1, 2, 3) и попытка my_tuple[0] = 5 вызовет ошибку.
"""

question = interview_plan['questions'][0]  # Первый вопрос
evaluation = interviewer.evaluate_answer(question, sample_answer)

print(f"\n=== ОЦЕНКА ОТВЕТА ===")
print(f"Общая оценка: {evaluation['overall_score']:.2f}")
print("Детальные оценки:")
for criterion, score in evaluation['detailed_scores'].items():
    print(f"  {criterion}: {score:.2f}")

print("\nОбратная связь:")
for feedback_item in evaluation['feedback']:
    print(f"  {feedback_item}")
```

## Аналитика и прогнозирование

### Прогнозирование текучести кадров
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class EmployeeTurnoverPredictor:
    """Прогнозирование текучести кадров"""
    
    def __init__(self):
        self.risk_factors = {
            'performance': {'weight': 0.25, 'threshold': 3.5},  # Из 5
            'satisfaction': {'weight': 0.30, 'threshold': 3.0},
            'engagement': {'weight': 0.20, 'threshold': 3.2},
            'work_life_balance': {'weight': 0.15, 'threshold': 3.0},
            'career_growth': {'weight': 0.10, 'threshold': 2.8}
        }
        
        self.historical_data = []
    
    def calculate_turnover_risk(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет риска увольнения сотрудника"""
        
        risk_score = 0
        factor_analysis = {}
        
        for factor, config in self.risk_factors.items():
            value = employee_data.get(factor, config['threshold'])
            weight = config['weight']
            threshold = config['threshold']
            
            # Чем ниже значение, тем выше риск
            if value < threshold:
                factor_risk = (threshold - value) / threshold
            else:
                factor_risk = 0
            
            weighted_risk = factor_risk * weight
            risk_score += weighted_risk
            
            factor_analysis[factor] = {
                'value': value,
                'threshold': threshold,
                'risk_contribution': weighted_risk,
                'status': 'high_risk' if factor_risk > 0.3 else 'low_risk'
            }
        
        # Дополнительные факторы риска
        additional_risks = self._analyze_additional_factors(employee_data)
        risk_score += additional_risks['total_additional_risk']
        
        # Классификация уровня риска
        if risk_score >= 0.7:
            risk_level = 'critical'
        elif risk_score >= 0.5:
            risk_level = 'high'
        elif risk_score >= 0.3:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        # Генерация рекомендаций
        recommendations = self._generate_retention_recommendations(
            factor_analysis, additional_risks, employee_data
        )
        
        return {
            'employee_id': employee_data.get('id'),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'factor_analysis': factor_analysis,
            'additional_factors': additional_risks,
            'recommendations': recommendations,
            'estimated_turnover_probability': min(risk_score * 1.2, 1.0)
        }
    
    def _analyze_additional_factors(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ дополнительных факторов риска"""
        
        additional_risk = 0
        factors = {}
        
        # Время в компании
        tenure_months = employee_data.get('tenure_months', 12)
        if tenure_months < 6:
            factors['short_tenure'] = 0.2
            additional_risk += 0.2
        elif tenure_months > 60:  # Более 5 лет
            factors['long_tenure_stagnation'] = 0.1
            additional_risk += 0.1
        
        # Зарплата относительно рынка
        salary_ratio = employee_data.get('salary_to_market_ratio', 1.0)
        if salary_ratio < 0.8:
            factors['underpaid'] = 0.3
            additional_risk += 0.3
        elif salary_ratio < 0.9:
            factors['below_market'] = 0.15
            additional_risk += 0.15
        
        # Частота изменений в команде
        team_turnover = employee_data.get('team_turnover_rate', 0.1)
        if team_turnover > 0.25:
            factors['high_team_turnover'] = 0.2
            additional_risk += 0.2
        
        # Отсутствие продвижения
        months_since_promotion = employee_data.get('months_since_promotion', 12)
        if months_since_promotion > 24:
            factors['no_recent_promotion'] = 0.15
            additional_risk += 0.15
        
        # Перегрузка работой
        avg_hours_per_week = employee_data.get('avg_hours_per_week', 40)
        if avg_hours_per_week > 50:
            factors['overwork'] = 0.25
            additional_risk += 0.25
        
        return {
            'factors': factors,
            'total_additional_risk': additional_risk
        }
    
    def _generate_retention_recommendations(self, factor_analysis: Dict, 
                                          additional_risks: Dict,
                                          employee_data: Dict) -> List[str]:
        """Генерация рекомендаций по удержанию"""
        
        recommendations = []
        
        # Рекомендации на основе основных факторов
        for factor, analysis in factor_analysis.items():
            if analysis['status'] == 'high_risk':
                if factor == 'performance':
                    recommendations.append("Предоставить дополнительное обучение и поддержку")
                    recommendations.append("Провести ментворинг с опытным коллегой")
                elif factor == 'satisfaction':
                    recommendations.append("Провести индивидуальную беседу о проблемах")
                    recommendations.append("Рассмотреть изменения в рабочих условиях")
                elif factor == 'engagement':
                    recommendations.append("Привлечь к интересным проектам")
                    recommendations.append("Дать больше автономии в работе")
                elif factor == 'career_growth':
                    recommendations.append("Обсудить карьерные планы и пути развития")
                    recommendations.append("Предложить участие в корпоративных программах обучения")
        
        # Рекомендации на основе дополнительных факторов
        additional_factors = additional_risks['factors']
        
        if 'underpaid' in additional_factors:
            recommendations.append("СРОЧНО: Пересмотреть уровень компенсации")
            recommendations.append("Предложить дополнительные льготы и бонусы")
        
        if 'overwork' in additional_factors:
            recommendations.append("Перераспределить рабочую нагрузку")
            recommendations.append("Обсудить work-life balance")
        
        if 'no_recent_promotion' in additional_factors:
            recommendations.append("Рассмотреть возможность продвижения")
            recommendations.append("Расширить зону ответственности")
        
        if 'high_team_turnover' in additional_factors:
            recommendations.append("Провести анализ проблем в команде")
            recommendations.append("Рассмотреть перевод в другую команду")
        
        return recommendations[:5]  # Топ-5 рекомендаций
    
    def batch_risk_assessment(self, employees_data: List[Dict]) -> Dict[str, Any]:
        """Массовая оценка рисков увольнения"""
        
        risk_assessments = []
        
        for employee in employees_data:
            risk_assessment = self.calculate_turnover_risk(employee)
            risk_assessments.append(risk_assessment)
        
        # Анализ по организации
        total_employees = len(risk_assessments)
        
        risk_distribution = {
            'critical': sum(1 for r in risk_assessments if r['risk_level'] == 'critical'),
            'high': sum(1 for r in risk_assessments if r['risk_level'] == 'high'),
            'medium': sum(1 for r in risk_assessments if r['risk_level'] == 'medium'),
            'low': sum(1 for r in risk_assessments if r['risk_level'] == 'low')
        }
        
        # Вычисляем проценты
        risk_percentages = {level: (count / total_employees) * 100 
                          for level, count in risk_distribution.items()}
        
        # Топ факторы риска
        all_factors = {}
        for assessment in risk_assessments:
            for factor, analysis in assessment['factor_analysis'].items():
                if analysis['status'] == 'high_risk':
                    all_factors[factor] = all_factors.get(factor, 0) + 1
        
        top_risk_factors = sorted(all_factors.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Критические случаи
        critical_employees = [r for r in risk_assessments if r['risk_level'] in ['critical', 'high']]
        
        return {
            'total_employees': total_employees,
            'risk_distribution': risk_distribution,
            'risk_percentages': risk_percentages,
            'top_risk_factors': top_risk_factors,
            'critical_employees_count': len(critical_employees),
            'estimated_turnover_rate': sum(r['estimated_turnover_probability'] for r in risk_assessments) / total_employees,
            'detailed_assessments': risk_assessments
        }

# Демонстрация системы прогнозирования текучести
predictor = EmployeeTurnoverPredictor()

# Создаем тестовые данные сотрудников
employees_test_data = [
    {
        'id': 'emp_001',
        'name': 'Анна Смирнова',
        'performance': 4.2,
        'satisfaction': 2.8,  # Низкая удовлетворенность
        'engagement': 3.1,
        'work_life_balance': 2.5,  # Проблемы с балансом
        'career_growth': 3.0,
        'tenure_months': 18,
        'salary_to_market_ratio': 0.75,  # Недоплачивают
        'team_turnover_rate': 0.15,
        'months_since_promotion': 30,
        'avg_hours_per_week': 55  # Переработки
    },
    {
        'id': 'emp_002', 
        'name': 'Петр Иванов',
        'performance': 4.8,
        'satisfaction': 4.5,
        'engagement': 4.2,
        'work_life_balance': 4.0,
        'career_growth': 3.8,
        'tenure_months': 36,
        'salary_to_market_ratio': 1.1,
        'team_turnover_rate': 0.05,
        'months_since_promotion': 8,
        'avg_hours_per_week': 42
    },
    {
        'id': 'emp_003',
        'name': 'Мария Петрова',
        'performance': 3.9,
        'satisfaction': 3.2,
        'engagement': 2.9,
        'work_life_balance': 3.5,
        'career_growth': 2.5,  # Низкий рост
        'tenure_months': 48,
        'salary_to_market_ratio': 0.85,
        'team_turnover_rate': 0.30,  # Высокая текучка в команде
        'months_since_promotion': 36,
        'avg_hours_per_week': 45
    }
]

# Проводим массовую оценку рисков
batch_assessment = predictor.batch_risk_assessment(employees_test_data)

print(f"\n=== АНАЛИЗ РИСКОВ ТЕКУЧЕСТИ ===")
print(f"Всего сотрудников: {batch_assessment['total_employees']}")
print(f"Прогнозируемая текучесть: {batch_assessment['estimated_turnover_rate']:.1%}")

print(f"\nРаспределение рисков:")
for level, percentage in batch_assessment['risk_percentages'].items():
    print(f"  {level.upper()}: {percentage:.1f}% ({batch_assessment['risk_distribution'][level]} чел.)")

print(f"\nТоп факторы риска:")
for factor, count in batch_assessment['top_risk_factors']:
    print(f"  {factor}: {count} сотрудников")

print(f"\nКритические случаи: {batch_assessment['critical_employees_count']}")

# Детальный анализ критических случаев
critical_assessments = [r for r in batch_assessment['detailed_assessments'] 
                       if r['risk_level'] in ['critical', 'high']]

for assessment in critical_assessments:
    print(f"\n--- Сотрудник ID: {assessment['employee_id']} ---")
    print(f"Уровень риска: {assessment['risk_level'].upper()}")
    print(f"Риск увольнения: {assessment['estimated_turnover_probability']:.1%}")
    
    print("Главные проблемы:")
    for factor, analysis in assessment['factor_analysis'].items():
        if analysis['status'] == 'high_risk':
            print(f"  ❌ {factor}: {analysis['value']:.1f} (норма: {analysis['threshold']})")
    
    print("Рекомендации:")
    for rec in assessment['recommendations'][:3]:  # Топ-3
        print(f"  💡 {rec}")
```

## Автоматизация HR процессов

### Система обратной связи и 360-градусной оценки
```python
class FeedbackSystem:
    """Система сбора и анализа обратной связи"""
    
    def __init__(self):
        self.feedback_types = ['self', 'manager', 'peer', 'subordinate', 'client']
        self.competency_framework = {
            'technical_skills': ['Профессиональные навыки', 'Качество работы', 'Инновации'],
            'communication': ['Устная коммуникация', 'Письменная коммуникация', 'Презентации'],
            'leadership': ['Мотивация команды', 'Принятие решений', 'Видение'],
            'collaboration': ['Работа в команде', 'Конфликты', 'Поддержка коллег'],
            'adaptability': ['Обучаемость', 'Гибкость', 'Изменения']
        }
    
    def collect_360_feedback(self, employee_id: str, 
                           feedback_requests: List[Dict]) -> Dict[str, Any]:
        """Сбор 360-градусной обратной связи"""
        
        feedback_data = {
            'employee_id': employee_id,
            'feedback_by_type': {},
            'competency_scores': {},
            'qualitative_feedback': [],
            'development_areas': [],
            'strengths': []
        }
        
        # Группируем фидбек по типам
        for feedback in feedback_requests:
            feedback_type = feedback['type']
            
            if feedback_type not in feedback_data['feedback_by_type']:
                feedback_data['feedback_by_type'][feedback_type] = []
            
            feedback_data['feedback_by_type'][feedback_type].append(feedback)
        
        # Анализируем по компетенциям
        for competency, sub_skills in self.competency_framework.items():
            competency_scores = []
            
            for feedback in feedback_requests:
                if competency in feedback.get('scores', {}):
                    competency_scores.append(feedback['scores'][competency])
            
            if competency_scores:
                avg_score = statistics.mean(competency_scores)
                std_dev = statistics.stdev(competency_scores) if len(competency_scores) > 1 else 0
                
                feedback_data['competency_scores'][competency] = {
                    'average': avg_score,
                    'std_deviation': std_dev,
                    'feedback_count': len(competency_scores),
                    'consistency': 1.0 - min(std_dev / 2, 1.0)  # Высокая согласованность если низкий разброс
                }
        
        # Определяем сильные стороны и области развития
        if feedback_data['competency_scores']:
            scores_items = list(feedback_data['competency_scores'].items())
            
            # Сортируем по средней оценке
            sorted_scores = sorted(scores_items, key=lambda x: x[1]['average'], reverse=True)
            
            # Топ-3 сильные стороны
            feedback_data['strengths'] = [item[0] for item in sorted_scores[:3] 
                                        if item[1]['average'] >= 4.0]
            
            # Области для развития (оценка < 3.5)
            feedback_data['development_areas'] = [item[0] for item in sorted_scores 
                                                if item[1]['average'] < 3.5]
        
        return feedback_data
    
    def generate_development_plan(self, feedback_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация плана развития"""
        
        development_plan = {
            'employee_id': feedback_analysis['employee_id'],
            'development_goals': [],
            'learning_recommendations': [],
            'timeline': '6 месяцев',
            'success_metrics': []
        }
        
        # Цели на основе областей развития
        for area in feedback_analysis['development_areas']:
            if area == 'technical_skills':
                development_plan['development_goals'].append(
                    "Повысить технические навыки до уровня 4.0/5.0"
                )
                development_plan['learning_recommendations'].extend([
                    "Пройти сертификацию по ключевым технологиям",
                    "Участвовать в технических конференциях",
                    "Взять ментора из senior команды"
                ])
            
            elif area == 'communication':
                development_plan['development_goals'].append(
                    "Улучшить коммуникативные навыки"
                )
                development_plan['learning_recommendations'].extend([
                    "Пройти курс публичных выступлений",
                    "Практиковать презентации в малых группах",
                    "Получить коучинг по коммуникации"
                ])
            
            elif area == 'leadership':
                development_plan['development_goals'].append(
                    "Развить лидерские компетенции"
                )
                development_plan['learning_recommendations'].extend([
                    "Пройти программу лидерского развития",
                    "Возглавить небольшой проект",
                    "Получить ментворинг от руководителя высшего звена"
                ])
        
        # Метрики успеха
        for goal in development_plan['development_goals']:
            if 'технические навыки' in goal.lower():
                development_plan['success_metrics'].append("Повышение технической оценки до 4.0+")
            elif 'коммуникация' in goal.lower():
                development_plan['success_metrics'].append("Улучшение коммуникативной оценки на 0.5 балла")
            elif 'лидерство' in goal.lower():
                development_plan['success_metrics'].append("Успешное завершение лидерского проекта")
        
        return development_plan

# Демонстрация системы обратной связи
feedback_system = FeedbackSystem()

# Создаем тестовые отзывы для 360-оценки
sample_feedback = [
    {
        'type': 'manager',
        'scores': {
            'technical_skills': 4.2,
            'communication': 3.8,
            'leadership': 3.5,
            'collaboration': 4.0,
            'adaptability': 4.1
        },
        'comments': 'Отличные технические навыки, но нужно работать над лидерством'
    },
    {
        'type': 'peer',
        'scores': {
            'technical_skills': 4.0,
            'communication': 3.2,
            'leadership': 3.0,
            'collaboration': 4.5,
            'adaptability': 3.8
        },
        'comments': 'Замечательный коллега, но иногда сложно понять объяснения'
    },
    {
        'type': 'subordinate',
        'scores': {
            'technical_skills': 4.5,
            'communication': 3.0,
            'leadership': 2.8,
            'collaboration': 3.8,
            'adaptability': 3.5
        },
        'comments': 'Очень компетентен технически, но недостаточно вовлекает команду в принятие решений'
    }
]

# Собираем и анализируем обратную связь
feedback_analysis = feedback_system.collect_360_feedback('emp_004', sample_feedback)

print(f"\n=== 360-ГРАДУСНАЯ ОЦЕНКА ===")
print(f"Сотрудник: {feedback_analysis['employee_id']}")

print(f"\nОценки по компетенциям:")
for competency, scores in feedback_analysis['competency_scores'].items():
    consistency_indicator = "🟢" if scores['consistency'] > 0.8 else "🟡" if scores['consistency'] > 0.6 else "🔴"
    print(f"  {competency}: {scores['average']:.2f} ± {scores['std_deviation']:.2f} {consistency_indicator}")

print(f"\nСильные стороны: {feedback_analysis['strengths']}")
print(f"Области развития: {feedback_analysis['development_areas']}")

# Генерируем план развития
development_plan = feedback_system.generate_development_plan(feedback_analysis)

print(f"\n=== ПЛАН РАЗВИТИЯ ===")
print(f"Срок: {development_plan['timeline']}")

print(f"\nЦели развития:")
for goal in development_plan['development_goals']:
    print(f"  🎯 {goal}")

print(f"\nРекомендации по обучению:")
for recommendation in development_plan['learning_recommendations'][:5]:
    print(f"  📚 {recommendation}")

print(f"\nМетрики успеха:")
for metric in development_plan['success_metrics']:
    print(f"  📊 {metric}")
```

## Ключевые моменты для экзамена

### Основные области применения AI в HR
1. **Рекрутинг**: Автоматический скрининг резюме и ранжирование кандидатов
2. **Подбор персонала**: Сопоставление навыков и требований вакансий
3. **Оценка производительности**: 360-градусная обратная связь и анализ
4. **Прогнозирование**: Риски текучести кадров и планирование персонала

### Технические решения
- **NLP для резюме**: Извлечение навыков, опыта, образования
- **Scoring algorithms**: Алгоритмы оценки соответствия кандидатов
- **Predictive analytics**: Машинное обучение для прогнозов
- **Sentiment analysis**: Анализ отзывов и комментариев

### Этические аспекты AI-HR
- **Bias prevention**: Предотвращение дискриминации в алгоритмах
- **Transparency**: Прозрачность процессов принятия решений
- **Privacy**: Защита персональных данных сотрудников
- **Fairness**: Справедливость в оценке и отборе

### Метрики и KPI
- **Recruitment metrics**: Time-to-hire, cost-per-hire, quality-of-hire
- **Retention metrics**: Turnover rate, tenure, engagement scores
- **Performance metrics**: Goal achievement, 360-feedback scores
- **Development metrics**: Learning completion, skill progression

### Практические преимущества
- Сокращение времени подбора персонала
- Повышение качества найма
- Раннее выявление рисков увольнения
- Персонализированное развитие сотрудников
- Объективизация HR процессов