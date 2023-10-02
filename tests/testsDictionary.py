import unittest
from unittest.mock import patch
from game.dictionary import Dictionary, DictionaryConnectionFailedException

class TestDictionary(unittest.TestCase):
    @patch('pyrae.dle.search_by_word')
    def testWordIsInDictionary(self, mock_search_by_word):
        word = "te"
        mock_search_by_word.return_value.title = "te | Definición | Diccionario de la lengua española | RAE - ASALE"
        self.assertEqual(Dictionary.isInDictionary(word), True)
        
    @patch('pyrae.dle.search_by_word')
    def testWordIsNotInDictionary(self, mock_search_by_word):
        word = "asd"
        mock_search_by_word.return_value.title = "Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE"
        self.assertEqual(Dictionary.isInDictionary(word), False)
    
    @patch('pyrae.dle.search_by_word')
    def testSearchFailed(self, mock_search_by_word):
        word = "hola"
        mock_search_by_word.return_value = None
        with self.assertRaises(DictionaryConnectionFailedException):
            Dictionary.isInDictionary(word)

if __name__ == '__main__':
    unittest.main()