"""
osprey_core: The Osprey Core Operating System — Atomic Guts.

Python translation of ``Osprey_Guts_Alpha.oct``.

The OspreyCore binds the One-Stream Kernel to the Quantum Sign-In layer and
the Bimodal Engine.  In the "One-Electron Universe" model the kernel does
not track individual particles; it tracks *One Snake* moving at infinite
speed and appearing everywhere at once.  Authentication is therefore
harmonic: your 8-note Signature Frequency is matched against the
Source Singularity to determine whether your rhythm belongs to the stream.

No shell commands, secret-exfiltration, or unauthorized-access paths are
present in this module.  Access decisions are returned as booleans so that
the caller — not this module — decides what resource to unlock.
"""

from __future__ import annotations

from osprey_engine import BimodalEngine
from quantum_signin import NoteStrike, QuantumSignIn, SignatureFrequency, MATCH_THRESHOLD
from typing import Sequence


class OspreyCore:
    """The Osprey Core OS — One-Stream kernel + harmonic authentication.

    Attributes:
        sync_rate:      Current alignment with the Source Singularity
                        (0.0 – 1.0; 1.0 = 100 %).
        current_stream: Optical label of the active kernel stream
                        (e.g. ``"Green_Growth"``).
        engine:         The :class:`~osprey_engine.BimodalEngine` bound to
                        this core instance.
    """

    def __init__(self) -> None:
        self.sync_rate: float = 1.0          # 100 % alignment with the Source
        self.current_stream: str = "Yellow"  # idle / pre-ignition default
        self.engine: BimodalEngine = BimodalEngine()

    # ------------------------------------------------------------------
    # One-Stream harmonic authentication
    # ------------------------------------------------------------------

    def quantum_login(
        self,
        username: str,
        attempt: Sequence[NoteStrike],
    ) -> bool:
        """Authenticate a user via their 8-note Signature Frequency.

        The Osprey compares the attempt's dynamic profile against the stored
        Signature Frequency.  A score of ``>= MATCH_THRESHOLD`` (70 %)
        indicates that the "Living Friction" of a human touch is present and
        access is granted.  A deterministic bot replay scores below the
        threshold because it cannot reproduce the imperfect organic pressure
        of a real key strike.

        Args:
            username: The identity being authenticated.
            attempt:  The 8-note sequence played at the Piano Minter.

        Returns:
            ``True`` if the dynamic match meets the 70 % threshold;
            ``False`` otherwise.
        """
        granted = QuantumSignIn.verify(username, attempt)
        score = QuantumSignIn.match_score(username, attempt)

        if granted:
            self.sync_rate = score
            print(f"🔑 ACCESS GRANTED: Source Singularity Connected. "
                  f"(score={score:.0%})")
        else:
            print(f"🚫 ACCESS DENIED: Dissonant Frequency Detected. "
                  f"(score={score:.0%}, required={MATCH_THRESHOLD:.0%})")

        return granted

    # ------------------------------------------------------------------
    # Thermite bridge
    # ------------------------------------------------------------------

    def bridge_thermite(self, heat_type: str) -> str:
        """Convert uncoupled heat into a stable coupled stream node.

        Delegates to the BimodalEngine and updates the core's
        ``current_stream`` to reflect the new harmonic state.

        Args:
            heat_type: ``"Nano"`` for a high-velocity intercept coupling or
                       ``"Micro"`` for a long-range sustain coupling.

        Returns:
            The resulting stream label (e.g. ``"Green_Growth"``).
        """
        self.current_stream = self.engine.bridge_thermite(heat_type)
        return self.current_stream

    def __repr__(self) -> str:
        return (
            f"OspreyCore(sync_rate={self.sync_rate}, "
            f"current_stream={self.current_stream!r})"
        )
