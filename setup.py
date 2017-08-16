import pathlib
import re
import subprocess

import setuptools

directory = pathlib.Path(__file__).parent.resolve()

# version
init_path = directory.joinpath('motors', '__init__.py')
text = init_path.read_text()
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)

# long_description
readme_path = directory.joinpath('README.md')
try:
    # Try to create an reStructuredText long_description from README.md
    args = 'pandoc', '--from', 'markdown', '--to', 'rst', readme_path
    long_description = subprocess.check_output(args)
    long_description = long_description.decode()
except Exception as error:
    # Fallback to markdown (unformatted on PyPI) long_description
    print('README.md conversion to reStructuredText failed. Error:')
    print(error)
    long_description = readme_path.read_text()


setuptools.setup(
    # Package details
    name='motors',
    version=version,
    url='https://github.com/slochower/nonequilibrium-master',
    description='Analysis tools for molecular motors',
    long_description=long_description,
    license='BSD 3-Clause',

    # Author details
    author='David R. Slochower',
    author_email='slochower@gmail.com',

    # Package topics
    keywords='nonequilibrium statistical thermodynamics',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only'
    ],

    packages=['motors'],

    # Specify python version
    python_requires='>=3.5',

    # Run-time dependencies
    install_requires=[
        'errorhandler',
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn'
    ],

    # Additional groups of dependencies
    extras_require={
    },

)
