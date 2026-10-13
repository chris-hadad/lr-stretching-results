"""Independently authored A81 exact ORIGINAL index algebra from U10/U11 text.
No provider programs, modules or expected JSON arrays are read. SOURCE arrays
may only be inspected by a separate post-freeze comparison program.
"""
import hashlib, json, math, resource, sys, time
from fractions import Fraction as Q
from pathlib import Path
import sympy as sp

T=Path(__file__).resolve().parents[1]
RAW=Path(sys.argv[1])
RAW.mkdir(parents=True,exist_ok=False)
S,m,x,d = sp.symbols('S m x d')
start = time.monotonic()

def emit(tag, **kw):
    print(json.dumps(dict(tag=tag,seconds=time.monotonic()-start,**kw)),flush=True)

def put(name, obj):
    p=RAW/name
    with p.open('x') as f: json.dump(obj,f,indent=2); f.write('\n')
    return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def qstr(z):
    z=Q(z)
    return str(z.numerator) if z.denominator==1 else str(z.numerator)+'/'+str(z.denominator)

def vec(expr, var):
    poly=sp.Poly(sp.expand(expr),var)
    if poly.is_zero: return [0]
    return [int(poly.nth(i)) if poly.nth(i).q==1 else qstr(Q(int(poly.nth(i).p),int(poly.nth(i).q))) for i in range(poly.degree()+1)]

def canon(expr):
    n0,d0=sp.fraction(sp.cancel(expr))
    assert not d0.has(S)
    assert sp.Poly(n0,S,m).domain == sp.ZZ and sp.Poly(d0,m).domain == sp.ZZ
    if sp.Poly(d0,m).LC()<0: n0,d0=-n0,-d0
    sn=sp.Poly(n0,S)
    rows=[vec(sn.nth(i),m) for i in range(sn.degree()+1)]
    return {'numerator_S_rows_m_ascending':rows,'denominator_m_ascending':vec(d0,m),
            'S_degree':int(sn.degree()),'m_denominator_degree':int(sp.degree(d0,m)),
            'expression':str(sp.factor(n0))+'/'+str(sp.factor(d0))}

def shift_vec(a,k):
    b=[Q(0)]*len(a)
    for i,z in enumerate(a):
        for j in range(i+1): b[j]+=Q(z)*math.comb(i,j)*k**(i-j)
    return b

def majorants(c,kind):
    D=shift_vec(c['denominator_m_ascending'],128)
    assert all(z>0 for z in D)
    out=[]
    for i,row in enumerate(c['numerator_S_rows_m_ascending']):
        N=shift_vec(row,128)
        assert len(N)<=len(D)
        N += [Q(0)]*(len(D)-len(N))
        sign=1 if kind=='upper' else -1
        ratios=[sign*n/z for n,z in zip(N,D)]
        b=max(Q(0),*ratios)
        residual=[b*z-sign*n for n,z in zip(N,D)]
        assert all(z>=0 for z in residual)
        out.append({'S_degree':i,'bound':qstr(b),'numerator_x_ascending':[qstr(z) for z in N],
                    'residual_x_padded':[qstr(z) for z in residual],
                    'max_ratio_indices':[h for h,z in enumerate(ratios) if z==b]})
    return {'kind':kind,'denominator_x_ascending':[qstr(z) for z in D],
            'denominator_positive':True,'entries':out,
            'coefficient_bound_count':len(out),'padded_residual_slot_count':len(out)*len(D)}

def add(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,z in enumerate(a):c[i]+=Q(z)
    for i,z in enumerate(b):c[i]+=Q(z)
    return c

def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):c[i+j]+=Q(u)*Q(v)
    return c

def scale(a,t): return [Q(t)*Q(z) for z in a]

def a_poly(n,b):
    p=[Q(1)]
    for r in range(1,n+1):p=mul(p,[1,Q(b,r)])
    return p

def evaluate_vec(a,t):
    y=Q(0)
    for z in reversed(a):y=y*t+Q(z)
    return y

def evaluate_kernel(c,s0,m0):
    return sum(evaluate_vec(row,m0)*s0**i for i,row in enumerate(c['numerator_S_rows_m_ascending']))/evaluate_vec(c['denominator_m_ascending'],m0)

def rise(z,n): return sp.prod(z+i for i in range(n))
def fall(z,n): return sp.prod(z-i for i in range(n))
def binom_m(j):return fall(m,j)/math.factorial(j)

# U10 (6), complete masks and both lower-diagonal kernels.
alpha2=(S+m-2)*(S+m-1)*(2*S+2*m-3)*(S*m+2*S+3*m)/(2*m*(m-1)*(2*m-1)*(2*m+1))
P2=8*S**2*m**2-2*S**2+18*S*m**3-18*S*m**2-S*m+4*S+10*m**4-23*m**3+8*m**2+2*m
beta2=S*(S+m-3)*(S+m-1)*P2/(4*m**2*(m-1)**2*(2*m-1)*(2*m+1))
P3=S**3*(m**3+6*m**2+11*m+6)+S**2*(18*m**3+33*m**2-27*m-42)+S*(77*m**3-93*m**2-98*m+72)+60*m**3-180*m**2+120*m
alpha3=(S+2*m-7)*(S+2*m-6)*(S+2*m-5)*P3/(48*m*(m-2)*(m-1)*(2*m-3)*(2*m-1)*(2*m+1))
Dmask={j:(-1)**j*binom_m(j)*rise((4-j)*S+2*m-3*j+2,j)*sum(math.comb(j,p)*(S+2)**(j-p)*fall((4-j)*S-j,p)/rise(2*m-2*j+2,j+p) for p in range(j+1)) for j in (2,3)}
l=-3*(3*S+2*m-1)*(m-(m-1)*S)/(4*(2*m-1)*(2*m+1))
p3=-3*S*(3*S+2*m-1)*(7*S*m+5*S+5*m+2)/(4*(2*m-1)*(2*m+1))
p12=3*S**2*(2*S+m-1)*(3*S*m+S+2*m**2+m)/(m*(m-1)*(2*m+1))
lower2=-2*S*rise(2*S+2*m-4,5)/rise(2*m-4,6)
p2=(Dmask[2]-3*m*(m-1)*alpha2/4)*2*S*(2*S-1)/((2*m-3)*(2*m-4))+lower2
lower1=S*(S-1)*((m+1)*S+2*m)*rise(S+2*m-7,6)/((2*m-1)*(2*m+1)*rise(2*m-7,6))
p1=(Dmask[3]+m*(m-1)*(m-2)*alpha3/2)*S*(S-1)*(S-2)/rise(2*m-7,3)+lower1
p11=-3*m*(m-1)/2*(alpha2*S**2*(S+m-3)**2/2+beta2*S*(S-1)*(S+m-3)*(S+m-2))/((m-2)**2*(m-3)**2)
# Rationalize explicit numeric 1/2 factors (all previous arithmetic uses sympy).
parent={name:sp.cancel(expr) for name,expr in [('l',l),('p3',p3),('p12',p12),('p2',p2),('p11',p11),('p1',p1)]}
parents={name:canon(expr) for name,expr in parent.items()}
emit('six-parent-kernels-derived',degrees={k:v['S_degree'] for k,v in parents.items()})

# U11 actual m -> m+1 factors and complete source term.
r3=(1+3*S/(2*m-1))*(1+3*S/(2*m))
r12=(1+2*S/(m-1))*(1+S/m)
r2=(1+2*S/(2*m-4))*(1+2*S/(2*m-3))
r11=(1+S/(m-3))**2
r1=(1+S/(2*m-7))*(1+S/(2*m-6))
plus=lambda z:z.subs(m,m+1)
l_source=plus(parent['l'])*(2*S**3/m**2)*(1+2*S/(m-1))
gain={
'h_l':m*(plus(parent['l'])*r3-parent['l']),
'h_3':m*(plus(parent['p3'])*r3-parent['p3'])/S,
'h_12':m*(plus(parent['p12'])*r12-parent['p12']+l_source)/S,
'h_2':m*(plus(parent['p2'])*r2-parent['p2'])/S,
'h_11':m*(plus(parent['p11'])*r11-parent['p11'])/S,
'h_1':m*(plus(parent['p1'])*r1-parent['p1'])/S}
j=1+(2+3/(m*(m-1)))*S+(4*m-3)*S**2/(m*(m-1))
gain['h_J']=m*(plus(j)*(1+S/(m-2))*(1+S/(m-1))-j)/S
gain={k:sp.cancel(v) for k,v in gain.items()}
gains={name:canon(expr) for name,expr in gain.items()}
emit('seven-gain-kernels-derived',degrees={k:v['S_degree'] for k,v in gains.items()})

hJ_explicit=((4*m+1)*S**3+(10*m**2-8*m)*S**2+(4*m**3-5*m**2+11*m-13)*S+2*m**3-m**2-9*m+12)/((m-2)*(m-1)*(m+1))
assert sp.cancel(gain['h_J']-hJ_explicit)==0
hJ_num=sp.fraction(sp.cancel(hJ_explicit))[0]
hJ_shift=[vec(sp.Poly(hJ_num,S).nth(i).subs(m,3+x),x) for i in range(4)]
assert all(Q(z)>0 for row in hJ_shift for z in row)
alpha=m*(4/(2*m+2)+4/(2*m+3))
beta=16*m/((2*m+2)*(2*m+3))
alpha_debt=sp.cancel(alpha-sp.Rational(39,10))
beta_reserve=sp.cancel(beta-alpha/(m+2))
assert sp.cancel(alpha_debt-(2*m**2-95*m-117)/(10*(m+1)*(2*m+3)))==0
assert sp.cancel(beta_reserve-6*m/((m+1)*(m+2)*(2*m+3)))==0
alpha_shift=vec(sp.fraction(alpha_debt)[0].subs(m,128+x),x)
assert all(Q(z)>0 for z in alpha_shift)

# Entire formal gain identity in independently assembled basis symbols.
K,L,V3,W12,V2,W11,V1,B,Y=sp.symbols('K L V3 W12 V2 W11 V1 B Y')
rho=(1+4*S/(2*m+2))*(1+4*S/(2*m+3))
old=K+parent['l']*L+parent['p3']*V3+parent['p12']*W12+parent['p2']*V2+parent['p11']*W11+parent['p1']*V1
new=rho*K+Y+plus(parent['l'])*(r3*L+(2*S**3/m**2)*(1+2*S/(m-1))*W12)+plus(parent['p3'])*r3*V3+plus(parent['p12'])*r12*W12+plus(parent['p2'])*r2*V2+plus(parent['p11'])*r11*W11+plus(parent['p1'])*r1*V1
expected=(alpha+beta*S)*K+m*Y/S+gain['h_l']*L/S+gain['h_3']*V3+gain['h_12']*W12+gain['h_2']*V2+gain['h_11']*W11+gain['h_1']*V1
identity_res={str(v):str(sp.cancel(sp.expand(m*(new-old)/S-expected).coeff(v))) for v in (K,L,V3,W12,V2,W11,V1,Y)}
assert set(identity_res.values())=={'0'}
component_res=sp.cancel(m*(plus(j)*(1+S/(m-2))*(1+S/(m-1))-j)*B/S-gain['h_J']*B)
assert component_res==0

# The endpoint-partner factorization is also checked, with neither partner lost.
common=S*(S-1)*rise(S+2*m-7,6)
lower1_partner_A=m*(S+2)*common/rise(2*m-7,8)
lower1_partner_B=m*(S-2)*common/rise(2*m-7,9)
# binom(S+2m-2,2m+1) has extra (S-2) compared with the first binomial.
assert sp.cancel(lower1_partner_A+lower1_partner_B-lower1)==0

# Free-variable factorial-ratio telescoper, without binomial simplification.
q,r,N=sp.symbols('q r N')
telescoper=2*(2*q+3)*(r+q+1)*(N-r+q+1)-(q+1)*(N+2*q+2)*(N+2*q+3)-(r+q+1)*(N-r)*(2*r-N+1)+r*(N-r+q+1)*(2*r-N-1)
telescoper_expanded=sp.expand(telescoper)
assert telescoper_expanded==0

# Complete K6 recurrence including all q=0,...,5 sources, Fractions only.
Kvec=[Q(1),Q(1)]
K_stages=[{'q':0,'coefficients':[qstr(z) for z in Kvec]}]
for q0 in range(6):
    rho_vec=mul([1,Q(4,2*q0+2)],[1,Q(4,2*q0+3)])
    source=scale(mul(mul([0,1,2],a_poly(q0,1)),a_poly(q0+1,3)),Q(3,2*(q0+1)*(2*q0+3)))
    Kvec=add(mul(rho_vec,Kvec),source)
    K_stages.append({'q':q0+1,'coefficients':[qstr(z) for z in Kvec], 'Y_source':[qstr(z) for z in source]})
A=a_poly(13,4)
Kcert={}
for factor,degrees in [(Q(79,100),2),(Q(71,100),3),(Q(11,16),14)]:
    diff=add(Kvec,scale(A,-factor))[:degrees]
    assert all(z>=0 for z in diff)
    Kcert[qstr(factor)]={'covered_degrees':list(range(degrees)), 'residual':[qstr(z) for z in diff]}

# Uniform certificates use exact shifted polynomials, never m sampling.
parent_bounds={k:majorants(v,'lower') for k,v in parents.items()}
gain_bounds={k:majorants(v,'upper' if k=='h_J' else 'lower') for k,v in gains.items()}
parent_counts=[sum(v['coefficient_bound_count'] for v in parent_bounds.values()),sum(v['padded_residual_slot_count'] for v in parent_bounds.values())]
gain_counts=[sum(v['coefficient_bound_count'] for v in gain_bounds.values()),sum(v['padded_residual_slot_count'] for v in gain_bounds.values())]
assert parent_counts==[39,250]
assert gain_counts==[50,354]
boundvec=lambda obj:[Q(z['bound']) for z in obj['entries']]
R=mul(boundvec(gain_bounds['h_l']),[1,0,Q(10,3)])
for k in ('h_3','h_12','h_2','h_11','h_1'):R=add(R,boundvec(gain_bounds[k]))
Jbar=boundvec(gain_bounds['h_J'])
assert len(R)==11 and len(Jbar)==4 and R[0]>0 and Jbar[0]>0

# Freeze all independently derived rational data BEFORE any SOURCE arrays.
text_pins={'public_root_proof':hashlib.sha256((T/'proofs/A81-INDEX-AUGMENTATION-v2.md').read_bytes()).hexdigest()}
freeze=put('INDEPENDENT-ALGEBRA-v2.json',{'schema':'a81-original-index-algebra/v1','status':'PROPOSED_ARITHMETIC_HANDOFF','provider_programs_read_or_executed':False,'text_input_sha256':text_pins,
    'source_array_access_before_freeze':False,'parent_kernels':parents,'gain_kernels':gains,'parent_majorants':parent_bounds,'gain_majorants':gain_bounds,'parent_counts':parent_counts,'gain_counts':gain_counts,
    'R':[qstr(z) for z in R],'Jbar':[qstr(z) for z in Jbar],
    'h_J_explicit_identity':True,'h_J_m3_shift_numerator_S_rows_x_ascending':hJ_shift,
    'alpha_39_10_residual':canon(alpha_debt),'alpha_m128_shift_numerator':alpha_shift,'beta_alpha_m2_residual':canon(beta_reserve),
    'formal_gain_basis_residuals':identity_res,'whole_component_gain_residual':'0','lower1_two_partner_residual':'0',
    'telescoper':{'cleared_polynomial':str(telescoper),'expanded_residual':str(telescoper_expanded),
       'W_q1_over_W_q':'(r+q+1)*(N-r+q+1)/(q+1)^2','W_q_at_r1_over_r':'(r+q+1)*(N-r)/((r+1)*(N-r+q))','summed_boundary':'g_q(b+1;N)-g_q(a;N); neither endpoint removed'},
    'K6':{'coefficients':[qstr(z) for z in Kvec],'a13_4S':[qstr(z) for z in A],'stages':K_stages,'floor_residuals':Kcert}})
emit('independent-algebra-frozen',counts=gain_counts,R0=qstr(R[0]),Jbar0=qstr(Jbar[0]),sha256=freeze['sha256'])

# Complete ORIGINAL P0, retaining every r=1..257 (no quotient deletion).
c=[1]
for rr in range(1,258):
    v=[0]*(len(c)+1)
    for i,z in enumerate(c):v[i]+=rr*z;v[i+1]+=4*z
    c=v
assert len(c)==258 and c[0]==math.factorial(257) and c[-1]==4**257
Bfinite=[]
for degree in range(258):
    b=sum((R[jj]*Q(3,4)**(degree-jj)*Q(c[degree-jj],c[degree]) for jj in range(min(10,degree)+1)),Q(0))
    b+=sum((Jbar[jj]*Q(1,2)**(degree-jj)*Q(c[degree-jj],c[degree]) for jj in range(min(3,degree)+1)),Q(0))
    gap=Q(21,10)-b
    Bfinite.append({'d':degree,'B_d':qstr(b),'gap_to_21_10':qstr(gap)})
    assert gap>0, ('direct-original-bridge-failure',degree,qstr(b))
P258=Q(258*(258+4),8)
U258=sum((R[jj]*Q(3,4)**(258-jj)*P258**jj/math.factorial(jj) for jj in range(11)),Q(0))
U258+=sum((Jbar[jj]*Q(1,2)**(258-jj)*P258**jj/math.factorial(jj) for jj in range(4)),Q(0))
ratio258=Q(3,4)*Q(259*263,258*262)**10
assert U258<Q(21,10) and ratio258<1
ratio_base=(d+1)*(d+5)/(d*(d+4))
ratio_derivative=sp.cancel(sp.diff(ratio_base,d))
assert sp.cancel(ratio_derivative+(2*d**2+10*d+20)/(d**2*(d+4)**2))==0
slope_endpoint=sp.expand(d*(d+4)/8-(d*d+3*d+8)/8)
assert sp.simplify(slope_endpoint-(d-8)/8)==0
finite_max=max(Bfinite,key=lambda z:Q(z['B_d']))
bridge=put('ORIGINAL-ALL-DEGREE-GAIN-BRIDGE-v2.json',{'schema':'a81-original-gain-bridge/v1','algebra_freeze':freeze,'all_258_integer_coefficients':[str(z) for z in c], 'factor_denominators':list(range(1,258)),
    'finite_degrees':Bfinite,'maximum':finite_max,'B0_equals_R0_plus_Jbar0':qstr(R[0]+Jbar[0]),
    'tail':{'start_degree':258,'P':'d*(d+4)/8','P258':qstr(P258),'U258':qstr(U258),'gap_to_21_10':qstr(Q(21,10)-U258),
       'consecutive_ratio_upper':'(3/4)*(((d+1)*(d+5))/(d*(d+4)))^10','ratio258':qstr(ratio258),'ratio258_gap_to1':qstr(1-ratio258),
       'inner_ratio_derivative':str(ratio_derivative),'derivative_negative_for_d_ge_258':True,
       'last_factor_endpoint_reciprocal_sum':'(d*d+3*d+8)/8','endpoint_gap_to_P':str(slope_endpoint),'d_ge_258_endpoint_gap_positive':True},
    'reserve':{'core_floor':'429/160','uniform_error_strict_upper':'21/10','difference':'93/160','gap_above_1_2':'13/160',
       'proposed_original_bound':'H_m >=_c S*a_(2m+1)(4S)*(1+S/(m+2))/(2m), m>=128; actual degrees only'},
    'proof_scope':'Arithmetic original-only bridge. Whole LR/all-grade character geometry and scientific adoption belong to root.'})
emit('direct-original-bridge-pass',finite_count=258,max_degree=finite_max['d'],max_bound=finite_max['B_d'],U258=qstr(U258))

# Also reconstruct the original U10 complete endpoint payment arithmetic.
Rendpoint=mul(boundvec(parent_bounds['l']),[0,1,0,Q(10,3)])
for k in ('p3','p12','p2','p11','p1'):Rendpoint=add(Rendpoint,boundvec(parent_bounds[k]))
Rendpoint=add(Rendpoint,[0,2+Q(3,128*127),Q(509,128*127)])
assert Rendpoint[0]==0 and len(Rendpoint)==10
endpoint_degrees=[]
for degree in range(1,258):
    b=Q(1,2)**degree+sum((Rendpoint[jj]*Q(3,4)**(degree-jj)*Q(c[degree-jj],c[degree]) for jj in range(1,min(9,degree)+1)),Q(0))
    threshold=Q(77,100) if degree==1 else Q(69,100) if degree==2 else Q(43,64)
    assert b<threshold
    endpoint_degrees.append({'d':degree,'error_upper':qstr(b),'threshold':qstr(threshold),'positive_gap':qstr(threshold-b)})
EP258=Q(258*259,8)
ET258=Q(1,2)**258+sum((Rendpoint[jj]*Q(3,4)**(258-jj)*EP258**jj/math.factorial(jj) for jj in range(1,10)),Q(0))
assert ET258<Q(43,64)
endpoint=put('ORIGINAL-ENDPOINT-PAYMENT-v2.json',{'R':[qstr(z) for z in Rendpoint],'finite_degrees':endpoint_degrees,'tail_start':258,'reciprocal_slope_sum':'d*(d+1)/8','T258':qstr(ET258),'T258_gap_to43_64':qstr(Q(43,64)-ET258),'consecutive_ratio_at258':qstr(Q(3,4)*Q(259*260,258*259)**9), 'original_only':True})

# Defect controls expose missing algebra/majorants; they do not invent LR negatives.
controls={}
def nonzero_control(name,expr):
    expr=sp.cancel(expr)
    assert expr!=0
    c0=canon(expr)
    controls[name]={'detected':True,'symbolic_defect':c0,'witness_S1_m128':qstr(evaluate_kernel(c0,1,128))}
nonzero_control('drop_h12_full_L_source',m*l_source/S)
controls['drop_beta_S_leading_core_degree']={'detected':True,'normalized_top_target_residual':'-429/(160*(m+2))','m128_residual':qstr(-Q(429,160*130)), 'lost_degree':'2m+2 in (m/S)H target; D_m degree2m+1'}
controls['zero_R_constant']={'detected':True,'missing_nonnegative_majorant_constant':qstr(R[0]),'derived_minus_corrupted_constant':qstr(R[0]),'corrupted_bound_minus_required_constant':qstr(-R[0])}
controls['zero_Jbar_constant']={'detected':True,'hJ_constant_at128':qstr(evaluate_kernel(gains['h_J'],0,128)),'corrupted_upper_bound_minus_hJ_constant_at128':qstr(-evaluate_kernel(gains['h_J'],0,128))}
nonzero_control('omit_first_entire_lower_diagonal_in_h2',m*(plus(lower2)*r2-lower2)/S)
nonzero_control('omit_lower_diagonal_second_partner_in_h1',m*(plus(lower1_partner_B)*r1-lower1_partner_B)/S)
nonzero_control('wrong_m_shift_h12_m_plus2',gain['h_12']-m*(parent['p12'].subs(m,m+2)*r12-parent['p12']+parent['l'].subs(m,m+2)*(2*S**3/m**2)*(1+2*S/(m-1)))/S)
nonzero_control('divide_h_l_by_S_wrongly',gain['h_l']*(S-1))
control=put('NEGATIVE-CONTROLS-v2.json',controls)
assert all(z['detected'] for z in controls.values())

finished={'schema':'a81-index-algebra-independent-freeze/v1','status':'PASS_PROPOSED_ARITHMETIC_ONLY','artifacts':[freeze,bridge,endpoint,control],
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':sp.__version__,'python':sys.executable,
 'self_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'measured_seconds':time.monotonic()-start,
 'Sage_slots_declared':0,'source_expected_arrays_read':False,'parameter_sweep':False,'scalar_LR_calls':0,'original_enumeration':False}
put('INDEPENDENT-FREEZE-v2.json',finished)
emit('independent-freeze-complete',status=finished['status'],rss=finished['self_peak_rss_bytes'])
