from pathlib import Path

from pynando.downloader import Downloader


path = Path('/usr/local/share/pynando/')


def find(resource_name):
    resource_name = resource_name.lower()
    assert resource_name in ['shoman', 'nanbyo']

    fp = path / '{}.json'.format(resource_name)
    if not fp.exists():
        Downloader().download()
    return fp
