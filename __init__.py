# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

__license__   = 'GPL 3'
__copyright__ = '2017, Leonardo Brondani Schenkel <leonardo@schenkel.net>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class BokusStore(StoreBase):
    name            = 'Bokus'
    version         = (2025, 3, 0)
    description     = 'Handla böcker online - billigt, snabbt & enkelt!'
    author          = 'Leonardo Brondani Schenkel <leonardo@schenkel.net>'
    actual_plugin   = 'calibre_plugins.lbschenkel_store_bokus_se.bokus:BokusStorePlugin'
    headquarters    = 'SE'
    formats         = ['EPUB', 'PDF']

