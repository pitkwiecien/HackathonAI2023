from typing import Dict


class IndexedObject:
    """
    A class representing an indexed object with data and associated metadata.

    Attributes:
    - data (str): The main data of the indexed object.
    - metadata (Dict[str, str]): Dictionary containing metadata associated with the indexed object.
    """

    def __init__(self, data: str, metadata: Dict[str, str]):
        """
        Initializes an IndexedObject with provided data and metadata.

        Args:
        - data (str): The main data of the indexed object.
        - metadata (Dict[str, str]): Dictionary containing metadata associated with the indexed object.
        """
        self.data = data
        self.metadata = metadata

    @classmethod
    def create_object(cls, indexed_data: str, **kwargs):
        """
        Alternative constructor method to create an IndexedObject.

        Args:
        - indexed_data (str): The main data for the indexed object.
        - **kwargs: Additional key-value pairs to be included in the metadata.

        Returns:
        - IndexedObject: An instance of IndexedObject.
        """
        return cls(indexed_data, kwargs)

    def __str__(self):
        """
        Returns a string representation of the IndexedObject.

        Returns:
        - str: String representation of the IndexedObject displaying its data and metadata.
        """
        s = f"IndexedObject(\n-> data : {self.data}\n-> metadata:["
        for key, value in self.metadata.items():
            s += f"\n-> -> {key} : {value}"
        s += "\n]\n)\n\n\n"
        return s
