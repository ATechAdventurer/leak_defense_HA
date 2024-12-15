"""Sensor platform for leak_defense."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import BlueprintDataUpdateCoordinator
from .entity import LeakDefenseEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from custom_components.integration_blueprint.models import Panel

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
    panels: list[Panel] = coordinator.data["panels"]
    entities: list[SensorEntity] = []

    for panel in panels:
        entities.append(PanelSceneSensor(coordinator, panel))
        entities.append(PanelFlowValueSensor(coordinator, panel))
        entities.append(PanelTripValueSensor(coordinator, panel))

    async_add_entities(entities)


class LeakDefenseSensor(LeakDefenseEntity, SensorEntity):
    """leak_defense Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("body")


class PanelSceneSensor(CoordinatorEntity[BlueprintDataUpdateCoordinator], SensorEntity):
    """Sensor for the panel's scene."""

    def __init__(self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel):
        """Initialize the scene sensor."""
        super().__init__(coordinator)
        self.panel = panel
        self._attr_name = f"{panel.text_identifier} Scene"
        self._attr_unique_id = f"leak_defense_{panel.id}_scene"

    @property
    def native_value(self) -> str:
        """Return the scene value."""
        return self.panel.scene


class PanelFlowValueSensor(
    CoordinatorEntity[BlueprintDataUpdateCoordinator], SensorEntity
):
    """Sensor for the panel's flow value."""

    def __init__(self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel):
        """Initialize the flow value sensor."""
        super().__init__(coordinator)
        self.panel = panel
        self._attr_name = f"{panel.text_identifier} Flow Value"
        self._attr_unique_id = f"leak_defense_{panel.id}_flow_value"
        self._attr_native_unit_of_measurement = "L/min"

    @property
    def native_value(self) -> float:
        """Return the flow value."""
        return self.panel.flow_value


class PanelTripValueSensor(
    CoordinatorEntity[BlueprintDataUpdateCoordinator], SensorEntity
):
    """Sensor for the panel's trip value."""

    def __init__(self, coordinator: BlueprintDataUpdateCoordinator, panel: Panel):
        """Initialize the trip value sensor."""
        super().__init__(coordinator)
        self.panel = panel
        self._attr_name = f"{panel.text_identifier} Trip Value"
        self._attr_unique_id = f"leak_defense_{panel.id}_trip_value"
        self._attr_native_unit_of_measurement = "L/min"

    @property
    def native_value(self) -> float:
        """Return the trip value."""
        return self.panel.trip_value
