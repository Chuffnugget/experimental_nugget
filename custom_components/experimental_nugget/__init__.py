#__init__.py
"""Initialize the experimental_nugget integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)
DOMAIN = "experimental_nugget"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration from configuration.yaml (if any)."""
    _LOGGER.debug("Setting up %s from configuration.yaml", DOMAIN)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry."""
    _LOGGER.debug("Setting up config entry %s for %s", entry.entry_id, DOMAIN)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.debug("Unloading config entry %s for %s", entry.entry_id, DOMAIN)
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
