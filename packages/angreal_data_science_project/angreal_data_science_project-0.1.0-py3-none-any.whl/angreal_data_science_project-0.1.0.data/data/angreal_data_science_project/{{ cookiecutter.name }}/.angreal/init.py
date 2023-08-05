import os


import angreal
from angreal import win,warn
from angreal.integrations.virtual_env import VirtualEnv
from angreal.integrations.git import Git


here = os.path.dirname(__file__)

pypirc = os.path.expanduser(os.path.join('~','.pypirc'))
requirements = os.path.join(here,'..','requirements','dev.txt')
setup_py = os.path.join(here,'..','setup.py')

@angreal.command()

def init():
    """
    intialize our data science project
    """
    g = Git()
    g.init()
    g.add('.')
    g.commit('-m','Project initialized via angreal.')

    warn('Creating virtual environment {{cookiecutter.name}} at ~/.venv/{{cookiecutter.name}}')
    VirtualEnv('{{ cookiecutter.name }}', python='python3', requirements=requirements)


    win('{{ cookiecutter.name }} successfully created !')
    return