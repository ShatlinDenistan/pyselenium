"""UI automation tests for the Request Demo page"""
import pytest
from pages.codegen_page import CodeGenPage
from pages.home_page import HomePage


@pytest.mark.regression
class TestWalkNodes:
    """UI automation tests for the Request Demo page"""

    @pytest.mark.set1
    @pytest.mark.parametrize(
        "index",
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
        ],
    )
    def test_walk_set1(self, index):
        self._execute(index)

    @pytest.mark.set2
    @pytest.mark.parametrize(
        "index",
        [
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
        ],
    )
    def test_walk_set_2(self, index):
        self._execute(index)

    def _execute(self, index):
        home_page = HomePage(self.driver)
        assert home_page.is_in_home_page()
        home_page.perform_tree_walk(index)

