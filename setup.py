from setuptools import setup, find_packages

setup(
    name='love_me_tender',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "openai",
    ],
    url='http://cottagelabs.com/',
    author='Cottage Labs',
    author_email='us@cottagelabs.com',
    description='Semantic search of tender docs using openai',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Copyheart',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)