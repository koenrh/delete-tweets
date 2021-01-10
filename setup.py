import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delete-tweets",
    version="2.0.1",
    author="Koen Rouwhorst",
    author_email="info@koenrouwhorst.nl",
    description="Delete tweets from your Twitter timeline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koenrh/delete-tweets",
    packages=["deletetweets"],
    install_requires=[
        "python-twitter>=3.5,<4",
        "python-dateutil>=2.8.1,<3"
    ],
    entry_points={
        "console_scripts": [
            'delete-tweets = deletetweets.__main__:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
