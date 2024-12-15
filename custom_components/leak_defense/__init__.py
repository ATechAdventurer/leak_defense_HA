"""
Leak Defense Integration
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.const import Platform
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import SelectSelectorMode
from homeassistant.loader import async_get_loaded_integration

from custom_components.leak_defense.models import SceneEnum

from .api import LeakDefenseApiClient
from .const import DOMAIN, LOGGER
from .coordinator import BlueprintDataUpdateCoordinator
from .data import LeakDefenseData

if TYPE_CHECKING:
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

    # Register the service
    async def async_set_panel_state(call) -> None:
        """Handle the service call to set the panel state."""
        device_id = call.data.get("device_id")
        state = call.data.get("state")

        # Map the device_id to panel_id
        dev_reg = dr.async_get(hass)
        device = dev_reg.async_get(device_id)
        if not device:
            msg = f"Device {device_id} not found"
            raise ValueError(msg)

        panel_id = next(
            (id_ for domain, id_ in device.identifiers if domain == DOMAIN),
            None,
        )
        if not panel_id:
            msg = f"No panel ID found for device {device_id}"
            raise ValueError(msg)

        try:
            await entry.runtime_data.client.async_send_scene(
                scene=state,
                panel_id=int(panel_id),
            )
            await coordinator.async_request_refresh()
        except Exception as err:
            LOGGER.exception(f"Failed to set panel state: {err}")
            raise

    hass.services.async_register(
        domain=DOMAIN,
        service="set_panel_state",
        schema=vol.Schema(
            {
                vol.Required("device_id"): selector.DeviceSelector(
                    selector.DeviceSelectorConfig(integration=DOMAIN)
                ),
                vol.Required("state"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[SceneEnum.HOME, SceneEnum.AWAY, SceneEnum.STANDBY],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        ),
        service_func=async_set_panel_state,
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
