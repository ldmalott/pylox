import sys

import click
from loguru import logger

from pylox.scanner import Scanner


logger.remove()
logger.add(sys.stdout, format='<level>{message}</level>')


class Lox(object):
    had_error: bool = False

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        logger.error(f'[line {line}] Error{where}: {message}')
        cls.had_error = True

    def run_file(path: str):
        with open(path, 'r') as fh:
            source = fh.read();

        self.run(source)

        if self.had_error:
            exit(65)

    def run_prompt(self):
        while True:
            line = input("> ")
            self.run(line)

    def run(self, source: str):
        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def lox(paths: str) -> int:
    runner = Lox()
    if paths:
        for path in paths:
            runner.run_file(path)
    else:
        runner.run_prompt()



