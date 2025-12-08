[![Latest Build PDF](https://img.shields.io/badge/PDF-Latest_Build-blue.svg)](https://forge.uclouvain.be/mcrucifix-teaching/LPHYS1213/-/jobs/artifacts/main/raw/lphys1213.pdf?job=build_pdf)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mcrucifix/lphys1213.git/HEAD?urlpath=%2Fdoc%2Ftree%2FIPynb%2F03_SF_with_circulation.ipynb)

# LPHYS1213 — Physique des fluides (template)

This repository is a course template that uses the shared `latex-tools` submodule.

## Setup

**epix** is used for creating mathematical figures.  
To install it from source:

1. **Download the epix source archive:**

```bash
wget https://mathcs.holycross.edu/~ahwang/epix/epix-1.2.22.tar.gz
tar -xvzf epix-1.2.22.tar.gz
cd epix-1.2.22
make
sudo make install # or get the epix binary in your path
```

---

## 2. Installing **bibbrowser** (bibliography management)

Install **bibbrowser** directly from the Git repository:

```bash
python3 -m pip install git+ssh://git@forge.uclouvain.be/mcrucifix/bibbrowser.git@python3
```

> Ensure your SSH keys are configured and you have access rights to the repository.

---

## 3. Installing **Inkscape** (SVG to PDF conversion)

### On Debian/Ubuntu:

```bash
sudo apt-get install inkscape
```


0. Depedenncies

```bash
  # bibbrowser
  python3 -m pip3 install git+ssh://git@forge.uclouvain.be/mcrucifix/bibbrowser.git@python3
  # to do here: add synchronisation to local bibliography


1. Initialise submodules:
   ```bash
   git submodule update --init --recursive

## Make
