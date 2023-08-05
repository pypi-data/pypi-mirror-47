import setuptools

with open("README.md") as f:
    long_description=f.read()

setuptools.setup(
    name="telemeter",
    version="1.0.3",
    author="Killian Meersman",
    author_email="killian.meersman@gmail.com ",
    description="Retrieves information about Telenet internet usage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KillianMeersman/telemeter",
    packages=setuptools.find_packages(),
    keywords="telenet telemeter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "pyyaml",
        "selenium"
    ]
)
