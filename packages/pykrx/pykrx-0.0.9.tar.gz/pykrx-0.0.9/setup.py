from setuptools import setup, find_packages

setup(
    name            = 'pykrx',
    version         = '0.0.9',
    description     = 'KRX scraping',
    url             = 'https://github.com/sharebook-kr/pykrx',
    author          = 'Brayden Jo, Lukas Yoo',
    author_email    = 'brayden.jo@outlook.com, jonghun.yoo@outlook.com, pystock@outlook.com',
    install_requires= ['requests', 'pandas', 'datetime',],
    license         = 'MIT',
    packages        = find_packages(include=['pykrx', 'pykrx.*', 'pykrx.stock.*', 'pykrx.e3.*', 'pykrx.bond.*' ]),
    python_requires = '>=3',
    zip_safe        = False
)