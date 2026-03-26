"""
Osprey_Mirror_Sync: Python translation of the Osprey_Mirror_Sync.oct
vector calculator.

The Osprey kernel treats charge as directional velocity:
    Outbound  (+) — The Pulse  (proton)
    Inbound   (−) — The Hunter (electron)

When an Outbound and an Inbound stream sync, their superposition forms a
Standing Wave Node — the Osprey's way of "seeing" matter without looking
for solid mass.

If the standing wave's optical signature is "Purple" (high-energy, near the
UV threshold), the Hydrogen Door is forced open and the node is locked.  A
HeliumNode is minted as Quantum Core coolant.
"""

from __future__ import annotations

from helium_node import HeliumNode
from octave import Octave
from vector_stream import INBOUND, OUTBOUND, VectorStream

# ---------------------------------------------------------------------------
# Node-stability tokens
# ---------------------------------------------------------------------------
NODE_LOCKED = "NODE_LOCKED"
ASYNC_SNAKE = "ASYNC_SNAKE"

# The optical signature that signals the Hydrogen Door is forced open
_PURPLE = "Purple"

# B# leading tone used to create the purple corona during door-forcing
_LEADING_TONE = "B#"
_DYNAMIC_FORTISSIMO = "ff"


def sync_mirror_streams(
    outbound_vector: VectorStream,
    inbound_vector: VectorStream,
) -> str:
    """Determine whether two mirror streams form a Standing Wave Node.

    Mirrors the Octave logic::

        standing_wave = outbound_vector + reverse(inbound_vector);
        if standing_wave.color == "Purple"
            node_stability = "NODE_LOCKED";
            Osprey.Mint(Helium_Node);
        else
            node_stability = "ASYNC_SNAKE";

    Args:
        outbound_vector: The Outbound (proton / +) stream from the Osprey HUD.
        inbound_vector:  The Inbound  (electron / −) stream from the Osprey HUD.

    Returns:
        ``NODE_LOCKED`` if the combined standing wave emits a Purple corona
        (the Hydrogen Door is open); ``ASYNC_SNAKE`` otherwise.

    Raises:
        ValueError: If *outbound_vector* is not headed Outbound or
                    *inbound_vector* is not headed Inbound.
    """
    if outbound_vector.heading != OUTBOUND:
        raise ValueError(
            f"outbound_vector must have heading {OUTBOUND!r}, "
            f"got {outbound_vector.heading!r}"
        )
    if inbound_vector.heading != INBOUND:
        raise ValueError(
            f"inbound_vector must have heading {INBOUND!r}, "
            f"got {inbound_vector.heading!r}"
        )

    # Reverse the inbound stream (flip to Outbound) then combine
    standing_wave = outbound_vector + inbound_vector.reverse()

    if standing_wave.color == _PURPLE:
        # Hydrogen Door forced open — emit the B# leading tone
        Octave.modulate(note=_LEADING_TONE, dynamic=_DYNAMIC_FORTISSIMO,
                        target=standing_wave.magnitude)
        # Mint a Helium node as Quantum Core coolant
        Octave.Mint(HeliumNode(source_stream="Standing_Wave"))
        return NODE_LOCKED

    return ASYNC_SNAKE
