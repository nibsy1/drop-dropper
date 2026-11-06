# Design decisions (resolved)

1. **No commercial tool exists** for vibration-based guttation harvesting; closest
   inspirations are vibratomes (voice-coil vibrating blades), ultrasonic de-icing
   droplet shedding, and electrodynamic leaf shakers. We build our own.
2. **Actuator: 150 V multilayer piezo stack** (10 x 10 x 20 mm, generic PZT, ~$10–25,
   buy spares) — precise high-frequency axial motion, no wear parts.
3. **Drive: function generator + HV linear amplifier (0–150 V unipolar)** — independent
   adjustment of frequency and amplitude; cheapest credible option is an A-301-class
   low-cost HV amp or used lab unit.
4. **Orientation: horizontal** — piezo and rod horizontal, clamp grips the stem from the
   side, shoot upright above the weighing dish, so falling droplets never hit the piezo.
   Axial rod motion = horizontal shaking; droplets fall into the dish by gravity.
5. **Rod–piezo coupling: bonded M3 stud on a steel end-cap + locknut coupler** —
   reversible, keeps the stack in compression.
6. **Rod: Ø4 x 80 mm stainless, horizontal at z = 40** — stiff, resonance far above the
   ~1 kHz operating range.
7. **Clamp: two-piece 3D-printed, silicone V-pads for the Ø1 mm stem, spring-loaded lever
   closed with two fingers, force-limiting spring** — holds the shoot during vibration
   without crushing the stem.
8. **Preload return spring** presses rod+clamp back against the piezo face (needed because
   the horizontal layout has no gravity preload and the unipolar drive can only push).
9. **Collection: plain weighing dish** under the rosette — no balance/camera integration.
10. **CAD toolchain: parametric Python (trimesh + manifold3d) + matplotlib renders** —
    headless, scriptable, STL output for printing/machining.
