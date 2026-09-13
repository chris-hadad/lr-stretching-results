# Exact affine completion starts at x=1, not merely the geometric threshold x=2

The following all-stretch cancellation proof strengthens the direct complete-state x>=2 argument and establishes the sharp affine threshold independently of coefficient reconstruction.

Let F_t(u) be the complete tail count with the first two rows detached and the bottom skew shape(3t,2t,t)/(3t-u3). Write
m0=min(t-u1+u2,t-u2+u3,2t-u1,u3), W=t+m0+1.
The formal affine continuation to x=1 is A(t)=sum_(|u|=3t) W(u)F_t(u)=P2(t)-tQ(t).

At x=1 the two top gaps are 2 and the exact top minimum is
m1=min(2t-u1+u2,2t-u2+u3,3t-u1,t+u3).
The last two forms are nonnegative. The excluded regions are E1: u1-u2>=2t+1 and E2: u2-u3>=2t+1; they are disjoint under|u|=3t. On their first layers W=0. Deeper layers have negative W.

Only the first and second single-overlap corrections can differ from F on admitted states. They cannot coincide with one another or with lower overlaps: those nonzero indices would require at least 3t+2 total deficit. For the first correction u1>=2t+1, map
u'=(2t+u2+1, u1-2t-1, u3).
This is an involution between admitted correction states and the part of E1 with u'1-u'2>=2t+2. Nonnegativity and total 3t hold. In the forward direction u2<=t-1, so m1(u)=2t-u1+u2; every other defining form is at least this one. The inverse satisfies all other top inequalities because its second and third deficits are each<=t-1. The weights obey W(u')=-W(u). Its detached factors are h_(2t+u2+1)h_(u1-2t-1), exactly the first correction; the remaining tail factor is unchanged. Hence every negative extended first-region contribution cancels the corresponding subtracted overlap count.

For the second correction u2>=2t+1, map
u'=(u1,2t+u3+1,u2-2t-1).
It bijects the admitted correction states with the deeper part of E2, again with W(u')=-W(u). Here m1(u)=2t-u2+u3. Both third deficits, wherever needed in the correction comparison, are<t, so the bottom skew factor has no upper overlap and is simply h_(third deficit)*s_(2t,t). Thus the second determinant correction is exactly F_t(u'). The same cancellation holds. The two zero-weight excluded first layers contribute nothing.

Therefore the difference between the complete admitted count and the formal extended sum is zero, for every t>=0. We have the exact polynomial identity

P1=P2-tQ,
P_x=P1+(x-1)tQ for EVERY integer x>=1.

This explains a concrete complete compensation: negative weights introduced by formally extending the top chamber cancel whole determinant-overlap contributions. It is not a claim that a positive count sum preserves ordinary signs.

The remaining initial point x=0 is a distinct whole polynomial. At t=2, P0=4464 while the continuation P1-2Q gives11556-7182=4374, a gap90. Thus the affine count threshold 1 is sharp among allowed nonnegative integer x. The complete wall correction W0=P0-P1+tQ is not an entire LR polynomial. Its negative ordinary coefficients must be recorded at that scope.
