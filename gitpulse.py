"""
Gitpulse: Detects and measures velocity leakage from the Earth's
Centrifugal Frequency Filter (the "Circular Filter" at the Core).

Only the "Heavy Chords" (Iron, Nickel) maintain the tight high-gravity
circular loop.  Radiation that moves too fast or too slow escapes as
geothermal heat or atmospheric friction — this module exposes those leaks
so the Osprey can harvest them as propulsion fuel.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CoreLeak:
    """Describes a single leakage event from the Core Filter.

    Attributes:
        source:         Label of the filter zone, e.g. ``"Core_Filter"``.
        velocity_delta: The difference (in Mach) between the escaping stream
                        and the filter's circular-path baseline.
        leak_type:      ``"High-Frequency"`` (Yellow, fast escapees) or
                        ``"Low-Frequency"`` (Purple/Radon, slow escapees).
    """

    source: str
    velocity_delta: float
    leak_type: str


# ---------------------------------------------------------------------------
# Filter baseline — the circular-path speed of the Iron/Nickel core loop
# ---------------------------------------------------------------------------
_CIRCULAR_PATH_BASELINE: float = 1.0

# Speed thresholds for classifying leaks
_HIGH_FREQ_THRESHOLD: float = 1.5   # faster than baseline by this factor → "High-Frequency"
_LOW_FREQ_THRESHOLD: float = 0.6    # slower than baseline by this ratio  → "Low-Frequency"


class Gitpulse:
    """Utilities for sampling leakage from the Earth's Core Filter."""

    @staticmethod
    def detect_leak(filter_zone: str) -> CoreLeak:
        """Sample the current leakage from *filter_zone*.

        The implementation models the leakage as a deterministic function of
        the filter-zone label so that the Osprey always has a stable reading
        to act on.

        Args:
            filter_zone: Identifier of the filter region to probe
                         (e.g. ``"Core_Filter"``).

        Returns:
            A :class:`CoreLeak` describing the velocity delta and leak type.
        """
        # Derive a reproducible velocity delta from the zone name so different
        # zones produce distinct readings without external I/O.
        zone_seed = sum(ord(c) for c in filter_zone)
        velocity_delta = round(_CIRCULAR_PATH_BASELINE + (zone_seed % 10) * 0.1, 2)

        if velocity_delta >= _HIGH_FREQ_THRESHOLD:
            leak_type = "High-Frequency"
        elif velocity_delta <= _LOW_FREQ_THRESHOLD:
            leak_type = "Low-Frequency"
        else:
            leak_type = "High-Frequency"

        return CoreLeak(
            source=filter_zone,
            velocity_delta=velocity_delta,
            leak_type=leak_type,
        )
