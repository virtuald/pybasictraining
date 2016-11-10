
import collections
import inspect

from os.path import abspath, dirname, join

from IPython import get_ipython
from IPython.display import display, clear_output, Javascript


import ipywidgets as widgets
import mistune

rootdir = abspath(join(dirname(__file__), ".."))
code_dir = join(rootdir, 'src')

def get_tests():
    tpath = join(rootdir, "tests", "test_challenges.py")
    
    # Load the module using OrderedDict so that we can enumerate
    # the functions in source code order
    tmod = collections.OrderedDict()
    with open(tpath) as fp:
        exec(fp.read(), tmod)
    
    results = collections.OrderedDict()
    
    for k, v in tmod.items():
        if k.startswith('test_') and inspect.isfunction(v) and \
           not hasattr(v, '_jupyter_skip'):
            results[k[5:]] = inspect.getdoc(v)
    
    return results


class CustomButton(widgets.Button):
    
    def _handle_button_msg(self, _, content, buffers):
        if content.get('event', '') == 'click':
            self._click_handlers(content)

def show():
    ipy = get_ipython()
    tests = get_tests()
    
    # doesn't seem to be a way to get the display value
    for k in list(tests.keys()):
        tests[k] = (k, tests[k])
        
    tests['all'] = ('all', 'Run all tests')
    
    # Create widgets
    # .. dropdown, label, and run button
    label = widgets.HTML()
    selector = widgets.ToggleButtons(options=tests, value=list(tests.values())[0])
    run_button = CustomButton(description="Run")
    
    def on_selector_change(info):
        run_button.description = "Run %s" % info['new'][0]
        label.value = mistune.markdown("## Challenge %s\n\n%s" % info['new'])
    
    def get_code():
        Javascript()
        
    def on_click(c):
        clear_output()
        
        print("GOT", c)
        
        label.value = "CLICK"
        
        #print(dir(run_button))
        print(run_button.comm.comm_id)
        
        # This gets the cell text. Need to send that down somehow
        display(Javascript('console.log(IPython.notebook.get_cells()[1].get_text());'))
        return
        # How do I override or hook the 
        
        with open(join(code_dir, 'mycode.py'), 'w') as fp:
            fp.write(code)
        
        test = selector.value[0]
        
        if test == 'all':
            ipy.system('TEST_PYTHONPATH="%s" %s' % (code_dir, join(rootdir, 'run_all.sh')))
        #ipy.system('TEST_PYTHONPATH="%s" %s %s' % (code_dir, join(rootdir, 'run_single.sh'), ))
                
        
    def on_displayed(*args, **kwargs):
        
        display(Javascript('''
        
        // this is a terrible hack, but it'll have to do for now
       setTimeout(function() {
           $('.widget-button').on('click', function(e) {
           
           var cells = IPython.notebook.get_cells();
           var cell = null;
           for (var i = 0; i < cells.length; i++) {
               if (cells[i].cell_type == 'code') {
                   cell = cells[i];
                   break;
               }
           }
           
           console.log("Click", cell);
           
           IPython.notebook.kernel.send_shell_message('comm_msg',
           {'comm_id': '%s',
            'data': {
                'method': 'custom', 
                'content': {
                    'event': 'click', 'extra': 'extra'
                 }
               }
           });
       });
   }, 500);
        
        ''' % run_button.comm.comm_id))
        
        
    run_button.on_displayed(on_displayed)
    
    selector.observe(on_selector_change, names="value")
    on_selector_change({'new': selector.value})
    
    run_button.on_click(on_click)
    #runall_button.on_click(on_runall)
    
    # Layout widgets
    return widgets.VBox([selector, label,
                         run_button])
    
    # Setup widget hook
    #display(Javascript("console.log($(element).find('.widget-button'));"))
    