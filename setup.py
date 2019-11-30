import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delete-tweets",
    version="1.0.4",
    author="Koen Rouwhorst",
    author_email="info@koenrouwhorst.nl",
    description="Delete tweets from your Twitter timeline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koenrh/delete-tweets",
    packages=["deletetweets"],
    entry_points={
        "console_scripts": [
            'delete-tweets = deletetweets.__main__:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
