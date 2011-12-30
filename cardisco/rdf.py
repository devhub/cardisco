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

from .base import BaseDiscoverer


class Discoverer(BaseDiscoverer):
    '''Looks for RDF autodiscovery tags. References:

    * http://www.w3.org/TR/rdf-syntax-grammar/#section-rdf-in-HTML
    * http://xmlns.com/foaf/spec/#sec-autodesc
    '''

    xpath = '/html:html/html:head/html:link[@href]' \
            '[@type=\'application/rdf+xml\']'
