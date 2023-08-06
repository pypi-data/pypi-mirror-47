import pypandoc

from setuptools import setup

setup(
    name='python-throttle',
    packages=['limiter'],
    version='0.1.8',
    description='Super naive python redis limiter',
    long_description=pypandoc.convert('README.md', 'rst'),
    author='soulomoon',
    author_email='fwy996602672@gmail.com',
    url='https://github.com/soulomoon/python-throttle',
    keywords=['throttle limiter redis counter timer middleware'],
    python_requires='>=3.5',
    install_requires=[
        'redis>=3',
        'pypandoc'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
