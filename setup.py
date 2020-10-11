import setuptools

setuptools.setup(
    name="pypopulation",
    version="2020.2",  # YYYY.MINOR
    description="Population lookup via ISO 3166 country codes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="kwzrd",
    author_email="kay.wzrd@gmail.com",
    url="https://github.com/kwzrd/pypopulation",
    packages=["pypopulation"],
    package_data={"pypopulation": ["resources/countries.json"]},
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
