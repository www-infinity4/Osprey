"""
osprey_engine: The Osprey's Bimodal Thermite Hybrid Engine.

The Osprey uses two thermite fuel profiles that mirror the ThermalStream
types already tracked by the kernel:

* **MicroThermite** — "Slow Burn."  Used for long-distance, low-intensity
  travel between nodes.  Its stream signature looks static and deliberate;
  it maps to the low-energy "Yellow" band.

* **NanoThermite** — "Explosive Propellant."  Used for high-speed snake
  intercepts.  Its stream signature is fast, high-potency, and uniquely
  pressurized; it maps to the high-energy "Purple" band.

The :class:`BimodalEngine` combines both profiles into a Hybrid Engine that
ignites fast (Nano) but sustains long enough (Micro) to cross the Distance
Gap between nodes.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class FuelProfile(str, Enum):
    """Fuel burn profile for an Osprey engine stage."""
    MICRO = "MicroThermite"   # Slow-burn, long-distance
    NANO = "NanoThermite"     # Fast intercept, high-potency


@dataclass
class ThermiteStage:
    """A single combustion stage in the Osprey engine.

    Attributes:
        profile:     Whether this is a Micro or Nano stage.
        burn_rate:   Fraction of fuel consumed per tick (0.0 – 1.0).
        velocity:    Current velocity output of this stage in Mach units.
        stream_color: Optical frequency signature of the exhaust stream.
    """
    profile: FuelProfile
    burn_rate: float
    velocity: float
    stream_color: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.burn_rate <= 1.0:
            raise ValueError(
                f"burn_rate must be between 0.0 and 1.0, got {self.burn_rate}"
            )
        if self.velocity < 0:
            raise ValueError(
                f"velocity must be non-negative, got {self.velocity}"
            )


# ---------------------------------------------------------------------------
# Default stage specifications
# ---------------------------------------------------------------------------

def _micro_stage() -> ThermiteStage:
    """Factory for a default MicroThermite sustainer stage."""
    return ThermiteStage(
        profile=FuelProfile.MICRO,
        burn_rate=0.10,       # slow, steady consumption
        velocity=0.5,         # sub-baseline Yellow band
        stream_color="Yellow",
    )


def _nano_stage() -> ThermiteStage:
    """Factory for a default NanoThermite igniter stage."""
    return ThermiteStage(
        profile=FuelProfile.NANO,
        burn_rate=0.80,       # rapid, high-potency burn
        velocity=2.0,         # super-threshold Purple band
        stream_color="Purple",
    )


class BimodalEngine:
    """The Osprey's Hybrid Engine — Nano ignition, Micro sustain.

    The engine fires in two phases:

    1. **Ignite** (Nano): delivers an immediate high-velocity burst to close
       the Distance Gap or intercept a fast-moving snake.
    2. **Cruise** (Micro): transitions to the slow-burn sustainer for
       energy-efficient long-range travel once the target is in range.

    Attributes:
        igniter:  The NanoThermite ignition stage.
        sustainer: The MicroThermite cruise stage.
        current_stream: Optical signature of the active exhaust (``"Purple"``
                        during Nano ignition, ``"Yellow"`` during Micro cruise,
                        ``"Green_Growth"`` after a successful bridge).
    """

    def __init__(self) -> None:
        self.igniter: ThermiteStage = _nano_stage()
        self.sustainer: ThermiteStage = _micro_stage()
        self.current_stream: str = self.sustainer.stream_color

    # ------------------------------------------------------------------
    # Engine operations
    # ------------------------------------------------------------------

    def ignite(self) -> str:
        """Fire the NanoThermite stage for a high-velocity intercept burst.

        Returns:
            Status string confirming the Nano burst velocity.
        """
        self.current_stream = self.igniter.stream_color
        return (
            f"NANO_IGNITION: {self.igniter.velocity} Mach | "
            f"stream={self.current_stream}"
        )

    def cruise(self) -> str:
        """Switch to the MicroThermite sustainer for long-distance travel.

        Returns:
            Status string confirming the Micro cruise velocity.
        """
        self.current_stream = self.sustainer.stream_color
        return (
            f"MICRO_CRUISE: {self.sustainer.velocity} Mach | "
            f"stream={self.current_stream}"
        )

    def bridge_thermite(self, heat_type: str) -> str:
        """Convert an uncoupled heat type into a stable coupled stream.

        This is the engine-level translation of the OspreyCore
        ``bridge_thermite`` operation.

        Args:
            heat_type: ``"Nano"`` for high-velocity intercept propulsion or
                       ``"Micro"`` for long-range sustain.

        Returns:
            The resulting ``current_stream`` label after bridging.
        """
        if heat_type == FuelProfile.NANO.value or heat_type == "Nano":
            self.current_stream = "Green_Growth"
        elif heat_type == FuelProfile.MICRO.value or heat_type == "Micro":
            self.current_stream = "Yellow"
        return self.current_stream

    def __repr__(self) -> str:
        return (
            f"BimodalEngine(current_stream={self.current_stream!r}, "
            f"igniter={self.igniter.profile.value}, "
            f"sustainer={self.sustainer.profile.value})"
        )
