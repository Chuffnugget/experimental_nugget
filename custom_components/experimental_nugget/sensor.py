# sensor.py
# This file creates a sensor entity for the experiemtental_nugget integration.
# It generates a random number between 1 and 100 every 3 seconds using a dedicated async thread.
# The sensor is tied to the Experimental Nugget device entry.

import asyncio
import random
import logging
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
DOMAIN = "experiemtental_nugget"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor platform from a config entry."""
    sensor = RandomNumberSensor(hass)
    async_add_entities([sensor])

class RandomNumberSensor(Entity):
    """Representation of a sensor that generates a random number every 3 seconds using a dedicated async thread."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.hass = hass
        self._state = None
        self._update_task = None

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
        """Return device information to tie this entity to your integration."""
        return {
            "identifiers": {(DOMAIN, "unique_random_number_sensor")},
            "name": "Experimental Nugget Sensor",
            "manufacturer": "Chuffnugget",
            "model": "Random Number Sensor",
        }

    async def async_added_to_hass(self):
        """Start the dedicated update loop when the entity is added."""
        self._update_task = self.hass.async_create_task(self._update_loop())

    async def _update_loop(self):
        """Continuously update the sensor every 3 seconds."""
        while True:
            try:
                await asyncio.sleep(3)
            except asyncio.CancelledError:
                break
            self._update_random_number()
            self.async_write_ha_state()

    def _update_random_number(self):
        """Generate a random number between 1 and 100."""
        self._state = random.randint(1, 100)
        _LOGGER.debug("Random number updated to: %s", self._state)

    async def async_will_remove_from_hass(self):
        """Cancel the update task when removing the entity."""
        if self._update_task is not None:
            self._update_task.cancel()
            try:
                await self._update_task
            except asyncio.CancelledError:
                pass
