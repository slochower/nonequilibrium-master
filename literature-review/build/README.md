# Building the manuscript

[`build.sh`](build.sh) builds the repository.
`sh build.sh` should be executed from the root directory of the repository.

## Environment

Install the [conda](https://conda.io) environment specified in [`environment.yml`](../environment.yml) by running:

```sh
conda env create --file environment.yml
```

Activate with `source activate literature`.

N.B. I've added extra logging to the citation processing step.