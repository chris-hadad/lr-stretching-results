# Complete positive-gap two-bank contraction

Throughout, lambda denotes the outer partition. This complete two-bank family is not identified with the synchronized section discussed in the separate synchronization construction.

## Whole LR map, rank, lattice and degree before coefficients

Apply the complete two-bank row map and its inverse with m=k+1>=2, g=1, h=0, p=2m-3. The source's complete row map and inverse apply at every nonnegative real dilation. With top row, m edge rows and banks U,V, the partitions are
lambda=(8m-2, (6m-2i)_(i=1..m),4m,2m),
mu=(6m-2, (6m-2-2i)_(i=1..m-1),2m+1,2m),
nu=(6m-3,2m,2m).
Each displayed range is an ordered list; repeats are retained and no implicit extra rows occur. Sizes are 5m^2+13m-2, 5m^2+3m+1 and 10m-3. Rank m+3, actual dimension2m-1=2k+1. The source selects m free y entries, m-2 internal z entries, and u; z1=zm=0. This is the saturated Z^(2m-1) lattice with its full integral inverse. The rank 5 case at m2 is already covered by known positivity results.

In the source coordinates, for all first m-1 rows, y_i,z_i>=0, y_i+z_i<=2t and z_i<=Y_<i-Z_<i. Let their totals be A,B. The last row has z_m=0 and 0<=y_m<=min((2m-1)t,2mt-A). Its ballot is automatic because A>=B. Every bank entry is then forced from u except u itself, which ranges B<=u<=min(t,A). These are all source inequalities: in particular the corrected third last column z_m<=h t is retained, not omitted. Thus the whole multiplicity over prefix(A,B) is
W(A,B)=(min(t,A)-B+1)_+*(2mt-max(t,A)+1).
On the prefix support A+B<=2kt the second factor is positive.

Relative interior requires z2,...,z_(m-1)>=1, u>B, and u<t. Therefore t>=m. At t=m take z_i=1 for2<=i<=m-1, z1=zm=0, y1=...=y_(m-1)=2, y_m=1, u=m-1. Every nonidentically-zero inequality of the full chart is strict. This proves true codegree m, without reflection or a unique-first-interior premise.

## Complete two-row character and summation by parts

Let M(A,B)=[x^A y^B]h_(2t)(1,x,y)^k, where h is complete homogeneous. Each first edge row contributes sum_(r=0)^(2t) h_r(x,y). Iterated two-row Pieri, or the usual two-letter ballot recurrence, gives the full nonnegative prefix multiplicity
N(A,B)=M(A,B)-M(A+1,B-1), A>=B>=0,
with M outside nonnegative support zero. This identity counts all permitted first-edge tableaux and does not impose a new support equation.

Sum N(A,B)W(A,B). Reindex the subtracted term by(A,B)->(A+1,B-1). For A<=t the resulting weight is2((2m-1)t+1), except the diagonal A=B where it is((2m-1)t+1). For A>t and B<=t it is(2m-1)t+1-A+B. Terms with both A,B>t vanish. The diagonal and off-diagonal square can be symmetrized since M(A,B)=M(B,A).

Let S_B=sum_A M(A,B). Conditional on z1,...,zk summing to B, each y_i ranges0..2t-z_i; reflection y_i->2t-z_i-y_i shows sum_A A M(A,B)=(kt-B/2) S_B. The residual square sum of(A-B)M vanishes by symmetry. Therefore the entire count is
P_m(t)=sum_(B=0)^t (mt+1+3B/2) S_B,                         (1)
`S_B=[y^B](sum_(z=0)^(2t)(2t+1-z)y^z)^k.`
No determinant, endpoint or bank coordinate remains uncounted. At t=0 this gives 1.

## All-stretch polynomial, not interpolation

Since B<=t, every z_i<=2t cap is automatic. Expand product_i(2t+1-z_i) over z_i>=0,sum z_i<=t. Standard geometric-series coefficient extraction gives
sum e_j(z)=binom(k,j)binom(t+k,k+j),
sum B e_j(z)=binom(k,j)[j binom(t+k,k+j)+(k+j)binom(t+k,k+j+1)].
Hence
P_m(t)=sum_(j=0)^k (-1)^j binom(k,j)(2t+1)^(k-j)
 *[((k+1)t+1+3j/2)binom(t+k,k+j)
   +(3/2)(k+j)binom(t+k,k+j+1)].                           (2)
Every binomial is its polynomial falling-factorial expression. Formula(2) agrees with the full count at every integer t>=0, hence is the entire LR polynomial. Its apparent alternating pieces do not supply sign conclusions without full aggregation. The parent has prior degree 2k+1, established independently by the chart.

The quotient after extracting binom(t+k,k) has degree k+1. It is an algebraic quotient and is not assigned an LR rank. A descending-width numerator considered during the derivation was incorrect and is not used in formula(2).
