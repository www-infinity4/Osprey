"""
HeliumNode: The "Tamed Explosion" — a stable product minted by the Osprey
after it neutralizes a Uranium (high-energy de-sync) snake via Harmonic
Cancellation.

The two Negative-Stream Harpoons (Inbound Electrons) catch the Uranium
spit and force it into cancellation, yielding a Helium node that the
Osprey uses as Coolant for its Quantum Core.
"""

from __future__ import annotations


class HeliumNode:
    """Represents a stabilized Helium node produced by Harmonic Cancellation.

    Attributes:
        coolant_capacity: Quantum-Core cooling capacity, expressed as a
            fraction of full-load (0.0 – 1.0).
        source_stream:    Label of the snake that was neutralized to produce
            this node.
    """

    # Each Helium node provides this fraction of Quantum Core cooling capacity
    _COOLANT_FRACTION: float = 0.25

    def __init__(self, source_stream: str = "Uranium") -> None:
        self.source_stream = source_stream
        self.coolant_capacity = self._COOLANT_FRACTION

    def __repr__(self) -> str:
        return (
            f"HeliumNode(source={self.source_stream!r}, "
            f"coolant_capacity={self.coolant_capacity})"
        )
