import os
import unittest
import tempfile
import io
import logging
import logging.handlers
import shutil
import mock

from ofxstatement import tool, statement, configuration, parser, exceptions

class TestTestFiles(unittest.TestCase):

    def test_with_saldo(self):
        ret = tool.run(['convert', '--type=ingde', './test/test_with_saldo.csv', './test/out.ofx'])
        self.assertEqual(ret, 0)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: Conversion completed: %s" % './test/test_with_saldo.csv'])

    def test_without_saldo(self):
        with self.assertRaises(RuntimeError):
            tool.run(['convert', '--type=ingde', './test/test_without_saldo.csv', './test/out.ofx'])

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(suffix='ofxstatement')
        self.setUpLogging()

    def tearDown(self):
        self.tearDownLogging()
        shutil.rmtree(self.tmpdir)

    def setUpLogging(self):
        self.log = io.StringIO()
        fmt = logging.Formatter("%(levelname)s: %(message)s")
        self.loghandler = logging.StreamHandler(self.log)
        self.loghandler.setFormatter(fmt)
        logging.root.addHandler(self.loghandler)
        logging.root.setLevel(logging.DEBUG)

    def tearDownLogging(self):
        logging.root.removeHandler(self.loghandler)

if __name__ == '__main__':
    unittest.main()