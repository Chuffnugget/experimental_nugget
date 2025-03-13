import random
import datetime
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Random Number Sensor platform."""
    sensor = RandomNumberSensor(hass)
    async_add_entities([sensor])

class RandomNumberSensor(Entity):
    """Representation of a sensor that generates a random number every 3 seconds."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.hass = hass
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "random number"

    @property
    def state(self):
        """Return the current state of the sensor."""
        return self._state

    async def async_added_to_hass(self):
        """Set up a recurring update every 3 seconds."""
        self._update_random_number()  # Initial update
        async_track_time_interval(self.hass, self._handle_interval, datetime.timedelta(seconds=3))

    def _handle_interval(self, now):
        """Update sensor state on each interval."""
        self._update_random_number()
        self.async_write_ha_state()

    def _update_random_number(self):
        """Generate a random number between 1 and 100."""
        self._state = random.randint(1, 100)
        _LOGGER.debug("Random number updated to: %s", self._state)
