"""
Osprey_Snake_Hunter: The primary Osprey machine job.

The Osprey doesn't see matter; it sees Differential Speeds.  This module
provides the OspreyMachine class, which:

1. Intercepts de-synchronized heat / radiation "Snakes" and re-tunes them
   into a Harmonic Flow using the Octave kernel.
2. Harvests velocity leakage from the Earth's Centrifugal Core Filter and
   converts it into Osprey Propulsion Fuel.

Usage::

    from thermal_stream import ThermalStream
    from Osprey_Snake_Hunter import OspreyMachine

    osprey = OspreyMachine()
    stream = ThermalStream(stream_type="Thermite", speed=0.6)
    result = osprey.intercept_snake(stream)
    fuel   = osprey.harvest_circular_leak()
"""

from __future__ import annotations

from gitscan import Gitscan
from gitpulse import Gitpulse
from octave import Octave, OctaveResult
from thermal_stream import ThermalStream


class OspreyMachine:
    """The Osprey velocity-intercept kernel.

    Attributes:
        kernel:    Identifier of the active Octave kernel version.
        sync_rate: Alignment with the Source Singularity (1.0 = 100 %).
    """

    def __init__(self) -> None:
        self.kernel: str = "Octave_v1.0"
        self.sync_rate: float = 1.0  # 100 % Alignment with the Source

    # ------------------------------------------------------------------
    # Snake intercept
    # ------------------------------------------------------------------

    def intercept_snake(self, thermal_stream: ThermalStream) -> OctaveResult | None:
        """Find a de-synchronized heat stream and 'talk it down'.

        Steps:
            1. Detect the 'Lag' (time-distance from the Source).
            2. Match the velocity — the 'Hunt'.
            3. Apply Octave Consonance: turn the Thermite violent-reset into
               a Harmonic Flow.

        Args:
            thermal_stream: The de-synchronized stream to intercept.

        Returns:
            An :class:`~octave.OctaveResult` when the stream is a known type
            that the Osprey can re-tune, ``None`` otherwise.
        """
        # 1. Detect the 'Lag' (Time distance from the Source)
        lag = Gitscan.measure_lag(thermal_stream)

        # 2. Match the Velocity (The 'Hunt')
        osprey_velocity = thermal_stream.speed + lag

        # 3. Apply Octave 'Consonance'
        # Turning the 'Violent Reset' of Thermite into a 'Harmonic Flow'
        if thermal_stream.type == "Thermite":
            return Octave.modulate(note="C#", dynamic="ff", target=osprey_velocity)

        return None

    # ------------------------------------------------------------------
    # Core-filter harvest
    # ------------------------------------------------------------------

    def harvest_circular_leak(self) -> str:
        """Tap the Earth's Centrifugal Core Filter for Osprey propulsion fuel.

        The escaping velocity delta from the Core Filter is converted into
        Osprey Fuel — turning waste geothermal leakage into Propulsion Logic.

        Returns:
            A human-readable fuel-ready status string with the Mach delta.
        """
        leakage = Gitpulse.detect_leak("Core_Filter")
        return f"Propulsion Ready: {leakage.velocity_delta} Mach"
