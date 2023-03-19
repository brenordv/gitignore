# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from pathlib import Path

import requests

from src.config import parse_config
from src.logger import set_target, log


def _parse_args():
    qty_args = len(sys.argv)
    if qty_args < 2:
        log("You must inform the target folder.", hide_target=True)
        exit(-1)
    if qty_args > 2:
        log("You need to pass only one argument: the target folder.", hide_target=True)
        exit(-1)

    path = Path(sys.argv[1])

    if not path.exists():
        log("The target folder does not exist.", hide_target=True)
        exit(-1)

    if not path.is_dir():
        log("The target folder is not a directory.", hide_target=True)
        exit(-1)

    return path


def _is_git(file: Path):
    return file.name == '.git' or [True for parent in file.parents if parent.name == '.git']


def _is_in_ignorable_folder(file: Path):
    ignorable_folders = ['.git', 'node_modules', 'venv', 'env', 'build', 'dist', 'bin', '.idea', '.vs', '.vscode']
    return [True for parent in file.parents if parent.name in ignorable_folders]


def _extract_gitignore_data(config_item: dict):
    gitignore_data = config_item.get('cache', [])
    if len(gitignore_data) > 0:
        log("Using cached gitignore data...")
        return gitignore_data

    log("Fetching gitignore data...")
    url = config_item.get('url')
    if url is None:
        log(f"Invalid config item: {config_item}")
        return []

    response = requests.get(url)

    if not response.ok:
        log(f"Error to get gitignore data from {url}. Status code: {response.status_code}")
        return []

    gitignore_data = response.text.splitlines()

    log(f"Gitignore data fetched successfully. Caching {len(gitignore_data)} lines of raw data...")

    config_item['cache'] = gitignore_data
    return gitignore_data


def _get_gitignore_for(target: str, config: dict) -> list:
    config_item = config.get(target)
    if config_item is None:
        return []

    config_cache = config_item.get('cache')
    if config_cache is not None and len(config_cache) > 0:
        return config_cache

    return _extract_gitignore_data(config_item)


def _get_target(file: Path):
    if file.is_dir() or len(file.suffixes) == 0 or file.suffix == "":
        target = file.name
    else:
        target = file.suffixes[-1]

    target = target.lower().strip()
    return target


def _sanitize_gitignore_data(gitignore_data):
    data = set()
    for line in gitignore_data:
        if line.startswith('#') or line in ["", "\n", "\r\n"]:
            continue

        data.add(line)

    return data


def _dump_gitignore_data(gitignore_data: list, target_gitignore):
    if target_gitignore.exists():
        log("The .gitignore already exists. Merging with the new data...", hide_target=True)
        current_gitignore = target_gitignore.read_text().splitlines()
        gitignore_data.extend(current_gitignore)

    clean_data = _sanitize_gitignore_data(gitignore_data)
    sorted_clean_data = sorted(clean_data)
    log(f"Writing {len(sorted_clean_data)} lines to .gitignore...", hide_target=True)
    target_gitignore.write_text("\n".join(sorted_clean_data), newline="\n")


def main():
    log("Generating .gitignore...")
    start = datetime.now()
    path = _parse_args()
    config = parse_config()
    gitignore_data = []
    already_added = []
    target_gitignore = path.joinpath('.gitignore')

    log("Scanning files...")
    for file in path.glob('**/*'):
        if _is_git(file) or file == target_gitignore or _is_in_ignorable_folder(file):
            continue

        target = _get_target(file)
        if target in already_added or target not in config:
            continue

        set_target(target)
        log(f"Adding {target} related data to .gitignore...")
        gitignore_data.extend(_get_gitignore_for(target, config))
        already_added.append(target)

    log("Dumping .gitignore...", hide_target=True)
    _dump_gitignore_data(gitignore_data, target_gitignore)
    elapsed_time = datetime.now() - start
    log(f"Done! Elapsed time: {elapsed_time}", hide_target=True)


if __name__ == '__main__':
    main()
