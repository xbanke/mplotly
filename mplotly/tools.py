#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

@version: 0.1
@author:  quantpy
@email:   quantpy@gmail.com
@file:    tools.py
@time:    2018/3/25 8:25
"""


import cufflinks as cf


def get_layout(kind=None, theme=None, title='', xlabel='', ylabel='', zlabel='',
               figsize=None, **kwargs):
    layout = cf.tools.getLayout(kind=kind, theme=theme,
                                title=title, xTitle=xlabel, yTitle=ylabel, zTitle=zlabel,
                                dimensions=figsize, **kwargs)
    return layout


def get_subplots(figures, layout=None, sharex=False, sharey=False,
                 start_cell='top-left', theme=None, base_layout=None, **kwargs):
    return cf.tools.subplots(figures, shape=layout, shared_xaxes=sharex, shared_yaxes=sharey,
                             start_cell=start_cell, theme=theme, base_layout=base_layout, **kwargs
                             )
