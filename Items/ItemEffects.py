"""
    On defining a hitEffect!
      Actors and Equipment can have "hitEffects"
      that trigger when damage is dealt to an enemy
      with a non-magical attack.

      A hitEffect has 2 (or a third optionally) effects
        Effect -- An Effect object
        Target -- "self" | "Actor"
          "self" will place the effect on the target hit
          "Actor" will place it on the attacker
        Args   -- A list of arguments.  All arguments
                  must be placed inside a string as
                  each string will be an argument for eval()
"""

from Effects import *

def hitDoT(pwr):    ## Burn/Poison DoT
    return [
        DoT,
        "self",
        ["2", str(pwr)]
        ]

def hitArmorRend(pwr):    ## Burn/Poison DoT
    return [
        ArmorReduction,
        "self",
        ["2", str(pwr)]
        ]
