import requests
from pathlib import Path

from .data import default_data_dir


class Downloader(object):
    def __init__(self, download_dir: Path=None):
        self.download_dir = download_dir
        if self.download_dir is None:
            self.download_dir = default_data_dir
        if not self.download_dir.exists():
            self.download_dir.mkdir()

    def download(self, resource: str):
        print(f'download {resource}')
        fname = f'{resource}.json'
        url = f'https://raw.githubusercontent.com/aidrd/nando/master/data/{fname}'
        fp = self.download_dir / fname
        res = requests.get(url)
        with fp.open(mode='wb') as f:
            f.write(res.content)
