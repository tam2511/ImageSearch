import csv
import zipfile
from typing import Dict
from io import BytesIO, StringIO


class ZipReader(object):
    def __init__(
            self,
            file: bytes
    ):
        self.zip_file = zipfile.ZipFile(BytesIO(file), 'r')
        files_list = self.zip_file.namelist()
        if 'data.csv' not in files_list:
            raise ValueError('Zip file must contains data.csv file.')
        self.csv_reader = csv.DictReader(
            StringIO(self.zip_file.read('data.csv').decode('utf-8')),
            delimiter=','
        )

    def __iter__(self):
        return self

    def __next__(self) -> Dict:
        row = next(self.csv_reader)
        blob_image = self.zip_file.read('data/{}'.format(row['image']))
        id = row['id']
        return {
            'id': id,
            'image': blob_image
        }
