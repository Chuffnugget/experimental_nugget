#config_flow.py
import logging
import voluptuous as vol

from homeassistant import config_entries

_LOGGER = logging.getLogger(__name__)
DOMAIN = "experimental_nugget"

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Experimental Nugget."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.debug("Entered async_step_user with user_input: %s", user_input)
        if user_input is not None:
            _LOGGER.debug("User provided input: %s", user_input)
            _LOGGER.info("Creating config entry for %s", DOMAIN)
            return self.async_create_entry(title="Experimental Nugget", data={})
        _LOGGER.debug("Showing form for async_step_user")
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
