from typing import Dict

def run_task(task: dict, variables: dict={}) -> dict:
    '''
    Runs one task, adding variables to the scope, and returns executions and evaluations
    Tasks can contains sub-tasks.

    input_task = {
        'vars': {
            'a': 1
        }],
        'scripts': [
            {'code': 'b = 2', 'type': 'exec'},
            {'code': '(a + b) * c', 'type': 'eval'}
        ],
        'tasks': []
    }

    output_task = run_task(input_task, variables={'c': 3})

    {
        'scripts': [
            {'value': None, 'error': None},
            {'value': 9, 'error': None},
        ],
        'tasks': []
    }

    Args:
        task (dict): task to execute
        variables (dict): variables to add in the scope
    Returns:
        task (dict): output task executed
    '''

    task = {
        'vars': {}, 
        'scripts': [], 
        'tasks': [], 
        **task,
    }

    variables = {
        **variables, 
        **(task['vars'] if 'vars' in task and isinstance(task['vars'], dict) else {}),
    }

    scripts = [run_script(s, variables) for s in task['scripts']] if 'scripts' in task and isinstance(task['scripts'], list) else []
    tasks = [run_task(t, variables) for t in task['tasks']] if 'tasks' in task and isinstance(task['tasks'], list) else []
    
    return {
        'scripts': scripts, 
        'tasks': tasks,
    }

def run_script(script: dict, variables: dict={}) -> dict:
    '''
    Runs one script

    input_script = {'code': 'a * 2', 'type': 'eval'}

    output_script = run_script(input_script, variables={'a': 2})

    {'value': 4, 'error': None}

    Args:
        script (dict): input script to execute or evaluate
        variables (dict): variables to add in the scope of the script

    Returns:
        script (dict): output script executed
    '''

    script = {
        'type': None, 
        'code': None, 
        **script,
    }

    value, error = None, None

    try:
        if 'exec' == script['type']:
            value = exec(script['code'], variables)

        elif 'eval' == script['type']:
            value = eval(script['code'], variables)

    except Exception as ex:
        error = str(ex)

    return {
        'value': value, 
        'error': error,
    }