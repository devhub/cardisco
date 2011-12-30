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

from urlparse import urljoin


class BaseDiscoverer(object):
    '''Code that is common amongst the different Discoverer modules.'''

    xpath = '/html:html/html:head/html:link[@type][@rel][@href]'

    @classmethod
    def _parse_base(cls, doc, nsmap):
        '''Parses the HTML for a ``<base/>`` element, which is then applied
        to any link found.

        :param doc: The HTML document.
        :type doc: :class:`lxml.etree._ElementTree`
        :param dict nsmap: The namespace map used with the ``<base/>`` XPath
                           expression.
        '''
        cls.base_element = None
        xpath = '/html:html/html:head/html:base'
        bases = doc.xpath(xpath, namespaces=nsmap)
        if bases:
            head_element = doc.xpath(xpath[:-10], namespaces=nsmap)[0]
            cls.head_children = list(head_element)
            cls.base_element = bases[0]
            cls.base_idx = cls.head_children.index(cls.base_element)
            cls.html_base = cls.base_element.attrib['href']

    @classmethod
    def _get_link_href(cls, doc_url, element):
        base = doc_url
        if cls.base_element is not None:
            link_idx = cls.head_children.index(element)
            if cls.base_idx < link_idx:
                base = cls.html_base
        href = element.attrib['href'].strip()
        if base:
            href = urljoin(base, href)
        return href

    @classmethod
    def parse(cls, doc, url=None):
        feeds = {}
        nsmap = doc.getroot().nsmap
        cls._parse_base(doc, nsmap)
        for element in doc.xpath(cls.xpath, namespaces=nsmap):
            if cls.check_link_element(element):
                href = cls._get_link_href(url, element)
                feeds[href] = element.attrib.get('title')
        return feeds

    @classmethod
    def check_link_element(cls, element):
        return True
