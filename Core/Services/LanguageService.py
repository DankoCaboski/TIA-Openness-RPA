def get_active_languages(myproject):
    return myproject.LanguageSettings.GetAttribute("ActiveLanguages")

    
def get_language(myproject, language_culture):
    return myproject.LanguageSettings.Languages.Find(language_culture)

def add_language(language, language_composition):
    try:
        language_composition.Add(language)
    except Exception as e:
        raise Exception("Failed to add language to composition: " + str(e))