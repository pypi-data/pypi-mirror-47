from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="audiomentations",
    version="0.7.0",
    author="Iver Jordal",
    description="A Python library for audio data augmentation. Inspired by albumentations."
    " Useful for machine learning.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iver56/audiomentations",
    packages=find_packages(exclude=["demo", "tests"]),
    install_requires=["numpy>=1.13.0", "librosa>=0.6.1", "scipy>=1.0.0,<2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
)
