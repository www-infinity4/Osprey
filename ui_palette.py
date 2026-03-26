"""
ui_palette: The Osprey-Infinite Architect UI Emoji Palette.

Every builder tool on the Osprey flight deck is represented as a
:class:`PaletteTool` descriptor.  The registry maps the tool's emoji key to
its descriptor, allowing any UI layer to enumerate available tools, display
their descriptions, and invoke their ``action`` handlers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional


@dataclass
class PaletteTool:
    """A single tool on the Osprey UI palette.

    Attributes:
        emoji:       Unicode emoji identifier shown on the HUD.
        name:        Short human-readable name.
        description: What the tool does in one sentence.
        action:      Optional callable that runs when the tool is activated.
                     If ``None`` the tool is registered but not yet wired.
    """
    emoji: str
    name: str
    description: str
    action: Optional[Callable[[], str]] = None

    def activate(self) -> str:
        """Invoke the tool's action, or return a not-yet-wired message."""
        if self.action:
            return self.action()
        return f"[{self.emoji} {self.name}] — not yet wired."


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_tools: Dict[str, PaletteTool] = {}


def register(tool: PaletteTool) -> None:
    """Add *tool* to the palette registry, keyed by its emoji."""
    _tools[tool.emoji] = tool


def get(emoji: str) -> Optional[PaletteTool]:
    """Return the tool for *emoji*, or ``None`` if not registered."""
    return _tools.get(emoji)


def all_tools() -> list[PaletteTool]:
    """Return a list of all registered tools in insertion order."""
    return list(_tools.values())


# ---------------------------------------------------------------------------
# Built-in tool definitions
# ---------------------------------------------------------------------------

register(PaletteTool(
    emoji="💲",
    name="Financial AI",
    description=(
        "Opens the Intelligent Card — detects page context to suggest "
        "PayPal Checkout, Token Mint, or Exchange."
    ),
))

register(PaletteTool(
    emoji="♠️",
    name="Bitcoin-Crusher Receipt",
    description=(
        "Connects to the Bitcoin-Crusher repo.  Each click prints a "
        "Living Receipt token containing a random Infinity AI Research Article."
    ),
))

register(PaletteTool(
    emoji="🟦",
    name="Content Scraper",
    description=(
        "Scrapes external data, restructures it with Octave Green Logic, "
        "and fits it to the CSS grid."
    ),
))

register(PaletteTool(
    emoji="🟥",
    name="Hamburger Architect",
    description=(
        "AI scans your GitHub and asks which repos become categories, "
        "then builds the navigation menu dynamically."
    ),
))

register(PaletteTool(
    emoji="🟨",
    name="The Plucker",
    description=(
        "Extracts styles, cards, or raw data from any site "
        "and moves them into the current build."
    ),
))

register(PaletteTool(
    emoji="🎷",
    name="Infinity Media",
    description=(
        "RSS-fed Radio, Games, TV, and Galleries.  "
        "Choose Radio → Local/World → Manual/Auto-Preset."
    ),
))

register(PaletteTool(
    emoji="♥️",
    name="The Love/Faith Node",
    description=(
        "Logical starting points for community/religion.  "
        "Connects to Puppy Dog Realms (Nature/Love) or established Theology books."
    ),
))

register(PaletteTool(
    emoji="⭐",
    name="The Fact-Checker",
    description=(
        "Updates content in real-time by comparing page data with "
        "Infinity Research Repos to ensure no dissonant logic is built."
    ),
))

register(PaletteTool(
    emoji="🟩",
    name="The Engineer",
    description=(
        "Suggests the next build move: add an image, expand research into "
        "a graph, or apply a schematic."
    ),
))

register(PaletteTool(
    emoji="😎",
    name="Visualizer",
    description=(
        "Pop-up to choose audio/data visualizers that meld into "
        "the background of your content."
    ),
))

register(PaletteTool(
    emoji="✨",
    name="Repo Unifier",
    description=(
        "Connects multiple repos and builds them out into "
        "a single unified machine."
    ),
))

register(PaletteTool(
    emoji="♣️",
    name="The Transformer",
    description=(
        "Assigns a Machine Part (Belt, Piston, Scraper, Memory) to every repo.  "
        "If a repo has a gap (e.g., no shop), it automatically adds the missing part."
    ),
))

register(PaletteTool(
    emoji="🎨",
    name="Art Studio",
    description=(
        "Quick-draw or 3-D studio.  "
        "Every stroke prints a Token Receipt via the Osprey printer."
    ),
))

register(PaletteTool(
    emoji="🟡",
    name="Token Walker",
    description="Deep manual design tool for custom minted tokens.",
))

register(PaletteTool(
    emoji="♦️",
    name="Merchant Mode",
    description="Adds business and point-of-sale options to any Living Page.",
))

register(PaletteTool(
    emoji="🧱",
    name="Commit-Crypt",
    description=(
        "Encrypts and stores user data via GitHub GHP Secrets."
    ),
))

register(PaletteTool(
    emoji="🍄",
    name="The Doubler",
    description=(
        "Scans your research and instantly doubles the content girth.  "
        "If it detects a gap in the logic, it pulls in additional scientific "
        "articles from the Infinity AI to bridge it."
    ),
))

register(PaletteTool(
    emoji="⬜",
    name="The Soul Unifier",
    description=(
        "Scans all repos, identifies the Soul Intent of each "
        "(e.g., healing, crushing), and weaves them into a single "
        "faceted interface gem."
    ),
))

register(PaletteTool(
    emoji="⚪",
    name="The Cloner",
    description=(
        "Clones the current repo and asks what to add "
        "based on the AI's context scan."
    ),
))

register(PaletteTool(
    emoji="💎",
    name="Facet Gem",
    description=(
        "Takes the intent of a single repo and starts "
        "a fresh, focused clone build from it."
    ),
))

register(PaletteTool(
    emoji="🔥",
    name="The Editor",
    description="Change, edit, or remove components from any Living Page.",
))

register(PaletteTool(
    emoji="🛸",
    name="The Triode",
    description=(
        "Connects three repos into a Control Grid "
        "(Weak + Strong + Control) to manage high-power data flows."
    ),
))
