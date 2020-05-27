from distutils.core import setup

setup(
    name='pylox',
    version='0.1.0',
    description="Python implementation for Lox interpreter",
    author="Levi Malott",
    entry_points = {
        'console_scripts': [
            'pylox=pylox.lox:lox',
            'generate-ast=pylox.tools.generate_ast:generate_ast'
        ]
    }
)
