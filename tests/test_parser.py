from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import (
    DeviceClass,
    DeviceKey,
    SensorDescription,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
    Units,
)

from tilt_ble.parser import TiltBluetoothDeviceData


def test_can_create():
    TiltBluetoothDeviceData()


def test_standard():
    parser = TiltBluetoothDeviceData()
    service_info = BluetoothServiceInfo(
        name="aa-bb-cc-dd-ee-ff",
        manufacturer_data={
            76: b"\x02\x15\xa4\x95\xbb \xc5\xb1KD\xb5\x12\x13p\xf0-t\xde\x00@\x04\x1cP"
        },
        service_uuids=[],
        address="aa:bb:cc:dd:ee:ff",
        rssi=-60,
        service_data={},
        source="local",
    )
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="Tilt Green",
                model="Green",
                manufacturer="Tilt",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="specific_gravity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="specific_gravity", device_id=None),
                device_class=DeviceClass.SPECIFIC_GRAVITY,
                native_unit_of_measurement=Units.SPECIFIC_GRAVITY,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_FAHRENHEIT,
            ),
        },
        entity_values={
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-60,
            ),
            DeviceKey(key="specific_gravity", device_id=None): SensorValue(
                device_key=DeviceKey(key="specific_gravity", device_id=None),
                name="Specific Gravity",
                native_value=1.052,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=64,
            ),
        },
    )


def test_pro():
    parser = TiltBluetoothDeviceData()
    service_info = BluetoothServiceInfo(
        name="aa-bb-cc-dd-ee-ff",
        manufacturer_data={
            76: (
                b"\x02\x15\xa4\x95\xbb\x30\xc5\xb1\x4b\x44\xb5\x12\x13\x70\xf0\x2d\x74"
                b"\xde\x02\x0e\x29\x05\xc5"
            )
        },
        service_uuids=[],
        address="aa:bb:cc:dd:ee:ff",
        rssi=-60,
        service_data={},
        source="local",
    )
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="Tilt Pro Black",
                model="Pro Black",
                manufacturer="Tilt",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="specific_gravity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="specific_gravity", device_id=None),
                device_class=DeviceClass.SPECIFIC_GRAVITY,
                native_unit_of_measurement=Units.SPECIFIC_GRAVITY,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_FAHRENHEIT,
            ),
        },
        entity_values={
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-60,
            ),
            DeviceKey(key="specific_gravity", device_id=None): SensorValue(
                device_key=DeviceKey(key="specific_gravity", device_id=None),
                name="Specific Gravity",
                native_value=1.0501,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=52.6,
            ),
        },
    )
