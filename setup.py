from setuptools import setup, find_packages

setup(
    name="blind-typing",
    version="0.0.1",
    description="Тренажёр слепой печати с аналитикой ошибок",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Xamz_pok",
    author_email="hamzatganukae@gmail.com",
    url="https://github.com/Xbasan/blind-typing",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "curses-menu",
    ],
    entry_points={
        "console_scripts": [
            "blind-typing=main:main",
        ],
    },
    data_files=[
        ("~/.config/blind-typing", ["src/test.txt"]),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
