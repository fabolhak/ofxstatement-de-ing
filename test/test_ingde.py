import os
import unittest
import tempfile
import io
import logging
import logging.handlers
import shutil

from ofxstatement import tool

class TestTestFiles(unittest.TestCase):

    def test_with_saldo_1(self):
        ret = tool.run(['convert', '--type=ingde', './test/test_with_saldo_1.csv', './test/out.ofx'])
        self.assertEqual(ret, 0)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: Conversion completed: %s" % './test/test_with_saldo_1.csv'])

    def test_with_saldo_2(self):
        ret = tool.run(['convert', '--type=ingde', './test/test_with_saldo_2.csv', './test/out.ofx'])
        self.assertEqual(ret, 0)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: Conversion completed: %s" % './test/test_with_saldo_2.csv'])

    def test_without_saldo_1(self):
        with self.assertRaises(RuntimeError):
            tool.run(['convert', '--type=ingde', './test/test_without_saldo_1.csv', './test/out.ofx'])

    def test_without_saldo_2(self):
        with self.assertRaises(RuntimeError):
            tool.run(['convert', '--type=ingde', './test/test_without_saldo_2.csv', './test/out.ofx'])

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