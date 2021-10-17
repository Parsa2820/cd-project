import unittest
from src.share import token


class TokenTest(unittest.TestCase):
    def test_token(self):
        num = token.Token(token.TokenType.NUM, '112')
        self.assertEqual(str(num), '(NUM, 112)')


if __name__ == '__main__':
    unittest.main()
