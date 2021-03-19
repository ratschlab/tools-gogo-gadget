import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from gogo_gadget import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_base(runner):
    cmd_names = ['foo', 'bar', 'more-foo', 'less-bar']

    cmd_dict = {c: {'cmd': 'some-command', 'help': 'blabla'} for c in
                cmd_names}

    cli.build_command(cmd_dict)

    result = runner.invoke(cli.main_cli)
    assert result.exit_code == 0
    assert not result.exception
    assert all(c in result.output for c in cmd_names)


def test_cli_base_execution(runner):
    cmd_dict = {'test-command': {'cmd': "touch", 'help': 'just calls touch'}}

    cli.build_command(cmd_dict)

    with tempfile.TemporaryDirectory() as t:
        p = Path(t, 'testfile')

        assert not p.exists()
        runner.invoke(cli.main_cli, args=['test-command', str(p)])
        assert p.exists()


def test_cli_base_not_parse_option(runner):
    cmd_dict = {'test-command': {'cmd': "echo", 'help': ''}}

    cli.build_command(cmd_dict)

    result = runner.invoke(cli.main_cli, args=['test-command', 'balbla', '-p',
                                               '-x'])
    assert result.exit_code == 0


def test_cli_nested(runner):
    cmd_dict = {'test-command': {'cmd': "hello", 'help': ''},
                'group1':
                    {'nested1': {'cmd': 'nested1', 'help': ''}},
                'group2':
                    {'nested2-1':
                        {
                            'nested2-1-1': {'cmd': 'nested2-1-1'},
                            'nested2-1-2': {'cmd': 'nested2-1-2'}
                        },
                        'nested2-2':
                            {
                                'nested2-2-1': {'cmd': 'nested2-2-1'},
                                'nested2-1-2': {'cmd': 'nested2-1-2'}
                            }
                    }
                }

    cli.build_command(cmd_dict)

    result = runner.invoke(cli.main_cli)
    assert all(x in result.output for x in ['test-command', 'group1', 'group2'])

    result = runner.invoke(cli.main_cli, args=['group1'])
    assert all(x in result.output for x in ['nested1'])

    result = runner.invoke(cli.main_cli, args=['group2'])
    assert all(x in result.output for x in ['nested2-1', 'nested2-2'])


def test_is_flat_dict():
    assert cli._is_flat_dict({})
    assert cli._is_flat_dict({'hello': 'world', 1: Path('bla')})

    assert cli._is_flat_dict({'hello': 'world', "x": {}}) == False
    assert cli._is_flat_dict({'hello': 'world', "x": {'foo': 'bar'}}) == False
