from setuptools import setup, find_packages

setup(
    name="cicdrepo",
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
