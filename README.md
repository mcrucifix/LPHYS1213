[![Latest Build PDF](https://img.shields.io/badge/PDF-Latest_Build-blue.svg)](https://forge.uclouvain.be/mcrucifix-teaching/LPHYS1213/-/jobs/artifacts/main/raw/lphys1213.pdf?job=build_pdf)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mcrucifix/lphys1213.git/HEAD?urlpath=%2Fdoc%2Ftree%2FIPynb%2F03_SF_with_circulation.ipynb)
[![pipeline status](https://forge.uclouvain.be/mcrucifix-teaching/LPHYS1213/badges/main/pipeline.svg)](https://forge.uclouvain.be/mcrucifix-teaching/LPHYS1213/-/pipelines)
![Status](https://img.shields.io/badge/Status-Under_Construction-yellow?logo=hammer)

# LPHYS1213 — Physique des fluides (template)

This repository is a course template that uses the shared `latex-tools` submodule.

```
git submodule init 
git submodule update
```

## Setup

**epix** is used for creating mathematical figures.  
To install it from source:

- **Download the epix source archive:**

```bash
wget https://mathcs.holycross.edu/~ahwang/epix/epix-1.2.22.tar.gz
tar -xvzf epix-1.2.22.tar.gz
cd epix-1.2.22
make
sudo make install # or get the epix binary in your path
```

---

- Installing **bibbrowser** (bibliography management)


```bash
python3 -m pip install https+ssh://git@forge.uclouvain.be/mcrucifix/bibbrowser.git
```

> Ensure your SSH keys are configured and you have access rights to the repository.

- Installing **Inkscape** (SVG to PDF conversion)


```bash
## on Ubuntu - Debian
sudo apt-get install inkscape
```

- Compile with 


```
make
```

