# CREATION-WALL ANATOMY — the 19 creation_unexplained deaths on the spent 48-task A+B draw

**Date:** 2026-11-07 · **Lane:** SIEVE successor-lane design (anatomy only — no machinery built, no fresh draw run, sealed exam and Friday pack untouched)
**Sources:** `nextgen_probe/diag2_bg_rows.json` (bg-lane rows; verdict source), `nextgen_probe/diag2_rows.json` (original-lane rows; reconciliation), `nextgen_probe/ng2_lane_bg.py` (the lane that issued the charges), `BG_GATE_RESULTS_2026-11-07.md`, `NOVEMBER_CONVERSION_PACKET.md`, `CENSUS_UPDATES_2026-11-06.md`, `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md` §3.1.

## 0. What the charge mechanically means

In the bg lane (`ng2_lane_bg.py`), a task is charged `creation_unexplained` when, in the
designated attempt — the first shape-compatible pretransform × the first functional
background account's downstream induction — `gen_candidates` returns `None`, i.e. at
least one output object has **zero surviving derivation candidates**. Two precisions
that matter for everything below:

- The bg lane's `gen_candidates` is richer than the original lane's: it returns
  `(cand_by_out, group_sizes)` or `(None, zero_out_indices)`, and split derivations
  are **group** derivations subject to a completeness prune ("prune split groups
  that cannot complete: every part index present", ng2_lane_bg.py ~lines 531–549).
  A candidate can therefore die in two ways: never generated, or generated and
  pruned because its split group cannot complete. One of the 19 (604001fa) dies
  the second way.
- φ (`phi_match` / `phi_consistent`) is a **functional** color map, many-to-one
  allowed, never injective-required. A zero candidate is therefore a
  shape/structure/source failure, not a color-map failure — a new color kills an
  object only when no shape route exists for it, or when the color must be bound
  per-instance (604001fa, 41e4d17e, 694f12f3; see §3).

**Method.** Each task's designated attempt was replayed with the lane's own
`segment` + `gen_candidates` under a generous deadline (120 s vs the lane's 25 s);
every task's zero objects reproduce identically, so no charge below is a budget
artifact of the replay. Zero objects were then read against rendered in/out grids
and settled by targeted computational checks (§2, per class). All 19 tasks carry
the charge in the bg-lane rows; 11 were already `creation_unexplained` under the
original lane, 8 arrived via the BG-GATE migration (marked † below — all 8 were
ex-`inconsistent_phi`). In all 19 the designated pretransform is `id|x1`; the
designated account is (agnostic, modal→modal) except af22c60d (modal→sea) and
e66aafb8 (modal→border_modal). **In every one of the 19, the failing stage is
candidate generation** — by construction (the charge is issued there) and verified
by replay; cover and certification are downstream and are never reached for the
zero objects.

## 1. The 19, classified

Classes (defined in §2): **Q** quotient/compression grid · **L** line/ray drawing ·
**R** replication/stamping/tiling · **S** symmetry completion · **M** mirror-tiling ·
**F** frame generalization · **C** count/multiset-parametric synthesis ·
**T** procedural texture · **P** part-selective split · **G** color-class gather.

| Task | Pool | Zero objects in designated attempt (cells) | What the output creates that the input lacks (operational) | Class | Minimal extension (mechanism) |
|---|---|---|---|---|---|
| 67b4a34d | A | 10 / 8+1 / 10 | A 4×4 symbolic grid computed from the 16×16 kaleidoscope input; the whole non-bg mass of the quotient is one underivable object | Q | Quotient account (scene stage): block partition + per-block classifier in Π |
| e66aafb8 † | A | 34 / 7 / 23 / 15 / 29 | A small grid whose size varies per pair (8×5, 4×3, 5×6, 3×8, 6×7 from 24×24) — the texture's fundamental domain emitted as the output | Q | Quotient account with the domain extracted from the scene's symmetry/period structure (not a fixed block grid) |
| 9110e3c5 † | B | 4 / 4 / 3 / – / 4 / 3 / 4 | A 3×3 binary (ink 8) encoding computed from a 7×7 input; the ink cells form the zero objects | Q | Quotient account: region partition + predicate classifier in Π (classifier unidentified, §2-Q) |
| 5d2a5c43 † | B | 3 / – / 2 / – / 4 | A 6×4 grid from a 6×9 input (rows 1:1, columns compressed, ink 4→8); zero objects are tiny blobs of color 0 — the *input's* background ink appearing as foreground inside the quotient | Q | Quotient account (column compression); the zero objects are the quotient grid's own non-bg cells |
| e3497940 | B | 14 / 10 / 12 | A narrow strip grid (10×4 / 8×4) summarizing the input row-by-row — spine + branch events compressed to a strip | Q | Quotient account with strip (row-band) partition |
| 55783887 | A | 6 / 13 / 7 / 26 / 22 | Diagonal lattice lines of color 1 drawn through/between scattered same-color dots on a uniform field; pair 3: rays extended both ways weave a diagonal lattice; lines merge with dots into single components | L | Stroke derivation: raster segment/ray, anchors from Π region-queries, direction in the 8 lattice directions, extent rule (to-anchor / to-edge) |
| 5c0a986e | B | 20 / 6+6 / 7+7 | Diagonal rays emitted from 2×2 blocks — one in a fresh color (1), one in the block's own color — running to the canvas edge; ray merges with its block | L | Stroke derivation (ray mode: anchor object + direction + to-edge extent) |
| 41e4d17e | B | 80 / 41 | Full-canvas straight lines in color 6 — **absent from the input** — drawn at the rows/columns through two ring objects' centers; lines touch the rings, so lines+rings segment as one zero object | L | Stroke derivation (full-span axis mode) + instance-color binding for the fresh ink |
| 27f8ce4f | B | 36 / 36 / 27 / 27 | The input's single 3×3 pattern stamped at 3–4 positions on a 9×9 canvas; copies touch diagonally and segment as one object. **Verified: output = exact translates of the input pattern, 0 leftover cells, every pair** | R | Stamp derivation: one binding, a *set* of placements (enumerated/lattice/marker-read) |
| 363442ee | B | 63 / 45 / 63 | A 3×4 motif tiled across the canvas — pair 2 verified as lattice tiling with a shared spine column; pairs 0–1 place copies at positions marked by "1" dots; copies merge with the spine into one component | R | Stamp derivation, lattice + marker placement modes |
| 85fa5666 | B | 52 / 48 / 19 / 17 | The input's sparse field of small objects extended over the whole canvas by repetition along a diagonal period; the repeated field segments (8-connected) as one mass | R | Stamp derivation at field scale: whole-scene pattern repeated at a bound period vector |
| af22c60d † | A | 620 / 592 / 592 / 674 | Occluded (0-filled) rectangles in a 30×30 texture filled in from the texture's own symmetry mates. **Verified: input is a strict subset of output — 100% of non-0 input cells preserved in all 4 pairs** | S | Symmetry-completion pretransform: close the (hole-masked) grid under a bound symmetry group, sourcing filled cells from their orbit mates, before segmentation |
| 760b3cac | B | 19 / 10 / 13 | A reflected copy of an object placed adjacent to it (width doubled); copy touches the original and merges with it (pair 0 also absorbs the neighboring object) | M | Reflected placement mode for derivations: pattern emitted at (reflection ∘ translation) outside its own bbox — the existing mirror kind only unions *within* the bbox |
| 08573cc6 | A | 20 / 27 / 54 | 2–3 concentric rectangular rings centered on a "1" marker, alternating the colors of two marker pixels; ring count and size grow across pairs | F | Frame iteration: ring count + color sequence as Π bindings around an addressed center (existing frame kind emits exactly one ring, margin 0/1, around canvas or a unique object) |
| 694f12f3 | B | 25+12 / 16+24 | An inner rectangle drawn *inside* each solid block, inset by 1, in a color **absent from the input** (2 in one block, 1 in the other), the composite block+inset matching no kind | F | Frame inset mode: ring at negative margin relative to a source object, ink as an instance-color binding |
| 3d6c6e23 | B | 9 / 4 / 9 | A filled pyramid whose cell count **equals** the count of scattered input dots. **Verified: cell count and full color multiset exactly preserved in all 3 pairs (9/4/9)** | C | Count-parametric shape synthesis: a canonical shape family (filled triangle) generated from a bound count/multiset read by a Π region-query |
| e9afcf9a † | B | 6 / 6 | A two-color checkerboard texture synthesized over the canvas from the two input bar colors | T | Texture derivation: periodic fill (checkerboard family) of a bound region from two bound colors + phase |
| 604001fa | A | 10+9+8 / 8 / 8+7 / 7+8 | Copies of the color-1 *part* of composite input objects (shape + a 3-cell color-7 appendage), each recolored to a different fresh color (3, 6, 4, 8 — all absent from input). **Verified: every zero shape equals a color-1 part exactly, under dihedral, in every pair** | P | Split-and-discard: a split group may complete on a subset of parts (dropped parts explicit), and the kept part's color binds per derivation instance (φ is global and functional — it cannot map color 1 to 3, 6, **and** 4 in one program) |
| 6d0160f0 | B | 44 / 43 / 43 / 44 | **Nothing is created.** The zero object is the input's entire color-5 scaffold class (plus 4 kept neighbor cells) gathered into one component by the deletion of everything else; no connected input object equals it | G | Color-class pattern source: all cells of a bound color offered to candidate generation as one pattern (a source-inventory addition, not a new kind) |

† arrived at creation via the BG-GATE migration (ex-`inconsistent_phi`).

## 2. Class definitions and the evidence that settles them

**Q — Quotient / compression grids (5).** The output (or its non-bg mass) is a new
grid whose cells are *computed* from input regions by a scene-level classification.
No object-level derivation can emit a grid, so candidate generation is the wrong
stratum for these tasks entirely; the mechanism belongs at scene stage, beside the
pretransforms and the bg accounts. Within the class: block quotient (67b4a34d,
b = 4), symmetry-domain quotient (e66aafb8 — output size varies per pair, so the
domain is read off the texture's symmetry, not a fixed divisor), symbolic/predicate
quotient (9110e3c5, 3×3 binary), column quotient (5d2a5c43, rows 1:1, 9→4 columns),
strip quotient (e3497940). **Classifier honesty:** the exact per-block classifier
was *not* identified at rows grade for 67b4a34d, 9110e3c5, or 5d2a5c43, and the
obvious candidates were tested and killed — block-modal (67b4a34d: 3/16, 1/16, 5/16
cells), kaleidoscope fold-majority (3/16, 3/16, 6/16), mod-4 translation-orbit
majority (3/16, 3/16, 6/16), stride sampling (best offset 6/16); (3,2,2)-block
majority and four predicate classifiers for 9110e3c5 (best 6/9); block any/all/
majority classifiers and row-period compression for 5d2a5c43 (best 20/24 on one
pair, ≤17/24 elsewhere). The class and the failing stage are certain; the
classifier is a Π-binding problem the build must solve per task family, and the
killed hypotheses are recorded here so they are not re-tried.

**L — Line/ray drawing (3).** Straight lattice strokes — diagonal segments between
addressed anchors (55783887), diagonal rays from an object to the edge (5c0a986e),
full-span axis lines through object centers (41e4d17e). The grammar has no stroke
kind at all: its kinds transform existing patterns. Anchors are exactly what
§3.1's addressed-content parameters supply (dots, centers); the stroke itself,
its direction/extent rules, and (41e4d17e) its fresh ink are not in §3.1.

**R — Replication / stamping / tiling (3).** One source pattern emitted at a *set*
of placements. The existing `copy` kind binds one instance per derivation and the
cover stage can in principle assemble several copies — but where copies touch
(27f8ce4f diagonally, 363442ee through the shared spine, 85fa5666 through the
diagonal field) they segment as **one** output object, and one segmented object
needs one derivation. 27f8ce4f is verified pure: the output is exactly 3–4
translates of the input pattern with zero leftover cells in every pair — no new
shape, no new color; the entire gap is multi-instance emission of a merged
component.

**S — Symmetry completion (1).** af22c60d: the output *contains* the input
(verified 100% preservation of non-0 cells, all pairs) and fills the occluded
rectangles from the pattern's symmetry mates. No single global involution
completes it (transpose alone explains 51/100, 65/117, 25/34, 49/59 filled cells;
the existential over all 8 dihedral maps covers 79/100, 98/117, 30/34, 57/59) —
the completing structure is the texture's own symmetry group (dihedral mates plus
period translates). The lane's pretransforms apply dihedral maps to the *whole*
grid; completion is a different operation: fill-by-orbit.

> **RECONSTRUCTION begins (2026-11-07).** The on-disk text above ends mid-word
> ("fill-by-or") at the truncation point, where a literal
> `[truncated 8182 chars]` marker stood (removed by this repair). Everything
> from here to the end of this file is a **reconstruction at source grade, not
> the lost original**. It is rebuilt only from surviving sources:
> `CREATION_MACHINERY_SPEC_2026-11-07.md` (written against the full anatomy —
> its mechanisms carry the anatomy's class detail, its §2 carries per-class
> task lists and unblocking expectations, its §5 summarizes §4 below),
> `CREATION_BUILD_PREREGISTRATION_2026-11-07.md` and
> `CREATION_BUILD_RESULTS_2026-11-07.md` (which record what the build took
> from the anatomy), the surviving §§0–2-S above, and §3.1 of
> `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md` (quoted verbatim where
> quoted). Where the build's measurement **corrected** an anatomy reading,
> the correction stands as the build recorded it and the anatomy reading is
> noted as superseded, never resurrected as fact. Where a detail cannot be
> grounded in these sources, the reconstruction says so in place.

### §2, remaining classes (reconstructed)

**M — Mirror-tiling (1).** 760b3cac: a reflected copy of an object placed
adjacent to it, the width doubled, the copy touching the original and merging
with it (in pair 0 absorbing the neighboring object as well). The lane's
existing mirror kind unions reflections *within* the source's bounding box;
the gap is a reflected placement *outside* the box — a reflection composed
with a translation (spec M-R, placement mode (iv)). Like R, the merged
component needs one derivation, and M-U carries the touching mass.

**F — Frame generalization (2).** 08573cc6: rings emitted around a "1" marker
center, ring count and size growing across pairs, colors alternating between
two marker pixels; 694f12f3: an inner rectangle drawn *inside* each solid
block, inset by 1, in a color absent from the input (2 in one block, 1 in the
other). The existing frame kind emits exactly one ring, at margin 0/1, around
the canvas or a unique object. The gaps: an iteration-count binding and a
color sequence bound from marker objects (08573cc6), an inset mode at
negative margin relative to a source object, the center as an
addressed-content parameter (the unique marker's position), and instance
colors for ink absent from the input (694f12f3; §0 above and P below).
**Superseded by build measurement** (build results, disclosed): the geometry
of 08573cc6 is a square **spiral** (segment lengths 5,5,4,3,2,…), not the
concentric rings this classification describes; the task stayed
creation_unexplained under the build's ring family. The concentric-ring
reading stands in this reconstruction only as the anatomy's original
classification, corrected at the point of use.

**C — Count/multiset-parametric synthesis (1).** 3d6c6e23: a filled shape
whose cell count equals the count of scattered input dots — verified in §1:
cell count and full color multiset are preserved exactly in all 3 pairs
(9/4/9). The grammar computes counts internally (its Π statistics) but no
kind *emits* a shape from a bound count; the gap is a count-parametric shape
kind: a canonical family (filled triangle) generated at exactly the count —
and colored from the multiset — that a Π region-query reads off a source
class.
**Corrected by build measurement** (build results, disclosed): the build's
recount does not sustain the "9/4/9" reading as per-color counts — the pair
totals are 9/4/9 across the whole scene, pair 2 being 5+3+1 over three
colors — and the shape the build measured and implemented is the odd-width
staircase of the scene's *total* count. The exact-preservation verdict of §1
(count and multiset, all pairs) is the anatomy's recorded verification; the
per-color decomposition is corrected at the point of use.

**T — Procedural texture (1).** e9afcf9a: a two-color checkerboard texture
synthesized over the canvas from the two input bar colors. No kind fills a
region periodically; the gap is a texture kind — periodic fill (checkerboard
family) of a bound region from two bound colors plus a phase (spec M-T).

**P — Part-selective split (1).** 604001fa dies the second death of §0:
generated, then pruned, because its split group cannot complete (every part
index present is required). Verified in §1: every zero shape equals the
color-1 *part* of a composite input object exactly, under dihedral, in every
pair, the appendage discarded; each kept part is recolored to a *different*
fresh color (3, 6, 4, 8 — all absent from the input), which the global
functional φ cannot bind (φ would have to map color 1 to 3, 6, **and** 4 in
one program). The gaps: split-and-discard (a group may complete on a subset
of parts, dropped parts explicit, kept-set identical across pairs) and
per-instance color binding in place of the global φ (spec M-P).

**G — Color-class gather (1).** 6d0160f0 creates nothing (§5 below): the zero
object is the input's entire color-5 scaffold class (plus 4 kept neighbor
cells) gathered into one component by the deletion of everything else, and no
connected input object equals it. The gap is in the pattern-source inventory,
not the kinds: all cells of a bound color offered to candidate generation as
one pattern (spec M-G).
**Build postscript** (build results, disclosed): the build could not
identify the mechanism for this task — the +4 scaffold cells are *created*,
not preserved (cell-diff verified) — and records that §2-G's detail was in
the truncated portion of this file. The gather reading above is grounded in
§1's table row and the spec's M-G; the +4 cells' status is noted here so the
reconstruction does not overstate the gather account.

### §2 coda — the cross-cutting mechanism (reconstructed from the spec and the preregistration)

One mechanism is cross-cutting and load-bearing: created content usually
*touches* preserved content and segments as one object (the merged components
throughout L/R/M/F above). The build therefore carries a **union derivation**
(spec M-U, built first): an output object whose cells partition into ≥ 2
parts, each part independently derivable by any kind, is emitted as one
composite candidate whose bindings are the parts' union. Without it, most
class mechanisms cannot unblock anything, because the object they must derive
is never offered to candidate generation as separate pieces.

## 3. The §3.1 requirements do not cover the wall (reconstructed)

§3.1 of `SHARED_WRONG_BINDING_DERIVATION_2026-11-04.md` banked three grammar
additions as defect requirements. Quoted in substance:

1. **A quotient kind** — "a derivation that partitions the input grid into
   b×b blocks (b a scene parameter in Π's sense — read off the scene's period
   structure, not a free constant), classifies each block by a
   pattern/parameter function from the existing kinds, and emits the quotient
   grid as the output (or as an object in it)."
2. **Addressed-content parameters** — "Π gains region-query functions —
   enclosed color, center-of-unique-solid-block, odd-one-out color within a
   uniform surround — as named, total scene functions, bindable exactly like
   the existing scalars."
3. **Size-parametric fate keys** — "a fate may bind to a pattern *modulo
   uniform scaling*, with the size function carried as an explicit binding —
   so one rule can be one binding at every size, instead of one binding per
   exercised size."

Mapping (this anatomy's §3; verdict labels are the reconstruction's, applied
to the recorded class structure):

- **Covered.** Requirement 1 covers class Q's block form — the quotient
  family's block quotient (67b4a34d at b = 4, and the tile-quotient form) —
  and the build's M-Q partition rules (i)–(ii) are its direct descendants.
  Requirement 1's letter covers only the uniform-block partition; §2-Q's
  symmetry-domain, strip, and column forms are extensions of it, not
  instances.
- **Partially covered (~6 tasks).** Requirement 2's addressed content stands
  *behind* parts of L (stroke anchors: dots, centers), R (marker-read
  placement positions), F (the marker center; the color sequence read off
  marker objects), and C (the count read by a Π region-query): the
  addressing is named, but in every case the *generative act itself* — the
  stroke, the multi-instance emission, the iterated frame, the shape
  synthesized from a count — is not. Requirement 3 (size-parametric fates)
  touches none of the 19 directly: no task in the wall fails because one
  rule was bound per size.
- **Uncovered.** The wall's generative mass is entirely unnamed by §3.1:
  strokes (L), multi-instance emission of merged components (R, M),
  completion by a symmetry group (S), procedural texture (T),
  split-and-discard with per-instance colors (P), and the color-class
  pattern source (G) — a source-inventory gap, not a kind at all.

**Verdict: a NEW requirement set dominates.** Seven new requirements,
drafted in §3.1's own form (a named mechanism, its binding discipline, and
the fence it touches). These are reconstructions assembled from the spec's
mechanisms M-Q…M-P and §3.1's requirements language; the original seven's
wording is **not recoverable from surviving sources** — their substance is,
one per mechanism the wall forced:

- **N1 (strokes; class L; spec M-L).** A stroke kind: a rasterized lattice
  segment or ray whose anchor is an addressed-content parameter (object
  center, unique dot, marker pair), whose direction is one of the 8 lattice
  directions, whose extent is a named rule (to-edge / to-second-anchor /
  to-obstacle), and whose ink is a color under φ or an instance color (N6).
- **N2 (multi-instance emission; classes R, M; spec M-R).** A stamp kind:
  one source pattern, one binding, a *placement set* — by lattice period,
  by marker-read positions, by explicit enumeration bound across pairs, or
  under reflection composed with translation — emitted as one pattern, so a
  merged component of copies is one derivation.
- **N3 (union derivation; cross-cutting; spec M-U).** A composite
  derivation over a partition of an output object into independently
  derivable parts, proposals drawn only from already-generated candidates
  and creation-kind proposals, never from subset enumeration.
- **N4 (frame generalization; class F; spec M-F).** The frame kind gains an
  iteration-count binding, a color sequence bound from marker objects, an
  inset mode at negative margin inside a source object, and its center as
  an addressed-content parameter.
- **N5 (count-parametric synthesis and periodic fill; classes C, T; spec
  M-C, M-T).** Shape and texture kinds over closed canonical families
  (filled triangle; checkerboard), generated at exactly the count /
  multiset a Π region-query binds, or as the periodic fill of a bound
  region from two bound colors and a phase. The family lists are closed;
  adding a family is a new commission.
- **N6 (split-and-discard and instance colors; class P, serving L/F; spec
  M-P).** A split group may complete on a subset of parts with dropped
  parts recorded and the kept-set identical across all pairs; a derivation
  may carry an instance color bound per derivation instance by cross-pair
  intersection, never through the global φ — the only sanctioned route to
  colors absent from the input. (The fence this weakens is priced in §4.)
- **N7 (pattern sources and scene-stage programs; classes G, S, and Q's
  non-block forms; spec M-G, M-S, M-Q rules (ii)–(iii)).** The source
  inventory gains whole-color-class pseudo-objects; the scene stage gains
  quotient accounts over strip and symmetry-domain partitions and a
  symmetry-completion pretransform that closes a grid under a *bound*
  symmetry group, conflicts killing the account.

## 4. Fence consequences (reconstructed; the spec's §5 is its summary)

Every extension named above enlarges or alters the old grammar's candidate
system, and the consequences are stated, not elided:

- The **F × U ≤ 0.842 ceiling and census U are void as bounds on the
  extended grammar** — they were measured over the old candidate system.
  §3.1's own text fixes the replacement discipline (quoted): "The net
  effect on U is not computable from this record — it is measurable, by
  the same survivor-census instrument on the new grammar's fits, and
  **that measurement, not a probe, is the commission's first gate** …
  no build is authorized by a bound; it is authorized by a measured U on
  spent draws, against a pre-registered band." The survivor-census
  re-measurement on the extended grammar is therefore the build's first
  gate, and the census bound 921/938 = 98.2% is recomputed, not
  inherited. §3.1's trade warning travels with the extensions: "every new
  kind is also a new way to fit wrongly."
- **M-P (N6) is the one deliberate weakening of a banked soundness fence**:
  split-group completeness (every part index present → every *kept* part
  index present, kept-set identical across pairs). Its cost is assigned to
  the same U re-measurement.
- **What survives intact:** the BG-GATE PASS as a component record; the
  Friday flat-null verdict; the census numbers as facts about the *old*
  grammar; the 4 banked fits (7d1f7ee8, a61f2674, 4acc7107, 8dae5dfc) as
  re-verification targets; and every per-task death record in §1 as
  history.

## 5. Not creation at all (reconstructed from §0, §1, and the preregistration)

- **6d0160f0 creates nothing.** The zero object is the input's own color-5
  scaffold class gathered into one component by the deletion of everything
  else; the gap is a pattern *source* (a whole color class as one pattern),
  not a generative kind. (Build postscript at §2-G: the +4 kept cells are
  created, not preserved, on the build's cell-diff; the mechanism for them
  was not identified by the build.)
- **604001fa creates no *shape*.** Every zero shape is a color-1 part of a
  composite input object, exactly, under dihedral, in every pair; the
  failure is the split-group completeness prune (§0) plus per-instance
  fresh colors that a global functional φ cannot bind. The content is
  selected, not created.
- **27f8ce4f creates no content.** The output is exactly 3–4 translates of
  the input's own 3×3 pattern, 0 leftover cells, every pair verified; the
  entire gap is multi-instance *emission* of a merged component.
- **No task among the 19 is a pure budget or cover death in disguise:**
  every charge was replayed at a generous 120 s deadline (vs the lane's
  25 s) and every zero object reproduced identically; the failing stage is
  candidate generation in all 19 (§0).

*End of reconstruction. The surviving original text (§§0–1, §2-Q/L/R, and
§2-S to its truncation point) is untouched above; everything from the
reconstruction note in §2-S onward is the 2026-11-07 reconstruction
described there, at source grade, with superseded readings and
unrecoverable details marked in place.*