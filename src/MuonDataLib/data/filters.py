"""
Dataclass for filters.

The Filters object serves as a schema for saving filters to file.
"""
from dataclasses import asdict, dataclass, field
import json

@dataclass
class Filter:
    """
    A class to define a filter.
    """
    name: str
    start: float
    end: float

@dataclass
class TimeFilters:
    """
    A class to define the set of all time filters.
    """
    keep_filters: list[Filter] = field(default_factory=list)
    remove_filters: list[Filter] = field(default_factory=list)

    def clear(self):
        """
        Clear the time filters.
        """
        self.keep_filters = []
        self.remove_filters = []

    def _add_filter(self,
                    name: str,
                    start: float,
                    end: float,
                    filter_list: list[Filter]):
        """
        Add a filter to a list of filters.
        :param name: the name for the filter
        :param start: the start point of the interval
        :param end: the end point of the interval
        :param filter_list: the list of filters to add to.
        """
        if name in [f.name for f in filter_list]:
            raise RuntimeError(f'The name {name} already exists.')
        if start > end:
            raise RuntimeError('The start time is after the end time.')
        filter_list.append(Filter(name, start, end))


    def add_keep_filter(self, name: str, start: float, end: float):
        """
        Adds a filter that keeps data in an interval.
        :param name: the name for the filter
        :param start: the start point for the interval
        :param end: the end point for the interval
        """
        self._add_filter(name, start, end, self.keep_filters)

    def add_remove_filter(self, name: str, start: float, end: float):
        """
        Adds a filter that removes data in an interval.
        :param name: the name for the filter
        :param start: the start point for the interval
        :param end: the end point for the interval
        """
        self._add_filter(name, start, end, self.remove_filters)


    def _delete_filter(self,
                       name: str,
                       filter_list: list[Filter]):
        """
        Delete a filter with a given name from a list of filters.
        :param name: the name for the filter
        :param start: the start point of the interval
        :param end: the end point of the interval
        :param filter_list: the list of filters to add to.
        """
        for i, f in enumerate(filter_list):
            if f.name == name:
                filter_list.pop(i)
                break
        # note this is an else for the for, so only runs at end if no break
        else:
            raise RuntimeError(f"The name {name} is not present.")

    def delete_keep_filter(self, name: str):
        """
        Delete a keep data filter.
        :param name: the name of the filter to remove
        """
        self._delete_filter(name, self.keep_filters)

    def delete_remove_filter(self, name: str):
        """
        Delete a keep data filter.
        :param name: the name of the filter to remove
        """
        self._delete_filter(name, self.remove_filters)

@dataclass
class PeakProperty:
    Amplitudes: float = 0.

@dataclass
class HistogramSettings:
    min_time: float = 0.
    max_time: float = 32.768
    num_bins: int = 2048

@dataclass
class Filters:
    time_filters: TimeFilters = field(default_factory=TimeFilters)
    sample_log_filters: list[Filter] = field(default_factory=list)
    peak_property: PeakProperty = field(default_factory=PeakProperty)
    histogram_settings: HistogramSettings = (
            field(default_factory=HistogramSettings)
            )

    def write_json(self, file_name):
        """
        Save this Filters object to a JSON file.
        :param file_name: The filename to write to.
        """
        data = asdict(self)
        with open(file_name, 'w') as file:
            json.dump(data, file, ensure_ascii=False,
                      sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, file_name):
        """
        Load a Filters object from a JSON file.
        :param file_name: The filename to read from.
        :returns: A Filters object corresponding to the data.
        """
        with open(file_name, 'r') as file:
            data = json.load(file)
        return Filters(
            time_filters = TimeFilters(
                keep_filters = [Filter(**f) for f
                                in data['time_filters']['keep_filters']],
                remove_filters = [Filter(**f) for f
                                  in data['time_filters']['remove_filters']]
                ),
            sample_log_filters = [Filter(**f) for f
                                  in data['sample_log_filters']],
            peak_property = PeakProperty(**data['peak_property']),
            histogram_settings=HistogramSettings(**data['histogram_settings'])
            )


