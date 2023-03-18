# -*- coding: utf-8 -*-

_current_target = None


def set_target(target):
    global _current_target
    _current_target = target


def log(message: str, hide_target: bool = False):
    global _current_target
    if _current_target is None or hide_target:
        print(message)
        return

    print(f"[{_current_target}] {message}")
