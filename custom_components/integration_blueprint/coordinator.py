"""DataUpdateCoordinator for leak_defense."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, TypedDict

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.integration_blueprint.models import Customer

from .api import (
    LeakDefenseApiClientAuthenticationError,
    LeakDefenseApiClientError,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from custom_components.integration_blueprint.models import Panel

    from .data import LeakDefenseConfigEntry


class CoordinatorData(TypedDict):
    panels: list[Panel]


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class BlueprintDataUpdateCoordinator(DataUpdateCoordinator[CoordinatorData]):
    """Class to manage fetching data from the API."""

    config_entry: LeakDefenseConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=1),
        )

    async def _async_update_data(self) -> CoordinatorData:
        """Update data via library."""
        try:
            customer_data = await self.config_entry.runtime_data.client.async_get_data()
        except LeakDefenseApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except LeakDefenseApiClientError as exception:
            raise UpdateFailed(exception) from exception

        # Extract relevant panel data
        panels = customer_data.panels  # List of Panel objects
        return {"panels": panels}
