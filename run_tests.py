"""
Test runner for discovering and executing tests.
"""

import unittest

loader = unittest.TestLoader()
suite = loader.discover("Tests")
runner = unittest.TextTestRunner()
runner.run(suite)
