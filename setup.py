import setuptools

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gradescope-ace",
    version="0.0.1",
    author="Sam Devorsetz",
    author_email="samdevorsetz@gmail.com",
    description="A tool for Gradescope's autograder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samdevo/gradescope-ace",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points={
        'console_scripts': ['gradescope-ace=src.main:main'],
    },
    python_requires=">=3.6",
)