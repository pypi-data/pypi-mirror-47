# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 09:51:45 2018

@author: kunlin.l
"""

# noinspection PyUnresolvedReferences
from atrader.tframe import sysclsbase as cnt
# noinspection PyUnresolvedReferences
from atrader.tframe.sysclsbase import smm
# noinspection PyUnresolvedReferences
from atrader.tframe.sysclsbase import gv
# noinspection PyUnresolvedReferences
from atrader.tframe.language import text
# noinspection PyUnresolvedReferences
from atrader.tframe.utils.argchecker import apply_rule, verify_that

__all__ = [
    'clear_cache'
]


@smm.force_phase(gv.RUMMODE_PHASE_DEFAULT)
def clear_cache():
    import os
    import shutil
    print(text.LOG_CLEAN_CACHE)
    root_dir = cnt.env.root_sub_dir()
    for d in os.listdir(root_dir):
        try:
            if d.startswith('record_'):
                shutil.rmtree(os.path.join(root_dir, d))
        except OSError:
            pass
    cnt.env.cls_root_sub_dir('mat')
    print(text.LOG_CLEAN_CACHE_END)
