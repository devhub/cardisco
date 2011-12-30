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

from base_testcase import BaseTestCase


class RSSTestCase(BaseTestCase):
    '''Tests the RSS autodiscovery class.'''

    dir_name = 'rss'
    module_name = 'cardisco.rss'

    def test_section_3(self):
        self.assertADLinks('section-3', {
            'http://feeds.feedburner.com/TheRssBlog': 'RSS',
        })

    def test_section_3_1(self):
        self.assertADLinks('section-3.1', {
            'http://www.rssboard.org/rss-feed': None,
        })

    def test_section_3_2(self):
        self.assertADLinks('section-3.2', {})

    def test_section_3_3(self):
        self.assertADLinks('section-3.3', {})

    def test_non_rss(self):
        self.assertADLinks('non-rss', {})
