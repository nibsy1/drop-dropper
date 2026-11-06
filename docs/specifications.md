# Specifications — Drop-Dropper

All dimensions in millimetres. Rod axis = X (horizontal), stem axis = Z (vertical), bench top = z = 0.

## 1. Mechanical parts

| Part | Dimensions | Material | Notes |
|---|---|---|---|
| Base plate | 110 x 70 x 6 | Aluminium | 4x Ø4.5 corner holes (M4 bolts / rubber feet) |
| Actuator mount block | 25 x 30 x 34, on base at x=15, y=35 | Aluminium | 10.5 x 10.5 x 20 pocket for piezo, Ø5 front hole for stud, 2x M4 bolt holes |
| Piezo stack | 10 x 10 x 20, 150 V multilayer PZT | PZT ceramic | ~15–20 µm free displacement, blocking force ~300–800 N class; buy 2–3 spares |
| End cap + stud | 12 x 12 x 3 cap, M3 x 8 stud | Steel | Epoxy-bonded to piezo front face |
| Coupler nut | M3 hex, across-flats Ø9.2, length 10 | Steel | Locknut joins stud to rod |
| Steel rod | Ø4 x 80, M3 threaded rear end, Ø7 collar at tip | Stainless steel | Axis at z = 40, y = 35; first bending resonance kept well above operating range |
| Clamp lower jaw | 20 x 24 x 12, 90° V-groove (vertical channel), pivot cross-hole | 3D print (PETG/ASA) | Fixed to rod tip |
| Clamp lever (upper jaw) | 34 x 12 x 7 arm with V-groove + silicone pad | 3D print | Spring-loaded, closes with two fingers, pivot Ø4 pin |
| Silicone pads | Ø3.2 x 16, in both V-grooves | Silicone | Grips Ø1 mm stem without point load; replaceable |
| Preload spring | Ø6 x 14 compression | Spring steel | Keeps rod+clamp pressed against piezo face (~5–10 N) |
| Weighing dish | Ø60 x 12, 2 mm wall | Glass / PP | Sits on bench under the rosette |

## 2. Operating point

- Drive: function generator -> HV linear amplifier, **unipolar 0–150 V** (stack must never see tension).
- Frequency: adjustable, design range **500 Hz – 2 kHz** (start ~1 kHz).
- Amplitude: 5–30 µm at the rod tip (adjust via amplifier gain).
- Physics check: shedding ~0.5–2 mm guttation droplets needs roughly >20–25 g peak
  acceleration. With 15 µm at 1 kHz: a = (2*pi*1000)^2 * 15e-6 ≈ 590 m/s² ≈ 60 g — sufficient.
- Rod motion is **axial (horizontal)**; detached droplets fall vertically into the dish.

## 3. Electrical

- Piezo capacitance ~1–2 µF; amplifier must supply ~150 V at the operating frequency
  (current ≈ 2*pi*f*C*V; at 1 kHz, 150 V, 1.5 µF ≈ 1.4 A peak — use an amplifier rated
  >= 100 mA continuous / several A peak, e.g. A-301-class or used lab HV amp).
- Wiring: HV lead from amplifier to stack; keep HV connections insulated; fuse the supply.
- Safety: 150 V DC is hazardous — enclosed terminals, power off while handling the plant.

## 4. Clamp force budget

- Stem Ø <= 1 mm; silicone pads distribute the grip over ~16 mm length.
- Closing force limited by the lever return spring to a few N — enough to transmit
  vibration, far below stem crush load.
- Clamp must be rigidly fixed to the rod (no soft interface) so motion is 1:1.
