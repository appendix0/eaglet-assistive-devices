// Door-knob lever adapter -- parametric starting point
// A cap that slips over a round door knob and turns it into a lever, so the
// knob can be opened by pushing down with the palm or forearm instead of gripping
// and twisting. Held by three radial screws with soft tips.
// Licence: CC BY-SA 4.0 (see LICENSE). Status: unrendered draft, see cad/README.md.
// Never modify the lock or latch itself; check the lever does not hit the frame.

/* [Door knob] */
knob_d = 55;          // knob diameter at its widest, mm
knob_depth = 25;      // how far the cap slides over the knob, mm
clearance = 0.8;      // radial clearance, mm -- screws take up the slack

/* [Cap] */
wall = 4;             // side wall, mm
front = 5;            // front face thickness, mm

/* [Lever] */
lever_len = 100;      // knob centre to lever tip, mm
lever_w = 24;         // mm
lever_t = 14;         // mm
tip_r = 12;           // rounded tip radius, mm

/* [Clamp screws] */
screw_hole_d = 3.4;   // pilot for M4 thread-forming screws
boss_d = 12;          // mm
boss_len = 6;         // how far the boss stands out from the wall, mm

$fn = 96;

inner_r = knob_d / 2 + clearance;
outer_r = inner_r + wall;
cap_h = knob_depth + front;

assert(lever_len > outer_r + tip_r, "lever_len too short for this knob");
assert(lever_t <= cap_h, "lever_t must not exceed knob_depth + front");

module lever() {
    // flush with the front face, pointing along +X
    translate([0, 0, cap_h - lever_t])
        hull() {
            translate([0, -lever_w / 2, 0]) cube([1, lever_w, lever_t]);
            translate([lever_len - tip_r, 0, 0]) cylinder(h = lever_t, r = tip_r);
        }
}

module bosses() {
    for (a = [60, 180, 300])
        rotate([0, 0, a]) translate([0, 0, knob_depth / 2]) rotate([0, 90, 0])
            cylinder(h = outer_r + boss_len, d = boss_d);
}

module screw_holes() {
    for (a = [60, 180, 300])
        rotate([0, 0, a]) translate([0, 0, knob_depth / 2]) rotate([0, 90, 0])
            cylinder(h = outer_r + boss_len + 1, d = screw_hole_d);
}

difference() {
    union() {
        cylinder(h = cap_h, r = outer_r);
        lever();
        bosses();
    }
    translate([0, 0, -1]) cylinder(h = knob_depth + 1, r = inner_r);   // knob cavity (door side open)
    screw_holes();
}
