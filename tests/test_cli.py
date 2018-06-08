import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from gogo_gadget import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_base(runner):
    cmd_names = ['foo', 'bar', 'more_foo', 'less_bar']

    cmd_dict = {c: {'cmd': 'some_command', 'help': 'blabla'} for c in
                cmd_names}

    cli.build_command(cmd_dict)

    result = runner.invoke(cli.main_cli)
    assert result.exit_code == 0
    assert not result.exception
    assert all(c in result.output for c in cmd_names)


def test_cli_base_execution(runner):
    cmd_dict = {'test_command': {'cmd': "touch", 'help': 'just calls touch'}}

    cli.build_command(cmd_dict)

    with tempfile.TemporaryDirectory() as t:
        p = Path(t, 'testfile')

        assert not p.exists()
        runner.invoke(cli.main_cli, args=['test_command', str(p)])
        assert p.exists()


def test_cli_base_not_parse_option(runner):
    cmd_dict = {'test_command': {'cmd': "echo", 'help': ''}}

    cli.build_command(cmd_dict)

    result = runner.invoke(cli.main_cli, args=['test_command', 'balbla', '-p',
                                               '-x'])
    assert result.exit_code == 0


def test_cli_nested(runner):
    cmd_dict = {'test_command': {'cmd': "hello", 'help': ''},
                'group1':
                    {'nested1': {'cmd': 'nested1', 'help': ''}},
                'group2':
                    {'nested2_1':
                        {
                            'nested2_1_1': {'cmd': 'nested2_1_1'},
                            'nested2_1_2': {'cmd': 'nested2_1_2'}
                        },
                        'nested2_2':
                            {
                                'nested2_2_1': {'cmd': 'nested2_2_1'},
                                'nested2_1_2': {'cmd': 'nested2_1_2'}
                            }
                    }
                }

    cli.build_command(cmd_dict)

    result = runner.invoke(cli.main_cli)
    assert all(x in result.output for x in ['test_command', 'group1', 'group2'])

    result = runner.invoke(cli.main_cli, args=['group1'])
    assert all(x in result.output for x in ['nested1'])

    result = runner.invoke(cli.main_cli, args=['group2'])
    assert all(x in result.output for x in ['nested2_1', 'nested2_2'])


def test_is_flat_dict():
    assert cli._is_flat_dict({}) == True
    assert cli._is_flat_dict({'hello': 'world', 1: Path('bla')}) == True

    assert cli._is_flat_dict({'hello': 'world', "x": {}}) == False
    assert cli._is_flat_dict({'hello': 'world', "x": {'foo': 'bar'}}) == False
