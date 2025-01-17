import os
import json
from typing import Dict, Any

class Localization:
    def __init__(self, default_lang: str = 'en'):
        self.default_lang = default_lang
        self.current_lang = default_lang
        self.translations: Dict[str, Dict[str, str]] = {}
        self.load_translations()

    def load_translations(self):
        translations_dir = os.path.join(os.path.dirname(__file__), '..', 'translations')
        os.makedirs(translations_dir, exist_ok=True)
        
        # Default translations
        default_translations = {
            'en': {
                'app_name': 'Hiel Essential Utility',
                'pdf_tools': 'PDF Tools',
                'image_tools': 'Image Tools',
                'ppt_tools': 'Presentation Tools',
                'color_tools': 'Color Tools',
                'toggle_theme': 'Toggle Theme'
            },
            'es': {
                'app_name': 'Utilidad Esencial de Hiel',
                'pdf_tools': 'Herramientas PDF',
                'image_tools': 'Herramientas de Imagen',
                'ppt_tools': 'Herramientas de Presentación',
                'color_tools': 'Herramientas de Color',
                'toggle_theme': 'Cambiar Tema'
            }
        }

        # Save default translations as JSON files
        for lang, translations in default_translations.items():
            lang_file = os.path.join(translations_dir, f'{lang}.json')
            if not os.path.exists(lang_file):
                with open(lang_file, 'w', encoding='utf-8') as f:
                    json.dump(translations, f, ensure_ascii=False, indent=4)

        # Load translations from files
        for filename in os.listdir(translations_dir):
            if filename.endswith('.json'):
                lang = os.path.splitext(filename)[0]
                with open(os.path.join(translations_dir, filename), 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)

    def set_language(self, lang_code: str):
        if lang_code in self.translations:
            self.current_lang = lang_code
        else:
            print(f"Language {lang_code} not found. Falling back to {self.default_lang}")
            self.current_lang = self.default_lang

    def translate(self, key: str, lang: str = None) -> str:
        lang = lang or self.current_lang
        
        # Try to get translation in specified language
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key]
        
        # Fallback to default language
        if self.default_lang in self.translations and key in self.translations[self.default_lang]:
            return self.translations[self.default_lang][key]
        
        # If no translation found, return the key itself
        return key

    def get_available_languages(self) -> list:
        return list(self.translations.keys())

# Singleton instance
localization = Localization()
