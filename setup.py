from setuptools import setup, find_packages

setup(name='cargo_dep_list',
      version='0.0.1',
      description='Listup dependencies in cargo.toml',
      author='Koji Hachiya',
      author_email='koji.hachiya@gmail.com',
      url='https://github.com/koji88/cargo-dep-list/',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      cargo_dep_list = cargo_dep_list.main:main
      """,
      install_requires=[
          'json',
          'requests'
      ],
)
