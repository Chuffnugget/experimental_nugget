# sensor.py
# This file creates a sensor entity for the experimental_nugget integration.
# It generates a random number between 1 and 100 every 3 seconds using a dedicated async thread.
# The sensor is tied to the Experimental Nugget device entry.

import asyncio
import random
import logging
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
DOMAIN = "experimental_nugget"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor platform from a config entry."""
    _LOGGER.debug("Setting up sensor platform for config entry %s", entry.entry_id)
    sensor = RandomNumberSensor(hass, entry)
    async_add_entities([sensor])

class RandomNumberSensor(Entity):
    """Representation of a sensor that generates a random number every 3 seconds using a dedicated async thread."""

    def __init__(self, hass, entry):
        """Initialize the sensor with the config entry."""
        self.hass = hass
        self._entry = entry
        self._state = None
        self._update_task = None
        _LOGGER.debug("Initializing RandomNumberSensor with entry_id: %s", self._entry.entry_id)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "random number"

    @property
    def state(self):
        """Return the current state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return device information to tie this entity to your integration.
        
        Using the config entry's unique entry_id ensures the sensor is attached to the
        Experimental Nugget device in the UI.
        """
        device_info = {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Experimental Nugget",
            "manufacturer": "Chuffnugget",
            "model": "Random Number Sensor",
        }
        _LOGGER.debug("device_info: %s", device_info)
        return device_info

    async def async_added_to_hass(self):
        """Start the dedicated update loop when the entity is added."""
        _LOGGER.debug("Adding sensor entity with entry_id: %s", self._entry.entry_id)
        self._update_task = self.hass.async_create_task(self._update_loop())

    async def _update_loop(self):
        """Continuously update the sensor every 3 seconds."""
        _LOGGER.debug("Starting update loop for sensor with entry_id: %s", self._entry.entry_id)
        while True:
            try:
                await asyncio.sleep(3)
            except asyncio.CancelledError:
                _LOGGER.debug("Update loop cancelled for sensor with entry_id: %s", self._entry.entry_id)
                break
            self._update_random_number()
            self.async_write_ha_state()

    def _update_random_number(self):
        """Generate a random number between 1 and 100."""
        self._state = random.randint(1, 100)
        _LOGGER.debug("Random number updated to: %s", self._state)

    async def async_will_remove_from_hass(self):
        """Cancel the update task when removing the entity."""
        _LOGGER.debug("Removing sensor entity with entry_id: %s", self._entry.entry_id)
        if self._update_task is not None:
            self._update_task.cancel()
            try:
                await self._update_task
            except asyncio.CancelledError:
                _LOGGER.debug("Update task cancelled successfully for sensor with entry_id: %s", self._entry.entry_id)
