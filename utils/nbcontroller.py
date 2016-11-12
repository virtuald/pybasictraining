
import collections
import imp
import inspect

from os.path import abspath, dirname, join
import sys

from IPython import get_ipython


import ipywidgets as widgets
import mistune
import py
import pytest

rootdir = abspath(join(dirname(__file__), ".."))
code_dir = join(rootdir, 'src')

def get_tests(tests=None):
    tpath = join(rootdir, "tests", "test_challenges.py")
    
    # Load the module using OrderedDict so that we can enumerate
    # the functions in source code order
    tmod = collections.OrderedDict()
    
    with open(tpath) as fp:
        exec(fp.read(), tmod)
    
    if tests is None:
        tests = collections.OrderedDict()
    
    for k, v in tmod.items():
        if k.startswith('test_') and inspect.isfunction(v) and \
           not hasattr(v, '_jupyter_skip'):
            tests[k[5:]] = inspect.getdoc(v)
    
    return tests


class FixedWidthTerminalWriter(py.io.TerminalWriter):
    '''Hack to force pytest output to be smaller'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fullwidth = 80

py.io.TerminalWriter = FixedWidthTerminalWriter

class CodeExecutor:
    
    @classmethod
    def get(cls):
        if not hasattr(cls, 'code_executor'):
            cls.code_executor = cls()
        return cls.code_executor
    
    def __init__(self):
        self.ipy = get_ipython()
        self.ipy.events.register('post_execute', self.post_execute)
        self.selected = False  
    
    def set_selector(self, widget):
        self.selector = widget
    
    def on_selector_fired(self):
        self.selected = True
    
    def post_execute(self):
        
        if self.selected:
            self.selected = False
            return
        
        # Determine which test to run
        test = self.selector.value[0]
        if test == 'None':
            return
        
        # Delete namespaces used in tests (except some_library)
        sys.modules.pop('mycode', None)
        sys.modules.pop('test_challenges', None)
        
        # Setup import modules for tests
        sys.modules['mycode'] = self.ipy.user_module
        self.ipy.user_module.__module__ = 'IPython Cell'
        
        print("Running challenge", test)
        
        if test == 'all':
            retval = pytest.main(['--color=yes', 'tests/test_challenges.py'])
        else:
            retval = pytest.main(['--color=yes', 'tests/test_challenges.py::test_%s' % test])
            
        print()
        if retval == 0:
            print("Challenge completed! :)")
        else:
            print("Nope. Try again!")


def show():
    
    # Import some_library
    if 'some_library' not in sys.modules:
        sys.modules['some_library'] = imp.load_source('some_library',
                                                      join(rootdir, 'src', 'some_library', '__init__.py'))
    
    # Load the module using OrderedDict so that we can enumerate
    # the functions in source code order
    tests = collections.OrderedDict()
    tests['None'] = ''
    
    tests = get_tests(tests)
    
    # doesn't seem to be a way to get the display value
    for k in list(tests.keys()):
        tests[k] = (k, tests[k])
    
    tests['all'] = ('all', 'Run all tests')
    
    # Create code executor
    exe = CodeExecutor.get()
    
    # Create widgets
    # .. dropdown, label, and run button
    label = widgets.HTML()
    selector = widgets.ToggleButtons(options=tests, value=list(tests.values())[0])
    exe.set_selector(selector)
    
    def on_selector_change(info):
        
        exe.on_selector_fired()
        
        new = info['new']
        if new[0] == 'None':
            label.value = 'Select a challenge below' 
        else:
            label.value = mistune.markdown("## Challenge %s\n\n%s" % new)
    
    
    selector.observe(on_selector_change, names="value")
    on_selector_change({'new': selector.value})
    
    # Layout widgets
    return widgets.VBox([label, selector])
