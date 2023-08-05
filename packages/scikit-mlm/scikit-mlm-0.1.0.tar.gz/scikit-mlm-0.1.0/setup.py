"""Setup file for skmlm."""
from setuptools import setup, find_packages

def read(filename):
    with open(filename, "r") as fh:
        return fh.read()

setup(
    name='scikit-mlm',
    version='0.1.0',
    description='Minimal Learning Machine implementation using the scikit-learn API',
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url='https://github.com/omadson/scikit-mlm',
    author='Madson Dias',
    author_email='madsonddias@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'numpy>=1.15.4',
        'scipy>=1.1.0',
        'scikit-learn>=0.21.0',
        'fuzzy-c-means>=0.0.5',
        'mrsr>=0.0.3'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
    ]
)
