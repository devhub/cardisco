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

from cardisco import parse_html
import os
from unittest import TestCase

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'from_rssbandit')


class FromRSSBanditTestCase(TestCase):
    '''Tests the Autodiscovery module using files from the RSS Bandit test
    suite.
    '''

    @staticmethod
    def file_obj_from_path(path):
        return open(os.path.join(BASE_DIR, path))

    def test_autodiscovery1(self):
        html_file = self.file_obj_from_path('AutoDiscovery1.htm')
        feeds = parse_html(html_file)
        self.assertEqual(feeds['application/rss+xml'], {
            'SampleRss0.91Feed.xml': 'RSS',
            'SampleRss0.92Feed.rss': 'RSS',
        })
        feeds = parse_html(html_file, url='http://localhost/foo/bar')
        self.assertEqual(feeds['application/rss+xml'], {
            'http://localhost/foo/SampleRss0.91Feed.xml': 'RSS',
            'http://localhost/foo/SampleRss0.92Feed.rss': 'RSS',
        })

    def test_get_rss_autodiscovery_links(self):
        html_file = self.file_obj_from_path('GetRssAutoDiscoveryLinks.html')
        feeds = parse_html(html_file)
        rss20_url = '''\
http://127.0.0.1:8081/RssLocaterTestFiles/SampleRss2.0Feed.xml'''
        self.assertEqual(feeds['application/rss+xml'], {
            'SampleRss0.91Feed.xml': 'RSS',
            'SampleRss0.92Feed.rss': 'RSS',
            'SampleRss1.0Feed.rss': 'RSS',
            rss20_url: 'RSS',
        })

    def test_no_feeds(self):
        html_file = self.file_obj_from_path('NoFeeds.html')
        feeds = parse_html(html_file)
        self.assertEqual(feeds['application/rss+xml'], {})

    def test_page_with_fake_atom_link(self):
        html_file = self.file_obj_from_path('NoFeeds.html')
        feeds = parse_html(html_file)
        self.assertEqual(feeds['application/rss+xml'], {})
        self.assertEqual(feeds['application/atom+xml'], {})
