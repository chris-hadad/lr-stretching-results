# Entire skew-content to ordinary LR lift

Let lambda/mu be a fixed skew shape, w=(w1,...,wm) nonnegative integers with
sum w=|lambda/mu|, m>=1. Put H=lambda1 when lambda is nonempty,
and H=0 only when lambda is the empty partition; put
B_i=sum_(j>i)w_j for i=1,...,m-1, and kappa_i=sum_(j>=i)w_j. Form

    Lambda=(H+B1,...,H+B_(m-1),lambda1,lambda2,...),
    Mu=(H,...,H,mu1,mu2,...), Nu=kappa.                  (7)

All are partitions, including repeated or zero parts, Mu is contained in
Lambda, and their sizes balance. The first m-1 rows form the translated
straight shape B. In a ballot tableau this component is uniquely
superstandard: its row i is entirely label i. Real column/ballot induction
starts with row one containing only label one,
and each next buffer row has no smaller labels; its fixed row sum determines
the diagonal label. It leaves residual content w in the lower skew shape.
The top inner endpoint H separates the components' columns. Within the lower
component retain EVERY ordinary semistandard inequality of lambda/mu.

The buffer surplus between labels i and i+1 is B_i-B_(i+1)=w_(i+1), with
B_m=0. Every lower prefix uses at most tw_(i+1) copies of i+1 and a
nonnegative number of i, so every extra ballot inequality is automatic.
Hence every semistandard filling of t(lambda/mu) with content tw extends
uniquely to an LR filling for `(tLambda, tMu, tNu)`, and deleting B is its inverse.
The argument is valid for nonnegative real row counts as well. The maps insert
or delete fixed integer coordinates tB; they identify entire affine integer
lattices, preserve nonemptiness and intrinsic dimension, and include t=0.

Thus the ENTIRE skew stretched-Kostka count equals one ordinary stretched LR
coefficient. A future negative in that family can be transferred without a
face or a sum over fibers. The construction preserves dimension; it does not
determine that dimension numerically, establish a negative coefficient
or authenticate an independently supplied native polynomial.
