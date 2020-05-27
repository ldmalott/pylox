import sys
import os
from io import IOBase
from typing import List


import click
from loguru import logger


@click.command()
@click.argument('output_dir', type=click.Path())
def generate_ast(output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    define_ast(output_dir, "Expr", [
        "Binary : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal : Any value",
        "Unary : Token operator, Expr right"
    ])


def write_header(fh: IOBase, base_name: str):
    print('from dataclasses import dataclass\n', file=fh)
    print('from pylox.token import Token\n\n', file=fh)
    print(f'class {base_name}(object):', file=fh)
    print('    pass\n\n', file=fh)


def define_ast(output_dir: str, name: str, definitions: List[str]):
    with open(f'{output_dir}/{name.lower()}.py', 'w') as fh:
        write_header(fh, name)

        for definition in definitions:
            class_name = definition.split(':')[0].strip()
            fields = definition.split(':')[1].strip()
            define_type(fh, name, class_name, fields)

        define_visitor(fh, name, definitions)


def define_type(fh: IOBase, base_name: str, class_name: str, fields: str):
    print('@dataclass', file=fh)
    print(f'class {class_name}({base_name}):', file=fh)

    fields = fields.split(', ')
    for field in fields:
        field_name = field.split(' ')[1].strip()
        field_type = field.split(' ')[0].strip()
        print(f'    {field_name}: {field_type}', file=fh)

    print('\n', file=fh)


def define_visitor(fh: IOBase, base_name: str, types: List[str]):
    print('class Visitor:', file=fh)
    print('    def __str__(self):', file=fh)
    print('        return self.__class__.__name__', file=fh)
    print('\n', file=fh)

    for type in types:
        type_name = type.split(":")[0].strip();
        print(f'    def visit_{type_name.lower()}_{base_name.lower()}({base_name.lower()}: {type_name.lower()}):', file=fh)
        print('        pass', file=fh)
        print('\n', file=fh)

    print('\n', file=fh)
