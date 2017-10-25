from setuptools import setup

setup(
    name='NBN Speed test',
    version='1.0',
    packages=[],
    url='',
    license='MIT',
    author='Brenton Collins',
    author_email='brenton.collins@outlook.com',
    description='Plot the NBN over a 24 hour period',
    install_requires=[
        'speedtest-cli',
        'matplotlib',
        'numpy'
    ],
)
