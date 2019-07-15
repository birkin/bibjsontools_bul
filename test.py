# -*- coding: utf-8 -*-

"""
To test single file

$ pwd
/path/to/bibjsontools_bul/test/

$ python ./openurl.py TestFromOpenURL.test_unicode_in_byte_string
(output)
"""

import unittest
from test import openurl
from test import ris


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(openurl.suite())
    test_suite.addTest(ris.suite())
    return test_suite

runner = unittest.TextTestRunner()
results = runner.run(suite())

if results.wasSuccessful():
    pass
else:
    raise Exception('Unit tests did not pass.  Check output.')

