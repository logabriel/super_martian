"""
ISPPJ1 2024
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for tiles.
"""

from typing import Dict, Any

TILES: Dict[int, Dict[str, Any]] = {
    # Ground
    0: {"solidness": dict(top=True, right=False, bottom=False, left=False)},
    1: {"solidness": dict(top=True, right=False, bottom=False, left=False)},
    2: {"solidness": dict(top=True, right=False, bottom=False, left=False)},
    3: {"solidness": dict(top=True, right=False, bottom=False, left=False)},
    4: {"solidness": dict(top=True, right=False, bottom=False, left=False)},
    5: {"solidness": dict(top=True, right=False, bottom=False, left=False)},
    10: {"solidness": dict(top=True, right=False, bottom=False, left=False)},
    # Blocks
    6: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    17: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    18: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    19: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    20: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    24: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    25: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    26: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    27: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    31: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    32: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    33: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    34: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    41: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    42: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    43: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
    44: {"solidness": dict(top=True, right=True, bottom=True, left=True)},
}
