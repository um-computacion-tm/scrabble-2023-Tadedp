from pyrae import dle

class Dictionary:
    def isInDictionary(word: str):
        searchResult = dle.search_by_word(word)
        failMessage = "Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE"
        if searchResult.to_dict()["title"] == failMessage:
            return False
        else:
            return True
        