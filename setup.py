from setuptools import setup

with open("requirements.txt") as file:
    lines = file.readlines()

requirements = [line.strip() for line in lines if not line.startswith("#")]

setup(
    name='GeoDataProcessor',
    version='1.0',
    packages=['geodataset', 'geodataset.fileutils', 'tests'],
    url='https://github.com/homomorfism/GeoDataProcessor/',
    license='MIT',
    author='Shamil Arslanov',
    author_email='arsl.sh056@mail.ru',
    description='Fast satellite image data processing library',
    keywords="tiff shp images geo",
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    install_reqs=requirements
)
