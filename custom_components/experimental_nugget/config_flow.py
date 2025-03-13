import voluptuous as vol

from homeassistant import config_entries

DOMAIN = "experiemtental_nugget"

class ExperimentalNuggetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Experimental Nugget."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # No options to configure; simply create the entry.
            return self.async_create_entry(title="Experimental Nugget", data={})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
