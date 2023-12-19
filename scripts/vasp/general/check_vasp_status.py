#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path

from .is_vasp_dir import is_vasp_dir


class vaspStatusChecker:
    def __init__(self, working_dir: Path) -> None:
        assert working_dir.is_dir()
        self.working_dir = working_dir


    def read_job_type(self) -> None:
        pass


    def check_convergence(self) -> bool:
        pass


    def print_out_results(self) -> None:
        pass


def check_vasp_status():
    pass


if __name__ == "__main__":
    check_vasp_status()
