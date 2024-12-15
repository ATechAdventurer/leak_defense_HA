"""Binary sensor platform for leak_defense."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import BlueprintDataUpdateCoordinator
from .models import Panel

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import LeakDefenseConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="leak_defense",
        name="Leak Defense Binary Sensor",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


class WaterValveEntity(
    CoordinatorEntity[BlueprintDataUpdateCoordinator], BinarySensorEntity
):
    """Entity for a water valve device."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel
    ) -> None:
        """Initialize the water valve entity."""
        super().__init__(coordinator)
        self.panel: Panel = panel
        self._attr_name: str = f"{panel.text_identifier} Water Valve"
        self._attr_unique_id: str = f"leak_defense_{panel.id}"

    @property
    def is_on(self) -> bool:
        """Return the state of the water valve (water is on)."""
        return self.panel.water_on

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes for the water valve."""
        return {
            "offline": self.panel.offline,
            "too_cold": self.panel.too_cold,
            "scene": self.panel.scene,
            "flow_value": self.panel.flow_value,
            "trip_value": self.panel.trip_value,
            "in_alarm": self.panel.in_alarm,
        }


class PanelTooColdEntity(
    CoordinatorEntity[BlueprintDataUpdateCoordinator], BinarySensorEntity
):
    """Binary sensor for panel too cold status."""

    def __init__(self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel):
        """Initialize the too cold binary sensor."""
        super().__init__(coordinator)
        self.panel = panel
        self._attr_name = f"{panel.text_identifier} Too Cold"
        self._attr_unique_id = f"leak_defense_{panel.id}_too_cold"

    @property
    def is_on(self) -> bool:
        """Return True if the panel is too cold."""
        return self.panel.too_cold


class PanelOfflineEntity(
    CoordinatorEntity[BlueprintDataUpdateCoordinator], BinarySensorEntity
):
    """Binary sensor for panel offline status."""

    def __init__(self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel):
        """Initialize the offline binary sensor."""
        super().__init__(coordinator)
        self.panel = panel
        self._attr_name = f"{panel.text_identifier} Offline"
        self._attr_unique_id = f"leak_defense_{panel.id}_offline"

    @property
    def is_on(self) -> bool:
        """Return True if the panel is offline."""
        return self.panel.offline


class PanelInAlarmEntity(
    CoordinatorEntity[BlueprintDataUpdateCoordinator], BinarySensorEntity
):
    """Binary sensor for panel in alarm status."""

    def __init__(self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel):
        """Initialize the in alarm binary sensor."""
        super().__init__(coordinator)
        self.panel = panel
        self._attr_name = f"{panel.text_identifier} In Alarm"
        self._attr_unique_id = f"leak_defense_{panel.id}_in_alarm"

    @property
    def is_on(self) -> bool:
        """Return True if the panel is in alarm."""
        return self.panel.in_alarm


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LeakDefenseConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the water valve entities."""
    coordinator: BlueprintDataUpdateCoordinator = entry.runtime_data.coordinator

    # Ensure initial data fetch
    await coordinator.async_config_entry_first_refresh()

    # Create entities for each panel
    panels: list[Panel] = coordinator.data["panels"]
    entities: list[BinarySensorEntity] = []

    for panel in panels:
        entities.append(WaterValveEntity(coordinator, panel))
        entities.append(PanelTooColdEntity(coordinator, panel))
        entities.append(PanelOfflineEntity(coordinator, panel))
        entities.append(PanelInAlarmEntity(coordinator, panel))

    async_add_entities(entities)
