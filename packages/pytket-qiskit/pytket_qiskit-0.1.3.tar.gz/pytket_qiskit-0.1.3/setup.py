import setuptools
from setuptools import setup


def find_pytket_subpackages():
    locations = [('pytket', 'pytket'), ('pytket/chemistry',
                                        'pytket.chemistry'), ('pytket/backends', 'pytket.backends')]
    # prefixes = 'qiskit.providers'
    pkg_list = []

    for location, prefix in locations:
        pkg_list += list(
            map(lambda package_name: '{}.{}'.format(prefix, package_name),
                setuptools.find_packages(where=location))
        )

    return pkg_list

setup(
    name='pytket_qiskit',
    version='0.1.3',
    author='Will Simmons',
    author_email='will.simmons@cambridgequantum.com',
    python_requires='>=3.6',
    url='https://github.com/CQCL/pytket',
    description='Extension for pytket, providing translation to and from the Qiskit framework',
    license='Apache 2.0',
    packages = find_pytket_subpackages(),
    install_requires = [
        'pytket >=0.2.0',
        'qiskit ~=0.10.1',
        'qiskit-chemistry ~=0.5',
        'matplotlib ~=2.2'
    ],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering"
    ],
    zip_safe=False
)
