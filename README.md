# Nanopattern design templates

Design templates and engineering source files for generating nanobar, nanopillar, NanoX, gradient array nanostructure, and MEA electrode GDS layouts for photolithography systems (Heidelberg MLA-150) or electron beam lithography systems (Raith EBPG 5200+) at nano@stanford Facilities.

## Contents

- `scripts/`: engineering files for each design.
- `templates/`: reusable parameter-only templates for new designs.
- `helpers/`: shared helper code used by the templates.

## Usage And Call

For a new design, start from a template, edit only the parameter block, then run:

```bash
python templates/nanobar_template.py
```

Generated GDS files are written by each script according to its `write_gds()` call.

## Citation

This project uses PHIDL for GDS layout generation: https://phidl.readthedocs.io/

## Disclaimers

These scripts are research design utilities and should be reviewed before fabrication. Verify all dimensions, layers, labels, and wafer placement in a GDS viewer before mask submission.
