# Deprecated: Please use [pl-N4BiasFieldCorrection](https://github.com/FNNDSC/pl-N4BiasFieldCorrection)

https://github.com/FNNDSC/pl-N4BiasFieldCorrection

## N4 Bias Field Correction

[![Version](https://img.shields.io/docker/v/fnndsc/pl-ants_n4biasfieldcorrection)](https://hub.docker.com/r/fnndsc/pl-ants_n4biasfieldcorrection/tags?page=1&ordering=last_updated)
[![MIT License](https://img.shields.io/github/license/FNNDSC/pl-ANTs_N4BiasFieldCorrection)](https://github.com/FNNDSC/pl-ANTs_N4BiasFieldCorrection/blob/master/LICENSE)

_ChRIS_ ds plugin wrapper around [ANTsPy](https://github.com/ANTsX/ANTsPy)
[N4BiasFieldCorrection](https://manpages.debian.org/testing/ants/N4BiasFieldCorrection.1.en.html).

> N4 is a variant of the popular N3 (nonparameteric nonuniform normalization)
> retrospective bias correction algorithm.

## Usage

Easiest way to run is using
[`singularity`](https://sylabs.io/singularity/).

```bash
mkdir in out
cp 1.nii 2.nii 3.nii in/
singularity exec docker://fnndsc/pl-ants_n4biasfieldcorrection:0.2.7.1 bfc in/ out/
```

Multithreading is used to parallelize on inputs.
CPU usage can be limited using a container engine like `docker` or `podman`.

```bash
docker run --rm -u $(id -u):$(id -g) --userns=host     \
    --cpuset-cpus 0-4                                  \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw   \
    fnndsc/pl-ants_n4biasfieldcorrection:0.2.7.1 bfc   \
    /incoming /outgoing
```

[![chrisstore.co](docs/badge.png)](https://chrisstore.co/plugin/77)
