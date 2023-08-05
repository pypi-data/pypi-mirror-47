from typing import Optional, List, Pattern, Union
from cmdi import command, CmdResult, set_result, strip_args

from . import lib


@command
def inject_interface_into_readme(
    interface_file: str,
    readme_file: str = 'README.md',
    **cmdargs,
) -> CmdResult:
    lib.inject_interface_into_readme(**strip_args(locals()))
    return set_result()


@command
def build_read_the_docs(
    clean_dir: bool = False,
    **cmdargs,
) -> CmdResult:
    lib.build_read_the_docs(**strip_args(locals()))
    return set_result()


@command
def create_py_venv(
    py_bin: str,
    venv_dir: str,
    **cmdargs,
) -> CmdResult:
    lib.create_py_venv(**strip_args(locals()))
    return set_result()


@command
def bump_py_module_version(
    file: str,
    new_version: str,
    **cmdargs,
) -> CmdResult:
    lib.bump_py_module_version(**strip_args(locals()))
    return set_result()
