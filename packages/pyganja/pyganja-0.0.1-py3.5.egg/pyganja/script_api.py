
from __future__ import print_function

from IPython.display import display, Javascript
from IPython import get_ipython

import os
from .GanjaScene import GanjaScene
import base64
from multiprocessing import Process


try:
    from .cefwindow import *
except:
    print('Failed to import cef_gui, cef functions will be unavailable')


def html_to_data_uri(html):
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    return ret


def read_ganja():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    ganja_filename = dir_name + '/static/ganja.js/ganja.js'
    with open(ganja_filename, 'r') as ganja_file:
        output = ganja_file.read()
    return output


def generate_notebook_js(script_json, sig=None, grid=True, scale=1.0):

    if sig is not None:
        p=(sig>0).sum()
        q=(sig<0).sum()
    else:
        p = 4
        q = 1
    sig_short = '%i,%i' % (p, q)
    mv_length = str(2 ** (p + q))

    # not the best way to test conformal, as it prevents non-euclidean  geometry
    conformal = 'false'
    if q!=0:
        conformal = 'true'

    if sig_short in ['4,1', '3', '3,1', '2']:
        if grid:
            gridstr = 'true'
        else:
            gridstr = 'false'
        scalestr = str(scale)
        js = read_ganja()
        js += """
        function add_graph_to_notebook(Algebra){
            var output = Algebra("""+sig_short+""",()=>{
              // When we get a file, we load and display.
                var canvas;
                var h=0, p=0;
                  // convert arrays of floats back to CGA elements.     
                     var data = """ + script_json + """;
                     data = data.map(x=>x.length=="""+mv_length+"""?new Element(x):x);
                  // add the graph to the page.
                     canvas = this.graph(data,{gl:true,conformal:"""+conformal+""",grid:"""+gridstr+""",scale:"""+scalestr+"""});
                     canvas.options.h = h; canvas.options.p = p;
                  // make it big.
                     canvas.style.width = '50vw';
                     canvas.style.height = '50vh';
                     return canvas;
                }
            );
            element.append(output);
        }
        require(['Algebra'],function(Algebra){add_graph_to_notebook(Algebra)});
        """
    else:
        raise ValueError('Algebra not yet supported')
    return js


def generate_full_html(script_json, sig=None, grid=True, scale=1.0):

    if sig is not None:
        p=(sig>0).sum()
        q=(sig<0).sum()
    else:
        p = 4
        q = 1
    if q > 0:
        sig_short = '%i,%i' % (p, q)
    else:
        sig_short = '%i' % (p)
    mv_length = str(2 ** (p + q))

    # not the best way to test conformal, as it prevents non-euclidean  geometry
    conformal = 'false'
    if q!=0:
        conformal = 'true'

    if sig_short in ['4,1', '3', '3,1', '2']:
        if grid:
            gridstr = 'true'
        else:
            gridstr = 'false'
        scalestr = str(scale)

        script_string = """
                Algebra("""+sig_short+""",()=>{
                  var canvas = this.graph((""" + script_json + """).map(x=>x.length=="""+mv_length+"""?new Element(x):x),
                  {conformal:"""+conformal+""",gl:true,grid:"""+gridstr+""",scale:"""+scalestr+"""});
                  canvas.style.width = '100vw';
                  canvas.style.height = '100vh';
                  document.body.appendChild(canvas);
                });
                """
        full_html = """<!DOCTYPE html>
        <html lang="en" style="height:100%;">
        <HEAD>
            <meta charset="UTF-8">
            <title>pyganja</title>
          <SCRIPT>""" + read_ganja() + """</SCRIPT>
        </HEAD>
        <BODY style="position:absolute; top:0; bottom:0; right:0; left:0; overflow:hidden;">
        <SCRIPT>
            """ + script_string + """
        </SCRIPT>
        </BODY>
        </html>
        """
        return full_html
    else:
        raise ValueError('Algebra not yet supported')


def render_notebook_script(script_json, sig=None, grid=True, scale=1.0):
    """
    In a notebook we dont need to start cefpython as we
    are already in the browser!
    """
    js = generate_notebook_js(script_json, sig=sig, grid=grid, scale=scale)
    display(Javascript(js))


def render_cef_script(script_json="", sig=None, grid=True, scale=1.0):
    def render_script():
        final_url = html_to_data_uri(generate_full_html(script_json, sig=sig, grid=grid, scale=scale))
        run_cef_gui(final_url, "pyganja")
    p = Process(target=render_script)
    p.start()
    p.join()


def isnotebook():
    # See:
    # https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def draw(objects, color=int('AA000000', 16), sig=None, grid=True, scale=1.0, new_window=False, static=True):
    if isinstance(objects, list):
        sc = GanjaScene()
        sc.add_objects(objects, color=color, static=static)
        if isnotebook():
            if not new_window:
                render_notebook_script(str(sc), sig=sig, grid=grid, scale=scale)
            else:
                render_cef_script(str(sc), sig=sig, grid=grid, scale=scale)
        else:
            render_cef_script(str(sc), sig=sig, grid=grid, scale=scale)
    else:
        raise ValueError('The input is not a list of objects')
