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

from cardisco.atom import Discoverer
import html5lib
import os
from base_testcase import BaseTestCase
from urllib2 import URLError, urlopen
from urlparse import urljoin

HTML5_TEMPLATE = '''\
<!DOCTYPE html>
<head>
<link %s>
</head>'''
SECTION_7_1_REL = [
     'rel="alternate"',
     'rel="alternate "',
     'rel=" alternate"',
     'rel=" alternate "',
     'rel="foo alternate"',
     'rel="alternate bar"',
     'rel="foo alternate bar"',
     'rel="ALTERNATE"',
     'rel="Alternate"',
     'rel="AlTeRnAtE"',
     'rel=\'alternate\'',
     'rel="&#65;lternate"',
     'REL="alternate"',
     'rel=alternate',
]
SECTION_7_2_TYPE = [
    'type="application/atom+xml"',
    'type="application/atom+xml "',
    'type=" application/atom+xml"',
    'type=" application/atom+xml "',
    'type="APPLICATION/ATOM+XML"',
    'type="Application/Atom+Xml"',
    'TYPE="application/atom+xml"',

]
SECTION_7_3_TEMPLATE = HTML5_TEMPLATE % \
                       'rel=%(rel)s type=%(type)s href=%(href)s'
SECTION_7_3_PARAMS = [
    {
        'rel': '"alternate"',
        'type': '"application/atom+xml"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"alternate"',
        'type': '"application/atom+xml"''',
        'href': '"xml/index.atom"',
    },
    {
        'rel': '"alternate"',
        'type': '"application/atom+xml"',
        'href': '"/xml/index.atom"',
    },
    {
        'rel': '\'alternate\'',
        'type': '\'application/atom+xml\'',
        'href': '\'http://www.example.com/xml/index.atom\'',
    },
    {
        'rel': 'alternate',
        'type': '\'application/atom+xml\'',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"AlTeRnAtE"',
        'type': '"application/atom+xml"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"alternate"',
        'type': '"APPLICATION/ATOM+XML"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"alternate foo"',
        'type': '"application/atom+xml"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"foo alternate"',
        'type': '"application/atom+xml"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"foo alternate bar"',
        'type': '"application/atom+xml"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"&#65;lternate"',
        'type': '"application/atom+xml"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
    {
        'rel': '"alternate"',
        'type': '"application/atom&#43;xml"',
        'href': '"http://www.example.com/xml/index.atom"',
    },
]
SECTION_7_4_EXPECTED = {
    'query': {
        'http://www.example.com/index.html?format=atom': None,
    },
    'base': {
        'http://www.example.org/index.atom': None,
    },
    'multi': {
        'http://www.example.com/xml/index.atom': 'Main Atom feed',
        'http://www.example.com/xml/comments.atom': 'Recent comments feed',
        'http://example.org/index.atom': 'Atom feed (mirror)',
    },
}


class AtomTestCase(BaseTestCase):
    '''Tests the Atom autodiscovery class.'''

    dir_name = 'atom'
    discoverer_class = Discoverer

    def parse_with_base(self, html, base=None):
        if base is None:
            base = 'http://www.example.com/index.html'
        return Discoverer.parse(html, url=base)

    def assertADWithRawHTML(self, params, expected, template=None):
        if not template:
            template = HTML5_TEMPLATE
        html = template % params
        doc = html5lib.parse(html, treebuilder='lxml')
        feeds = self.parse_with_base(doc)
        self.assertEqual(feeds, expected)

    def test_section_7_1(self):
        for rel in SECTION_7_1_REL:
            attrs = '%s type=application/atom+xml href=index.atom' % rel
            self.assertADWithRawHTML(attrs, {
                'http://www.example.com/index.atom': None,
            })

    def test_section_7_2(self):
        for ltype in SECTION_7_2_TYPE:
            attrs = '%s rel=alternate href=index.atom' % ltype
            self.assertADWithRawHTML(attrs, {
                'http://www.example.com/index.atom': None,
            })

    def test_section_7_3(self):
        for params in SECTION_7_3_PARAMS:
            self.assertADWithRawHTML(params, {
                'http://www.example.com/xml/index.atom': None,
            }, template=SECTION_7_3_TEMPLATE)
        self.assertADLinks('section-7.3', {
            'http://www.example.com/xml/index.atom': None,
            'http://www.example.com/xml/index2.atom': None,
        }, parse_func=self.parse_with_base)

    def test_section_7_4(self):
        for suffix in ['query', 'base', 'multi']:
            self.assertADLinks('section-7.4-%s' % suffix,
                               SECTION_7_4_EXPECTED[suffix],
                               parse_func=self.parse_with_base)

    def do_diveintomark_test(self, path, check_for_feed=True):
        url = urljoin('http://diveintomark.org/tests/client/autodiscovery/',
                      path)
        html = urlopen(url)
        doc = html5lib.parse(html, treebuilder='lxml')
        if check_for_feed:
            base = os.path.splitext(url)[0]
            expected = '%s.xml' % base
            if base.endswith(('047', '048', '049', '050')):
                expected = expected.replace('diveintomark.org',
                                            'www.ragingplatypus.com')
            feeds = self.parse_with_base(doc, url)
            self.assertEqual(feeds, {
                expected: feeds.values()[0],
            })
        xpath = '/html:html/html:head/html:link[@rel=\'next\']'
        result = doc.xpath(xpath, namespaces=doc.getroot().nsmap)
        if result:
            self.do_diveintomark_test(result[0].attrib['href'])

    def test_diveintomark_testsuite(self):
        try:
            self.do_diveintomark_test('index.html', check_for_feed=False)
        except URLError:
            self.skipTest('network connection not available.')
