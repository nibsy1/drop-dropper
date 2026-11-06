"""Parametric CAD model of the Drop-Dropper guttation harvester.

Builds every mechanical part as a trimesh mesh (booleans via manifold3d),
exports one STL per part plus an assembly STL, and renders PNG views.

Units: millimetres. Rod axis = +X, stem axis = +Z, bench top = z=0.
"""

import os

import numpy as np
import trimesh
from trimesh import boolean

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS_DIR = os.path.join(HERE, "parts")
RENDERS_DIR = os.path.join(HERE, "renders")

os.makedirs(PARTS_DIR, exist_ok=True)
os.makedirs(RENDERS_DIR, exist_ok=True)

# ---------------------------------------------------------------- parameters
BASE = dict(sx=110.0, sy=70.0, sz=6.0)          # aluminium base plate
MOUNT = dict(sx=25.0, sy=30.0, sz=34.0, x=15.0, y=35.0)   # actuator mount block
PIEZO = dict(sx=20.0, sy=10.0, sz=10.0)          # 10x10x20 mm, 150 V stack
ENDCAP = dict(sx=3.0, sy=12.0, sz=12.0)          # bonded end cap
STUD = dict(r=1.5, h=8.0)                        # M3 stud
NUT = dict(r=4.6, h=10.0)                        # M3 hex coupler nut
ROD = dict(r=2.0, length=80.0, thread_r=1.5, thread_h=8.0)
ROD_Z = 40.0                                     # rod axis height
ROD_Y = 35.0
CLAMP = dict(w=20.0, d=24.0, h=12.0)             # jaw block (X width, Y depth, Z height)
LEVER = dict(l=34.0, w=12.0, t=7.0)               # spring lever arm
PAD = dict(r=1.6, h=16.0)                        # silicone pad (fits ~1 mm stem)
SPRING = dict(r=3.0, h=14.0)                     # preload return spring
DISH = dict(r=30.0, h=12.0, wall=2.0)            # weighing dish
STEM = dict(r=0.5, h=55.0)                       # arabidopsis stem (context)


def box(sx, sy, sz):
    return trimesh.creation.box(extents=[sx, sy, sz])


def cyl(r, h, sections=48, axis="z"):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=sections)
    if axis == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    elif axis == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    return m


def at(mesh, x=0.0, y=0.0, z=0.0):
    mesh.apply_translation([x, y, z])
    return mesh


def union(meshes):
    return boolean.union(meshes, engine="manifold")


def difference(a, bs):
    return boolean.difference([a] + bs, engine="manifold")


def wedge(sx, sy, sz, axis="z", apex="+y"):
    """V-groove cutter: triangular prism, cross-section sx (X) by sz, apex inward.

    axis='z' extrudes the prism vertically (stem channel); apex '+y'/'-y'
    points the V toward +Y / -Y in the horizontal cross-section.
    """
    v = np.array([
        [-sx / 2, -sy / 2, sz / 2], [sx / 2, -sy / 2, sz / 2], [0, -sy / 2, -sz / 2],
        [-sx / 2, sy / 2, sz / 2], [sx / 2, sy / 2, sz / 2], [0, sy / 2, -sz / 2],
    ])
    f = [[0, 2, 1], [3, 4, 5], [0, 1, 4], [0, 4, 3],
         [1, 2, 5], [1, 5, 4], [2, 0, 3], [2, 3, 5]]
    m = trimesh.Trimesh(vertices=v, faces=f)
    if axis == "z":
        ang = np.pi / 2 if apex == "+y" else -np.pi / 2
        m.apply_transform(trimesh.transformations.rotation_matrix(ang, [1, 0, 0]))
    return m


# ---------------------------------------------------------------- part builders
def part_base_plate():
    m = box(BASE["sx"], BASE["sy"], BASE["sz"])
    holes = [cyl(2.2, BASE["sz"] + 2) for _ in range(4)]
    for i, (hx, hy) in enumerate([(8, 8), (BASE["sx"] - 8, 8), (8, BASE["sy"] - 8), (BASE["sx"] - 8, BASE["sy"] - 8)]):
        holes[i] = at(holes[i], hx - BASE["sx"] / 2, hy - BASE["sy"] / 2, 0)
    return at(difference(m, holes), BASE["sx"] / 2, BASE["sy"] / 2, BASE["sz"] / 2)


def part_mount_block():
    m = box(MOUNT["sx"], MOUNT["sy"], MOUNT["sz"])
    pocket = box(PIEZO["sx"] + 1.0, PIEZO["sy"] + 1.0, PIEZO["sz"] + 1.0)
    pocket = at(pocket, MOUNT["sx"] / 2 - (PIEZO["sx"] + 1.0) / 2 + 0.5, 0, 0)
    front_hole = at(cyl(2.5, 6, axis="x"), MOUNT["sx"] - 3, 0, 0)
    bolts = [at(cyl(2.2, MOUNT["sz"] + 2), -MOUNT["sx"] / 2 + 5, -MOUNT["sy"] / 2 + 6, 0),
              at(cyl(2.2, MOUNT["sz"] + 2), -MOUNT["sx"] / 2 + 5, MOUNT["sy"] / 2 - 6, 0)]
    m = difference(m, [pocket, front_hole] + bolts)
    return at(m, MOUNT["x"], MOUNT["y"], BASE["sz"] + MOUNT["sz"] / 2)


def part_piezo():
    return at(box(PIEZO["sx"], PIEZO["sy"], PIEZO["sz"]),
              MOUNT["x"] + MOUNT["sx"] - PIEZO["sx"] / 2, ROD_Y, ROD_Z)


def part_end_cap():
    cap = box(ENDCAP["sx"], ENDCAP["sy"], ENDCAP["sz"])
    stud = at(cyl(STUD["r"], STUD["h"], axis="x"), ENDCAP["sx"] / 2 + STUD["h"] / 2, 0, 0)
    m = union([cap, stud])
    return at(m, MOUNT["x"] + MOUNT["sx"] + ENDCAP["sx"] / 2, ROD_Y, ROD_Z)


def part_coupler_nut():
    nut = cyl(NUT["r"], NUT["h"], sections=6, axis="x")
    bore = cyl(STUD["r"] + 0.2, NUT["h"] + 2, axis="x")
    m = difference(nut, [bore])
    x0 = MOUNT["x"] + MOUNT["sx"] + ENDCAP["sx"] + STUD["h"]
    return at(m, x0 + NUT["h"] / 2, ROD_Y, ROD_Z)


def rod_x0():
    return MOUNT["x"] + MOUNT["sx"] + ENDCAP["sx"] + STUD["h"] + NUT["h"]


def part_rod():
    body = at(cyl(ROD["r"], ROD["length"] - ROD["thread_h"], axis="x"), (ROD["length"] - ROD["thread_h"]) / 2, 0, 0)
    thread = at(cyl(ROD["thread_r"], ROD["thread_h"], axis="x"), -ROD["thread_h"] / 2, 0, 0)
    collar = at(cyl(3.5, 6, axis="x"), ROD["length"] - 3, 0, 0)
    m = union([body, thread, collar])
    return at(m, rod_x0() + ROD["length"] / 2, ROD_Y, ROD_Z)


def part_clamp_lower():
    m = box(CLAMP["w"], CLAMP["d"], CLAMP["h"])
    groove = wedge(CLAMP["w"] + 2, 8.0, 8.0, axis="z", apex="+y")
    groove = at(groove, 0, -CLAMP["d"] / 2, 0)
    m = difference(m, [groove])
    m = difference(m, [at(cyl(1.5, CLAMP["w"] + 2, axis="x"), 0, 0, CLAMP["h"] / 2 - 2)])
    x = rod_x0() + ROD["length"] - CLAMP["w"] / 2
    return at(m, x, ROD_Y, ROD_Z + CLAMP["h"] / 2 + 2)


def part_clamp_lever():
    arm = box(LEVER["l"], LEVER["w"], LEVER["t"])
    pad = at(cyl(PAD["r"], PAD["h"], axis="z"), -LEVER["l"] / 2 + 6, 0, -LEVER["t"] / 2 - 1.0)
    m = union([arm, pad])
    groove = wedge(LEVER["l"] + 2, 8.0, 8.0, axis="z", apex="-y")
    groove = at(groove, -LEVER["l"] / 2 + 6, LEVER["w"] / 2, -LEVER["t"] / 2 - 1.0)
    m = difference(m, [groove])
    pivot = at(cyl(2.0, LEVER["w"] + 2, axis="y"), LEVER["l"] / 2 - 4, 0, 0)
    m = difference(m, [pivot])
    x = rod_x0() + ROD["length"] - CLAMP["w"] / 2
    return at(m, x, ROD_Y, ROD_Z + CLAMP["h"] + LEVER["t"] / 2 + 3)


def part_preload_spring():
    return at(cyl(SPRING["r"], SPRING["h"], axis="x"),
              MOUNT["x"] - SPRING["h"] / 2 - 2, ROD_Y, ROD_Z)


def part_silicone_pads():
    p1 = at(cyl(PAD["r"], PAD["h"], axis="z"), 0, 0, 0)
    p2 = at(cyl(PAD["r"], PAD["h"], axis="z"), 0, 0, 0)
    x = rod_x0() + ROD["length"] - CLAMP["w"] / 2
    return [at(p1, x, ROD_Y, ROD_Z + CLAMP["h"] / 2 + 2), at(p2, x, ROD_Y, ROD_Z + CLAMP["h"] + 3)]


def part_weighing_dish():
    outer = cyl(DISH["r"], DISH["h"])
    inner = at(cyl(DISH["r"] - DISH["wall"], DISH["h"], axis="z"), 0, 0, DISH["wall"])
    m = difference(outer, [inner])
    return at(m, rod_x0() + ROD["length"] + 5, ROD_Y, DISH["h"] / 2)


def part_stem_context():
    return at(cyl(STEM["r"], STEM["h"], axis="z"),
              rod_x0() + ROD["length"] - CLAMP["w"] / 2, ROD_Y, ROD_Z + CLAMP["h"] + 4 + STEM["h"] / 2)


PARTS = {
    "01_base_plate": (part_base_plate, "aluminium"),
    "02_mount_block": (part_mount_block, "aluminium"),
    "03_piezo_stack": (part_piezo, "PZT ceramic"),
    "04_end_cap_stud": (part_end_cap, "steel"),
    "05_coupler_nut": (part_coupler_nut, "steel"),
    "06_steel_rod": (part_rod, "steel"),
    "07_clamp_lower_jaw": (part_clamp_lower, "3D print"),
    "08_clamp_lever": (part_clamp_lever, "3D print"),
    "09_preload_spring": (part_preload_spring, "spring steel"),
    "10_silicone_pad_a": (lambda: part_silicone_pads()[0], "silicone"),
    "10_silicone_pad_b": (lambda: part_silicone_pads()[1], "silicone"),
    "11_weighing_dish": (part_weighing_dish, "glass/PP"),
    "12_stem_context": (part_stem_context, "plant"),
}


# ---------------------------------------------------------------- rendering
def render(mesh, path, title, color, elev=20, azim=-60, figsize=(7, 5)):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    tri = mesh.triangles
    normals = mesh.face_normals
    light = np.array([0.4, -0.6, 0.7])
    light = light / np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(np.abs(normals @ light), 0, 1)
    base = np.array(matplotlib.colors.to_rgb(color))
    colors = shade[:, None] * base[None, :]

    fig = plt.figure(figsize=figsize, dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    pc = Poly3DCollection(tri, facecolors=colors, edgecolors="none")
    ax.add_collection3d(pc)
    mins, maxs = mesh.bounds
    c = (mins + maxs) / 2
    r = (maxs - mins).max() / 2 * 1.15
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=11)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


COLORS = {
    "aluminium": "#b8bcc4", "PZT ceramic": "#c8a24a", "steel": "#8f979e",
    "3D print": "#4a7fc8", "spring steel": "#7fae6e", "silicone": "#d96a5a",
    "glass/PP": "#a8d4e6", "plant": "#5a8f4a",
}


def main():
    meshes = {}
    for name, (fn, mat) in PARTS.items():
        m = fn()
        meshes[name] = m
        m.export(os.path.join(PARTS_DIR, name + ".stl"))
        render(m, os.path.join(RENDERS_DIR, name + ".png"),
               f"{name}  ({mat})", COLORS[mat])
        print("part:", name)

    assembly = boolean.union(list(meshes.values()), engine="manifold")
    assembly.export(os.path.join(PARTS_DIR, "00_assembly.stl"))
    render(assembly, os.path.join(RENDERS_DIR, "00_assembly.png"),
           "Drop-Dropper assembly (rod axis horizontal, dish under shoot)",
           "#4a7fc8", elev=18, azim=-55, figsize=(10, 6))

    exploded = []
    for name, m in meshes.items():
        if name in ("12_stem_context", "11_weighing_dish"):
            exploded.append(m)
            continue
        shift = {"09_preload_spring": -25, "04_end_cap_stud": -12, "05_coupler_nut": 12,
                 "06_steel_rod": 30, "07_clamp_lower_jaw": 55, "08_clamp_lever": 75,
                 "10_silicone_pad_a": 55, "10_silicone_pad_b": 75}.get(name, 0)
        exploded.append(at(m.copy(), shift, 0, 0))
    exp = boolean.union(exploded, engine="manifold")
    exp.export(os.path.join(PARTS_DIR, "00_assembly_exploded.stl"))
    render(exp, os.path.join(RENDERS_DIR, "00_assembly_exploded.png"),
           "Exploded view along rod axis", "#4a7fc8", elev=18, azim=-55, figsize=(12, 6))
    print("assembly + exploded done")


if __name__ == "__main__":
    main()
