from setuptools import find_packages, setup

setup(
    name='cmake_checker',
    version='0.1.0',
    author='Maciej Patro',
    author_email='maciejpatro@gmail.com',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    url='https://github.com/MaciejPatro/cmake-checker',
    license='LICENSE',
    description='cmake-checker is a tool to search for violations to \'modern\' cmake rules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.5.0',
    install_requires=[
        "ply == 3.11",
        "junit-xml == 1.8",
    ],
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
