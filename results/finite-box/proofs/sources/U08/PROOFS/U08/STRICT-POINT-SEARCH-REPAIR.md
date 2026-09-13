# A point-search refusal is not hidden dimension

The old strict-point search at grade D+1 can hit its bounded branch limit even on an actually full-dimensional chart. The U08 pilot exposes this at group214713, lambda=(8,7,6,5,2,1,1), mu=(5,5,2,2,1), nu=(7,4,2,1,1). Its prior nine-coordinate chart and every complete row remain unchanged. No zero or lower-dimensional claim follows from that search refusal.

For any positive integer grade t, a single integer x with c_r*t+a_r.x>=1 for every nonconstant defining row and c_r*t>=0 for constant rows proves actual ambient dimension D: x/t has a real open D-ball in the complete polytope. No search heuristic or exhaustive search premise is needed once that explicit witness is checked. The chart's integer inverse and full forced affine-hull proof supply the saturated lattice independently.

The repair searches smaller grades first for a wholly feasible one-coordinate interval, stops after one supplied point, and directly substitutes the resulting point into every original row and rhombus. The search remains bounded; any failure remains unresolved. The relative-coordinate compiler and independent checker then preserve the complete semistandard/ballot map. Serialization to the recorded integer-array format is not a mathematical change: the first combined pilot repair incorrectly compared in-memory tuples with lists and failed before recording this new witness. Its saved earlier repairs and failure survive; a fresh version checks canonical serialized arrays and supplies the actual witness certificate.

This is an implementation repair to the previously proved strict-point gate, not a new theorem equating an upper bound and actual dimension. Its production application must retain every successful witness and every remaining refusal.
