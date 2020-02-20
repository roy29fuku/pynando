from git import Repo

import pynando.data


def default_download_dir():
    return pynando.data.path


class Downloader(object):
    def __init__(self, download_dir=None):
        self._download_dir = download_dir
        if self._download_dir is None:
            self._download_dir = default_download_dir()

    def download(self):
        print('download nando data')
        print('data are private currently')
        name = input('Username for https://github.com: ')
        url = 'https://{}@github.com/precemia/nando_originalData.git'.format(name)
        Repo.clone_from(url, self._download_dir)
        return
