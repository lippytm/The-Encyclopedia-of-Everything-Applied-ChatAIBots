"""
setup.py — lippytmai AI Deployment Activation Launcher
Installs the `lippytmai-launch` CLI command system-wide.

Usage after install:
    lippytmai-launch B-001              # launch book artifact
    lippytmai-launch B-001 --audio      # generate audiobook
    lippytmai-launch B-001 --quiz       # interactive quiz
    lippytmai-launch --list             # all books
    lippytmai-launch --status           # deployment dashboard
    lippytmai-launch --api              # start ADA web API on :8000
"""
from setuptools import setup, find_packages

setup(
    name="lippytmai-launch",
    version="1.0.0",
    description="AI Deployment Activation launcher for the Earn-while-you-Learn ebook series",
    author="lippytmai",
    author_email="lippytmai@lippytm.ai",
    url="https://github.com/lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.12",
    install_requires=[
        "httpx>=0.27.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "fastapi>=0.111.0",
        "uvicorn[standard]>=0.30.0",
        "pydantic>=2.7.0",
    ],
    extras_require={
        "audiobook": [
            "pydub>=0.25.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "lippytmai-launch=lippytmai_launch:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
    ],
)
