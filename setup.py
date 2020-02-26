from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='muss',
      version='0.1',
      description='Python code execution module',
      author='jalepi',
      author_email='jalepi@live.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jalepi/muss',
      packages=[]
    )