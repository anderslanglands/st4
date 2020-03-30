import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='st4',
    version='0.1.0',
    author='Anders Langlands',
    author_email='anderslanglands@gmail.com',
    description='A Python module for controlling the eMotimo Spectrum ST4 vis serial USB',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/anderslanglands/st4',
    packages=['st4'],
    install_requires=['PySerial'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Linux',
    ],
    python_requires='>=3.6',
)
