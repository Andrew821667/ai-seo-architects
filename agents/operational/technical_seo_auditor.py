"""
Technical SEO Auditor Agent - Operational уровень
Специализированный агент для проведения технического SEO аудита сайтов
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import math
import re
from urllib.parse import urlparse

from core.base_agent import BaseAgent
from core.interfaces.data_models import LeadInput, LeadOutput
from core.enhanced_methods import SEOAIModelsEnhancer

class TechnicalSEOAuditorAgent(BaseAgent):
    """
    Technical SEO Auditor Agent - Operational уровень

    Ответственность:
    - Комплексный технический SEO аудит сайтов
    - Core Web Vitals анализ и оптимизация
    - Crawling и индексация (robots.txt, sitemaps, canonicals)
    - Структурированные данные (Schema.org)
    - Мобильная оптимизация (Mobile-First)
    - Международное SEO (hreflang, геотаргетинг)
    - Performance optimization (скорость загрузки)
    - Security & HTTPS анализ
    """

    def __init__(self, data_provider=None, **kwargs):
        # Устанавливаем модель по умолчанию для Operational уровня
        if 'model_name' not in kwargs:
            kwargs['model_name'] = "gpt-4o-mini"
            
        super().__init__(
            agent_id="technical_seo_auditor",
            name="Technical SEO Auditor Agent",
            data_provider=data_provider,
            knowledge_base="knowledge/operational/technical_seo_auditor.md",
            **kwargs
        )

        # Инициализация SEO AI Models enhancer
        self.enhancer = SEOAIModelsEnhancer(data_provider) if data_provider else None

        # Инициализация статистики
        self.stats = {
            'total_tasks': 0,
            'success_count': 0,
            'error_count': 0,
            'total_processing_time': 0.0,
            'audits_completed': 0,
            'critical_issues_found': 0,
            'sites_audited': set()
        }

        # Technical SEO Audit Configuration
        self.audit_categories = {
            'core_web_vitals': {
                'weight': 0.25,  # 25% важности
                'thresholds': {
                    'lcp': {'good': 2.5, 'needs_improvement': 4.0},  # seconds
                    'fid': {'good': 100, 'needs_improvement': 300},  # milliseconds
                    'cls': {'good': 0.1, 'needs_improvement': 0.25}, # score
                    'fcp': {'good': 1.8, 'needs_improvement': 3.0},  # seconds
                    'ttfb': {'good': 0.6, 'needs_improvement': 1.6}  # seconds
                }
            },
            'crawling_indexing': {
                'weight': 0.20,  # 20% важности
                'checks': [
                    'robots_txt_valid', 'xml_sitemap_present', 'canonical_tags',
                    'meta_robots', 'noindex_issues', 'redirect_chains',
                    'status_codes', 'duplicate_content'
                ]
            },
            'mobile_optimization': {
                'weight': 0.20,  # 20% важности
                'checks': [
                    'mobile_friendly', 'responsive_design', 'viewport_meta',
                    'touch_elements', 'mobile_page_speed', 'amp_implementation'
                ]
            },
            'structured_data': {
                'weight': 0.15,  # 15% важности
                'checks': [
                    'schema_markup', 'json_ld_valid', 'rich_snippets',
                    'product_markup', 'organization_markup', 'breadcrumbs'
                ]
            },
            'technical_foundation': {
                'weight': 0.10,  # 10% важности
                'checks': [
                    'https_implementation', 'html_validation', 'css_validation',
                    'javascript_errors', 'broken_links', 'image_optimization'
                ]
            },
            'international_seo': {
                'weight': 0.10,  # 10% важности
                'checks': [
                    'hreflang_tags', 'language_targeting', 'geo_targeting',
                    'currency_localization', 'content_localization'
                ]
            }
        }

        # Critical Issue Thresholds
        self.critical_thresholds = {
            'technical_score_min': 70,  # Минимальный технический балл
            'core_web_vitals_failing': 3,  # Максимум провальных CWV метрик
            'crawling_errors_max': 10,  # Максимум ошибок crawling
            'broken_links_max': 50,  # Максимум битых ссылок
            'page_speed_min': 3.0,  # Минимальная скорость загрузки (сек)
            'mobile_score_min': 80   # Минимальный мобильный балл
        }

        # Audit Tools & APIs (будущие интеграции)
        self.audit_tools = {
            'crawling': ['Screaming Frog API', 'Sitebulb API', 'ContentKing API'],
            'performance': ['PageSpeed Insights API', 'GTmetrix API', 'WebPageTest API'],
            'validation': ['W3C Validator', 'Schema.org Validator', 'Rich Results Test'],
            'monitoring': ['Google Search Console API', 'Bing Webmaster API'],
            'security': ['SSL Labs API', 'Security Headers API']
        }

        # Industry-specific audit focuses
        self.industry_audit_focus = {
            'ecommerce': {
                'priority_checks': ['product_schema', 'checkout_optimization', 'category_crawling'],
                'critical_metrics': ['conversion_funnel', 'product_page_speed', 'mobile_commerce'],
                'weight_adjustments': {'structured_data': 0.20, 'mobile_optimization': 0.25}
            },
            'news_media': {
                'priority_checks': ['article_schema', 'amp_pages', 'news_sitemap'],
                'critical_metrics': ['article_load_time', 'google_news_compliance'],
                'weight_adjustments': {'core_web_vitals': 0.30, 'structured_data': 0.20}
            },
            'local_business': {
                'priority_checks': ['local_business_schema', 'google_my_business', 'local_citations'],
                'critical_metrics': ['local_pack_visibility', 'mobile_local_speed'],
                'weight_adjustments': {'mobile_optimization': 0.25, 'international_seo': 0.05}
            },
            'b2b_services': {
                'priority_checks': ['service_schema', 'contact_optimization', 'lead_generation'],
                'critical_metrics': ['conversion_tracking', 'form_optimization'],
                'weight_adjustments': {'technical_foundation': 0.15, 'crawling_indexing': 0.25}
            }
        }

        print(f"🔧 {self.name} инициализирован:")
        print(f"📊 Audit Categories: {len(self.audit_categories)} основных категорий")
        print(f"🎯 Critical Score Threshold: {self.critical_thresholds['technical_score_min']}+")
        print(f"⚡ Core Web Vitals: LCP<{self.audit_categories['core_web_vitals']['thresholds']['lcp']['good']}s")
        print(f"🛠️ Tools Integration: {sum(len(tools) for tools in self.audit_tools.values())} инструментов")

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки технического SEO аудита
        """
        start_time = datetime.now()

        try:
            # Извлекаем данные
            input_data = task_data.get('input_data', {})
            task_type = input_data.get('task_type', 'full_technical_audit')

            print(f"🔧 Обработка Technical SEO задачи: {task_type}")

            # Роутинг по типам задач с enhanced функциональностью
            if task_type == 'full_technical_audit':
                # Базовый аудит
                result = await self._conduct_full_technical_audit(task_data)
                
                # Enhanced анализ через SEO AI Models
                if self.enhancer and input_data.get('domain'):
                    try:
                        enhanced_result = await self.enhancer.enhanced_technical_audit(
                            input_data['domain'], 
                            **input_data
                        )
                        result['enhanced_analysis'] = enhanced_result
                        result['enhanced'] = True
                    except Exception as e:
                        result['enhanced_error'] = str(e)
                        result['enhanced'] = False
            elif task_type == 'core_web_vitals_audit':
                result = await self._audit_core_web_vitals(input_data)
            elif task_type == 'crawling_audit':
                result = await self._audit_crawling_indexing(input_data)
            elif task_type == 'mobile_audit':
                result = await self._audit_mobile_optimization(input_data)
            elif task_type == 'structured_data_audit':
                result = await self._audit_structured_data(input_data)
            elif task_type == 'performance_audit':
                result = await self._audit_performance_optimization(input_data)
            elif task_type == 'security_audit':
                result = await self._audit_security_https(input_data)
            else:
                # Default: Full Technical Audit
                result = await self._conduct_full_technical_audit(task_data)

            # Метрики производительности
            processing_time = (datetime.now() - start_time).total_seconds()

            # Обновляем статистику агента
            self.stats['total_tasks'] += 1
            self.stats['total_processing_time'] += processing_time
            self.stats['success_count'] += 1
            self.stats['audits_completed'] += 1
            
            # Считаем критические проблемы
            critical_issues = result.get('audit_summary', {}).get('critical_issues_count', 0)
            self.stats['critical_issues_found'] += critical_issues
            
            # Добавляем сайт в статистику
            domain = input_data.get('domain', input_data.get('url', ''))
            if domain:
                self.stats['sites_audited'].add(domain)

            # Формируем финальный результат
            audit_result = {
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'task_type': task_type,
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': round(processing_time, 2),
                'result': result,
                'operational_level': True,
                'audit_quality': result.get('audit_quality', 'comprehensive'),
                'requires_immediate_action': result.get('requires_immediate_action', False),
                'success': True
            }

            print(f"✅ Technical SEO аудит завершен за {processing_time:.2f}с")
            return audit_result

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.stats['total_tasks'] += 1
            self.stats['total_processing_time'] += processing_time
            self.stats['error_count'] += 1

            error_result = {
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'task_type': task_data.get('input_data', {}).get('task_type', 'unknown'),
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': round(processing_time, 2),
                'error': str(e),
                'operational_level': True,
                'success': False
            }

            print(f"❌ Ошибка в Technical SEO аудите: {str(e)}")
            return error_result

    async def _conduct_full_technical_audit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Проведение полного технического SEO аудита
        """
        # Умное извлечение данных
        if 'input_data' in data:
            audit_data = data.get('input_data', {})
        else:
            audit_data = data.get('audit_data', {})
            
        domain = audit_data.get('domain', audit_data.get('url', 'example.com'))
        industry = audit_data.get('industry', 'b2b_services').lower()
        
        print(f"🔍 Technical SEO Auditor анализирует:")
        print(f"   Domain: {domain}")
        print(f"   Industry: {industry}")
        print(f"   Audit Type: Full Technical Audit")

        # 1. Core Web Vitals Analysis
        core_web_vitals = self._analyze_core_web_vitals(audit_data)
        
        # 2. Crawling & Indexing Analysis
        crawling_analysis = self._analyze_crawling_indexing(audit_data)
        
        # 3. Mobile Optimization Analysis
        mobile_analysis = self._analyze_mobile_optimization(audit_data)
        
        # 4. Structured Data Analysis
        structured_data_analysis = self._analyze_structured_data(audit_data, industry)
        
        # 5. Technical Foundation Analysis
        technical_foundation = self._analyze_technical_foundation(audit_data)
        
        # 6. International SEO Analysis
        international_seo = self._analyze_international_seo(audit_data)
        
        # 7. Calculate Overall Technical Score
        overall_score = self._calculate_technical_seo_score(
            core_web_vitals, crawling_analysis, mobile_analysis,
            structured_data_analysis, technical_foundation, international_seo,
            industry
        )
        
        # 8. Generate Prioritized Recommendations
        recommendations = self._generate_technical_recommendations(
            overall_score, core_web_vitals, crawling_analysis, mobile_analysis
        )
        
        # 9. Create Action Plan
        action_plan = self._create_technical_action_plan(recommendations, overall_score)

        return {
            'technical_audit_results': {
                'overall_technical_score': overall_score['total_score'],
                'core_web_vitals': core_web_vitals,
                'crawling_indexing': crawling_analysis,
                'mobile_optimization': mobile_analysis,
                'structured_data': structured_data_analysis,
                'technical_foundation': technical_foundation,
                'international_seo': international_seo
            },
            'audit_summary': {
                'audit_quality': self._determine_audit_quality(overall_score['total_score']),
                'critical_issues_count': overall_score['critical_issues'],
                'priority_level': self._determine_priority_level(overall_score['total_score']),
                'estimated_fix_time': self._estimate_fix_timeline(recommendations)
            },
            'prioritized_recommendations': recommendations,
            'technical_action_plan': action_plan,
            'requires_immediate_action': overall_score['total_score'] < self.critical_thresholds['technical_score_min'],
            'confidence_score': self._calculate_audit_confidence(overall_score, audit_data)
        }

    def _analyze_core_web_vitals(self, audit_data: Dict) -> Dict[str, Any]:
        """
        Анализ Core Web Vitals метрик
        """
        # Симуляция данных (в реальности - через PageSpeed Insights API)
        current_lcp = audit_data.get('lcp', 3.2)  # seconds
        current_fid = audit_data.get('fid', 150)  # milliseconds
        current_cls = audit_data.get('cls', 0.15) # score
        current_fcp = audit_data.get('fcp', 2.1)  # seconds
        current_ttfb = audit_data.get('ttfb', 0.8) # seconds

        thresholds = self.audit_categories['core_web_vitals']['thresholds']
        
        # Оценка каждой метрики
        def evaluate_metric(current, thresholds_dict):
            if current <= thresholds_dict['good']:
                return {'status': 'good', 'score': 100}
            elif current <= thresholds_dict['needs_improvement']:
                return {'status': 'needs_improvement', 'score': 60}
            else:
                return {'status': 'poor', 'score': 20}

        lcp_eval = evaluate_metric(current_lcp, thresholds['lcp'])
        fid_eval = evaluate_metric(current_fid, thresholds['fid'])
        cls_eval = evaluate_metric(current_cls, thresholds['cls'])
        fcp_eval = evaluate_metric(current_fcp, thresholds['fcp'])
        ttfb_eval = evaluate_metric(current_ttfb, thresholds['ttfb'])

        # Общий балл Core Web Vitals
        cwv_score = int((lcp_eval['score'] + fid_eval['score'] + cls_eval['score']) / 3)
        extended_score = int((cwv_score + fcp_eval['score'] + ttfb_eval['score']) / 3)

        return {
            'overall_cwv_score': cwv_score,
            'extended_performance_score': extended_score,
            'metrics': {
                'lcp': {'current': current_lcp, 'target': thresholds['lcp']['good'], **lcp_eval},
                'fid': {'current': current_fid, 'target': thresholds['fid']['good'], **fid_eval},
                'cls': {'current': current_cls, 'target': thresholds['cls']['good'], **cls_eval},
                'fcp': {'current': current_fcp, 'target': thresholds['fcp']['good'], **fcp_eval},
                'ttfb': {'current': current_ttfb, 'target': thresholds['ttfb']['good'], **ttfb_eval}
            },
            'failing_metrics': [
                metric for metric, data in {
                    'lcp': lcp_eval, 'fid': fid_eval, 'cls': cls_eval
                }.items() if data['status'] == 'poor'
            ],
            'priority_fixes': self._identify_cwv_priority_fixes(current_lcp, current_fid, current_cls)
        }

    def _analyze_crawling_indexing(self, audit_data: Dict) -> Dict[str, Any]:
        """
        Анализ crawling и индексации
        """
        # Симуляция анализа crawling (в реальности - через Screaming Frog API)
        domain = audit_data.get('domain', 'example.com')
        
        # Базовые проверки
        robots_txt_valid = audit_data.get('robots_txt_valid', True)
        xml_sitemap_present = audit_data.get('xml_sitemap_present', True)
        canonical_issues = audit_data.get('canonical_issues', 5)
        redirect_chains = audit_data.get('redirect_chains', 3)
        status_code_errors = audit_data.get('status_code_errors', 12)
        duplicate_content_pages = audit_data.get('duplicate_content_pages', 8)

        # Расчет балла crawling
        crawling_issues = []
        crawling_score = 100

        if not robots_txt_valid:
            crawling_issues.append('robots_txt_invalid')
            crawling_score -= 15

        if not xml_sitemap_present:
            crawling_issues.append('xml_sitemap_missing')
            crawling_score -= 20

        if canonical_issues > 10:
            crawling_issues.append('canonical_issues_high')
            crawling_score -= 15
        elif canonical_issues > 0:
            crawling_score -= canonical_issues * 1.5

        if redirect_chains > 5:
            crawling_issues.append('redirect_chains_excessive')
            crawling_score -= 10
        elif redirect_chains > 0:
            crawling_score -= redirect_chains * 2

        if status_code_errors > 20:
            crawling_issues.append('status_code_errors_high')
            crawling_score -= 20
        elif status_code_errors > 0:
            crawling_score -= status_code_errors * 1

        if duplicate_content_pages > 15:
            crawling_issues.append('duplicate_content_high')
            crawling_score -= 15
        elif duplicate_content_pages > 0:
            crawling_score -= duplicate_content_pages * 0.5

        crawling_score = max(int(crawling_score), 0)

        return {
            'crawling_score': crawling_score,
            'crawling_health': 'excellent' if crawling_score >= 90 else 'good' if crawling_score >= 70 else 'needs_improvement' if crawling_score >= 50 else 'poor',
            'technical_checks': {
                'robots_txt_valid': robots_txt_valid,
                'xml_sitemap_present': xml_sitemap_present,
                'canonical_issues_count': canonical_issues,
                'redirect_chains': redirect_chains,
                'status_code_errors': status_code_errors,
                'duplicate_content_pages': duplicate_content_pages
            },
            'crawling_issues': crawling_issues,
            'indexing_recommendations': self._generate_crawling_recommendations(crawling_issues, crawling_score)
        }

    def _analyze_mobile_optimization(self, audit_data: Dict) -> Dict[str, Any]:
        """
        Анализ мобильной оптимизации
        """
        # Симуляция мобильного анализа
        mobile_friendly = audit_data.get('mobile_friendly', True)
        responsive_design = audit_data.get('responsive_design', True)
        viewport_meta = audit_data.get('viewport_meta', True)
        mobile_page_speed = audit_data.get('mobile_page_speed', 4.2)  # seconds
        touch_elements_appropriate = audit_data.get('touch_elements_appropriate', True)
        amp_implemented = audit_data.get('amp_implemented', False)

        # Расчет мобильного балла
        mobile_score = 100
        mobile_issues = []

        if not mobile_friendly:
            mobile_issues.append('not_mobile_friendly')
            mobile_score -= 30

        if not responsive_design:
            mobile_issues.append('not_responsive')
            mobile_score -= 25

        if not viewport_meta:
            mobile_issues.append('viewport_meta_missing')
            mobile_score -= 10

        if mobile_page_speed > 5.0:
            mobile_issues.append('mobile_speed_very_slow')
            mobile_score -= 20
        elif mobile_page_speed > 3.0:
            mobile_issues.append('mobile_speed_slow')
            mobile_score -= 10

        if not touch_elements_appropriate:
            mobile_issues.append('touch_elements_too_small')
            mobile_score -= 15

        # Бонус за AMP
        if amp_implemented:
            mobile_score += 5

        mobile_score = max(int(mobile_score), 0)

        return {
            'mobile_score': mobile_score,
            'mobile_grade': self._get_mobile_grade(mobile_score),
            'mobile_checks': {
                'mobile_friendly': mobile_friendly,
                'responsive_design': responsive_design,
                'viewport_meta': viewport_meta,
                'mobile_page_speed': mobile_page_speed,
                'touch_elements_appropriate': touch_elements_appropriate,
                'amp_implemented': amp_implemented
            },
            'mobile_issues': mobile_issues,
            'mobile_recommendations': self._generate_mobile_recommendations(mobile_issues, mobile_page_speed),
            'mobile_first_compliance': mobile_score >= self.critical_thresholds['mobile_score_min']
        }

    def _analyze_structured_data(self, audit_data: Dict, industry: str) -> Dict[str, Any]:
        """
        Анализ структурированных данных
        """
        # Симуляция анализа Schema.org
        schema_markup_present = audit_data.get('schema_markup_present', False)
        json_ld_valid = audit_data.get('json_ld_valid', True)
        rich_snippets_eligible = audit_data.get('rich_snippets_eligible', 0)
        schema_types_count = audit_data.get('schema_types_count', 2)

        # Отраслевые Schema.org требования
        industry_schemas = self.industry_audit_focus.get(industry, {}).get('priority_checks', [])
        
        structured_data_score = 0
        structured_data_issues = []

        if schema_markup_present:
            structured_data_score += 40
            
            if json_ld_valid:
                structured_data_score += 20
            else:
                structured_data_issues.append('json_ld_invalid')
                
            structured_data_score += min(schema_types_count * 10, 30)
            structured_data_score += min(rich_snippets_eligible * 5, 10)
        else:
            structured_data_issues.append('schema_markup_missing')

        # Отраслевые проверки
        industry_compliance = len([check for check in industry_schemas if audit_data.get(check, False)])
        industry_score = (industry_compliance / max(len(industry_schemas), 1)) * 20
        structured_data_score += industry_score

        structured_data_score = min(int(structured_data_score), 100)

        return {
            'structured_data_score': structured_data_score,
            'schema_implementation_level': self._get_schema_level(structured_data_score),
            'schema_checks': {
                'schema_markup_present': schema_markup_present,
                'json_ld_valid': json_ld_valid,
                'schema_types_count': schema_types_count,
                'rich_snippets_eligible': rich_snippets_eligible,
                'industry_compliance_score': industry_score
            },
            'structured_data_issues': structured_data_issues,
            'schema_recommendations': self._generate_schema_recommendations(industry, structured_data_issues),
            'rich_snippet_opportunities': self._identify_rich_snippet_opportunities(industry)
        }

    def _analyze_technical_foundation(self, audit_data: Dict) -> Dict[str, Any]:
        """
        Анализ технической основы
        """
        https_implemented = audit_data.get('https_implemented', True)
        html_valid = audit_data.get('html_valid', True)
        css_valid = audit_data.get('css_valid', True)
        javascript_errors = audit_data.get('javascript_errors', 3)
        broken_links = audit_data.get('broken_links', 8)
        image_optimization = audit_data.get('image_optimization_score', 75)

        foundation_score = 100
        foundation_issues = []

        if not https_implemented:
            foundation_issues.append('https_not_implemented')
            foundation_score -= 30

        if not html_valid:
            foundation_issues.append('html_validation_errors')
            foundation_score -= 10

        if not css_valid:
            foundation_issues.append('css_validation_errors')
            foundation_score -= 5

        if javascript_errors > 10:
            foundation_issues.append('javascript_errors_high')
            foundation_score -= 15
        elif javascript_errors > 0:
            foundation_score -= javascript_errors * 1.5

        if broken_links > self.critical_thresholds['broken_links_max']:
            foundation_issues.append('broken_links_excessive')
            foundation_score -= 20
        elif broken_links > 0:
            foundation_score -= broken_links * 0.5

        if image_optimization < 60:
            foundation_issues.append('image_optimization_poor')
            foundation_score -= 15
        elif image_optimization < 80:
            foundation_score -= (80 - image_optimization) * 0.5

        foundation_score = max(int(foundation_score), 0)

        return {
            'technical_foundation_score': foundation_score,
            'foundation_health': 'excellent' if foundation_score >= 90 else 'good' if foundation_score >= 75 else 'needs_improvement',
            'foundation_checks': {
                'https_implemented': https_implemented,
                'html_valid': html_valid,
                'css_valid': css_valid,
                'javascript_errors': javascript_errors,
                'broken_links': broken_links,
                'image_optimization_score': image_optimization
            },
            'foundation_issues': foundation_issues,
            'security_compliance': https_implemented and len(foundation_issues) <= 2
        }

    def _analyze_international_seo(self, audit_data: Dict) -> Dict[str, Any]:
        """
        Анализ международной SEO оптимизации
        """
        has_multiple_languages = audit_data.get('has_multiple_languages', False)
        hreflang_implemented = audit_data.get('hreflang_implemented', False)
        language_targeting = audit_data.get('language_targeting_correct', True)
        geo_targeting = audit_data.get('geo_targeting_setup', False)
        
        if not has_multiple_languages:
            # Если сайт одноязычный, международное SEO менее критично
            return {
                'international_seo_score': 80,  # Базовый балл для одноязычных сайтов
                'international_relevance': 'single_language_site',
                'international_checks': {
                    'has_multiple_languages': False,
                    'requires_international_seo': False
                },
                'international_recommendations': ['Consider expansion to international markets']
            }

        # Анализ для многоязычных сайтов
        international_score = 50  # Базовый балл за многоязычность
        international_issues = []

        if hreflang_implemented:
            international_score += 30
        else:
            international_issues.append('hreflang_missing')

        if language_targeting:
            international_score += 10
        else:
            international_issues.append('language_targeting_incorrect')

        if geo_targeting:
            international_score += 10
        else:
            international_issues.append('geo_targeting_not_setup')

        return {
            'international_seo_score': min(international_score, 100),
            'international_relevance': 'multi_language_site',
            'international_checks': {
                'has_multiple_languages': has_multiple_languages,
                'hreflang_implemented': hreflang_implemented,
                'language_targeting_correct': language_targeting,
                'geo_targeting_setup': geo_targeting
            },
            'international_issues': international_issues,
            'international_recommendations': self._generate_international_recommendations(international_issues)
        }

    def _calculate_technical_seo_score(self, core_web_vitals: Dict, crawling: Dict, 
                                     mobile: Dict, structured_data: Dict, 
                                     foundation: Dict, international: Dict, 
                                     industry: str) -> Dict[str, Any]:
        """
        Расчет общего технического SEO балла с учетом весов
        """
        # Получаем веса (возможно скорректированные для индустрии)
        weights = self._get_industry_adjusted_weights(industry)
        
        # Рассчитываем взвешенный балл
        total_score = (
            core_web_vitals['overall_cwv_score'] * weights['core_web_vitals'] +
            crawling['crawling_score'] * weights['crawling_indexing'] +
            mobile['mobile_score'] * weights['mobile_optimization'] +
            structured_data['structured_data_score'] * weights['structured_data'] +
            foundation['technical_foundation_score'] * weights['technical_foundation'] +
            international['international_seo_score'] * weights['international_seo']
        )

        total_score = int(total_score)
        
        # Подсчет критических проблем
        critical_issues = 0
        if core_web_vitals['overall_cwv_score'] < 60:
            critical_issues += 1
        if crawling['crawling_score'] < 70:
            critical_issues += 1
        if mobile['mobile_score'] < self.critical_thresholds['mobile_score_min']:
            critical_issues += 1
        if foundation['technical_foundation_score'] < 70:
            critical_issues += 1

        return {
            'total_score': total_score,
            'grade': self._get_technical_grade(total_score),
            'critical_issues': critical_issues,
            'category_scores': {
                'core_web_vitals': core_web_vitals['overall_cwv_score'],
                'crawling_indexing': crawling['crawling_score'],
                'mobile_optimization': mobile['mobile_score'],
                'structured_data': structured_data['structured_data_score'],
                'technical_foundation': foundation['technical_foundation_score'],
                'international_seo': international['international_seo_score']
            },
            'weighted_contributions': {
                category: score * weight for category, (score, weight) in zip(
                    ['core_web_vitals', 'crawling_indexing', 'mobile_optimization', 
                     'structured_data', 'technical_foundation', 'international_seo'],
                    [(core_web_vitals['overall_cwv_score'], weights['core_web_vitals']),
                     (crawling['crawling_score'], weights['crawling_indexing']),
                     (mobile['mobile_score'], weights['mobile_optimization']),
                     (structured_data['structured_data_score'], weights['structured_data']),
                     (foundation['technical_foundation_score'], weights['technical_foundation']),
                     (international['international_seo_score'], weights['international_seo'])]
                )
            }
        }

    def _generate_technical_recommendations(self, overall_score: Dict, 
                                          core_web_vitals: Dict, crawling: Dict, 
                                          mobile: Dict) -> List[Dict[str, Any]]:
        """
        Генерация приоритизированных технических рекомендаций
        """
        recommendations = []

        # Critical Issues (Priority: Critical)
        if overall_score['total_score'] < self.critical_thresholds['technical_score_min']:
            recommendations.append({
                'type': 'critical_technical_issues',
                'priority': 'critical',
                'category': 'overall',
                'issue': f"Общий технический балл {overall_score['total_score']} ниже критического порога {self.critical_thresholds['technical_score_min']}",
                'action': 'Немедленная техническая оптимизация по всем категориям',
                'estimated_impact': 'high',
                'estimated_effort': 'high',
                'timeline': '2-4 недели'
            })

        # Core Web Vitals Issues
        if core_web_vitals['overall_cwv_score'] < 70:
            for metric in core_web_vitals.get('failing_metrics', []):
                recommendations.append({
                    'type': 'core_web_vitals',
                    'priority': 'high',
                    'category': 'performance',
                    'issue': f"Core Web Vitals: {metric.upper()} не соответствует стандартам Google",
                    'action': self._get_cwv_fix_action(metric),
                    'estimated_impact': 'high',
                    'estimated_effort': 'medium',
                    'timeline': '1-2 недели'
                })

        # Mobile Issues
        if mobile['mobile_score'] < self.critical_thresholds['mobile_score_min']:
            for issue in mobile.get('mobile_issues', []):
                recommendations.append({
                    'type': 'mobile_optimization',
                    'priority': 'high',
                    'category': 'mobile',
                    'issue': f"Мобильная оптимизация: {issue}",
                    'action': self._get_mobile_fix_action(issue),
                    'estimated_impact': 'high',
                    'estimated_effort': 'medium',
                    'timeline': '1-3 недели'
                })

        # Crawling Issues
        if crawling['crawling_score'] < 70:
            for issue in crawling.get('crawling_issues', []):
                recommendations.append({
                    'type': 'crawling_indexing',
                    'priority': 'medium',
                    'category': 'technical',
                    'issue': f"Crawling и индексация: {issue}",
                    'action': self._get_crawling_fix_action(issue),
                    'estimated_impact': 'medium',
                    'estimated_effort': 'low',
                    'timeline': '3-7 дней'
                })

        # Сортируем по приоритету
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))

        return recommendations[:10]  # Топ-10 рекомендаций

    def _create_technical_action_plan(self, recommendations: List[Dict], 
                                    overall_score: Dict) -> Dict[str, Any]:
        """
        Создание технического action plan
        """
        # Группировка рекомендаций по фазам
        phases = {
            'phase_1_critical': {
                'duration': '1-2 недели',
                'focus': 'Критические технические проблемы',
                'actions': [r for r in recommendations if r['priority'] == 'critical'],
                'success_criteria': 'Технический балл > 70'
            },
            'phase_2_performance': {
                'duration': '2-4 недели',
                'focus': 'Core Web Vitals и производительность',
                'actions': [r for r in recommendations if r['priority'] == 'high' and r['category'] == 'performance'],
                'success_criteria': 'Все CWV метрики в зеленой зоне'
            },
            'phase_3_optimization': {
                'duration': '4-6 недель',
                'focus': 'Полная техническая оптимизация',
                'actions': [r for r in recommendations if r['priority'] in ['medium', 'low']],
                'success_criteria': 'Технический балл > 90'
            }
        }

        # Оценка временных затрат
        total_effort_weeks = sum([
            2 if len(phases['phase_1_critical']['actions']) > 0 else 0,
            3 if len(phases['phase_2_performance']['actions']) > 0 else 0,
            4 if len(phases['phase_3_optimization']['actions']) > 0 else 0
        ])

        return {
            'implementation_phases': phases,
            'timeline_estimation': {
                'total_duration_weeks': total_effort_weeks,
                'immediate_actions_count': len(phases['phase_1_critical']['actions']),
                'high_priority_actions': len(phases['phase_2_performance']['actions']),
                'optimization_actions': len(phases['phase_3_optimization']['actions'])
            },
            'resource_requirements': {
                'technical_developer': 'required' if overall_score['total_score'] < 70 else 'recommended',
                'seo_specialist': 'required',
                'ux_designer': 'recommended' if any(r['category'] == 'mobile' for r in recommendations) else 'optional'
            },
            'expected_outcomes': {
                'traffic_improvement': self._estimate_traffic_improvement(overall_score['total_score']),
                'ranking_improvement': 'moderate' if overall_score['total_score'] < 70 else 'minor',
                'user_experience_improvement': 'significant' if overall_score['critical_issues'] > 0 else 'moderate'
            }
        }

    # Вспомогательные методы
    def _get_industry_adjusted_weights(self, industry: str) -> Dict[str, float]:
        """Получение весов с учетом отраслевых особенностей"""
        base_weights = {category: data['weight'] for category, data in self.audit_categories.items()}
        
        if industry in self.industry_audit_focus:
            adjustments = self.industry_audit_focus[industry].get('weight_adjustments', {})
            for category, new_weight in adjustments.items():
                if category in base_weights:
                    base_weights[category] = new_weight
                    
        return base_weights

    def _identify_cwv_priority_fixes(self, lcp: float, fid: float, cls: float) -> List[str]:
        """Идентификация приоритетных исправлений для CWV"""
        fixes = []
        if lcp > 4.0:
            fixes.extend(['optimize_images', 'improve_server_response', 'eliminate_render_blocking'])
        if fid > 300:
            fixes.extend(['reduce_javascript', 'optimize_main_thread', 'code_splitting'])
        if cls > 0.25:
            fixes.extend(['set_image_dimensions', 'reserve_ad_space', 'avoid_dynamic_content'])
        return fixes

    def _generate_crawling_recommendations(self, issues: List[str], score: int) -> List[str]:
        """Генерация рекомендаций по crawling"""
        recommendations = []
        if 'robots_txt_invalid' in issues:
            recommendations.append('Correct robots.txt syntax and directives')
        if 'xml_sitemap_missing' in issues:
            recommendations.append('Create and submit XML sitemap to search engines')
        if 'canonical_issues_high' in issues:
            recommendations.append('Review and fix canonical tag implementation')
        if 'redirect_chains_excessive' in issues:
            recommendations.append('Eliminate redirect chains and loops')
        if score < 70:
            recommendations.append('Conduct comprehensive crawl audit with Screaming Frog')
        return recommendations

    def _generate_mobile_recommendations(self, issues: List[str], speed: float) -> List[str]:
        """Генерация рекомендаций по мобильной оптимизации"""
        recommendations = []
        if 'not_mobile_friendly' in issues:
            recommendations.append('Implement mobile-friendly design immediately')
        if 'not_responsive' in issues:
            recommendations.append('Implement responsive web design')
        if 'viewport_meta_missing' in issues:
            recommendations.append('Add viewport meta tag to all pages')
        if speed > 5.0:
            recommendations.append('Optimize mobile page speed (critical)')
        elif speed > 3.0:
            recommendations.append('Improve mobile page speed performance')
        if 'touch_elements_too_small' in issues:
            recommendations.append('Increase touch element sizes and spacing')
        return recommendations

    def _generate_schema_recommendations(self, industry: str, issues: List[str]) -> List[str]:
        """Генерация рекомендаций по структурированным данным"""
        recommendations = []
        if 'schema_markup_missing' in issues:
            recommendations.append('Implement basic Schema.org structured data')
        if 'json_ld_invalid' in issues:
            recommendations.append('Fix JSON-LD validation errors')
            
        # Отраслевые рекомендации
        industry_schemas = {
            'ecommerce': ['Product', 'Review', 'Organization', 'BreadcrumbList'],
            'news_media': ['Article', 'Organization', 'Person', 'BreadcrumbList'],
            'local_business': ['LocalBusiness', 'Organization', 'PostalAddress'],
            'b2b_services': ['Service', 'Organization', 'ContactPoint']
        }
        
        if industry in industry_schemas:
            for schema_type in industry_schemas[industry]:
                recommendations.append(f'Implement {schema_type} schema markup')
                
        return recommendations

    def _generate_international_recommendations(self, issues: List[str]) -> List[str]:
        """Генерация рекомендаций по международному SEO"""
        recommendations = []
        if 'hreflang_missing' in issues:
            recommendations.append('Implement hreflang tags for language/region targeting')
        if 'language_targeting_incorrect' in issues:
            recommendations.append('Configure correct language targeting in Search Console')
        if 'geo_targeting_not_setup' in issues:
            recommendations.append('Set up geo-targeting for international markets')
        return recommendations

    def _identify_rich_snippet_opportunities(self, industry: str) -> List[str]:
        """Идентификация возможностей для rich snippets"""
        opportunities = {
            'ecommerce': ['Product rich snippets', 'Review stars', 'Price', 'Availability'],
            'news_media': ['Article snippets', 'Author information', 'Publication date'],
            'local_business': ['Business information', 'Reviews', 'Hours', 'Location'],
            'b2b_services': ['Service snippets', 'FAQ', 'How-to guides']
        }
        return opportunities.get(industry, ['Organization info', 'Breadcrumbs', 'FAQ'])

    def _get_mobile_grade(self, score: int) -> str:
        """Получение мобильной оценки"""
        if score >= 90: return 'A+'
        elif score >= 80: return 'A'
        elif score >= 70: return 'B'
        elif score >= 60: return 'C'
        else: return 'D'

    def _get_schema_level(self, score: int) -> str:
        """Получение уровня Schema.org реализации"""
        if score >= 80: return 'advanced'
        elif score >= 60: return 'intermediate'
        elif score >= 40: return 'basic'
        else: return 'minimal'

    def _get_technical_grade(self, score: int) -> str:
        """Получение общей технической оценки"""
        if score >= 90: return 'A+'
        elif score >= 80: return 'A'
        elif score >= 70: return 'B'
        elif score >= 60: return 'C'
        else: return 'D'

    def _determine_audit_quality(self, score: int) -> str:
        """Определение качества аудита"""
        if score >= 85: return 'comprehensive'
        elif score >= 70: return 'thorough'
        elif score >= 50: return 'standard'
        else: return 'basic'

    def _determine_priority_level(self, score: int) -> str:
        """Определение уровня приоритета"""
        if score < 50: return 'critical'
        elif score < 70: return 'high'
        elif score < 85: return 'medium'
        else: return 'low'

    def _estimate_fix_timeline(self, recommendations: List[Dict]) -> str:
        """Оценка времени на исправления"""
        critical_count = len([r for r in recommendations if r['priority'] == 'critical'])
        high_count = len([r for r in recommendations if r['priority'] == 'high'])
        
        if critical_count > 0:
            return '2-4 недели'
        elif high_count > 3:
            return '3-6 недель'
        else:
            return '1-3 недели'

    def _estimate_traffic_improvement(self, current_score: int) -> str:
        """Оценка улучшения трафика"""
        if current_score < 50:
            return '25-40%'
        elif current_score < 70:
            return '15-25%'
        elif current_score < 85:
            return '5-15%'
        else:
            return '2-8%'

    def _get_cwv_fix_action(self, metric: str) -> str:
        """Получение действия для исправления CWV метрики"""
        actions = {
            'lcp': 'Optimize Largest Contentful Paint: compress images, improve server response time',
            'fid': 'Reduce First Input Delay: optimize JavaScript, reduce main thread work',
            'cls': 'Fix Cumulative Layout Shift: set image dimensions, avoid dynamic content'
        }
        return actions.get(metric, 'Optimize Core Web Vitals metric')

    def _get_mobile_fix_action(self, issue: str) -> str:
        """Получение действия для исправления мобильной проблемы"""
        actions = {
            'not_mobile_friendly': 'Implement mobile-friendly responsive design',
            'not_responsive': 'Add responsive CSS media queries',
            'viewport_meta_missing': 'Add viewport meta tag to HTML head',
            'mobile_speed_very_slow': 'Critical mobile speed optimization required',
            'mobile_speed_slow': 'Optimize mobile page loading speed',
            'touch_elements_too_small': 'Increase touch target sizes (min 44x44px)'
        }
        return actions.get(issue, 'Fix mobile optimization issue')

    def _get_crawling_fix_action(self, issue: str) -> str:
        """Получение действия для исправления crawling проблемы"""
        actions = {
            'robots_txt_invalid': 'Fix robots.txt syntax and directives',
            'xml_sitemap_missing': 'Create and submit XML sitemap',
            'canonical_issues_high': 'Review and fix canonical tag implementation',
            'redirect_chains_excessive': 'Eliminate redirect chains and loops',
            'status_code_errors_high': 'Fix HTTP status code errors',
            'duplicate_content_high': 'Resolve duplicate content issues'
        }
        return actions.get(issue, 'Fix crawling and indexing issue')

    def _calculate_audit_confidence(self, overall_score: Dict, audit_data: Dict) -> float:
        """Расчет уверенности в аудите"""
        base_confidence = 0.8  # Базовая уверенность
        
        # Корректировка на основе количества данных
        data_completeness = len([v for v in audit_data.values() if v is not None]) / 20  # Предполагаем 20 ключевых полей
        confidence = base_confidence * data_completeness
        
        # Бонус за высокий балл (больше данных для анализа)
        if overall_score['total_score'] > 80:
            confidence += 0.1
            
        return min(round(confidence, 2), 1.0)

    # Заглушки для других типов аудита
    async def _audit_core_web_vitals(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Специализированный аудит Core Web Vitals"""
        return {
            'audit_type': 'core_web_vitals_focused',
            'cwv_score': 75,
            'recommendations': ['Optimize LCP', 'Reduce FID', 'Fix CLS']
        }

    async def _audit_crawling_indexing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Специализированный аудит crawling и индексации"""
        return {
            'audit_type': 'crawling_indexing_focused',
            'crawling_health': 'good',
            'indexing_issues': 5
        }

    async def _audit_mobile_optimization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Специализированный мобильный аудит"""
        return {
            'audit_type': 'mobile_focused',
            'mobile_score': 85,
            'mobile_friendly': True
        }

    async def _audit_structured_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Специализированный аудит структурированных данных"""
        return {
            'audit_type': 'structured_data_focused',
            'schema_score': 60,
            'rich_snippet_opportunities': 8
        }

    async def _audit_performance_optimization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Специализированный аудит производительности"""
        return {
            'audit_type': 'performance_focused',
            'performance_score': 70,
            'page_speed': 3.5
        }

    async def _audit_security_https(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Специализированный аудит безопасности"""
        return {
            'audit_type': 'security_focused',
            'security_score': 90,
            'https_implemented': True,
            'ssl_grade': 'A'
        }