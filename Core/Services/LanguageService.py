from . import OpennessService

def get_active_languages(myproject):
    language_settings = myproject.LanguageSettings
    enum = OpennessService.get_attibutes(["ActiveLanguages"], language_settings)
    return enum[0]
    
def get_language_by_culture(myproject, language_culture):
    for language in myproject.LanguageSettings.Languages:
        culture = OpennessService.get_attibutes(["Culture"], language)
        if str(culture[0]) == language_culture:
            return language
    
    raise Exception("Language not found")

def add_language(language, language_composition):
    try:
        language_composition.Add(language)
    except Exception as e:
        raise Exception("Failed to add language to composition: " + str(e))