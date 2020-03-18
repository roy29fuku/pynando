import requests
from pathlib import Path

import pynando.data


def default_download_dir():
    return pynando.data.path


class Downloader(object):
    def __init__(self, download_dir: Path=None):
        self._download_dir = download_dir
        if self._download_dir is None:
            self._download_dir = default_download_dir()
        if not self._download_dir.exists():
            self._download_dir.mkdir()

    def download(self):
        print('download nando data')
        url_list = [
            'https://raw.githubusercontent.com/aidrd/nando/master/data/nanbyo.json',
            'https://raw.githubusercontent.com/aidrd/nando/master/data/nanbyo_class.json',
            'https://raw.githubusercontent.com/aidrd/nando/master/data/shoman.json',
            'https://raw.githubusercontent.com/aidrd/nando/master/data/shoman_class.json',
        ]
        for url in url_list:
            fname = url.split('/')[-1]
            fp = self._download_dir / fname

            print('downloading {}'.format(fname))
            res = requests.get(url)
            with fp.open(mode='wb') as f:
                f.write(res.content)
