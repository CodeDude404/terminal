"""
Demonstrates how to display a tree of files / directories with the Tree renderable.
"""

import os
import pathlib
import sys

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree
from rich.console import Console
from rich.prompt import Prompt
import socket


def walk_directory(directory: pathlib.Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    # Sort dirs first then by filename
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        # Remove hidden files
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            # walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            try:
                file_size = path.stat().st_size
                text_filename.append(f" ({decimal(file_size)})", "blue")
            except:
                pass
            icon = "🐍 " if path.suffix == ".py" else "📄 "
            tree.add(Text(icon) + text_filename)


def getdirtxt(dir):
    dirtxt = "/"
    for i in dir:
        dirtxt = dirtxt + f'{i}/'

    return dirtxt


def ls(dir):
    try:
        directory = os.path.abspath(dir)
    except IndexError:
        print("[b]Usage:[/] python tree.py <DIRECTORY>")
    else:
        tree = Tree(
            f":open_file_folder: [link file://{directory}]{directory}",
            guide_style="bold bright_blue",
        )
        walk_directory(pathlib.Path(directory), tree)
        print(tree)


if __name__ == "__main__":
    console = Console()
    dir = ['home', 'liamo', 'Desktop']

    while True:

        cmd = Prompt.ask('[green][bold]' + os.getlogin() + '[/green]@[purple]' + socket.gethostname() +'[/purple]:[blue]' + getdirtxt(dir) + '[/blue][/bold]' + '\n$')

        if cmd == 'ls':
            ls(getdirtxt(dir))

        elif cmd.startswith('cd'):
            if cmd.replace('cd ', '') == '..':
                dir.pop()
            elif cmd.replace('cd ', '') == '/':
                dir = []
            else:
                dir.extend(cmd.replace('cd ', '').split('/'))

        elif cmd == 'clear':
            os.system('clear')

        elif cmd.startswith('python3'):
            os.system('python3 ' + getdirtxt(dir) + cmd.replace('python3 ', ''))
        else:
            text = Text()
            text.append(f"E: {cmd} was not recognized as a application.", style="bold red")
            console.print(text)
