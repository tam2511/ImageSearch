from typing import List, Dict
import base64

from src.torch_serve_utils.wrapper import TorchServeWrapper
from src.file_utils.zip_utils import ZipReader
from src.search_utils.matrix_index import MatrixIndex
from src.db_utils.sqlite_utils import SqlitePeeweeWrapper


class Handler(object):
    def __init__(self):
        self.model = TorchServeWrapper('')
        self.search_index = MatrixIndex()
        self.db_connector = SqlitePeeweeWrapper('test.db')

    def upload(
            self,
            zip_file: bytes
    ):
        zip_reader = ZipReader(zip_file)

        images_batch, ids_batch = [], []

        for row in zip_reader:
            images_batch.append(row['image'])
            ids_batch.append(str(row['id']))
            if len(images_batch) == 32:
                embeds = self.model(images_batch)
                self.search_index.add(embeds, ids_batch)
                self.db_connector.add(images_batch, ids_batch)
        if len(images_batch) > 0:
            embeds = self.model(images_batch)
            self.search_index.add(embeds, ids_batch)
            self.db_connector.add(images_batch, ids_batch)

    def search(
            self,
            image_file: bytes,
            number_images: int
    ) -> List[Dict]:
        embedding = self.model([image_file]).squeeze(0)
        result = self.search_index.search(embedding)[:number_images]
        for idx in range(len(result)):
            result[idx]['image'] = base64.b64encode(self.db_connector.select([idx])[0]['image_blob'])
            del result[idx]['idx']
        return result
