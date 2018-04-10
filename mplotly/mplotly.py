#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

@version: 0.1
@author:  quantpy
@file:    mplotly.py
@time:    2018/3/25 8:59
"""

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import cufflinks as cf
from . import tools

cf.go_offline()


def distplot1d(ss: pd.Series, bins=10, hist=True, kde=True, rug=True, color=None,
               as_figure=False, legend=True, title=True, grid=True, figsize=None, **kwargs):
    ss = pd.Series(ss)
    bin_size = (ss.max() - ss.min()) / bins
    curve_type = 'kde' if kde else 'normal'
    fig = ff.create_distplot(hist_data=[ss.values], group_labels=[str(ss.name)], bin_size=bin_size,
                             curve_type=curve_type, colors=color, show_hist=hist, show_rug=rug, **kwargs)
    fig['layout'].update(showlegend=legend, title=title)
    if figsize:
        fig['layout'].update(width=figsize[0], height=figsize[1])
    for k, v in fig['layout'].items():
        if 'axis' in k:
            v.update(showgrid=grid)
    if as_figure:
        return fig
    cf.iplot(fig)


def distplot(df: pd.DataFrame, bins=10, hist=True, kde=True, rug=False, color=None,
             as_figure=False, legend=True, title=True, grid=True, figsize=None,
             subplots=False, layout=None, sharex=False, sharey=False, **kwargs):
    """mimic seaborn.distplot"""
    df = pd.DataFrame(df).rename(columns=str)
    if not subplots:
        hist_data = [v.values for k, v in df.iteritems()]
        group_labels = df.columns.tolist()
        bin_size = (np.max(df.max()) - np.min(df.min())) / bins
        curve_type = 'kde' if kde else 'normal'
        fig = ff.create_distplot(hist_data=hist_data, group_labels=group_labels,
                                 bin_size=bin_size, curve_type=curve_type,
                                 colors=color, show_hist=hist, show_rug=rug, **kwargs
                                 )
    else:
        figures = [distplot1d(ss, bins=bins, hist=hist, kde=kde, rug=rug, color=color, as_figure=True, **kwargs)
                   for _, ss in df.iteritems()]
        fig = tools.get_subplots(figures, sharex=sharex, sharey=sharey, layout=layout)

    fig['layout'].update(showlegend=legend, title=title)
    if figsize:
        fig['layout'].update(width=figsize[0], height=figsize[1])
    for k, v in fig['layout'].items():
        if 'axis' in k:
            v.update(showgrid=grid)
    if as_figure:
        return fig
    cf.iplot(fig)


def pairplot(df: pd.DataFrame, kind='scatter', diag_kind='dist', theme=None, bins=10, color='grey', size=2,
             figsize=None, title=False, as_figure=False, sharex=False, sharey=False, grid=False):
    """"""
    if not theme:
        theme = cf.auth.get_config_file()['theme']

    figs = []
    for coly in df.columns:
        for colx in df.columns:
            if colx == coly:
                if diag_kind == 'dist':
                    fig = distplot(df[colx], hist=False, as_figure=True, rug=False, bins=bins)
                else:
                    fig = df.iplot(kind=diag_kind, keys=[colx], asFigure=True, bins=bins)
                figs.append(fig)
            else:
                figs.append(
                    df.iplot(kind=kind, mode='markers', x=colx, y=coly, asFigure=True, size=size, colors=[color]))
    layout = tools.get_layout(theme=theme)
    layout['xaxis1'].update(showgrid=grid)
    layout['yaxis1'].update(showgrid=grid)
    fig = tools.get_subplots(figs, layout=(len(df.columns), len(df.columns)), sharex=sharex, sharey=sharey,
                             horizontal_spacing=.05, vertical_spacing=.07, base_layout=layout)

    if isinstance(title, bool) and title:
        fig['layout'].update(title=df.columns.name)
    elif title:
        fig['layout'].update(title=title)
    if figsize:
        fig['layout'].update(width=figsize[0], height=figsize[1])
    fig['layout'].update(bargap=.02, showlegend=False)
    if as_figure:
        return fig
    cf.iplot(fig)


def mplot(df: pd.DataFrame,
          kind='scatter',
          subplots=False,
          sharex=False,
          sharey=False,
          layout=(1, -1),
          figsize=None,
          title=None,
          xlabel=True,
          ylabel=True,
          legend=True,
          xlim=None,
          ylim=None,
          as_figure=False,
          grid=True, **kwargs):
    name = df.columns.name if isinstance(df, pd.DataFrame) else df.name
    title = title or name
    xTitle = xlabel
    if isinstance(xlabel, bool) and xlabel:
        xTitle = df.index.name
    yTitle = ylabel
    if isinstance(ylabel, bool) and ylabel:
        yTitle = name

    dist_kws = kwargs.pop('dist_kws', dict())
    if kind == 'dist':
        fig = distplot(df, as_figure=True, subplots=subplots, sharex=sharex, sharey=sharey, legend=legend, title=title,
                       layout=layout, grid=grid, figsize=figsize, **dist_kws)
        # fig['layout'].update(width=figsize[0], height=figsize[1])
    else:
        fig = df.iplot(kind=kind, subplots=subplots, shared_xaxes=sharex, shared_yaxes=sharey,
                       showlegend=legend, dimensions=figsize, title=title, xTitle=xTitle, yTitle=yTitle,
                       shape=layout, asFigure=True, xrange=xlim, yrange=ylim, **kwargs)

    layout = fig.setdefault('layout', dict())
    layout.update(showlegend=legend)

    for k, v in layout.items():
        if k.startswith(('xaxis', 'yaxis')):
            v.update(showgrid=grid)
            if True:
                if k.startswith('xaxis'):
                    v.update(title=xTitle)
                    if xlim:
                        v.update(range=xlim)
                if k.startswith('yaxis'):
                    v.update(title=yTitle)
                    if ylim:
                        v.update(range=ylim)
    if as_figure:
        return fig

    cf.iplot(fig)


pd.DataFrame.mplot = mplot
pd.Series.mplot = mplot
