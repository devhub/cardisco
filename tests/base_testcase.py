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

import html5lib
from importlib import import_module
import os
from unittest2 import TestCase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseTestCase(TestCase):
    '''Base test case for tesing autodiscovery classes.'''

    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.join(BASE_DIR, cls.dir_name)
        if not hasattr(cls, 'discoverer_class'):
            cls.discoverer_class = import_module(cls.module_name).Discoverer

    def doc_from_path(self, path):
        abspath = '%s.html' % os.path.join(self.base_dir, path)
        return html5lib.parse(open(abspath), treebuilder='lxml')

    def assertADLinks(self, basename, expected, parse_func=None):
        if not parse_func:
            parse_func = self.discoverer_class.parse
        doc = self.doc_from_path(basename)
        feeds = parse_func(doc)
        self.assertEqual(feeds, expected)
