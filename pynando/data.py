from pathlib import Path
import os


default_data_dir = Path(os.path.expanduser('~/pynando_data/'))
resources = ['shoman', 'nanbyo', 'shoman_class', 'nanbyo_class']


def find(resource, data_dir: Path=None):
    resource = resource.lower()
    assert resource in resources, f'Available resoureces are bellow: {resources}'

    if data_dir is None:
        data_dir = default_data_dir

    fp = data_dir / '{}.json'.format(resource)
    return fp
