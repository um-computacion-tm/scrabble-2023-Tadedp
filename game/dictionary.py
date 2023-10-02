from pyrae import dle

class DictionaryConnectionFailedException(Exception):
    pass

dle.set_log_level(log_level = 'CRITICAL')

class Dictionary:
    def isInDictionary(word: str):
        searchResult = dle.search_by_word(word)

        if searchResult == None:
            raise DictionaryConnectionFailedException("No fue ingresada una palabra o el servicio está caído.")
        
        failMessage = "Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE"
        return searchResult.title != failMessage
