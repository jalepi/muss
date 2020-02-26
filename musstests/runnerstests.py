import unittest
import math
from muss import runners

def compare_task(actual, expected, compare_fn):
    if 'scripts' in actual:
        for actual_script, expected_script in zip(actual['scripts'], expected['scripts']):
            compare_script(actual_script, expected_script, compare_fn)

    if 'tasks' in actual:
        for actual_task, expected_task in zip(actual['tasks'], expected['tasks']):
            compare_task(actual_task, expected_task, compare_fn)


def compare_script(actual, expected, compare_fn):
    compare_fn(actual['value'], expected['value'])
    compare_fn(actual['error'], expected['error'])

def test_script(given_script, expected_script, compare_fn):
    actual_script = runners.run_script(given_script)
    compare_script(expected_script, actual_script, compare_fn)

def test_tasks(given_task, expected_task, compare_fn):
    actual_task = runners.run_task(given_task)
    compare_task(expected_task, actual_task, compare_fn)

given_simple_script = { 'type': 'eval', 'code': '1.0 + 2.0' }
expected_simple_script = { 'value': 3, 'error': None }

given_simple_task = {
    'vars': {'a': 1.0, 'b': 2.0, 'aa': [1.0, 2.0], 'bb': [3.0, 4.0],},
    'scripts': [
        {'type': 'exec', 'code': 'import math'},
        {'type': 'exec', 'code': 'def somefn(): return math'},
        {'type': 'eval', 'code': '1.0 + 2.0'},
        {'type': 'eval', 'code': '[1.0, 2.0, 3.0]'},
        {'type': 'eval', 'code': 'a + b'},
    ],
    'tasks': [],
}

expected_simple_task = {
    'scripts': [
        {'value': None, 'error': None},
        {'value': None, 'error': None},
        {'value': 3.0, 'error': None},
        {'value': [1.0, 2.0, 3.0], 'error': None},
        {'value': 3.0, 'error': None},
    ],
}

given_nested_task = {
    'vars': {'a': 1.0, 'b': 2.0},
    'scripts': [
        {'type': 'exec', 'code': 'import math'},
        {'type': 'eval', 'code': 'math.sqrt(a + b)'},
    ],
    'tasks': [
        {
            'vars': {'x': 5.0},
            'scripts': 
            [
                {'type': 'exec', 'code': 'def calc_x(v): return math.sqrt(v)'},
                {'type': 'eval', 'code': 'calc_x(x)'},
                {'type': 'eval', 'code': 'x**x'},
            ],
            'tasks': [
                {
                    'vars': {'s': 1},
                    'scripts': [
                        {'type': 'exec', 'code': 's = s + 1'},
                        {'type': 'eval', 'code': 's + 1'},
                    ],
                },
                {
                    'vars': {},
                    'scripts': [
                        {'type': 'eval', 'code': 's'},
                        {'type': 'eval', 'code': 'math.sqrt(9)'},
                    ],
                },
                {
                    'vars': {'exp': 'a[i] + b[i]', 'ts': [0, 1], 'a': [2.0, 3.0], 'b':[5.0, 7.0]},
                    'scripts': [
                        {
                            'type': 'exec', 
                            'code': '''
def __hf(): 
    return [eval(exp) for i, t in enumerate(ts)]
''',
                        }, 
                        {'type': 'eval', 'code': '__hf()'},
                    ],
                },
            ],
        },
    ],
}

expected_nested_task = {
    'scripts': [
        {'value': None, 'error': None},
        {'value': math.sqrt(1.0 + 2.0), 'error': None},
    ],
    'tasks': [
        {
            'scripts': [
                {'value': None, 'error': None},
                {'value': math.sqrt(5.0), 'error': None},
                {'value': 5.0**5.0, 'error': None},
            ],
            'tasks': [
                {
                    'scripts': [
                        {'value': None, 'error': None},
                        {'value': 1 + 1 + 1, 'error': None},
                    ],
                    'tasks': [],
                },
                {
                    'scripts': [
                        {'value': None, 'error': "name 's' is not defined"},
                        {'value': 3, 'error': None},
                    ],
                    'tasks': [],
                },
                {
                    'scripts': [
                        {'value': None, 'error': None},
                        {'value': [2.0 + 5.0, 3.0 + 7.0], 'error': None},
                    ],
                    'tasks': [],
                },
            ],
        },
    ],
}

given_high_load_task = {
    'scripts': [
        {'type': 'exec', 'code': '''
def fibo(n: int) -> int:
    if n > 2:
        return fibo(n - 1) + fibo(n - 2)
    else:
        return n
'''},
        {'type': 'eval', 'code': 'fibo(31)'}
    ]
}

expected_high_load_task = {
    'scripts': [
        {'error': None, 'value': None},
        {'error': None, 'value': 2178309},
    ]
}

class RunnersTest(unittest.TestCase):

    def test_simple_script(self):
        test_script(given_simple_script, expected_simple_script, self.assertEqual)

    def test_simple_task(self):
        test_tasks(given_simple_task, expected_simple_task, self.assertEqual)

    def test_nested_task(self):
        test_tasks(given_nested_task, expected_nested_task, self.assertEqual)