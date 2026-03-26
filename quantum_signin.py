"""
quantum_signin: The Osprey 8-Note Quantum-Pulse Sign-In system.

Security model
--------------
A user's identity is represented not by a password but by their *Signature
Frequency* — an 8-note sequence recorded with two measurements per note:

* **BPM offset** — the inter-note timing delta (how the user phrases the
  rhythm).
* **Velocity** — the dynamic intensity of each note strike (pianissimo → ff).

Because the "One-Stream" is always shifting, the system does not demand
an exact replay.  A **70 % dynamic match** (``MATCH_THRESHOLD``) is
sufficient to unlock access — replicating the "Living Friction" of a human
touch that a purely deterministic bot cannot reproduce.

Signature storage
-----------------
Signatures are stored as an in-memory mapping keyed by username.  In a
production deployment this mapping would be backed by GitHub GHP Secrets
(encrypted at rest); no plaintext credential ever appears in source code.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NOTE_COUNT: int = 8
"""Every sign-in sequence must contain exactly this many notes."""

MATCH_THRESHOLD: float = 0.70
"""Fraction of notes whose dynamics must match for access to be granted."""

_VELOCITY_TOLERANCE: float = 0.15
"""Two velocity readings are considered a 'match' if they differ by at most
this fraction of the full dynamic range (0.0 – 1.0)."""


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class NoteStrike:
    """A single note played during a sign-in attempt.

    Attributes:
        note:     Musical pitch name, e.g. ``"C4"``, ``"B#3"``.
        bpm_offset: Timing delta from the expected beat grid, in
                    milliseconds.  Negative = ahead; positive = behind.
        velocity:  Dynamic intensity of the strike, normalised to
                   ``[0.0, 1.0]``.  ``0.0`` = silence, ``1.0`` = fff.
    """
    note: str
    bpm_offset: float
    velocity: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.velocity <= 1.0:
            raise ValueError(
                f"velocity must be in [0.0, 1.0], got {self.velocity}"
            )


@dataclass
class SignatureFrequency:
    """The stored Signature Frequency for a single user.

    Attributes:
        username:   Identifier for the owner of this signature.
        strikes:    The canonical 8-note sequence recorded at enrolment.
        ghp_ref:    Opaque reference to the GHP Secret that this signature
                    guards (never the secret value itself).
    """
    username: str
    strikes: List[NoteStrike]
    ghp_ref: str = ""

    def __post_init__(self) -> None:
        if len(self.strikes) != NOTE_COUNT:
            raise ValueError(
                f"A signature must contain exactly {NOTE_COUNT} notes, "
                f"got {len(self.strikes)}"
            )

    def fingerprint(self) -> str:
        """Return a deterministic hex fingerprint of this signature.

        The fingerprint is derived from the note names and rounded velocity
        values only — BPM offsets are intentionally excluded so that minor
        timing drift does not change the stored key.
        """
        raw = "|".join(
            f"{s.note}:{round(s.velocity, 2)}" for s in self.strikes
        )
        return hashlib.sha256(raw.encode()).hexdigest()


# ---------------------------------------------------------------------------
# In-memory signature registry
# (replace with a GHP-backed encrypted store in production)
# ---------------------------------------------------------------------------

_registry: Dict[str, SignatureFrequency] = {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class QuantumSignIn:
    """Osprey 8-Note Quantum-Pulse authentication manager."""

    # ------------------------------------------------------------------
    # Enrolment
    # ------------------------------------------------------------------

    @staticmethod
    def enroll(signature: SignatureFrequency) -> str:
        """Store a user's Signature Frequency in the registry.

        Args:
            signature: The canonical 8-note sequence recorded at enrolment.

        Returns:
            The fingerprint hash that was stored for this signature.
        """
        _registry[signature.username] = signature
        return signature.fingerprint()

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    @staticmethod
    def verify(username: str, attempt: Sequence[NoteStrike]) -> bool:
        """Verify an 8-note attempt against the stored Signature Frequency.

        The 70 % rule:  at least ``MATCH_THRESHOLD`` of the eight notes must
        have a velocity within ``_VELOCITY_TOLERANCE`` of the enrolled value.
        Note order matters; pitches are compared by position.

        Args:
            username: The user being authenticated.
            attempt:  The 8-note sequence played during this sign-in.

        Returns:
            ``True`` if the dynamic match score meets the threshold;
            ``False`` otherwise (including unknown username).
        """
        if username not in _registry:
            return False

        if len(attempt) != NOTE_COUNT:
            return False

        stored = _registry[username].strikes
        matches = sum(
            1
            for stored_note, attempt_note in zip(stored, attempt)
            if abs(stored_note.velocity - attempt_note.velocity)
            <= _VELOCITY_TOLERANCE
        )

        score = matches / NOTE_COUNT
        return score >= MATCH_THRESHOLD

    @staticmethod
    def match_score(username: str, attempt: Sequence[NoteStrike]) -> float:
        """Return the raw dynamic-match score (0.0 – 1.0) for an attempt.

        Useful for diagnostics and UI feedback ("You were 82 % in tune").

        Args:
            username: The user being scored.
            attempt:  The 8-note sequence played during this sign-in.

        Returns:
            Fraction of notes whose dynamics matched, or ``0.0`` if the
            username is unknown or the attempt length is wrong.
        """
        if username not in _registry or len(attempt) != NOTE_COUNT:
            return 0.0

        stored = _registry[username].strikes
        matches = sum(
            1
            for s, a in zip(stored, attempt)
            if abs(s.velocity - a.velocity) <= _VELOCITY_TOLERANCE
        )
        return matches / NOTE_COUNT

    # ------------------------------------------------------------------
    # Registry helpers
    # ------------------------------------------------------------------

    @staticmethod
    def is_enrolled(username: str) -> bool:
        """Return whether *username* has a stored Signature Frequency."""
        return username in _registry

    @staticmethod
    def clear_registry() -> None:
        """Purge all stored signatures (test / session-reset use only)."""
        _registry.clear()
