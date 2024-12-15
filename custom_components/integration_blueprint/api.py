"""Leak Defense API Client."""

from __future__ import annotations

import socket
import uuid
from typing import Any

import aiohttp
import async_timeout

from .models import Customer, TokenResponse

import logging

_LOGGER = logging.getLogger(__name__)


class LeakDefenseApiClientError(Exception):
    """Exception to indicate a general API error."""


class LeakDefenseApiClientCommunicationError(
    LeakDefenseApiClientError,
):
    """Exception to indicate a communication error."""


class LeakDefenseApiClientAuthenticationError(
    LeakDefenseApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise LeakDefenseApiClientAuthenticationError(msg)
    response.raise_for_status()


class LeakDefenseApiClient:
    """Sample API Client."""

    _base_url: str = "https://www.catchaleak.com/mobile-hex-api/api"

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str | None = None,
        device_hash: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """
        Initialize the API Client.

        Args:
            session: An aiohttp.ClientSession instance.
            token: An optional token for authentication.
            device_hash: An optional device ID for authentication.
            username: Optional username for generating credentials.
            password: Optional password for generating credentials.

        """
        self._session = session
        self._token = token
        self._device_hash = device_hash
        self._username = username
        self._password = password
        self._device_id = str(uuid.uuid4())

    async def async_register_application(self) -> TokenResponse:
        """Register device and generate token and device ID using username and password."""
        if not self._username or not self._password:
            msg = "Username and password must be provided to register application."
            raise LeakDefenseApiClientAuthenticationError(msg)

        if self._token and self._device_id:
            data = {"token": self._token, "deviceHash": self._device_hash}
            return TokenResponse(**data)

        # Simulate a call to the API to generate token and device ID.
        response = await self._api_wrapper(
            method="post",
            endpoint="/Account/Token",
            data={
                "username": self._username,
                "password": self._password,
                "deviceId": self._device_id,
            },
        )
        self._token = response.get("token")
        self._device_hash = response.get("deviceHash")

        if not self._token or not self._device_hash:
            msg = "Failed to retrieve token and device ID."
            raise LeakDefenseApiClientAuthenticationError(msg)

        return TokenResponse(**response)

    async def async_get_data(self) -> Customer:
        """Get data from the API."""
        if not self._token or not self._device_id:
            msg = "Token and device ID must be provided."
            raise LeakDefenseApiClientAuthenticationError(msg)

        response = await self._api_wrapper(
            method="get",
            endpoint="/Customer/GetV3",
            headers={
                "deviceid": self._device_hash,
                "token": self._token,
            },
        )
        return Customer(**response.get("customer"))

    def _make_headers(self, additional_headers: dict) -> dict:
        return {
            "user-agent": "LeakDefense/6 CFNetwork/1568.200.51 Darwin/24.1.0",
            **additional_headers,
        }

    async def _api_wrapper(
        self,
        method: str,
        endpoint: str,
        headers: dict | None = None,
        data: dict | None = None,
    ) -> Any:
        """Make a request to the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=self._base_url + endpoint,
                    headers=self._make_headers(headers or {}),
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise LeakDefenseApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise LeakDefenseApiClientCommunicationError(msg) from exception
        except Exception as exception:
            msg = f"Something really wrong happened! - {exception}"
            raise LeakDefenseApiClientError(msg) from exception
