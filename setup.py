from setuptools import setup, find_packages
import io

def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()

def requirements(filename):
    reqs = list()
    with io.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs



setup(
    name="mstarpy",
    packages=find_packages(),
    version="8.0.0",
    python_requires='>=3.10',
    license='MIT License',
    author="Maël Jourdain",
    author_email='mael.jourdain@gmail.com',
    description="Mutual funds and stocks data extraction from MorningStar with Python",
    long_description= readme(),
    long_description_content_type="text/markdown",
    install_requires=requirements(filename='requirements/requirements.txt'),
    include_package_data=True,
)