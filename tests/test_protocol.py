"""
Test cases for the protocol handling code.
"""
from __future__ import print_function
from __future__ import division

import unittest

from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import parse_qs

import htsget.protocol as protocol

EXAMPLE_URL = "http://example.com"


class TestTicketRequestUrl(unittest.TestCase):
    """
    Tests the ticket request URL generator.
    """
    def test_defaults(self):
        url = protocol.ticket_request_url(EXAMPLE_URL)
        self.assertEqual(url, EXAMPLE_URL)

    def test_reference_name(self):
        full_url = protocol.ticket_request_url(
                "http://example.co.uk/path/to/resource", reference_name="1",
                start=2, end=100)
        parsed = urlparse(full_url)
        self.assertEqual(parsed.scheme, "http")
        self.assertEqual(parsed.netloc, "example.co.uk")
        self.assertEqual(parsed.path, "/path/to/resource")
        query = parse_qs(parsed.query)
        self.assertEqual(query["referenceName"], ["1"])
        self.assertEqual(query["start"], ["2"])
        self.assertEqual(query["end"], ["100"])
        self.assertEqual(len(query), 3)

    def test_reference_md5(self):
        md5 = "b9185d4fade27aa27e17f25fafec695f"
        full_url = protocol.ticket_request_url(
                "https://example.com/resource", reference_md5=md5)
        parsed = urlparse(full_url)
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.netloc, "example.com")
        self.assertEqual(parsed.path, "/resource")
        query = parse_qs(parsed.query)
        self.assertEqual(query["referenceMd5"], [md5])
        self.assertEqual(len(query), 1)

    def test_url_scheme(self):
        full_url = protocol.ticket_request_url("http://a.com")
        self.assertEqual(urlparse(full_url).scheme, "http")
        full_url = protocol.ticket_request_url("https://a.com")
        self.assertEqual(urlparse(full_url).scheme, "https")

    def test_url_netloc(self):
        full_url = protocol.ticket_request_url("http://a.com")
        self.assertEqual(urlparse(full_url).netloc, "a.com")
        full_url = protocol.ticket_request_url("http://a.com/other/stuff")
        self.assertEqual(urlparse(full_url).netloc, "a.com")
        full_url = protocol.ticket_request_url("https://192.168.0.1")
        self.assertEqual(urlparse(full_url).netloc, "192.168.0.1")
        full_url = protocol.ticket_request_url("https://192.168.0.1:8080/xyz")
        self.assertEqual(urlparse(full_url).netloc, "192.168.0.1:8080")

    def test_url_path(self):
        full_url = protocol.ticket_request_url("http://a.com/path/to/resource")
        self.assertEqual(urlparse(full_url).path, "/path/to/resource")
        full_url = protocol.ticket_request_url("http://a.com/")
        self.assertEqual(urlparse(full_url).path, "/")
        full_url = protocol.ticket_request_url("http://a.com")
        self.assertEqual(urlparse(full_url).path, "")

    def test_embedded_query_strings(self):
        full_url = protocol.ticket_request_url("http://a.com/stuff?a=a&b=b")
        query = parse_qs(urlparse(full_url).query)
        self.assertEqual(query["a"], ["a"])
        self.assertEqual(query["b"], ["b"])

        full_url = protocol.ticket_request_url(
            "http://a.com/stuff?a=a&b=b", reference_name="123")
        query = parse_qs(urlparse(full_url).query)
        self.assertEqual(query["a"], ["a"])
        self.assertEqual(query["b"], ["b"])
        self.assertEqual(query["referenceName"], ["123"])
