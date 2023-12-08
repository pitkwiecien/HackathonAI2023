from typing import Dict


class IndexedObject:
    def __init__(self, data: str, metadata: Dict[str, str]):
        self.data = data
        self.metadata = metadata

    @classmethod
    def create_object(cls, indexed_data: str, **kwargs):
        return cls(indexed_data, kwargs)

    def __str__(self):
        s = f"IndexedObject(\n-> data : {self.data}\n-> metadata:["
        for key, value in self.metadata.items():
            s += f"\n-> -> {key} : {value}"
        s += "\n]\n)\n\n\n"
        return s

