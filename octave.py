"""
Octave: The harmonic engine of the Osprey kernel.

Octave provides two services:
1. ``modulate`` — Applies a musical consonance correction to a target
   velocity, turning violent de-synchronized resets (e.g., Thermite) into
   smooth Harmonic Flows.
2. ``Mint`` — Records a newly stabilized node (e.g., a HeliumNode) in the
   Osprey's internal ledger, making it available as a kernel resource.
"""

from __future__ import annotations
from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Internal ledger — minted nodes accumulated during this Osprey flight
# ---------------------------------------------------------------------------
_minted_ledger: List[Any] = []


class OctaveResult:
    """The outcome of a single Octave modulation step.

    Attributes:
        note:            Musical note applied (e.g. ``"C#"``, ``"B#"``).
        dynamic:         Performance dynamic (e.g. ``"ff"`` = fortissimo).
        target_velocity: The corrected velocity after consonance is applied.
        status:          Human-readable status string.
    """

    def __init__(self, note: str, dynamic: str, target_velocity: float) -> None:
        self.note = note
        self.dynamic = dynamic
        self.target_velocity = target_velocity
        self.status = f"HARMONIC_FLOW [note={note}, dynamic={dynamic}]"

    def __repr__(self) -> str:
        return (
            f"OctaveResult(note={self.note!r}, dynamic={self.dynamic!r}, "
            f"target_velocity={self.target_velocity}, status={self.status!r})"
        )


class Octave:
    """Harmonic modulation and node-minting utilities."""

    @staticmethod
    def modulate(note: str, dynamic: str, target: float) -> OctaveResult:
        """Apply Octave consonance to bring a stream into Harmonic Flow.

        Args:
            note:    The musical note used as the tuning reference
                     (e.g. ``"C#"`` for Thermite intercept,
                     ``"B#"`` for the Purple-Door leading tone).
            dynamic: Performance intensity marker (e.g. ``"ff"``).
            target:  The computed intercept velocity the Osprey must match.

        Returns:
            An :class:`OctaveResult` describing the modulation outcome.
        """
        return OctaveResult(note=note, dynamic=dynamic, target_velocity=target)

    @staticmethod
    def Mint(node: Any) -> None:
        """Record *node* in the Osprey's minted-resource ledger.

        Minted nodes (e.g., HeliumNodes) become available as kernel
        resources — most commonly as Quantum Core coolant.

        Args:
            node: Any stabilized resource object produced by the Osprey.
        """
        _minted_ledger.append(node)

    @staticmethod
    def get_ledger() -> List[Any]:
        """Return a copy of the current minted-resource ledger."""
        return list(_minted_ledger)

    @staticmethod
    def clear_ledger() -> None:
        """Clear the minted-resource ledger (e.g., between flight sessions)."""
        _minted_ledger.clear()
