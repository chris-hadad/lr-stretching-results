"""Independent four-symbol character and complete U07 mask linkage.
Only own prior algebra freeze and SOURCE mathematical text pins are read.
No provider code or expected mathematical JSON is read.
"""
import hashlib,json,math,resource,sys,time
from pathlib import Path
import sympy as sp
T=Path(__file__).resolve().parents[1]
RAW=Path(sys.argv[1])
assert RAW.is_dir()
S,m,q=sp.symbols('S m q')
start=time.monotonic()
def emit(tag,**kw):print(json.dumps(dict(tag=tag,seconds=time.monotonic()-start,**kw)),flush=True)
def rise(z,n):return sp.prod(z+i for i in range(n))
def fall(z,n):return sp.prod(z-i for i in range(n))
def read_kernel(c):
    n=sum(sp.Integer(z)*m**h*S**i for i,row in enumerate(c['numerator_S_rows_m_ascending']) for h,z in enumerate(row))
    den=sum(sp.Integer(z)*m**h for h,z in enumerate(c['denominator_m_ascending']))
    return n/den
own=json.loads((RAW/'INDEPENDENT-ALGEBRA-v2.json').read_text())
parent={k:read_kernel(v) for k,v in own['parent_kernels'].items()}
def serialize(z):
    a,b=sp.fraction(sp.cancel(z))
    return {'numerator':str(sp.factor(a)),'denominator':str(sp.factor(b)), 'expanded_numerator':str(sp.expand(a)), 'expanded_denominator':str(sp.expand(b))}
def put(name,obj):
    p=RAW/name
    with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
    return hashlib.sha256(p.read_bytes()).hexdigest()

# U04: d=aU+b, replace x^U/y^U by independent X/Y, INCLUDING h_{U-1}.
a,b,X,Y=sp.symbols('x y X Y')
def h(ind,offset):
    return 1/((1-a)*(1-b))-a**(offset+1)*X**ind/((1-a)*(1-b/a))+a**-1*b**(offset+2)*Y**ind/((1-b)*(1-b/a))
h2,h3,h4,h0=h(2,0),h(3,1),h(4,2),h(1,-1)
determinant=h2**3-2*h2*h3*h0+h4*h0**2
weyl=X**2*((1-a*X)/(1-a))**2*((1-b*Y)/(1-b))**2*((1-(b/a)*(Y/X))/(1-b/a))**2
character_res=sp.cancel(determinant-weyl)
assert character_res==0
empty_hminus1=sp.cancel(h(0,-1))
assert empty_hminus1==0
character={'four_independent_symbols':['x','y','X','Y'],'X_meaning':'x^U','Y_meaning':'y^U', 'h2U':serialize(h2),'h3U1':serialize(h3),'h4U2':serialize(h4),'hUm1':serialize(h0),'complete_determinant':serialize(determinant),'squared_Weyl_character':serialize(weyl),'free_variable_residual':'0','h_minus1_residual':'0','no_U_sampling':True}
char_sha=put('FOUR-SYMBOL-TOP-CHARACTER-v1.json',character)
emit('four-symbol-character-pass',sha256=char_sha)

# Derive alphas from all bounded Newton differences/factorial moments.
alpha={};P={};moments={}
for j in (1,2,3):
    n=m-j;Nj=(4-j)*S-j
    P[j]=rise(S-q,j)*rise(Nj-q+n+1,j)/(math.factorial(j)*rise(n+1,j))
    deltas=[];terms=[]
    for k in range(2*j+1):
        delta=sp.cancel(sum((-1)**(k-i)*math.comb(k,i)*P[j].subs(q,i) for i in range(k+1)))
        term=delta*fall(Nj,k)*rise(n+1,k)/(math.factorial(k)*rise(2*n+2,k))
        deltas.append(serialize(delta));terms.append(term)
    # The Newton expansion is a separate complete polynomial identity in q.
    newton=sum(sp.fraction(sp.cancel(sum((-1)**(k-i)*math.comb(k,i)*P[j].subs(q,i) for i in range(k+1))))[0]/sp.fraction(sp.cancel(sum((-1)**(k-i)*math.comb(k,i)*P[j].subs(q,i) for i in range(k+1))))[1]*fall(q,k)/math.factorial(k) for k in range(2*j+1))
    assert sp.cancel(P[j]-newton)==0
    alpha[j]=sp.cancel(sum(terms))
    moments[j]={'j':j,'n':str(n),'N_j':str(Nj),'full_P_j':serialize(P[j]),'Delta_k_P_at0':deltas,'all_factorial_moment_terms':[serialize(t) for t in terms],'alpha':serialize(alpha[j]),'newton_residual':'0','term_count':2*j+1}
    emit('alpha-derived',j=j,terms=2*j+1)
alpha1=(3*S+2*m-1)*(m-(m-1)*S)/(2*m*(2*m+1))
alpha2=(S+m-2)*(S+m-1)*(2*S+2*m-3)*(S*m+2*S+3*m)/(2*m*(m-1)*(2*m-1)*(2*m+1))
P3=S**3*(m**3+6*m**2+11*m+6)+S**2*(18*m**3+33*m**2-27*m-42)+S*(77*m**3-93*m**2-98*m+72)+60*m**3-180*m**2+120*m
alpha3=(S+2*m-7)*(S+2*m-6)*(S+2*m-5)*P3/(48*m*(m-2)*(m-1)*(2*m-3)*(2*m-1)*(2*m+1))
for j,target in [(1,alpha1),(2,alpha2),(3,alpha3)]:assert sp.cancel(alpha[j]-target)==0

# Solve q-polynomial antidifferences by descending coefficient elimination.
# The operator sends q^k to degree k+1 with nonzero leading -(k+2n+2),
# so the solution is unique. No source R coefficients are imported.
Rsol={};Rcert={}
for j in (1,2):
    n=m-j;Nj=(4-j)*S-j
    def op(poly):return (q+n+1)*(Nj-q)*poly.subs(q,q+1)-q*(Nj-q+n+1)*poly
    remaining=sp.Poly(sp.expand(P[j]-alpha[j]),q)
    values=[remaining.nth(i) for i in range(2*j+1)]
    Rj=sp.Integer(0);steps=[]
    for k in reversed(range(2*j)):
        basis=sp.Poly(sp.expand(op(q**k)),q)
        assert sp.expand(basis.nth(k+1)+(k+2*n+2))==0
        c=sp.cancel(values[k+1]/basis.nth(k+1))
        Rj+=c*q**k
        steps.append({'q_power':k,'operator_leading_coefficient':str(basis.nth(k+1)),'solved_coefficient':serialize(c)})
        for h0 in range(k+2):values[h0]=sp.cancel(values[h0]-c*basis.nth(h0))
    assert all(v==0 for v in values)
    Rj=sp.cancel(Rj);Rsol[j]=Rj
    residual=sp.cancel(P[j]-alpha[j]-op(Rj))
    assert residual==0
    beta=sp.cancel(S*(Nj-S+n+1)*Rj.subs(q,S))
    Rcert[j]={'R_j':serialize(Rj),'solution_steps':steps,'whole_q_polynomial_residual':'0','beta_endpoint':serialize(beta),'degree_q':int(sp.degree(sp.fraction(Rj)[0],q))}
    emit('polynomial-telescoper-solved',j=j)
R1source=(5*S*m+S+2*m**2-2*m*q+m)/(2*m**2*(2*m+1))
assert sp.cancel(Rsol[1]-R1source)==0
beta1=S*(2*S+m-1)*(3*S*m+S+2*m**2+m)/(2*m**2*(2*m+1))
P2=8*S**2*m**2-2*S**2+18*S*m**3-18*S*m**2-S*m+4*S+10*m**4-23*m**3+8*m**2+2*m
beta2=S*(S+m-3)*(S+m-1)*P2/(4*m**2*(m-1)**2*(2*m-1)*(2*m+1))
for j,target in [(1,beta1),(2,beta2)]:
    n=m-j;Nj=(4-j)*S-j
    assert sp.cancel(S*(Nj-S+n+1)*Rsol[j].subs(q,S)-target)==0

# Gamma/factorial-ratio reduction with ONLY integral, bounded offsets.
# gamma(z)/gamma(w), where z-w is a known integer, is a finite rise product.
def gamma_ratio(z,w):
    k=sp.simplify(z-w)
    assert k.is_Integer
    k=int(k)
    return rise(w,k) if k>=0 else 1/rise(z,-k)
def bin_to_a(U,K,L,slope):
    return sp.cancel(gamma_ratio(U+1,slope*S+L+1)*gamma_ratio(L+1,K+1)*gamma_ratio(slope*S+1,U-K+1))
D={};mask_factorials={}
for j in (1,2,3):
    Uv=(4-j)*S+2*m-3*j+1;Kv=2*m-2*j+1
    items=[]
    D[j]=sp.Integer(0)
    for p0 in range(j+1):
        Ua=(4-j)*S+2*m+1-2*j;Ka=2*m+1-j+p0
        ratio=gamma_ratio(Ua+1,Uv+1)*gamma_ratio(Kv+1,Ka+1)*gamma_ratio(Uv-Kv+1,Ua-Ka+1)
        expected=rise((4-j)*S+2*m-3*j+2,j)*fall((4-j)*S-j,p0)/rise(2*m-2*j+2,j+p0)
        assert sp.cancel(ratio-expected)==0
        D[j]+=(-1)**j*fall(m,j)/math.factorial(j)*math.comb(j,p0)*(S+2)**(j-p0)*ratio
        items.append({'p':p0,'factorial_ratio':serialize(ratio),'residual':'0'})
    D[j]=sp.cancel(D[j]);mask_factorials[j]=items
V1ratio=bin_to_a(3*S+2*m-2,2*m-1,2*m-2,3)
V2ratio=bin_to_a(2*S+2*m-5,2*m-3,2*m-5,2)
V3ratio=bin_to_a(S+2*m-8,2*m-5,2*m-8,1)
W1ratio=bin_to_a(S+m-1,m-1,m-1,1)*bin_to_a(2*S+m-2,m-1,m-2,2)
WCratio=bin_to_a(S+m-3,m-2,m-4,1)**2
W2ratio=bin_to_a(S+m-2,m-2,m-4,1)*bin_to_a(S+m-4,m-2,m-4,1)
low_first=bin_to_a(2*S+2*m,2*m+1,2*m-5,2)
low_second=m*(S+2)*bin_to_a(S+2*m-2,2*m,2*m-8,1)
low_third=m*bin_to_a(S+2*m-2,2*m+1,2*m-8,1)
normal={
'l':-3*m*alpha[1]/(2*(2*m-1)),
'p3':(D[1]+3*m*alpha[1]/2)*V1ratio,
'p12':3*m*beta1*W1ratio,
'p2':(D[2]-3*m*(m-1)*alpha[2]/4)*V2ratio-low_first,
'p11':-3*m*(m-1)/2*(alpha[2]*WCratio/2+beta2*W2ratio),
'p1':(D[3]+m*(m-1)*(m-2)*alpha[3]/2)*V3ratio+low_second+low_third}
normal_res={k:str(sp.cancel(v-parent[k])) for k,v in normal.items()}
assert set(normal_res.values())=={'0'}
ratios={'V1_to_V3positive':V1ratio,'V2_to_V2positive':V2ratio,'V3_to_V1positive':V3ratio,'W1_to_W12positive':W1ratio,'Wcenter_to_W11positive':WCratio,'W2_to_W11positive':W2ratio,'full_low_first_to_V2positive':low_first,'full_low_second_to_V1positive':low_second,'full_low_third_to_V1positive':low_third}
proof={'schema':'a81-complete-original-kernel-linkage/v1','status':'PASS_PROPOSED_ARITHMETIC_ONLY','four_symbol_character_sha256':char_sha,
 'moment_alphas':moments,'solved_R_polynomials':Rcert,'R1_source_text_comparison_residual':'0','beta1_beta2_complete_endpoint_residuals':['0','0'],
 'total_mask_factorial_ratios':mask_factorials,'bounded_gamma_ratios':{k:serialize(v) for k,v in ratios.items()},
 'six_parent_kernels_from_complete_normal_form':{k:serialize(v) for k,v in normal.items()},'six_kernel_identity_residuals':normal_res,
 'both_lower_diagonal_signed_partners_retained':True,'third_mask_uses_all_seven_moments':True,
 'no_parameter_sweep':True,'no_expected_SOURCE_arrays_read':True,'no_provider_programs_read_or_executed':True,
 'text_pins':{'public_root_proof':hashlib.sha256((T/'proofs/A81-INDEX-AUGMENTATION-v2.md').read_bytes()).hexdigest()},
 'self_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'seconds':time.monotonic()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'Sage_slots_declared':0,
 'claim_ceiling':'Free-variable arithmetic linkage only. Physical support, whole-original character extraction and scientific adoption require root proof/gate.'}
sha=put('COMPLETE-ORIGINAL-KERNEL-LINKAGE-v1.json',proof)
emit('complete-original-linkage-pass',sha256=sha,rss=proof['self_peak_rss_bytes'])
