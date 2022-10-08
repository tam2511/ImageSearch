from typing import List, Dict

from peewee import *


class ImageModel(Model):
    image_blob = BlobField()
    id_name = TextField()


class SqlitePeeweeWrapper(object):
    def __init__(
            self,
            db_path: str
    ):
        self.db = SqliteDatabase(db_path)
        self.db.bind([ImageModel])
        self.db.create_tables([ImageModel])

    def add(
            self,
            images: List[bytes],
            ids: List[str]
    ):
        with self.db.atomic():
            ImageModel.insert_many(
                [
                    {
                        'image_blob': images[idx],
                        'id_name': ids[idx]
                    }
                    for idx in range(len(images))
                ]
            ).execute()

    def select(
            self,
            idxs: List[int]
    ) -> List[Dict]:
        idxs = [_ + 1 for _ in idxs]
        result = list(ImageModel.select().where(ImageModel.id << idxs).dicts())
        return result
