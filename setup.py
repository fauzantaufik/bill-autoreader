from setuptools import setup, find_packages

setup(
    name="bill-autoreader",
    version="0.1.0",
    packages=find_packages(),
    description="A utility to process bill data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/BILL-AUTOREADER",
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
