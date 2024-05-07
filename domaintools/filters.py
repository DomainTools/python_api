from typing import List, Dict, Optional, Any, Callable

from domaintools.utils import convert_str_to_dateobj


class DTResultFilter:
    """Calls the given available callable filters."""

    def __init__(self, result_set, item_path: Optional[str] = "results"):
        self._result_set = result_set.get(item_path) or []

    def by(self, available_filters: List[Callable]):
        for _dt_filter in available_filters:
            self._result_set = _dt_filter(self._result_set)

        return self._result_set


class filter_by_field:
    """
    Returns the filtered result by checking if the field exits on each results.
    Can be included or excluded based on the `filter_type` param given.
    """

    def __init__(self, field: str, filter_type: str = "include"):
        self._field = field
        self._filter_type = filter_type

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results

        if self._field is None:
            return self._results

        filtered_result = []
        for result in self._results:
            result_keys = result.keys()
            lookup_field = result.get(self._field) or None

            if self._filter_type == "include":
                # for 'include' case
                # append/include the result even the key is missing or the value inside of it is empty
                if not lookup_field or lookup_field:
                    filtered_result.append(result)
                continue

            elif self._filter_type == "exclude":
                # for 'exclude' case
                # append the result ONLY when the key exists and the value inside of it has value
                if lookup_field:
                    filtered_result.append(result)

        return filtered_result


class filter_by_date_updated_after:
    """Returns the filtered result set by checking each result's 'date_updated_after' field."""

    def __init__(self, date: str):
        self._updated_after_date = date

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results

        if self._updated_after_date is None:
            # Don't do any filtering if date is not given
            return self._results

        # convert string date to datetime object before comparing
        if isinstance(self._updated_after_date, str):
            self._updated_after_date = convert_str_to_dateobj(self._updated_after_date)

        filtered_result = []
        for result in self._results:
            data_updated_timestamp = result.get("data_updated_timestamp") or None
            if not data_updated_timestamp:
                # skip uncomparable date
                continue
            data_updated_timestamp = convert_str_to_dateobj(
                data_updated_timestamp, date_format="%Y-%m-%dT%H:%M:%S.%f"
            )

            if data_updated_timestamp > self._updated_after_date:
                filtered_result.append(result)

        return filtered_result


class filter_by_expire_date:
    """
    Returns the filtered result set by checking each result's expiration date.
    Can be before or after the given date.
    """

    def __init__(self, date: str, lookup_type="before"):
        self._date = date
        self._type = lookup_type

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results

        if self._date is None:
            # Don't do any filtering if date is not given
            return self._results

        # convert string date to datetime object before comparing
        if isinstance(self._date, str):
            self._date = convert_str_to_dateobj(self._date)

        filtered_result = []
        for result in self._results:
            domain_exp_date = result.get("expiration_date", {}).get("value") or None
            if not domain_exp_date:
                # skip uncomparable date
                continue
            domain_exp_date = convert_str_to_dateobj(domain_exp_date)

            if self._type == "before":
                # check if given date is less than the expiration date
                if self._date < domain_exp_date:
                    filtered_result.append(result)
            elif self._type == "after":
                # check if given date is greather than the expiration date
                if self._date > domain_exp_date:
                    filtered_result.append(result)

        return filtered_result


class filter_by_riskscore:
    """Returns the filtered result set by a given risk score threshold."""

    def __init__(self, threshold: Optional[int] = None):
        self._threshold = threshold

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results

        if self._threshold is None:
            # Don't do any filtering if threshold is not given
            return self._results

        filtered_result = []
        for result in self._results:
            domain_risk_score = result.get("domain_risk", {}).get("risk_score")
            if domain_risk_score > self._threshold:
                filtered_result.append(result)

        return filtered_result
