from setuptools import setup, find_packages

setup(

    name="...",
    version="1.0",
    description="...",
    author="Ning",
    author_email="makiasagawa@gmail.com",
    packages=find_packages(),
    install_requires=["nltk", "pickle", "ast", "json", "pandas", "numpy", "matplotlib"],
    url='...',
    entry_points='''
        [console_scripts]
        emr=engine.emr
    '''

)

