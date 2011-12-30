# -*- coding: utf-8 -*-
# Copyright 2010 Mark Lee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cardisco
from copy import copy
from StringIO import StringIO
from unittest2 import TestCase

MINIMAL_HTML = '''\
<!DOCTYPE html>
<head>
    <link href=foo.rss rel=alternate type=application/rss+xml>
    <link href=foo.atom rel=alternate type=application/atom+xml>
</head>
'''


class FakeHTTPResponse(StringIO):
    '''A fake HTTP response for FakeHTTPConnection. Copied from
    https://code.google.com/p/httplib2/source/browse/python2/httplib2test.py
    (the _MyResponse class).
    '''

    def __init__(self, body, **kwargs):
        StringIO.__init__(self, body)
        self.headers = kwargs

    def iteritems(self):
        return self.headers.iteritems()


class FakeHTTPConnection(object):
    '''A fake HTTP connection for unit testing.'''
    def __init__(self, host, **kwargs):
        pass

    def set_debuglevel(self, level):
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def request(self, method, request_uri, body, headers):
        pass

    def getresponse(self):
        raise NotImplementedError()


class FakeAtomConnection(FakeHTTPConnection):
    '''Fake HTTP connection for a fake Atom document.'''

    def getresponse(self):
        return FakeHTTPResponse('', content_type='application/atom+xml')


class FakeHTMLConnection(FakeHTTPConnection):
    '''Fake HTTP connection for a fake RSS document.'''

    def getresponse(self):
        return FakeHTTPResponse(MINIMAL_HTML, content_type='text/html')


class FakeRSSConnection(FakeHTTPConnection):
    '''Fake HTTP connection for a fake RSS document.'''

    def getresponse(self):
        return FakeHTTPResponse('', content_type='application/rss+xml')


class BaseFunctionalityTestCase(TestCase):
    '''Tests base functionality of the discover/parse_html functions.'''

    @classmethod
    def setUpClass(cls):
        cls.reset_modules = copy(cardisco.MODULES)

    def setUp(self):
        cardisco.MODULES = copy(self.reset_modules)

    def assertContainsMIMEType(self, feeds, mime_type, expected):
        self.assertIn(mime_type, feeds.keys())
        self.assertEqual(feeds[mime_type], expected)

    def assertMinimalFeedsEqual(self, feeds, prefix=''):
        self.assertContainsMIMEType(feeds, 'application/rss+xml', {
            '%sfoo.rss' % prefix: None,
        })
        self.assertContainsMIMEType(feeds, 'application/atom+xml', {
            '%sfoo.atom' % prefix: None,
        })

    def test_discover(self):
        feeds = cardisco.discover('http://a/atom',
                                       connection_type=FakeAtomConnection)
        self.assertContainsMIMEType(feeds, 'application/atom+xml', {
            'http://a/atom': None,
        })
        feeds = cardisco.discover('http://a/rss',
                                       connection_type=FakeRSSConnection)
        self.assertContainsMIMEType(feeds, 'application/rss+xml', {
            'http://a/rss': None,
        })
        feeds = cardisco.discover('http://a/html',
                                       connection_type=FakeHTMLConnection)
        self.assertMinimalFeedsEqual(feeds, 'http://a/')

    def do_test_parse_minimal(self, html):
        feeds = cardisco.parse_html(MINIMAL_HTML)
        self.assertMinimalFeedsEqual(feeds)

    def test_parse_from_string(self):
        self.do_test_parse_minimal(MINIMAL_HTML)

    def test_from_file_like_object(self):
        obj = StringIO(MINIMAL_HTML)
        self.do_test_parse_minimal(obj)

    def assertModuleRaises(self, key, module, exception):
        cardisco._MODULE_CACHE = {}
        cardisco.MODULES[key] = module
        self.assertRaises(exception, cardisco.parse_html,
                          MINIMAL_HTML)

    def test_invalid_module(self):
        self.assertModuleRaises('invalid', 'invalid_module', ImportError)

    def test_class_not_found(self):
        self.assertModuleRaises('no_class', 'no_class', AttributeError)
