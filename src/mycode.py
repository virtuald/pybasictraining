
import some_library

#some_library = 1
#x

x = 3

s = 'I am a string'

b = False

def do_something(x1, x2):
    '''
        This does something
    '''

    return x1 * x2

def keyword_fn(keyword=None):
    if keyword is None:
        return 'No'
    else:
        return keyword + 2
    

def return_many(x, y, z):
    return (x+2, y+2, z+2)

r1, r2, r3 = return_many(1, 2, 3)

teapot = some_library.i_am_a_teapot()

def gonna_call_stuff(p1):
    return some_library.multiply_by_2(p1)

t1 = ()
t2 = (False,)
t3 = (False,)*32000
t4 = ('foo', 1, False)

t5 = t4[0]

def measure_tuple(t):
    return len(t)

def sum_tuple(t):
    if len(t) == 5:
        return sum(t)

l1 = []
l2 = [False]
l3 = [False,]*32000
l4 = ['foo', 1, False]

l5 = l4[0]

def measure_list(t):
    return len(t)

def sum_list(t):
    if len(t) == 5:
        return sum(t)

def wopit(l):
    if l:
        l.append(l[0])

def bopit(l):
    if l:
        l.pop()

def mopit(l):
    if l:
        l.pop(0)

def zopit(l):
    try:
        if l.index('item') > 100:
            return True
    except ValueError:
        pass

    return False

d1 = {}
d2 = {'k1': 'item', 'k2': (1, 2)}
d3 = d2['k2']

def superd(d):
    for i in range(10000):
        d[i] = str(i)


class MyClass(object):

    clsvar = 3

    def __init__(self, v):
        self.instvar = v

        if v == 'Hi':
            self.instvar = 'Hello'

    def add5(self, v):
        self.instvar += v + 5
        return self.instvar > 100

    @property
    def prop(self):
        return 'hi'

    @prop.setter
    def prop(self, v):
        self._prop = v

    def a(self, v):
        self._a = v

    def b(self):
        if hasattr(self, '_a'):
            return self._a

mine = MyClass('Hi')
mine2 = MyClass(mine.instvar)

class StateMachine(object):
    
    def __init__(self, state):
        self._state = state
        self._cnt = 0

    @property
    def state(self):
        return self._state

    def reset(self):
        self._state = 'init'

    def process(self, sensed):

        if self.state == 'init':
            if sensed:
                self._state = 'running'
                self._cnt = 0

            return sensed

        elif self.state == 'running':
            self._cnt += 1
            if self._cnt == 20:
                self._state = 'slowing'
                self._cnt = 0

            return True

        elif self.state == 'slowing':
            self._cnt += 1
            if self._cnt == 10:
                self._state = 'init'
                return sensed

            return True

