#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test objectives: test the results of reactionSteps and compare it to manual calculations.

Target Reaction One: H+ + e- --> 0.5 * H2_g for the following ΔGs:
    a. pH = 0, U = 0 (expect 0)
    b. pH = 7, U = 0 (expect X)
    d. pH = 0, U = 1 (expect X)
    e. pH = 0, U = -1 (expect X)
    f. pH = 7, U = 1 (expect X)

Target Reaction Two: 0.5 * H2_g --> H+ + e- for the following ΔGs:
    (Expect reverses of Target One)
    a. pH = 0, U = 0
    b. pH = 7, U = 0
    d. pH = 0, U = 1
    e. pH = 0, U = -1
    f. pH = 7, U = 1

Target Reaction Three: H2O_l --> 0.5 * H2_g + OH- - e- for the following ΔGs:
    a. pH = 14, U = 0 (expect X)
    b. pH = 7, U = 0 (expect 0)
    c. pH = 14, U = 1 (expect 0)

"""

from ..src.reactionStep import ReactionStep

if __name__ == "__main__":
    pass
