import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "simplejson"
]

setuptools.setup(
    name="structured_logger",
    version="1.0.4",
    author="Danger Farms",
    author_email="hello@dangerfarms.com",
    description="A small wrapper around the standard Python logger",
    install_requires=requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dangerfarms/logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
