import unittest

from server.service.llm import callGemini

class TestProcess(unittest.TestCase):

    def setUp(self):
        pass

    def test_callGemini(self):
        result = callGemini("why is the sky blue?")
        print(result)

if __name__ == '__main__':
    unittest.main()