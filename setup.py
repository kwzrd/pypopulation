import setuptools

setuptools.setup(
    name="pypopulation",
    version="2020.1",  # YYYY.MINOR
    description="Find population for ISO 3166 alpha-2/3 country codes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="kwzrd",
    author_email="kay.wzrd@gmail.com",
    url="https://github.com/kwzrd/pypopulation",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
        "Topic :: Utilities",
    ],
    python_requires=">=3.5",
    include_package_data=True,
)
