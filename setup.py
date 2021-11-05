from setuptools import setup, find_packages

from missingadjunct import __name__, __version__

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    package_data={'itemsa': ['items/*.py']},
    include_package_data=True,
    install_requires=[
        'scipy~=1.7.1'
        'numpy~=1.21.3'
        'pyitlib~=0.2.2'
        'pandas~=1.3.4'
        'scikit-learn~=1.0.1'
    ],
    url='https://github.com/phueb/MissingAdjunct',
    license='',
    author='Philip Huebner',
    author_email='info@philhuebner.com',
    description='Generate pseudo-English sentences for research in semantic composition'
)
