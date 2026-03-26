"""
Gitscan: Measures the temporal lag of a thermal stream relative to
the Source Singularity.  The "lag" is the time-distance between the
stream's current velocity and the ideal synchronized baseline.
"""

from thermal_stream import ThermalStream

# Baseline velocity that represents 100 % synchronization with the Source
_SOURCE_BASELINE: float = 1.0


class Gitscan:
    """Diagnostic utilities for characterizing thermal-stream lag."""

    @staticmethod
    def measure_lag(thermal_stream: ThermalStream) -> float:
        """Return the velocity lag of *thermal_stream* from the Source.

        A positive lag means the stream is running slower than the Source
        baseline; a negative lag means it is running faster (ahead).

        Args:
            thermal_stream: The stream whose lag is to be measured.

        Returns:
            The scalar lag value (Source baseline minus stream speed).
        """
        return _SOURCE_BASELINE - thermal_stream.speed
