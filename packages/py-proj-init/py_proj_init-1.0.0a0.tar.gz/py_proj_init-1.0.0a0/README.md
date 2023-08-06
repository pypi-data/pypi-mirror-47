# py-proj-init

A simple Python3 project directory initializer.

## How to use

```bash
# install
pip3 install py-proj-init
# run
py-proj-init YOUR-PROJECT-NAME
# or jus
py-proj-init
```

## What you will get

```text
.
└── [project namespace]
    ├── [project package name]
    │   ├── data
    │   │   └── .gitkeep
    │   │
    │   ├── __main__.py
    │   └── __init__.py
    │
    ├── tests
    │   └── test.py
    │
    ├── .gitignore
    ├── LICENSE[DEFAULT MIT]
    ├── MANIFEST.in
    ├── README.md
    ├── requirements.txt
    └── setup.py
```

## Refs

- https://packaging.python.org/tutorials/packaging-projects/
- https://setuptools.readthedocs.io/en/latest/setuptools.html
