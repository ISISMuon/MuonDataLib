"""Generate the filter files used by tests."""
from MuonDataLib.data.filters import Filters, Filter, PeakProperty, TimeFilters

filter_exclude = Filters(
    time_filters = TimeFilters(
        keep_filters = [Filter('default_1', 200, 400),
                        Filter('default_2', 600, 1100)]
        )
    )

filter_include = Filters(
    time_filters = TimeFilters(
        keep_filters = [Filter('default_1', 200, 400),
                        Filter('default_2', 600, 1100)]
        )
    )

load_filter = Filters(
    time_filters = TimeFilters(
        keep_filters = [Filter('first', 0.01, 0.02),
                        Filter('second', 0.05, 0.06)]
        ),
    sample_log_filters = [Filter('Temp', 0.0044, 0.163)],
    peak_property = PeakProperty(3.14)
    )

load_bad_filter = Filters(
    time_filters = TimeFilters(
        keep_filters = [Filter('first', 0.01, 0.02),
                        Filter('second', 0.05, 0.06)],
        remove_filters = [Filter('one', 1, 2),
                          Filter('two', 5, 7)]
        ),
    sample_log_filters = [Filter('Temp', 0.0044, 0.163)],
    peak_property = PeakProperty(3.14)
    )

filter_exclude.write_json("filter_exclude.json")
filter_include.write_json("filter_include.json")
load_filter.write_json("load_filter.json")
load_bad_filter.write_json("load_bad_filter.json")
load_bad_filter.write_json("script_load_filter.json")
