from typing import List, Dict
import json
import os

from src.torch_serve_utils.wrapper import TorchServeWrapper
from src.file_utils.zip_utils import ZipReader
from src.search_utils.matrix_index import MatrixIndex
from src.db_utls.alphabet_store import AlphabetStore


class Handler(object):
    def __init__(self):
        self.cfg = json.load(open(
            os.environ['BACKEND_CONFIG'],
            'r'
        ))
        self.model = TorchServeWrapper(
            api_url=self.cfg['torch_serve']['api_url']
        )
        self.search_index = MatrixIndex()
        self.store = AlphabetStore(
            images_path=self.cfg['store']['images_path'],
            max_size=self.cfg['store']['max_size'],
            image_height=self.cfg['store']['image_height']
        )

    def upload(
            self,
            zip_file: bytes
    ):
        added_count = 0

        def add(images_batch: List, ids_batch: List):
            nonlocal added_count
            embeds = self.model(images_batch)
            self.search_index.add(embeds)
            added_count += self.store.add(images_batch, ids_batch)

        zip_reader = ZipReader(zip_file)

        images_batch, ids_batch = [], []

        for row in zip_reader:
            images_batch.append(row['image'])
            ids_batch.append(int(row['id']))
            if len(images_batch) == self.cfg['batch_size']:
                add(images_batch=images_batch, ids_batch=ids_batch)
        if len(images_batch) > 0:
            add(images_batch=images_batch, ids_batch=ids_batch)
        return added_count

    def search(
            self,
            image_file: bytes,
    ) -> List[Dict]:
        embedding = self.model([image_file]).squeeze(0)
        idxs, scores = self.search_index.search(embedding)
        data = self.store.select(idxs)
        return [
            {
                'id': data[i]['id'],
                'image_path': data[i]['image_path'],
                'score': scores[i]
            }
            for i in range(len(data))
        ]
