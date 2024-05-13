import unittest

from domaintools.filters import (
    DTResultFilter,
    filter_by_riskscore,
    filter_by_expire_date,
    filter_by_date_updated_after,
    filter_by_field,
)
from tests.responses import iris_investigate_data


class DTFiltersTest(unittest.TestCase):

    def setUp(self):
        domaintools_iris_result = iris_investigate_data.domaintools()
        int_chase_iris_result = iris_investigate_data.int_chase()

        test_results = {
            "results": domaintools_iris_result["results"]
            + int_chase_iris_result["results"]
        }

        self.dt_res_filter = DTResultFilter(result_set=test_results)

    def test_filter_by_riskscore(self):
        """Test domaintools filter by riskcore"""
        risk_score = 69

        result = self.dt_res_filter.by(
            [
                filter_by_riskscore(threshold=risk_score),
            ]
        )

        assert len(result) == 1
        assert result[0]["domain"] == "int-chase.com"

    def test_filter_younger_than_expire_date(self):
        """Test filter result younger than the expire date"""
        younger_than = "2024-02-24"
        younger_than_result = self.dt_res_filter.by(
            [
                filter_by_expire_date(younger_than, lookup_type="before"),
            ]
        )

        assert len(younger_than_result) == 1
        assert younger_than_result[0]["domain"] == "domaintools.com"

    def test_filter_older_than_expire_date(self):
        """Test filter result older than the expire date"""
        older_than = "2024-03-24"
        older_than_result = self.dt_res_filter.by(
            [
                filter_by_expire_date(older_than, lookup_type="after"),
            ]
        )

        assert len(older_than_result) == 1
        assert older_than_result[0]["domain"] == "int-chase.com"

    def test_filter_by_date_updated_after(self):
        """Test filter result by the date updated after"""
        updated_after = "2023-07-24"
        updated_after_result = self.dt_res_filter.by(
            [
                filter_by_date_updated_after(date=updated_after),
            ]
        )

        assert len(updated_after_result) == 1
        assert updated_after_result[0]["domain"] == "int-chase.com"

    def test_filter_by_field_include_mode(self):
        include_domains_with_missing_field = "ga4"

        results = self.dt_res_filter.by(
            [
                filter_by_field(
                    field=include_domains_with_missing_field, filter_type="include"
                ),
            ]
        )

        assert len(results) == 2

    def test_filter_by_field_exclude_mode(self):
        exclude_domains_with_missing_field = "ga4"

        results = self.dt_res_filter.by(
            [
                filter_by_field(
                    field=exclude_domains_with_missing_field, filter_type="exclude"
                ),
            ]
        )

        assert len(results) == 1
        assert results[0]["domain"] == "int-chase.com"
