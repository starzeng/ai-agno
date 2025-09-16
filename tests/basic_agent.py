import unittest

from tests.hello_test import test_hello


class MyTestCase(unittest.TestCase):

    def test_hello(self):
        print("hello")
        test_hello()

if __name__ == '__main__':
    unittest.main()
