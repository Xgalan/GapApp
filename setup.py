# pylint: disable=bad-whitespace
import setuptools


setuptools.setup(
    name="GapApp",
    author="Erik Mascheri",
    author_email="erik.mascheri@gmail.com",
    license="GPLv3",
    packages=setuptools.find_packages(),
    install_requires=[
        "Django>=3.2,<3.3",
        "djangorestframework",
        "django-extensions",
        "django-treebeard",
        "django-import-export",
        "django-filter",
        "pyyaml",
        "uritemplate",
        "whitenoise",
        "django-environ",
        "gunicorn",
        "django-cors-headers",
        "django-htmx>=1.14,<2",
        "django-debug-toolbar",
    ],
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
