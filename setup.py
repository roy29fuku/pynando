import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name='pynando',
    version='0.0.8',
    author='Ryota Yamada',
    author_email='roy29fuku@gmail.com',
    description='wrapper for Nando (Nanbyo data ontology)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/roy29fuku/pynando',
    packages=setuptools.find_packages(exclude="tests"),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
    ],
    install_requires=required,
    python_requires='>=3.8',
)
