from setuptools import setup

setup(
    name="flit6",
    version="0.1",
    description="cross-compat flit install",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    py_modules=["flit6"],
    entry_points={"console_scripts": ["flit=flit6:main"]},
    author="Wim Glenn",
    author_email="hey@wimglenn.com",
    license="MIT",
    url="https://github.com/wimglenn/flit6",
    install_requires=["pip", "flit; python_version>='3'"],
)
