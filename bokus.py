# -*- coding: utf-8 ts=4 sw=4 sts=4 et -*-
from __future__ import (absolute_import, print_function, unicode_literals)

__license__   = 'GPL 3'
__copyright__ = '2017, Leonardo Brondani Schenkel <leonardo@schenkel.net>'
__docformat__ = 'restructuredtext en'

from six.moves import urllib

from PyQt5.Qt import QUrl
from contextlib import closing
from lxml import html

from calibre import browser
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog

if __name__ == '__main__':
    from lib import GenericStore, xpath, text
else:
    from calibre_plugins.lbschenkel_store_bokus_se.lib import GenericStore, xpath, text

class BokusStore(GenericStore):

    url                = 'https://www.bokus.com'
    search_url         = '{0}/cgi-bin/product_search.cgi?binding_normalized=ebok&search_word={1}'
    words_drm_locked   = ['adobe-kryptering', 'lcp-kryptering']
    words_drm_unlocked = ['vattenmärke']

    def find_search_results(self, doc):
        return xpath(doc, '//li', 'ProductList__item')

    def parse_search_result(self, node):
        r = SearchResult()
        r.detail_item = text(node, './/*', 'Item__title', '/a/@href')
        r.title       = text(node, './/*', 'Item__title', '/a/text()')
        r.author      = text(node, './/*', 'Item__authors')
        r.price       = text(node, './/*', 'pricing__price') + ' kr'
        r.formats     = text(node, './/*', 'Item__format-as-link')
        r.cover_url   = text(node, './/img', 'Item__image', '/@data-src')
        return r

    def find_book_details(self, doc):
        return doc

    def parse_book_details(self, node):
        r = SearchResult()
        r.title     = text(node, '//*', 'product-page__title', '/text[1]')
        r.author    = text(node, '//*', 'u-m-t--1 deci')
        r.price     = text(node, '//*', 'product-page__pricing') + ' kr'
        r.cover_url = text(node, '//div', 'product-image', '/img/@src')
        details     = xpath(node, '//dl', 'product-page__facts')[0]
        for item in xpath(details, './dt'):
            name = text(item, '.')
            if 'Filformat' == name:
                r.formats = text(item, './following-sibling::dd[1]')
                r.drm     = r.formats
        return r

    def normalize_author(self, text):
        if text.startswith('av '):
            text = text[3:].strip()
        return text

    def normalize_formats(self, text):
        if text.startswith('EPUB'):
            return 'EPUB'
        elif text.startswith('PDF'):
            return 'PDF'
        else:
            return text

class BokusStorePlugin(StorePlugin):
    store = BokusStore()

    def search(self, query, max_results, timeout):
        return self.store.search(query, max_results, timeout)

    def get_details(self, result, timeout):
        return self.store.get_details(result, timeout)

    def open(self, parent, item, external):
        return self.store.open(self.name, self.gui, parent, item, external)

    def create_browser(self):
        return self.store.create_browser()

if __name__ == '__main__':
    import sys

    query   = ' '.join(sys.argv[1:])
    max     = 3
    timeout = 10

    store = BokusStore()
    for r in store.search(query, max, timeout):
        print(r)
        store.get_details(r, timeout)
        print(r)
        print()
