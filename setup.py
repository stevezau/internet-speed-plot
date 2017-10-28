from setuptools import setup

setup(
    name='Internet Speed test',
    version='1.0',
    packages=[],
    url='',
    license='MIT',
    author='Brenton Collins',
    author_email='brenton.collins@outlook.com',
	description='Plot internet speed over a 24 hour period',
    install_requires=[
        'speedtest-cli',
        'matplotlib',
        'numpy',
		'requests',
		'pyvirtualdisplay',
		'selenium',
		'bs4'
    ],
)
