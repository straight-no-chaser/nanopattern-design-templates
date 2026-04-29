# Nanopattern design templates

This repository contains design templates and engineering source files for generating nanobar, nanopillar, NanoX, gradient array nanostructure, and MEA electrode GDS layouts used in photolithography systems (Heidelberg MLA-150) at Stanford Nanofabrication Facility.

The engineering files are parts of ongoing research efforts in the [Cui Lab](https://cuilab.stanford.edu/research), Stanford University.

## Project Structure

- `projects_cui/`: engineering files for each design.
- `templates/`: reusable parameter-only templates for new designs.
- `gds_templates/`: shared helper code used by the templates.

## Dependencies

Install the required packages:

```bash
pip install phidl numpy matplotlib
```

## Usage And Call

Use the cleaned project scripts directly:

```bash
python project/jane-doe/script.py
```

For a new design, start from a template, edit only the parameter block, then run it:

```bash
python templates/nanobar_template.py
```

Generated GDS files are written by each script according to its `write_gds()` call.

## Citation And Acknowledge

This project uses PHIDL for GDS layout generation. If these scripts support published work, please cite PHIDL:

McCaughan, A. N., et al. "PHIDL: Python-based layout and geometry creation for nanolithography." Journal of Vacuum Science and Technology B 39, 062601 (2021). https://doi.org/10.1116/6.0001203

PHIDL documentation: https://phidl.readthedocs.io/

## Disclaimers

These scripts are research design utilities and should be reviewed before fabrication. Verify all dimensions, layers, labels, and wafer placement in a GDS viewer before mask submission. The authors are responsible for process compatibility, design-rule checks, and final fabrication validation.
