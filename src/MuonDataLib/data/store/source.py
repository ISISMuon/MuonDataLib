from MuonDataLib.data.store.data_template import dataTemplate


class Source(dataTemplate):
    """
    A class for the source information
    """
    def __init__(self, name: str, probe: str, source_type: str):
        self._name = name
        self._probe = probe
        self._source_type = source_type

    @property
    def get_name(self) -> str:
        return self._name

    @property
    def get_probe(self) -> str:
        return self._probe

    @property
    def get_type(self) -> str:
        return self._source_type
