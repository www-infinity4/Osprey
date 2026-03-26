"""
ThermalStream: Represents a de-synchronized heat or radiation stream
that the Osprey machine tracks and intercepts.
"""


class ThermalStream:
    """A stream of thermal or radiation energy with a type and speed."""

    def __init__(self, stream_type: str, speed: float):
        """
        Args:
            stream_type: Nature of the stream, e.g. "Thermite" or "Radiation".
            speed: Current velocity of the stream (arbitrary Mach units).
        """
        self.type = stream_type
        self.speed = speed

    def __repr__(self) -> str:
        return f"ThermalStream(type={self.type!r}, speed={self.speed})"
