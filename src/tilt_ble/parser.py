import logging
from struct import unpack
from typing import Final

from bluetooth_sensor_state_data import BluetoothData
from habluetooth import BluetoothServiceInfo
from sensor_state_data import DeviceClass, Units

_LOGGER = logging.getLogger(__name__)


_UUID_TO_COLOR: Final = {
    0xA495BB10C5B14B44B5121370F02D74DE: "Red",
    0xA495BB20C5B14B44B5121370F02D74DE: "Green",
    0xA495BB30C5B14B44B5121370F02D74DE: "Black",
    0xA495BB40C5B14B44B5121370F02D74DE: "Purple",
    0xA495BB50C5B14B44B5121370F02D74DE: "Orange",
    0xA495BB60C5B14B44B5121370F02D74DE: "Blue",
    0xA495BB70C5B14B44B5121370F02D74DE: "Yellow",
    0xA495BB80C5B14B44B5121370F02D74DE: "Pink",
}


class TiltBluetoothDeviceData(BluetoothData):
    """Data update for Tilt Bluetooth devices"""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing Tilt BLE advertisement data: %s", service_info)

        manufacturer_data = service_info.manufacturer_data

        if not manufacturer_data:
            return

        try:
            data = manufacturer_data[76]
        except KeyError:
            _LOGGER.debug("Manufacturer ID 76 not found in data")
            return

        if data[0] != 0x02 or data[1] != 0x15:
            _LOGGER.debug("Wrong subtype or subtype length for Tilt iBeacon")
            return

        uuid = int.from_bytes(data[2:18], byteorder="big")

        try:
            color = _UUID_TO_COLOR[uuid]
        except KeyError:
            _LOGGER.debug("Not a Tilt iBeacon UUID")
            return

        self.set_device_manufacturer("Tilt")

        (major, minor, power) = unpack(">hhb", data[18:23])

        changed_manufacturer_data = self.changed_manufacturer_data(service_info)
        if not changed_manufacturer_data:
            return

        tilt_pro = minor >= 5000

        self.set_device_type(f"Pro {color}" if tilt_pro else color)
        self.set_device_name(f"Tilt Pro {color}" if tilt_pro else f"Tilt {color}")

        # up the scale rate if a tilt pro
        temp_scalar = 10 if tilt_pro else 1
        grav_scalar = 10000 if tilt_pro else 1000

        temperature = major / temp_scalar
        specific_gravity = minor / grav_scalar

        _LOGGER.debug(
            "Tilt %s data: temp=%.3f, gravity=%.3f, power=%.2f",
            color,
            temperature,
            specific_gravity,
            power,
        )

        self.update_sensor(
            key=DeviceClass.TEMPERATURE,
            device_class=DeviceClass.TEMPERATURE,
            native_unit_of_measurement=Units.TEMP_FAHRENHEIT,
            native_value=temperature,
        )
        self.update_sensor(
            key=DeviceClass.SPECIFIC_GRAVITY,
            device_class=DeviceClass.SPECIFIC_GRAVITY,
            native_unit_of_measurement=Units.SPECIFIC_GRAVITY,
            native_value=specific_gravity,
        )
        self.update_sensor(
            key=DeviceClass.SIGNAL_STRENGTH,
            device_class=DeviceClass.SIGNAL_STRENGTH,
            native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            native_value=power,
        )
