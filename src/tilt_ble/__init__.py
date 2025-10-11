"""Parser for Inkbird BLE advertisements."""

from __future__ import annotations

from sensor_state_data import (
    DeviceClass,
    DeviceKey,
    SensorDescription,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
    Units,
)

from .parser import TiltBluetoothDeviceData

__version__ = "1.0.0"

__all__ = [
    "DeviceClass",
    "DeviceKey",
    "SensorDescription",
    "SensorDeviceInfo",
    "SensorUpdate",
    "SensorValue",
    "TiltBluetoothDeviceData",
    "Units",
]
