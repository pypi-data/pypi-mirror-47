"""Response descriptions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List

from .description import Description, Predicate
from .status import Status, merge_statuses
from .verification import Verification


@dataclass
class ResponseVerification:
    status: Status
    status_code: Verification
    body: Verification


class ResponseDescription:
    """
    When given no descriptions, then skips.
    >>> description = ResponseDescription(
    ...     status_code_predicates=[],
    ...     body_descriptions=[],
    ... )
    >>> verification = description(status_code=200, body='')
    >>> verification.status_code.status
    SKIPPED
    >>> verification.body.status
    SKIPPED
    >>> verification.status
    SKIPPED

    When given invalid body, then marks as failure.
    >>> from unittest.mock import MagicMock
    >>> description = ResponseDescription(
    ...     status_code_predicates=[
    ...         MagicMock(return_value=Verification.succeed()),
    ...     ],
    ...     body_descriptions=[
    ...         MagicMock(return_value=Verification.succeed()),
    ...     ],
    ... )
    >>> verification = description(status_code=200, body='invalid-format')
    >>> description.status_code_predicates[0].assert_called_once_with(200)
    >>> description.body_descriptions[0].assert_not_called()
    >>> verification.status
    FAILURE
    >>> verification.body.status
    FAILURE
    >>> verification.body.message
    'JSONDecodeError: Expecting value: line 1 column 1 (char 0)'

    >>> from unittest.mock import MagicMock, call
    >>> description = ResponseDescription(
    ...     status_code_predicates=[],
    ...     body_descriptions=[
    ...         MagicMock(return_value=Verification(status=Status.UNSTABLE)),
    ...         MagicMock(return_value=Verification.succeed()),
    ...     ],
    ... )
    >>> verification = description(status_code=200, body='{}')
    >>> description.body_descriptions[0].assert_called_once_with({})
    >>> description.body_descriptions[1].assert_called_once_with({})
    >>> verification.status
    UNSTABLE
    >>> verification.body.status
    UNSTABLE
    >>> verification.body.children[0].status
    UNSTABLE
    >>> verification.body.children[1].status
    SUCCESS
    """
    def __init__(
        self: ResponseDescription,
        status_code_predicates: List[Predicate],
        body_descriptions: List[Description],
    ) -> None:
        self._status_code_predicates = status_code_predicates
        self._body_descriptions = body_descriptions

    def __call__(
        self: ResponseDescription,
        status_code: int,
        body: str,
    ) -> ResponseVerification:
        status_code_verification = self._verify_status_code(status_code)
        try:
            body_verification = self._verify_body(body)
        except Exception as error:
            body_verification = Verification.of_error(error)

        status = merge_statuses(
            status_code_verification.status,
            body_verification.status,
        )
        return ResponseVerification(
            status=status,
            status_code=status_code_verification,
            body=body_verification,
        )

    @property
    def status_code_predicates(self: ResponseDescription) -> List[Predicate]:
        return self._status_code_predicates

    @property
    def body_descriptions(self: ResponseDescription) -> List[Description]:
        return self._body_descriptions

    def _verify_status_code(
        self: ResponseDescription,
        code: int,
    ) -> Verification:
        children = [pred(code) for pred in self._status_code_predicates]
        status = merge_statuses(v.status for v in children)
        return Verification(status=status, children=children)

    def _verify_body(self: ResponseDescription, body: str) -> Verification:
        if not self._body_descriptions:
            return Verification.skipped()

        data = json.loads(body)
        verifications = [
            describe(data) for describe in self._body_descriptions
        ]
        status = merge_statuses(v.status for v in verifications)
        return Verification(status=status, children=verifications)
