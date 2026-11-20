// Built-up utensil handle -- parametric starting point
// Slides over a spoon/fork handle to give a thicker, easier grip.
// Set the parameters from the case's 02-requirements.md measurements.
// Licence: CC BY-SA 4.0 (see LICENSE). Status: unrendered draft, see cad/README.md.

/* [Grip] */
grip_d = 32;          // outer diameter, mm -- the cylinder the user can hold comfortably
grip_len = 90;        // length, mm
end_chamfer = 3;      // chamfer at both ends, mm

/* [Utensil slot] */
slot_shape = "rect";  // "rect" for flat handles, "round" for round handles
slot_w = 12;          // flat handle width, or round handle diameter, mm
slot_t = 3;           // flat handle thickness, mm (ignored for "round")
clearance = 0.3;      // per side, mm. PLA/PETG 0.2-0.4; TPU 0 (friction fit)
slot_through = true;  // true: slot runs the full length
slot_depth = 70;      // blind slot depth from the top end, mm (when slot_through = false)

/* [Finger grooves] */
grooves = 4;          // 0 = smooth grip
groove_r = 6;         // groove profile radius, mm
groove_depth = 1.5;   // mm
groove_start = 15;    // centre of first groove from the bottom end, mm
groove_pitch = 18;    // spacing, mm

$fn = 96;

assert(grip_d / 2 - groove_depth > slot_w / 2 + 2, "grip_d too small for slot and grooves");
assert(grooves == 0 || groove_start + (grooves - 1) * groove_pitch <= grip_len - groove_r,
       "grooves do not fit in grip_len");

module body() {
    c = end_chamfer;
    union() {
        cylinder(h = c, r1 = grip_d / 2 - c, r2 = grip_d / 2);
        translate([0, 0, c]) cylinder(h = grip_len - 2 * c, r = grip_d / 2);
        translate([0, 0, grip_len - c]) cylinder(h = c, r1 = grip_d / 2, r2 = grip_d / 2 - c);
    }
}

module slot() {
    depth = slot_through ? grip_len + 2 : slot_depth + 1;
    z0 = slot_through ? -1 : grip_len - slot_depth;
    translate([0, 0, z0])
        if (slot_shape == "round")
            cylinder(h = depth, d = slot_w + 2 * clearance);
        else
            translate([-(slot_w / 2 + clearance), -(slot_t / 2 + clearance), 0])
                cube([slot_w + 2 * clearance, slot_t + 2 * clearance, depth]);
}

module groove_ring(z) {
    translate([0, 0, z])
        rotate_extrude()
            translate([grip_d / 2 + groove_r - groove_depth, 0]) circle(r = groove_r);
}

difference() {
    body();
    slot();
    if (grooves > 0)
        for (i = [0 : grooves - 1]) groove_ring(groove_start + i * groove_pitch);
}
