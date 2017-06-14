
from BuildStructure import placePeptide
from chimera import runCommand as rc
aa = "H"

# Build a sequence
placePeptide(aa, [(-50, 70)] * len(aa), model="peptide")
# Add hydrogens automatically
rc("addh")
# Align so the CA-CB bond is going into the page
rc("align @CA @N")
rc("set fieldOfView 14.5227")
rc("set scale 1.0")
rc("set projection orthographic")
rc("windowsize 800 600")
# Color and highlight
rc("color grey")
rc("repr stick")
rc("shape sphere radius 0.5 center @CA color red")
rc("shape sphere radius 0.5 center @C color blue")
rc("shape sphere radius 0.5 center @N color green")
rc("shape sphere radius 0.5 center @CA color orange")
# Save
rc("copy file HIS-omega.png supersample 3")
# rc("close all")
