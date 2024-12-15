"""Custom types for leak_defense."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import LeakDefenseApiClient
    from .coordinator import BlueprintDataUpdateCoordinator


type LeakDefenseConfigEntry = ConfigEntry[LeakDefenseData]


@dataclass
class LeakDefenseData:
    """Data for the Blueprint integration."""

    client: LeakDefenseApiClient
    coordinator: BlueprintDataUpdateCoordinator
    integration: Integration
