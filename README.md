# How I merged several nonequilibrium code repositories into one master

This will stay distinct from `nonequilibrium-gilsonlabucsd`, which should remain
as the "publicly" available version of the code.
- Make new directory `nonequilibrium-master` on local.
- Inside `nonequilibrium-master/` create...


  - `manuscript` for files from `nonequilibrium-manuscript`. These are similar to -- but not exactly the same as --  the files in `nonequilibrium-gilsonlabucsd`. They contain additional explorations that did not make it into the final manuscript. **Now this is in `code/`, copied there using `rsync -au`**


  - `literature` for files from `nonequilibrium-literature-review`. These are
  Markdown files with associated build CI build scripts modeled after
  `deep-review`.
  - `explorations` for files from `nonequilibrium/nonequilibrium-explorations`.
  These contain notebooks for PDB searching and achiral to chiral transitions.
  - `md-data` for the raw simulation data (excluding trajectories, which are stored in `large-file-storage` on Kirkwood and GPFS).
  - `code` filled with `nonequilibrium/code/SG-model-v2`, `nonequilibrium/code/torsion-individual`, and `nonequilibrium/code/torque-scans` copied with `rsync -au`.

Now, there needs to be a good way to store the code. There is code from the manuscript, and code from just before making the manuscript, and then much older code.


There are still several side projects that could be merged:
- The `torsion-individual` that...
- The `torsion-scan` that ...
- The `shiny` web app
- The old Brownian dynamics code