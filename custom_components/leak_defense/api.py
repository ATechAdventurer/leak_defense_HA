"""Leak Defense API Client."""

from __future__ import annotations

import logging
import socket
import uuid
from typing import Any

import aiohttp
import async_timeout

from .models import (
    CommandSetScene,
    Customer,
    HexRequest,
    LegacyRequest,
    SceneEnum,
    TokenResponse,
)

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
    """Leak Defense API Client."""

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
        """Register device with the API."""
        if not self._username or not self._password:
            msg = "Username and password must be provided to register application."
            raise LeakDefenseApiClientAuthenticationError(msg)

        if self._token and self._device_id:
            data = {"token": self._token, "device_hash": self._device_hash}
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

    async def async_send_scene(self, scene: SceneEnum, panel_id: int) -> None:
        """Send a scene to the API."""
        if not self._token or not self._device_id:
            msg = "Token and device ID must be provided."
            raise LeakDefenseApiClientAuthenticationError(msg)

        _LOGGER.info("Sending scene to the API.")

        customer = await self.async_get_data()

        # Get the panel with the specified ID

        current_panel = next(
            (panel for panel in customer.panels if panel.id == panel_id),
            None,
        )

        if not current_panel:
            msg = f"Panel with ID {panel_id} not found."
            raise LeakDefenseApiClientError(msg)

        scene_payload = CommandSetScene(
            ApiSource=2,
            ReturnPanelVM=True,
            LegacyRequest=LegacyRequest(
                id=panel_id,
                mode=scene,
                tripTime=str(int(current_panel.countdown_timer)),
                tripVal=str(int(current_panel.trip_value)),
                waterOff=not current_panel.water_on,
                clearAlarm=False,
            ),
            HexRequest=HexRequest(Scene=None, value=None),
        )
        _LOGGER.log(msg=scene_payload.model_dump_json(), level=logging.INFO)
        await self._api_wrapper(
            method="post",
            endpoint="/Command/SetScene",
            headers={
                "deviceid": self._device_hash,
                "token": self._token,
            },
            data=scene_payload.model_dump(),
        )

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
