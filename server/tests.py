import re
import sys
import socket
import httplib
import unittest

arg_host = "localhost"
arg_port = 8902
if len(sys.argv) > 1:
  arg_host = sys.argv[1]
if len(sys.argv) > 2:
  arg_port = int(sys.argv[2])

class HttpServer(unittest.TestCase):
  host = arg_host
  port = arg_port

  def setUp(self):
    self.conn = httplib.HTTPConnection(self.host, self.port, timeout=10)

  def tearDown(self):
    self.conn.close()

  def test_filetype_swf(self):
    """Content-Type for .swf"""
    self.conn.request("GET", "/httptest/b16261023.swf")
    r = self.conn.getresponse()
    data = r.read()
    length = r.getheader("Content-Length")
    ctype = r.getheader("Content-Type")
    self.assertEqual(int(r.status), 200)
    self.assertEqual(int(length), 35344)
    self.assertEqual(len(data), 35344)
    self.assertEqual(ctype, "application/x-shockwave-flash")

loader = unittest.TestLoader()
suite = unittest.TestSuite()
a = loader.loadTestsFromTestCase(HttpServer)
suite.addTest(a)

class NewResult(unittest.TextTestResult):
  def getDescription(self, test):
    doc_first_line = test.shortDescription()
    return doc_first_line or ""

class NewRunner(unittest.TextTestRunner):
  resultclass = NewResult

runner = NewRunner(verbosity=2)
runner.run(suite)