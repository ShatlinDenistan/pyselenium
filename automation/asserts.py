import re


class Verify:
    def should_not_be_true(self, condition, msg=None):
        if condition:
            raise AssertionError(msg or f"'{condition}' should not be true.")

    def should_be_true(self, condition, msg=None):
        if not condition:
            raise AssertionError(msg or f"'{condition}' should be true.")

    def _fix_inputs(
        self,
        first,
        second,
        ignore_case=False,
        strip_spaces=False,
        collapse_spaces=False,
    ):
        if not isinstance(first, str) or not isinstance(second, str):
            return first, second
        if ignore_case:
            first = first.lower()
            second = second.lower()
        if strip_spaces:
            first = first.replace(" ", "")
            second = second.replace(" ", "")
        if collapse_spaces:
            first = self._collapse_spaces(first)
            second = self._collapse_spaces(second)
        return first, second

    def should_be_equal(
        self,
        first,
        second,
        msg=None,
        ignore_case=False,
        strip_spaces=False,
        collapse_spaces=False,
    ):
        first, second = self._fix_inputs(
            first, second, ignore_case, strip_spaces, collapse_spaces
        )
        if first != second:
            raise AssertionError(msg or f"'{first}' and '{second}' should be equal.")

    def _collapse_spaces(self, value):
        return re.sub(r"\s+", " ", value) if isinstance(value, str) else value

    def should_not_be_equal(
        self,
        first,
        second,
        msg=None,
        ignore_case=False,
        strip_spaces=False,
        collapse_spaces=False,
    ):
        first, second = self._fix_inputs(
            first, second, ignore_case, strip_spaces, collapse_spaces
        )
        if first == second:
            raise AssertionError(
                msg or f"'{first}' and '{second}' should not be equal."
            )

    def should_not_start_with(
        self,
        first,
        second,
        msg=None,
        ignore_case=False,
        strip_spaces=False,
        collapse_spaces=False,
    ):
        first, second = self._fix_inputs(
            first, second, ignore_case, strip_spaces, collapse_spaces
        )
        if first.startswith(second):
            raise AssertionError(msg or f"'{first}' should not start with '{second}'")

    def should_start_with(
        self,
        first,
        second,
        msg=None,
        ignore_case=False,
        strip_spaces=False,
        collapse_spaces=False,
    ):
        first, second = self._fix_inputs(
            first, second, ignore_case, strip_spaces, collapse_spaces
        )
        if not first.startswith(second):
            raise AssertionError(msg or f"'{first}' should start with '{second}'")

    def should_not_end_with(
        self,
        first,
        second,
        msg=None,
        ignore_case=False,
        strip_spaces=False,
        collapse_spaces=False,
    ):
        first, second = self._fix_inputs(
            first, second, ignore_case, strip_spaces, collapse_spaces
        )
        if first.endswith(second):
            raise AssertionError(msg or f"'{first}' should not end with '{second}'")

    def should_end_with(
        self,
        first,
        second,
        msg=None,
        ignore_case=False,
        strip_spaces=False,
        collapse_spaces=False,
    ):
        first, second = self._fix_inputs(
            first, second, ignore_case, strip_spaces, collapse_spaces
        )
        if not first.endswith(second):
            raise AssertionError(msg or f"'{first}' should end with '{second}'")

    def should_not_contain(
        self,
        container,
        item,
        msg=None,
    ):
        if item in container:
            raise AssertionError(msg or f"'{container}' should not contain'{item}'")

    def should_contain(
        self,
        container,
        item,
        msg=None,
    ):
        if item not in container:
            raise AssertionError(msg or f"'{container}' should contain'{item}'")

    def should_be_empty(self, item, msg=None):
        if len(item) > 0:
            raise AssertionError(msg or f"'{item}' should be empty.")

    def should_not_be_empty(self, item, msg=None):
        if len(item) == 0:
            raise AssertionError(msg or f"'{item}' should not be empty.")
