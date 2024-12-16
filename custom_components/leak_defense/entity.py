"""BlueprintEntity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import BlueprintDataUpdateCoordinator

if TYPE_CHECKING:
    from .models import Panel


class LeakDefenseEntity(CoordinatorEntity[BlueprintDataUpdateCoordinator]):
    """BlueprintEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.panel = panel
        self._attr_unique_id = f"leak_defense_{panel.id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(panel.id))},
            name=f"Panel {panel.text_identifier}",
            manufacturer="Leak Defense",
            model="Water Panel",
            sw_version="1.0",
        )
