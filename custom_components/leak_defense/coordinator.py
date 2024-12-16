"""DataUpdateCoordinator for leak_defense."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, TypedDict

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    LeakDefenseApiClientAuthenticationError,
    LeakDefenseApiClientError,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import LeakDefenseConfigEntry
    from .models import Panel


class CoordinatorData(TypedDict):
    """Coordinator data."""

    panels: dict[int, Panel]


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
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self) -> CoordinatorData:
        """Update data via library."""
        try:
            customer_data = await self.config_entry.runtime_data.client.async_get_data()
        except LeakDefenseApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except LeakDefenseApiClientError as exception:
            raise UpdateFailed(exception) from exception

        # Transform list of panels to a dictionary with panel ID as key
        panels_dict = {panel.id: panel for panel in customer_data.panels}
        return {"panels": panels_dict}
