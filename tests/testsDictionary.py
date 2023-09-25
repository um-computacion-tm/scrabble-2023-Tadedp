import unittest
from game.dictionary import Dictionary

class TestDictionary(unittest.TestCase):
    def testWordIsInDictionary(self):
        word = "hola"
        self.assertEqual(Dictionary.isInDictionary(word), True)
    
    def testWordIsNotInDictionary(self):
        word = "asd"
        self.assertEqual(Dictionary.isInDictionary(word), False)
           
if __name__ == '__main__':
    unittest.main()