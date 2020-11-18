import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="retry_helper",
    version="0.0.3",
    author="Ondřej Lanč",
    author_email="ondrej.lanc@gmail.com",
    description="Helper for retrying code when exception occur",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lancondrej/retry-helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)