"""
Leak Defense Integration
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.const import ATTR_ENTITY_ID, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from custom_components.leak_defense.models import SceneEnum

from .api import LeakDefenseApiClient
from .const import DOMAIN, LOGGER
from .coordinator import BlueprintDataUpdateCoordinator
from .data import LeakDefenseData

if TYPE_CHECKING:
    from homeassistant.core import ServiceCall
    from homeassistant.core import HomeAssistant

    from .data import LeakDefenseConfigEntry


PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: LeakDefenseConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = BlueprintDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = LeakDefenseData(
        client=LeakDefenseApiClient(
            token=entry.data["token"],
            device_hash=entry.data["device_hash"],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_set_scene(call: ServiceCall) -> None:
        """Handle setting scene."""
        device_id = call.data["device_id"]
        scene = call.data["scene"]

        device_registry = dr.async_get(hass)
        device = device_registry.async_get(device_id)

        if not device:
            raise ValueError(f"Device {device_id} not found")

        # Get the panel_id from the device identifier
        panel_id = next(
            (id_ for domain, id_ in device.identifiers if domain == DOMAIN),
            None,
        )

        if not panel_id:
            raise ValueError(f"No panel ID found for device {device_id}")

        # Send the scene command
        await entry.runtime_data.client.async_send_scene(
            scene=scene,
            panel_id=int(panel_id),
        )
        await entry.runtime_data.coordinator.async_request_refresh()

    # Register the service with schema validation
    service_schema = vol.Schema(
        {
            vol.Required("device_id"): str,
            vol.Required("scene"): vol.In([scene.value for scene in SceneEnum]),
        }
    )

    hass.services.async_register(
        DOMAIN,
        "set_scene",
        async_set_scene,
        schema=service_schema,
    )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: LeakDefenseConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: LeakDefenseConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
