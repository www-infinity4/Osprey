"""
VectorStream: The Osprey's unified model for charged-particle streams.

In the Osprey HUD there are no "particles," only *Headings*.  A proton is
an Outbound pulse; an electron is an Inbound hunter.  This module encodes
that abstraction so every downstream component speaks the same language.

Frequency / Color mapping (visible-band analog):
    magnitude >= 1.8  →  "Purple"  (highest-energy visible; near-UV threshold)
    0.8 <= mag < 1.8  →  "Green"   (mid-band, stable harmonic)
    magnitude <  0.8  →  "Yellow"  (low-energy, drifting)
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Heading constants
# ---------------------------------------------------------------------------
OUTBOUND = "Outbound"   # Proton (+) — the Pulse
INBOUND = "Inbound"     # Electron (−) — the Hunter

# Frequency thresholds that define the visible color of a standing wave
_PURPLE_THRESHOLD: float = 1.8
_GREEN_THRESHOLD: float = 0.8


def _color_from_magnitude(magnitude: float) -> str:
    """Map a scalar magnitude to its optical frequency signature."""
    if magnitude >= _PURPLE_THRESHOLD:
        return "Purple"
    if magnitude >= _GREEN_THRESHOLD:
        return "Green"
    return "Yellow"


class VectorStream:
    """A directional velocity stream tracked by the Osprey kernel.

    Attributes:
        heading:   Direction of travel — ``OUTBOUND`` or ``INBOUND``.
        magnitude: Scalar speed in Mach units.
        color:     Optical frequency signature derived from *magnitude*.
    """

    def __init__(self, heading: str, magnitude: float) -> None:
        if heading not in (OUTBOUND, INBOUND):
            raise ValueError(
                f"heading must be {OUTBOUND!r} or {INBOUND!r}, got {heading!r}"
            )
        if magnitude < 0:
            raise ValueError(f"magnitude must be non-negative, got {magnitude}")
        self.heading = heading
        self.magnitude = magnitude
        self.color = _color_from_magnitude(magnitude)

    # ------------------------------------------------------------------
    # Mirror / reverse
    # ------------------------------------------------------------------

    def reverse(self) -> "VectorStream":
        """Return a new stream with the opposite heading and the same magnitude.

        Reversing an Inbound stream yields an Outbound stream and vice-versa.
        This is the Osprey's "mirror" operation used when computing standing
        waves.
        """
        flipped = OUTBOUND if self.heading == INBOUND else INBOUND
        return VectorStream(flipped, self.magnitude)

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------

    def __add__(self, other: "VectorStream") -> "VectorStream":
        """Combine two streams into a single resultant standing-wave vector.

        When headings match the magnitudes reinforce; when they are opposite
        they partially cancel (absolute difference).  The resulting heading
        follows the dominant (larger-magnitude) stream.
        """
        if self.heading == other.heading:
            combined_magnitude = self.magnitude + other.magnitude
            dominant_heading = self.heading
        else:
            combined_magnitude = abs(self.magnitude - other.magnitude)
            dominant_heading = (
                self.heading if self.magnitude >= other.magnitude else other.heading
            )
        return VectorStream(dominant_heading, combined_magnitude)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"VectorStream(heading={self.heading!r}, "
            f"magnitude={self.magnitude}, color={self.color!r})"
        )
