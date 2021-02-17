"""Setup module for setuptools."""
from pathlib import Path

from setuptools import find_packages, setup


package_dir = Path(__file__).parent.absolute()
requirements = Path(package_dir, 'requirements.txt').read_text().split('\n')
test_requirements = Path(package_dir, 'test-requirements.txt').read_text().split('\n')
version = Path(package_dir, 'version.txt').read_text().strip()


setup(
    name='jsonvl',
    description='JSON schema validator.',
    author='Chris Gregory',
    author_email='christopher.b.gregory@gmail.com',
    url='https://github.com/gregorybchris/jsonvl',
    long_description=open(package_dir / 'README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['json', 'schema', 'validator', 'checker', 'types', 'typing', 'constraint'],
    version=version,
    license='Apache Software License',
    install_requires=requirements,
    extras_require={'testing': test_requirements},
    packages=find_packages(exclude=['tests']),
    entry_points={'console_scripts': ['jsonvl=jsonvl._cli.main:run']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Environment :: Console',
        'Natural Language :: English',
        'Topic :: Utilities',
    ],
)
