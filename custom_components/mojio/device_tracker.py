"""Support for Mojio Platform."""
import logging

from mojio_sdk.api import API
from mojio_sdk.trip import Trip
from datetime import datetime
import requests
import voluptuous as vol

from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_DOMAIN,
    CONF_PASSWORD,
    CONF_USERNAME,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_utc_time_change

_LOGGER = logging.getLogger(__name__)

CONF_INCLUDE = "include"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_DOMAIN): cv.string,
        vol.Required(CONF_CLIENT_ID): cv.string,
        vol.Required(CONF_CLIENT_SECRET): cv.string,
        vol.Optional(CONF_INCLUDE, default=[]): vol.All(cv.ensure_list, [cv.string]),
    }
)


def setup_scanner(hass, config: dict, see, discovery_info=None):
    """Set up the DeviceScanner and check if login is valid."""
    scanner = MojioDeviceScanner(config, see)
    if not scanner.login(hass):
        _LOGGER.error("Mojio authentication failed")
        return False
    return True


class MojioDeviceScanner:
    """Define a scanner for the Mojio platform."""

    def __init__(self, config, see):
        """Initialize MojioDeviceScanner."""

        self._include = config.get(CONF_INCLUDE)
        self._see = see

        self._api = API(
            config.get(CONF_DOMAIN),
            config.get(CONF_CLIENT_ID),
            config.get(CONF_CLIENT_SECRET),
            config.get(CONF_USERNAME),
            config.get(CONF_PASSWORD),
        )

    def setup(self, hass):
        """Set up a timer and start gathering devices."""
        self._refresh()
        # For testing
        # track_utc_time_change(hass, lambda now: self._refresh(), second=59)
        track_utc_time_change(hass, lambda now: self._refresh(), minute=range(0, 60, 5))

    def login(self, hass):
        """Perform a login on the Mojio API."""
        if self._api.login():
            self.setup(hass)
            return True
        return False

    def _refresh(self) -> None:
        """Refresh device information from the platform."""
        try:
            _LOGGER.info("Calling refresh: %s" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            trips = self._api.get_trips()
            vehicles = self._api.get_vehicles()
            for vehicle in vehicles:
                last_comp_trip = Trip.get_last_trip(trips, vehicle.mojio_id, True)
                if last_comp_trip.is_empty:
                    last_comp_trip = self._api.get_trip(vehicle.last_trip_id)
                car_attr = {"VIN": vehicle.getattribute("vin"),
                            "name": vehicle.getattribute("name"),
                            "parked": vehicle.getattribute("parked"),
                            "status": vehicle.getattribute("status"),
                            "direction": vehicle.getattribute("heading_direction"),
                            "left_turn": vehicle.getattribute("left_turn"),
                            "idle": vehicle.getattribute("idle"),
                            "ignition_state": vehicle.getattribute("ignition_state"),
                            "disturbance_state": vehicle.getattribute("disturbance_state"),
                            "tow_state": vehicle.getattribute("tow_state"),
                            "last_contact": vehicle.getattribute("last_contact"),
                            "last_trip_id": vehicle.getattribute("last_trip_id"),
                            "rpm": vehicle.getattribute("current_rpm", None),
                            "speed_mph": vehicle.getattribute("current_speed_mph", None),
                            "speed_kph": vehicle.getattribute("current_speed_kph", None),
                            "seatbelt_warn": vehicle.getattribute("seatbelt_status_warning", False),
                            "address": vehicle.location.getattribute("formatted_address"),
                            "battery_voltage": vehicle.battery.getattribute("value"),
                            "fuel_level": vehicle.fuel.getattribute("fuel_level", None),
                            "virtual_fuel_level": vehicle.fuel.getattribute("virtual_fuel_level", None),
                            "oil_temp_f": vehicle.engine_oil.getattribute("temp_f", None),
                            "oil_temp_c": vehicle.engine_oil.getattribute("temp_c", None),
                            "dtc_count": vehicle.dtc.getattribute("count"),
                            "dtc_details": vehicle.dtc.getattribute("details", None),
                            "lct_start": last_comp_trip.getattribute("start_date"),
                            "lct_end": last_comp_trip.getattribute("end_date"),
                            "lct_mpg": last_comp_trip.getattribute("mpg", None),
                            "lct_kpl": last_comp_trip.getattribute("kpl", None),
                            "lct_max_mph": last_comp_trip.getattribute("max_speed_mph", None),
                            "lct_max_kph": last_comp_trip.getattribute("max_speed_kph", None),
                            "lct_distance_mi": last_comp_trip.getattribute("distance_mi", None),
                            "lct_distance_km": last_comp_trip.getattribute("distance_km", None),
                            "lct_duration": last_comp_trip.getattribute("duration"), }
                self._see(
                    dev_id=vehicle.id,
                    gps=(vehicle.location.latitude, vehicle.location.longitude),
                    icon="mdi:car",
                    attributes=car_attr,
                )

        except requests.exceptions.ConnectionError:
            _LOGGER.error("ConnectionError: Could not connect to Mojio")
