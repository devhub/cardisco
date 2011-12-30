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
'''\
An autodiscovery library.

.. moduleauthor:: Mark Lee <cardisco lazymalevolence com>
'''

import html5lib
import httplib2
from importlib import import_module

MODULES = {
    'application/atom+xml': '.atom',
    'application/rss+xml': '.rss',
    'application/rdf+xml': '.rdf',
    'application/opensearchdescription+xml': '.opensearch',
}

_MODULE_CACHE = {}

HTTP_ACCEPT = '%s, text/html, text/*; q=0.5' % ', '.join(MODULES.keys())


def discover(url, http=None, **kwargs):
    '''Discovers various metadata URLs embedded in an HTML document, such
    as feeds and RDF.

    :param str url: The URL to retrieve the HTML document from.
    :param http: The :mod:`httplib2` HTTP object. If it's not set, one will
                 be created.
    :type http: :class:`httplib2.Http` or :const:`None`
    :param dict \*\*kwargs: Extra arguments to :meth:`httplib2.Http.request`.
    :returns: A dictionary, where the key is the URL's MIME type and the value
              is a dictionary of URL-title pairs.
    :rtype: :class:`dict`
    '''
    if not http:
        http = httplib2.Http()
    if 'headers' in kwargs:
        kwargs['headers']['Accept'] = HTTP_ACCEPT
    else:
        kwargs['headers'] = {
            'Accept': HTTP_ACCEPT,
        }
    response, content = http.request(url, **kwargs)
    if response['content-type'] in MODULES:
        # assume the server's not lying
        return {
            response['content_type']: {
                url: None,
            },
        }
    # TODO if someone wishes to, they can implement the MIME sniffing
    # algorithm here.
    return parse_html(content, url=url)


def parse_html(file_obj_or_str, url=None):
    '''Discovers various metadata URLs embedded in a given HTML document, such
    as feeds and RDF.

    :param file_obj_or_str: The HTML document to be parsed.
    :type file_obj_or_str: a file-like object or :class:`str`
    :param url: The URL that the HTML document was retrieved from.
    :type url: :class:`str` or :const:`None`
    :returns: A dictionary, where the key is the URL's MIME type and the value
              is a dictionary of URL-title pairs.
    :rtype: :class:`dict`
    '''
    urls = {}

    # load the modules only when the function is first called.
    if not _MODULE_CACHE:
        for name, module in MODULES.iteritems():
            mod = import_module(module, package=__name__)
            try:
                _MODULE_CACHE[name] = mod.Discoverer
            except AttributeError:
                raise AttributeError('''\
Could not find a Discoverer object in the %s module.''' % name)

    doc = html5lib.parse(file_obj_or_str, treebuilder='lxml')
    print type(doc)
    for name, discoverer in _MODULE_CACHE.iteritems():
        urls[name] = discoverer.parse(doc, url=url)
    return urls
