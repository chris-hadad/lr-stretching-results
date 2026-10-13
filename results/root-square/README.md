# Root-square originals: height and raw index are distinct operations

For m>=3 and s,u>=0, retain all m+3 physical rows in the literal family


```text
lambda=(ms+4u,ms+3u,ms+2u,ms,(m-1)s,...,s),
mu=(ms+2u,ms+u,ms,(m-1)s,(m-2)s,...,0),
nu=((m-2)s+3u,s+2u,s+u).
```

Lambda is outer, the skew/content size is ms+6u, and the original tableau
chart retains every capacity and both ballot-prefix families in saturated
Z^(2m+1). At s>0 its actual degree is 2m+1 in the proved domains below.
At s=0 the general original is 1+ut, with interval and point cases separate.
These statements concern entire originals, not isolated clipping terms.

## Height augmentation

For every m>=3 and u>=max(3,m-2)s, the complete original is strict in degrees
zero through 2m+1. For v>=u in that same domain,


```text
C_m(st,vt)-C_m(st,ut)
  >=_coef (v-u)t a_(2m-1)(st)[1+(1-3/(2m))st].
```

The gain is strict in every nonconstant degree through 2m+1 when s>0,v>u.
[The full A80 proof](proofs/A80-COLLAR-EXTENSION-v1.md) keeps the complete weak-row
reflection, clipping union, rejected-prefix population and second-band
correction. A correction with a negative ordinary coefficient is paid jointly
by its entire parent. Lower heights outside this exact domain remain open.

## Fixed u=2s raw index augmentation

At the separate fixed wall u=2s, every C_m is strict through degree 2m+1.
The explicitly embedded complete component J_m and its complement E_m=C_m-J_m
satisfy


```text
C_(m+1)-C_m >=_coef S T_m/(4m), m>=3,
E_(m+1)-E_m >=_coef S T_m/(4m), m>=4,
T_m=a_(2m+1)(4S)(1+S/(m+2)), S=st.
```

At m>=96 the denominator improves to 2m. These raw gains have zero constant
and actual degree 2m+3 for s>0. The entire J gain is nonnegative.
The first complementary gain is exceptional:


```text
[S](E_4-E_3)=-499/2520,
[S](J_4-J_3)=5/4,
[S](C_4-C_3)=2651/2520.
```

The SAME ordinary coefficient is compensated. This is not a negative LR
original. At s=0 the fixed wall has u=0: C=J=1,E=0 and gains zero.
[Original geometry](proofs/A81-ORIGINALS-AND-GEOMETRY-v1.md) and
[the full raw-index proof](proofs/A81-INDEX-AUGMENTATION-v2.md) retain all four
capacity masks, six Weyl targets, strict shifts, lower-diagonal partners,
complete component embedding, finite exceptions and the uniform tail.
No rho-normalized, quotient or arbitrary-height index law is inferred.

## Indispensable certificates and reproduction

The public data contains every selected endpoint m=3..96 and every selected
gain m=3..95, including the adverse H3. It contains the full free-variable
kernel/linkage certificates and all 194 threshold-96 finite comparisons,
with the infinite consecutive-ratio tail proof. The additional historical
m=97..109 endpoint controls are unnecessary for this theorem and are not copied.
All fields include their complete ordinary slots and common denominator.

```sh
python3 -B verification/check_recent_sources.py --module root-square
python3 -B results/root-square/code/reproduce.py --output /path/to/new-root-square-check.json
```

This standard-library command checks every stored endpoint and gain join,
exact degrees, constants, raw reserves, exceptional compensation and selected
fresh low-index definitions. It does not rerun the historical large endpoint
expansion or claim a standard-library runtime equal to its Sage-accelerated
source calculation. The uniform proof and full symbolic certificates are
separate obligations; [verification status](VERIFICATION.json) states the
observed selected export scope. Completed Pro053 and Pro055 supplied the
originating formulas and operation; Codex reconstructed the accepted proofs
and arithmetic. No returned program is included or executed.

The full selected fixed-wall fields use deterministic `.json.gz` files; the portable checker reads them directly. For the three complete height bases and uniform beta use `python3 -B results/root-square/code/verify_height.py /path/to/new-height.json`.

The complete independent symbolic linkage and uniform tail can also be rebuilt
with ordinary Python plus SymPy, in this order and at a fresh shared output root:

```sh
python3 -B results/root-square/code/derive_index.py /path/to/new-index-symbolic
python3 -B results/root-square/code/link_index.py /path/to/new-index-symbolic
python3 -B results/root-square/code/verify_threshold96.py /path/to/new-index-symbolic
```

These reconstruct every rational parent/gain kernel, complete original-character
and factorial-moment linkage, all threshold-96 majorants, all 194 finite degree
comparisons and the infinite ratio tail. The checker sources import SymPy,
not Sage or a provider program. Stored certificate replay, symbolic rederivation
and full high-index endpoint regeneration retain their separate meanings.
