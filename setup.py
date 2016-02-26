from distutils.core import setup

setup(
    name='kleaner',
    version='0.0.1',
    author='Boris Lau',
    author_email='boris@techie.im',
    packages=['kleaner'],
    url='https://github.com/sketchytechky/kleaner/',
    description='Simple utils for cleaning data.',
    install_requires=[
        "pandas>= 0.16"
    ],
)
