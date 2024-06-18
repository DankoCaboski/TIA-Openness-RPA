from Services import LanguageService

def add_language(myproject, language_culture):
    active_languages = LanguageService.get_active_languages(myproject)
    language = LanguageService.get_language(myproject, language_culture)
    LanguageService.add_language(language, active_languages)