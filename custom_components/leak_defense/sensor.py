"""Sensor platform for leak_defense."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import LeakDefenseEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from custom_components.leak_defense.models import Panel

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import LeakDefenseConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="leak_defense",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: LeakDefenseConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities."""
    coordinator: BlueprintDataUpdateCoordinator = entry.runtime_data.coordinator

    # Ensure initial data fetch
    await coordinator.async_config_entry_first_refresh()

    # Create entities for each panel
    entities: list[SensorEntity] = []

    for panel in coordinator.data["panels"].values():
        entities.append(PanelSceneSensor(coordinator, panel))
        entities.append(PanelFlowValueSensor(coordinator, panel))
        entities.append(PanelTripValueSensor(coordinator, panel))

    async_add_entities(entities)


class PanelSceneSensor(LeakDefenseEntity, SensorEntity):
    """Sensor for the panel's scene."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, inital_panel: Panel
    ) -> None:
        """Initialize the scene sensor."""
        super().__init__(coordinator, inital_panel)
        self.panel = inital_panel
        self._attr_name = f"{inital_panel.text_identifier} Scene"
        self._attr_unique_id = f"leak_defense_{inital_panel.id}_scene"

    @property
    def native_value(self) -> str:
        """Return the scene value."""
        updated_panel = self.coordinator.data["panels"].get(self.panel.id)

        return updated_panel.scene if updated_panel else "Unknown"


class PanelFlowValueSensor(LeakDefenseEntity, SensorEntity):
    """Sensor for the panel's flow value."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, inital_panel: Panel
    ) -> None:
        """Initialize the flow value sensor."""
        super().__init__(coordinator, panel=inital_panel)
        self.panel = inital_panel
        self._attr_name = f"{inital_panel.text_identifier} Flow Value"
        self._attr_unique_id = f"leak_defense_{inital_panel.id}_flow_value"
        self._attr_native_unit_of_measurement = "L/min"

    @property
    def native_value(self) -> float:
        """Return the flow value."""
        updated_panel = self.coordinator.data["panels"].get(self.panel.id)
        return updated_panel.flow_value if updated_panel else float("nan")


class PanelTripValueSensor(LeakDefenseEntity, SensorEntity):
    """Sensor for the panel's trip value."""

    def __init__(
        self, coordinator: BlueprintDataUpdateCoordinator, inital_panel: Panel
    ) -> None:
        """Initialize the trip value sensor."""
        super().__init__(coordinator, panel=inital_panel)
        self.panel = inital_panel
        self._attr_name = f"{inital_panel.text_identifier} Trip Value"
        self._attr_unique_id = f"leak_defense_{inital_panel.id}_trip_value"
        self._attr_native_unit_of_measurement = "L/min"

    @property
    def native_value(self) -> float:
        """Return the trip value."""
        updated_panel = self.coordinator.data["panels"].get(self.panel.id)
        return updated_panel.trip_value if updated_panel else float("nan")
