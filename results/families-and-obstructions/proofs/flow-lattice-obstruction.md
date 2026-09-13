# Primitive edge relations obstruct a direct flow realization

Derivation dated 9 September 2026. This concerns affine lattice equivalence
of complete objects. It does not exclude arbitrary projections,
sections, nonlinear count identities, or ordinary hives in general.

## An invariant of standard network-flow polytopes

Let `F={f: D*f=b, l<=f<=u}` be a bounded standard single-commodity network-flow
polytope, with integral incidence matrix `D` and coordinate bounds. Work in
its saturated affine lattice. Every primitive edge direction of `F` has all
coordinates in `{-1,0,1}`.

Here is the elementary argument. In the relative interior of an edge, freeze
every coordinate that is at a lower or upper bound throughout that edge. On
the other arcs, the kernel of the remaining incidence matrix has dimension
one. The remaining graph therefore has exactly one independent undirected
cycle after bridges are deleted. Its primitive circulation has entries plus
or minus one on that cycle and zero elsewhere. It generates the entire
integer kernel of the edge direction. Additional globally forced coordinates
do not change this argument; the saturated lattice keeps this generator
primitive. Loops give a coordinate unit direction and cause no exception.

Consequently, if three primitive edge directions satisfy

```text
v-w = m*u,
```

then `|m|<=2`: choose a coordinate where `u` is nonzero. The left side is
between minus two and two, and the right side has absolute value `|m|`.
The existence of such an integral relation, with all three directions
primitive, is preserved by an affine lattice isomorphism.

## Applying it to the negative split-width join

The triangular facet `x=0` of the split-width join `Q_ab` has primitive edge directions

```text
v=(1,0,0), w=(1,0,-b), u=(0,0,1),
v-w=b*u.
```

The other endpoint facet supplies the corresponding relation with coefficient
`a`. All these directions are primitive in `Z^3`; the first two have first
coordinate one. Therefore `Q_ab` with `max(a,b)>2` cannot be affine-lattice
isomorphic to any complete standard network-flow polytope, at any graph size.
In particular every negative member of the split-width join family is excluded from this direct route.

This rules out an unchanged transportation or ordinary incidence-flow model
for the negative join, including adding redundant flow variables through an
affine lattice isomorphism. It does not show that all transportation or flow
polytopes are ordinary positive: other geometries can be negative, as the
bounded-circulation examples already show. The obstruction is to
this amplified triangular edge configuration.

## Scope of the whole-LR realization question

A realization through non-flow hive constraints, a different negative shape,
or a complete count or projection identity remains possible if its lattice
and stabilization premises can be proved. Increasing the size of a standard
flow graph alone does not remove this affine-lattice obstruction.

This gives a bounded, reusable test for a proposed exact realization. It is
not a no-go theorem for rank-six or rank-seven hives. Their rhombus systems
are not incidence matrices, and the primitive directions of their whole
faces need not have unit coordinates in a common incidence representation.
Nor does a projected direction retain primitivity automatically; the theorem
cannot be pushed through a noninjective map without a new argument.

The primary-source check is Borgwardt and Brugger,
[Circuits in Extended Formulations](https://arxiv.org/abs/2208.05467), and its
[published introduction](https://www.sciencedirect.com/science/article/pii/S1572528624000045).
It identifies network circuits with cycles and emphasizes the distinction
between edge/circuit behavior and projection. The elementary proof above
supplies the specific primitive-relation bound used here. No full-paper
reproduction or novelty claim is made.
