"""
A tool to aggregate custom command line tools into one.

On startup, a gogo file in YAML format is read and a command line interface
is created on the fly.
"""

import os
from pathlib import Path

import click
import sys
import subprocess

from gogo_gadget import config

GOGO_FILE_ENV_VAR = "GOGO_FILE_PATH"
ignore_opt = {'context_settings': dict(ignore_unknown_options=True)}
cmd_fields = ['cmd', 'help']


@click.group()
def main_cli():
    pass


def _create_function(name, command):
    def f(ctx, args):
        final_cmd = ' '.join([command] + list(args))
        exit_code = subprocess.call(final_cmd, shell=True)
        ctx.exit(exit_code)

    f.__name__ = name
    return f


def _is_flat_dict(d):
    return all(not isinstance(v, dict) for v in d.values())


def _bind_function(name):
    def f():
        pass

    f.__name__ = name
    return f


def process_node(cmd_name, children, parent_cmd):
    if 'cmd' in children:
        cmd = click.command(**ignore_opt)
        a = click.argument('args', nargs=-1)
        c = click.pass_context
        cmd_f = _create_function(cmd_name, children['cmd'])
        base_cmd = cmd(a(c(cmd_f)))

        parent_cmd.add_command(base_cmd)

    if not _is_flat_dict(children):
        c = _bind_function(cmd_name)
        node_group = parent_cmd.group()(c)

        for k, v in children.items():
            if k not in cmd_fields:
                if not isinstance(v, dict):
                    raise ValueError(
                        "Don't know what to do with {} : {}".format(
                            k, v))

                process_node(k, v, node_group)


def construct_commands(cfg_dict, parent_cmd):
    for k, v in cfg_dict.items():
        process_node(k, v, parent_cmd)


def build_command(config_dict):
    construct_commands(config_dict, main_cli)


def main():
    gogo_file_path = Path(Path.home(), '.gogo.yml')

    if GOGO_FILE_ENV_VAR in os.environ:
        gogo_file_path = os.environ[GOGO_FILE_ENV_VAR]

    d = config.load_config(gogo_file_path)
    build_command(d)
    return main_cli()


if __name__ == '__main__':
    sys.exit(main())
