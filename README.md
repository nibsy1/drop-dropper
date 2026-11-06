# Drop-Dropper

A small mechanised harvester for guttation droplets from *Arabidopsis* shoots.
A piezo stack actuator drives a steel rod in fast axial oscillation; a soft
clamp at the rod tip holds the plant stem (<= 1 mm diameter) and shakes the
shoot horizontally so droplets detach and fall into a weighing dish below.

## Layout

```
bench ──┬─ base plate + actuator mount (rigid, bolted down)
        │     └─ piezo stack (horizontal) → end cap/stud → coupler nut
        │         → steel rod (horizontal, axial oscillation)
        │             └─ two-piece silicone-padded lever clamp gripping the stem
        └─ weighing dish on the bench under the rosette
```

## Repo contents

- `cad/drop_dropper.py` — parametric model of every mechanical part (trimesh + manifold3d)
- `cad/parts/*.stl` — one STL per part, plus assembly and exploded assembly
- `cad/renders/*.png` — CAD renderings of all parts, assembly and exploded view
- `docs/specifications.md` — dimensions, materials, forces, electrical and operating specs
- `docs/design-decisions.md` — resolved design decisions and rationale
- `docs/assembly.md` — step-by-step assembly method
- `docs/bom.md` — bill of materials with indicative prices

## Quickstart

```bash
pip install -r cad/requirements.txt
python3 cad/drop_dropper.py   # regenerates all STLs and PNG renders
```
