"""
Install script~
"""
from setuptools import find_packages, setup

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='vkopt_telegram_parser',
    version='0.0.1',
    description='Utilities for collecting dialog data from VK.com (VkOpt dump) and Telegram',
    long_description=readme,
    author='saber-nyan',
    author_email='saber-nyan@ya.ru',
    url='https://github.com/saber-nyan/vkopt_telegram_parser',
    license='WTFPL',
    install_requires=[
        'beautifulsoup4==4.8.2',
        'lxml==4.5.0',
        'ujson==1.35',
    ],
    packages=find_packages(),
    include_package_data=True
)
