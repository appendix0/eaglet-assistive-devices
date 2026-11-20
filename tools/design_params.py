#!/usr/bin/env python3
"""Turn measurements into starting design parameters, using published rules.

Every rule names its source by reference ID [Rn] in docs/references.md. These are
starting values for a prototype, not a substitute for the real-use evaluation.

Usage:
  python3 tools/design_params.py grip --hand-length 175
  python3 tools/design_params.py lever [--torque 1.2] [--width 24] [--thickness 18]
"""
import argparse
import math
import sys

# [R3] Kong & Lowe 2005: optimal cylindrical handle diameter for grip force tasks
# was 19.7% of the user's hand length; 30, 35, 40 mm rated most comfortable.
GRIP_RATIO = 0.197
GRIP_COMFORT_RANGE_MM = (30.0, 40.0)
# [R1] Jordon et al. 2026: 29 of 35 people with RA chose the 1.50 in handle.
RA_PREFERRED_MM = 38.1

# [R5] ADA 2010 Standards 309.4: operating force 5 lbf (22.2 N) maximum,
# no tight grasping, pinching or twisting of the wrist.
ADA_MAX_FORCE_N = 22.2
# [R6] ICC A117.1-2017 (as quoted by Greene, iDigHardware): rotational hardware
# 28 lbf-in (3.16 N*m) maximum. Used as the design torque when unmeasured.
LBF_IN_TO_NM = 0.112985
DEFAULT_TORQUE_NM = 28 * LBF_IN_TO_NM

# [R7] Prusament PETG TDS (search excerpt; verify): printed tensile yield, horizontal 47 MPa;
# interlayer adhesion 18 MPa.
PETG_YIELD_XY_MPA = 47.0
PETG_INTERLAYER_MPA = 18.0
# Team assumption (no source): someone leans on or yanks the lever.
DEFAULT_MISUSE_N = 200.0
MIN_SAFETY_FACTOR = 2.0


def grip_diameter(hand_length_mm):
    """Return (kong_lowe_optimum_mm, comfort_range_mm, ra_preferred_mm)."""
    if not 120 <= hand_length_mm <= 230:
        raise ValueError("hand length should be wrist crease to middle fingertip, 120-230 mm")
    return GRIP_RATIO * hand_length_mm, GRIP_COMFORT_RANGE_MM, RA_PREFERRED_MM


def min_lever_length_mm(torque_nm=DEFAULT_TORQUE_NM, max_force_n=ADA_MAX_FORCE_N):
    """Shortest lever (knob centre to the point pressed) that keeps force <= limit."""
    if torque_nm <= 0 or max_force_n <= 0:
        raise ValueError("torque and force must be positive")
    return torque_nm / max_force_n * 1000.0


def lever_bending_stress_mpa(length_mm, width_mm, thickness_mm, load_n=DEFAULT_MISUSE_N):
    """Root bending stress of a rectangular cantilever loaded at its tip.

    The user pushes down, in the plane of the door, so the section depth is the
    lever width (lever_w in cad/knob_lever.scad), not its thickness:
    sigma = M*c/I = 6*F*L / (t*w^2). Print the lever with its front face on the
    bed so these stresses run along the layers (XY).
    """
    if min(length_mm, width_mm, thickness_mm, load_n) <= 0:
        raise ValueError("dimensions and load must be positive")
    return 6.0 * load_n * length_mm / (thickness_mm * width_mm ** 2)


def lever_report(torque_nm, width_mm, thickness_mm, load_n, margin_mm=5.0):
    length = math.ceil(min_lever_length_mm(torque_nm) + margin_mm)
    stress = lever_bending_stress_mpa(length, width_mm, thickness_mm, load_n)
    sf = PETG_YIELD_XY_MPA / stress
    return {"lever_len_mm": length, "stress_mpa": stress, "safety_factor": sf,
            "ok": sf >= MIN_SAFETY_FACTOR}


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grip", help="built-up handle diameter")
    g.add_argument("--hand-length", type=float, required=True, help="mm")
    lv = sub.add_parser("lever", help="door-knob lever length and strength")
    lv.add_argument("--torque", type=float, default=DEFAULT_TORQUE_NM,
                    help=f"measured knob torque, N*m (default {DEFAULT_TORQUE_NM:.2f}, R6 maximum)")
    lv.add_argument("--width", type=float, default=24.0, help="lever width in the push direction (lever_w), mm")
    lv.add_argument("--thickness", type=float, default=14.0, help="lever thickness out of the door (lever_t), mm")
    lv.add_argument("--load", type=float, default=DEFAULT_MISUSE_N, help="misuse load, N")
    a = p.parse_args(argv[1:])

    if a.cmd == "grip":
        opt, (lo, hi), ra = grip_diameter(a.hand_length)
        print(f"Kong & Lowe optimum [R3]   : {opt:.1f} mm  (19.7% x {a.hand_length:g} mm)")
        print(f"Comfortable range [R3]     : {lo:.0f}-{hi:.0f} mm")
        print(f"Chosen by most RA users [R1]: {ra:.1f} mm (1.50 in)")
        print("Start at the optimum, print 2-3 diameters around it, let the user choose.")
    else:
        r = lever_report(a.torque, a.width, a.thickness, a.load)
        print(f"Design torque              : {a.torque:.2f} N*m")
        print(f"Lever length [R5, R6]      : >= {r['lever_len_mm']} mm  "
              f"(force at tip <= {ADA_MAX_FORCE_N} N, +5 mm margin)")
        print(f"Bending at {a.load:g} N misuse : {r['stress_mpa']:.1f} MPa  "
              f"(PETG XY yield {PETG_YIELD_XY_MPA:g} MPa [R7])")
        print(f"Safety factor              : {r['safety_factor']:.2f}  "
              f"{'OK' if r['ok'] else f'TOO LOW - need >= {MIN_SAFETY_FACTOR}; thicken or widen'}")
        print("Print front face down so bending runs along the layers "
              f"(interlayer only {PETG_INTERLAYER_MPA:g} MPa [R7]).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
