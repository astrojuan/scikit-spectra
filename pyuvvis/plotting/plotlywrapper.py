# pyuvvis intefrace to plotly:
# http://nbviewer.ipython.org/github/plotly/python-user-guide/blob/master/s00_homepage/s00_homepage.ipyn

#import requests #bug if not imported
import plotly.graph_objs as grobs
import numpy as np
from pyuvvis.plotting.plot_utils import _df_colormapper, cmget

def make_linetrace(x, y, **tracekwargs):#, linecolor):  
    """Trace-generating function (returns a Scatter object) from timespectra"""
    # good example of trace options http://plot.ly/python/bubblecharts
    
    name = tracekwargs.pop('name', '')
    tracekwargs.setdefault('color', 'rgb(255,0,0)') #markercolor
    tracekwargs.setdefault('opacity', 1.0) 
    
    return grobs.Scatter(x=x,
                         y=y,          
                         mode='lines',          
                         name=name,          
                         marker= grobs.Line(**tracekwargs) 
                         )

def make_pointtrace(x, y, **tracekwargs):#, linecolor):  
    """Trace-generating function (returns a Scatter object) from timespectra"""
    # good example of trace options http://plot.ly/python/bubblecharts
    
    name = tracekwargs.pop('name', '')    
    tracekwargs.setdefault('color', 'rgb(255,0,0)') #markercolor
    tracekwargs.setdefault('symbol', 'circle')
    tracekwargs.setdefault('opacity', 1.0)
    tracekwargs.setdefault('size', 12)

    return grobs.Scatter(x=x,
                         y=y,
                         mode='markers',
                         marker=grobs.Marker(**tracekwargs)
                         )


def layout(ts, *args, **kwargs):
    """ Make a plotly layout from timespectra attributes """    
    
    kwargs.setdefault('title', ts.name)
    kwargs.setdefault('plot_bgcolor', '#EFECEA') #gray
    kwargs.setdefault('showlegend', False)

    # Map x,y title into grobs.XAxis and grobs.YAxis
    xtitle = kwargs.pop('xtitle', ts.specunit)
    ytitle = kwargs.pop('ytitle', ts.iunit)
    kwargs['xaxis'] = grobs.XAxis(title=xtitle)
    kwargs['yaxis'] = grobs.YAxis(title=ytitle)
    
    layout = grobs.Layout(**kwargs)

    axis_style = dict(zeroline=False,       # remove thick zero line
                     gridcolor='#FFFFFF',  # white grid lines
                     ticks='outside',      # draw ticks outside axes 
                     ticklen=8,            # tick length
                     tickwidth=1.5)        #   and width

    # Can I just set these in XAxis and YAxis __init__?
    layout['xaxis'].update(axis_style)
    layout['yaxis'].update(axis_style)
    return layout
    

def ply_figure(ts, color='jet', **layoutkwds):
    """ Convert a timespectra to plotly Figure.  Figures can be then directly
    plotted with plotly.iplot(figure) in the notebook.
    """
    
    data = grobs.Data()
    lout = layout(ts, **layoutkwds)    
    
    # List of colors, either single color or color map
    try:
        cmapper = cmget(color) #Validate color map
    except AttributeError:
        cmapper = [color for i in range(len(ts.columns))]
    else:
        cmapper = _df_colormapper(ts, color, axis=0)        
        
    ### REFACTOR COLORS
    out = []
    for c in cmapper:
        r,g,b = c[0:3]
        out.append('rgb(%s,%s,%s)'%(r*255., g*255., b*255))
    cmapper = out
    
    for idx, clabel in enumerate(ts):
        trace = make_linetrace(x=np.array(ts.index), 
                           y=np.array(ts[clabel]), 
                           name=clabel,
                           color=cmapper[idx]) #marker color
        data.append(trace)

    return grobs.Figure(data=data, layout=lout)
    
    
if __name__ == '__main__':
    from pyuvvis.data import test_spectra
    ts = test_spectra()
    out = ply_figure(ts)
    
    import plotly.plotly as py
    py.sign_in('reeveslab', 'pdtrwl7yjd')
    
    fig = ply_figure(ts, color='jet')
    py.iplot(fig, filename='foo', fileopt='new')    
    print 'FINISHED PLOT 1'
    
    fig = ply_figure(ts, color='bone')
    py.iplot(fig, filename='bar', fileopt='new')        
    print 'FINISHED PLOT 2'