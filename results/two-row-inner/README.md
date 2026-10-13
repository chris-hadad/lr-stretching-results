# Every two-row-inner LR family, at arbitrary rank

For partitions lambda, mu and nu, with lambda outer, if either inner partition
has at most two parts, every ordinary coefficient of the complete stretching
polynomial is nonnegative. There is no outer-rank, area or free-row bound.
An infeasible positive-stretch family has polynomial zero; a feasible point has
polynomial one. Every other feasible family is strictly positive in every
degree from zero through its actual degree.

This closes all two-row-inner coefficient indices, extending the earlier
[linear-coefficient addition law](../linear-coefficient-geometry/TWO-ROW-ADDITION.md).
It also proves a complete coefficientwise content-majorization operation at
fixed two-row output, with a terminating sequence from an actual paid parent.
It does not settle arbitrary three-row-inner families or whole rank seven.

## Complete recognition and degree

Commute the inner factors to write nu=(A,B), A>=B>=0. Check containment, size
balance and the partition conditions. Pad lambda and mu with their original
zero slots. A three-cell skew column, detected by lambda_(i+2)>mu_i, makes the
family infeasible. Otherwise define


```text
h_i=max(lambda_(i+1)-mu_i,0), h_0=h_n=0,
H=sum h_i, ell_i=lambda_i-mu_i-h_(i-1)-h_i,
w=the positive ell_i, W=sum w_i, k=B-H.
```

The full skew character is (xy)^H product h_(ell_i)(x,y), and the entire LR count is


```text
K(w;k;t)=[z^(kt)](1-z) product_i(1+z+...+z^(t w_i)).
```

The empty list is feasible exactly at k=0. For a nonempty list feasibility is
k>=0, 2k<=W and max(w)<=W-k. Append W-2k to w and delete zeros, calling this
list u of length m and half-total S=W-k. The point cases are m<=3 or max(u)=S.
Every remaining family has actual degree m-3. The trivalent-tree proof retains
each affine parity coset and the full original integer stretching parameter.

## Paid transfer and proof

An admitted balancing step replaces U,V by U-b,V+b with
0<b<=floor((U-V)/2). Its exact finite-string difference is


```text
h_((U-b)t)h_((V+b)t)-h_(Ut)h_(Vt)
  =z^(Vt+1)h_(bt-1)h_((U-V-b)t-1).
```

The once-only endpoint +1 and both strict caps remain. The complete marked-cycle
coefficient identity has both its ordinary cycle term W and its distinguished
endpoint term V. Symmetric unimodality signs their complete difference. Sorting
unit transfers decreases the integer distance to the target by at least two;
the initial content (T-k,k,0,...) has complete polynomial one. Splitting is
included by padding a zero. Changing the output shape is a separate question.

[The full proof](PROOF.md) derives every identity, termination, point case,
parity lattice, exact degree and strictness. It is self-contained apart from
the classical LR/skew-Schur and two-variable Pieri identities stated and used
there. The source map records FR044's accepted reconstruction and antecedent
credit: the A006 skew reduction, Ferroni–McGinnis compatible cycles,
Pro042/A050 marked endpoints, and Pro044 U07's comparison and synthesis.

## Reproduction

With Python 3.11+, from the repository root:

```sh
python3 -B verification/check_recent_sources.py --module two-row-inner
python3 -B results/two-row-inner/code/check_two_row.py --output /path/to/new-check.json
```

The standard-library checker retains the complete historical finite control
roster: 1,643 transfers, 7,451 cycle slots, 717 feasible Kostka vectors, 1,083
original triples, direct tableaux and parity counts, and endpoint-omission
controls. These are error controls; the proof supplies the unbounded quantifiers.
[Verification status](VERIFICATION.json) records the actual fresh-export result.
No private source checkout or returned program is needed.
