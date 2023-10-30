from MuonDataLib.data.store.data_template import dataTemplate


class Sample(dataTemplate):
    """
    Class for storing sample information
    """
    def __init__(self, ID: int,
                 thickness: float, height: float, width: float,
                 B_field: float, Temp: float, name: str):
        """
        Initialise the sample object

        """
        super().__init__
        self._ID = ID
        self._thickness = thickness
        self._height = height
        self._width = width
        self._B_field = B_field
        self._Temp = Temp
        self._name = name

    @property
    def get_ID(self) -> int:
        return self._ID

    @property
    def get_thickness(self) -> float:
        return self._thickness

    @property
    def get_height(self) -> float:
        return self._height

    @property
    def get_width(self) -> float:
        return self._width

    @property
    def get_magnetic_field(self) -> float:
        return self._B_field

    @property
    def get_temperature(self) -> float:
        return self._Temp

    @property
    def get_name(self) -> str:
        return self._name
