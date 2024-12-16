"""Binary sensor platform for leak_defense."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from custom_components.leak_defense.entity import LeakDefenseEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import LeakDefenseConfigEntry
    from .models import Panel

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="leak_defense",
        name="Leak Defense Binary Sensor",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


class WaterValveEntity(LeakDefenseEntity, BinarySensorEntity):
    """Entity for a water valve device."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, inital_panel: Panel
    ) -> None:
        """Initialize the water valve entity."""
        super().__init__(coordinator, panel=inital_panel)
        self.panel: Panel = inital_panel
        self._attr_name: str = f"{inital_panel.text_identifier} Water Valve"
        self._attr_unique_id: str = f"leak_defense_{inital_panel.id}"

    @property
    def is_on(self) -> bool:
        """Return the state of the water valve (water is on)."""
        updated_panel = self.coordinator.data["panels"].get(self.panel.id)
        # Return the trip value or a default value if the panel is not found
        return updated_panel.water_on if updated_panel else False

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


class PanelTooColdEntity(LeakDefenseEntity, BinarySensorEntity):
    """Binary sensor for panel too cold status."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, inital_panel: Panel
    ) -> None:
        """Initialize the too cold binary sensor."""
        super().__init__(coordinator, panel=inital_panel)
        self.panel = inital_panel
        self._attr_name = f"{inital_panel.text_identifier} Too Cold"
        self._attr_unique_id = f"leak_defense_{inital_panel.id}_too_cold"

    @property
    def is_on(self) -> bool:
        """Return True if the panel is too cold."""
        updated_panel = self.coordinator.data["panels"].get(self.panel.id)
        # Return the trip value or a default value if the panel is not found
        return updated_panel.too_cold if updated_panel else False


class PanelOfflineEntity(LeakDefenseEntity, BinarySensorEntity):
    """Binary sensor for panel offline status."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, inital_panel: Panel
    ) -> None:
        """Initialize the offline binary sensor."""
        super().__init__(coordinator, panel=inital_panel)
        self.panel = inital_panel
        self._attr_name = f"{inital_panel.text_identifier} Offline"
        self._attr_unique_id = f"leak_defense_{inital_panel.id}_offline"

    @property
    def is_on(self) -> bool:
        """Return True if the panel is offline."""
        updated_panel = self.coordinator.data["panels"].get(self.panel.id)
        # Return the trip value or a default value if the panel is not found
        return updated_panel.offline if updated_panel else False


class PanelInAlarmEntity(LeakDefenseEntity, BinarySensorEntity):
    """Binary sensor for panel in alarm status."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, inital_panel: Panel
    ) -> None:
        """Initialize the in alarm binary sensor."""
        super().__init__(coordinator, panel=inital_panel)
        self.panel = inital_panel
        self._attr_name = f"{inital_panel.text_identifier} In Alarm"
        self._attr_unique_id = f"leak_defense_{inital_panel.id}_in_alarm"

    @property
    def is_on(self) -> bool:
        """Return True if the panel is in alarm."""
        updated_panel = self.coordinator.data["panels"].get(self.panel.id)
        # Return the trip value or a default value if the panel is not found
        return updated_panel.in_alarm if updated_panel else False


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: LeakDefenseConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the water valve entities."""
    coordinator: BlueprintDataUpdateCoordinator = entry.runtime_data.coordinator

    # Ensure initial data fetch
    await coordinator.async_config_entry_first_refresh()

    # Create entities for each panel
    entities: list[BinarySensorEntity] = []

    for panel in coordinator.data["panels"].values():
        entities.append(WaterValveEntity(coordinator, panel))
        entities.append(PanelTooColdEntity(coordinator, panel))
        entities.append(PanelOfflineEntity(coordinator, panel))
        entities.append(PanelInAlarmEntity(coordinator, panel))

    async_add_entities(entities)
