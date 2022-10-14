from typing import List, Tuple, Dict


class BaseStore(object):
    def add(
            self,
            images: List[bytes],
            ids: List[str]
    ) -> int:
        raise NotImplementedError

    def select(
            self,
            idxs: List[int]
    ) -> List[Dict]:
        raise NotImplementedError
