"""Fresh threshold96 certificate using frozen independent kernels only."""
import hashlib,json,math,resource,sys,time
from fractions import Fraction as Q
from pathlib import Path

T=Path(__file__).resolve().parents[1]
R=Path(sys.argv[1])
assert R.is_dir()
start=time.monotonic()
failures=[]
def check(ok,label,**evidence):
    if not ok:failures.append(dict(check=label,**evidence))
    return ok

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def qs(z):
    z=Q(z)
    return str(z.numerator) if z.denominator==1 else str(z.numerator)+'/'+str(z.denominator)
def put(name,data):
    p=R/name
    with p.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
    return {'path':str(p),'sha256':sha(p)}
def shift(a,k):
    out=[Q(0)]*len(a)
    for i,z in enumerate(a):
        for h in range(i+1):out[h]+=Q(z)*math.comb(i,h)*k**(i-h)
    return out
def add(a,b):
    out=[Q(0)]*max(len(a),len(b))
    for i,z in enumerate(a):out[i]+=z
    for i,z in enumerate(b):out[i]+=z
    return out
def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):out[i+j]+=u*v
    return out

input_path=R/'INDEPENDENT-ALGEBRA-v2.json'
own=json.loads(input_path.read_text())
bindings={'input_path':str(input_path),'input_sha256':sha(input_path),'script_sha256':sha(Path(__file__))}
put('PRE-CALCULATION-BINDING-v1.json',dict(bindings,identity='public-threshold96',threshold=96,expected_SOURCE_arrays_read=False))

bounds={}
for name in ('h_l','h_3','h_12','h_2','h_11','h_1','h_J'):
    kernel=own['gain_kernels'][name]
    D=shift(kernel['denominator_m_ascending'],96)
    if not check(all(z>0 for z in D),name+'.strictly_positive_denominator',coefficients=[qs(z) for z in D]):
        raise ValueError('Nonpositive denominator: '+name)
    sign=1 if name=='h_J' else -1
    entries=[]
    for i,row in enumerate(kernel['numerator_S_rows_m_ascending']):
        N=shift(row,96)
        if not check(len(N)<=len(D),name+'.numerator_degree_bound',S_degree=i):raise ValueError('Degree debt')
        N += [Q(0)]*(len(D)-len(N))
        ratios=[sign*n/d for n,d in zip(N,D)]
        b=max(Q(0),*ratios)
        residual=[b*d-sign*n for n,d in zip(N,D)]
        check(all(z>=0 for z in residual),name+'.all_residual_coefficients',S_degree=i)
        entries.append({'S_degree':i,'bound':qs(b),'numerator_x_ascending':[qs(z) for z in N],
            'coefficient_ratios':[qs(z) for z in ratios],'max_ratio_indices':[h for h,z in enumerate(ratios) if z==b],
            'residual_x_padded':[qs(z) for z in residual]})
    bounds[name]={'kind':'upper' if name=='h_J' else 'lower','denominator_x_ascending':[qs(z) for z in D],
        'entries':entries,'coefficient_count':len(entries),'padded_residual_slots':len(entries)*len(D)}
count=sum(z['coefficient_count'] for z in bounds.values())
slots=sum(z['padded_residual_slots'] for z in bounds.values())
check(count==50,'all50_bounds',actual=count)
check(slots==354,'all354_padded_slots',actual=slots)
bv=lambda name:[Q(z['bound']) for z in bounds[name]['entries']]
R96=mul(bv('h_l'),[Q(1),Q(0),Q(10,3)])
for name in ('h_3','h_12','h_2','h_11','h_1'):R96=add(R96,bv(name))
J96=bv('h_J')
check(len(R96)==11 and len(J96)==4,'complete_error_degrees')
check(R96[0]>0 and J96[0]>0,'retain_both_constants',R0=qs(R96[0]),Jbar0=qs(J96[0]))
check(all(z>=0 for z in R96+J96),'all_error_coefficients_nonnegative')

alpha_numerator=shift([-117,-95,2],96)
check(alpha_numerator==list(map(Q,[9195,289,2])),'alpha_shift_exact')
check(all(z>0 for z in alpha_numerator),'alpha_shift_positive')
alpha_old=own['alpha_39_10_residual']
check(shift(alpha_old['numerator_S_rows_m_ascending'][0],96)==alpha_numerator,'previous_symbolic_alpha_identity_binding')
check(all(z>0 for z in shift(alpha_old['denominator_m_ascending'],96)),'alpha_denominator_positive')
beta_old=own['beta_alpha_m2_residual']
check(all(z>0 for z in shift(beta_old['numerator_S_rows_m_ascending'][0],96)),'beta_reserve_numerator_positive')
check(all(z>0 for z in shift(beta_old['denominator_m_ascending'],96)),'beta_reserve_denominator_positive')
K6=own['K6']
check(all(Q(z)>=0 for z in K6['floor_residuals']['11/16']['residual']),'existing_full_K6_floor_all14_slots')
check(Q(11,16)*Q(39,10)==Q(429,160),'core_floor_scalar')
majorants=put('MAJORANTS-v1.json',{'schema':'a81-original-gain-majorants-threshold96/v1',**bindings,'m0':96,'kernels':bounds,
    'coefficient_count':count,'padded_residual_slot_count':slots,'R96':[qs(z) for z in R96],'Jbar96':[qs(z) for z in J96],
    'alpha_m96_numerator_x_ascending':[qs(z) for z in alpha_numerator],'beta_identity_unchanged':True,'K6_floor_unchanged':True,'failures':list(failures)})

# EVERY original factor r=1..193, retaining every integer coefficient.
c=[1]
for r in range(1,194):
    v=[0]*(len(c)+1)
    for i,z in enumerate(c):v[i]+=r*z;v[i+1]+=4*z
    c=v
check(len(c)==194,'all194_integer_coefficients')
check(c[0]==math.factorial(193) and c[-1]==4**193,'full_product_endpoints')
finite=[]
for d in range(194):
    pieces_R=[R96[j]*Q(3,4)**(d-j)*Q(c[d-j],c[d]) for j in range(min(10,d)+1)]
    pieces_J=[J96[j]*Q(1,2)**(d-j)*Q(c[d-j],c[d]) for j in range(min(3,d)+1)]
    value=sum(pieces_R+pieces_J,Q(0));gap=Q(21,10)-value
    check(gap>0,'finite_B_'+str(d),B_d=qs(value),gap=qs(gap))
    finite.append({'d':d,'R_terms':[qs(z) for z in pieces_R],'Jbar_terms':[qs(z) for z in pieces_J],
        'B_d':qs(value),'gap_to_21_10':qs(gap)})

P194=Q(194*198,8)
tail_R=[R96[j]*Q(3,4)**(194-j)*P194**j/math.factorial(j) for j in range(11)]
tail_J=[J96[j]*Q(1,2)**(194-j)*P194**j/math.factorial(j) for j in range(4)]
U194=sum(tail_R+tail_J,Q(0));tail_gap=Q(21,10)-U194
check(tail_gap>0,'U194_strictly_below_21_10',U194=qs(U194),gap=qs(tail_gap))
ratio194=Q(3,4)*Q(195*199,194*198)**10
check(ratio194<1,'consecutive_ratio_at194',value=qs(ratio194),gap=qs(1-ratio194))
# Existing program-checked derivative is -(2d^2+10d+20)/(d^2(d+4)^2).
# Numerator at d=194+x is 77232+786x+2x^2, strictly positive.
derivative_positive=shift([20,10,2],194)
check(all(z>0 for z in derivative_positive),'ratio_derivative_negative_for_d_ge194')
check(Q(194-8,8)>0,'extra_factor_endpoint_gap_at194')
maxrow=max(finite,key=lambda z:Q(z['B_d']))
bridge=put('ORIGINAL-ALL-DEGREE-BRIDGE-v1.json',{'schema':'a81-original-gain-threshold96-bridge/v1',**bindings,'majorants_binding':majorants,
    'm0':96,'all_original_factor_denominators':list(range(1,194)),'all194_integer_coefficients':[str(z) for z in c],
    'finite_degrees':finite,'finite_count':len(finite),'maximum':maxrow,
    'tail':{'start_degree':194,'P':'d*(d+4)/8','P194':qs(P194),'all_R_terms_at194':[qs(z) for z in tail_R],'all_Jbar_terms_at194':[qs(z) for z in tail_J],
        'U194':qs(U194),'gap_to_21_10':qs(tail_gap),'consecutive_ratio194':qs(ratio194),'ratio194_gap_to1':qs(1-ratio194),
        'decreasing_ratio_derivative':'-(2*d^2+10*d+20)/(d^2*(d+4)^2)','negative_derivative_numerator_at194_x':[qs(z) for z in derivative_positive],
        'original_first_d_reciprocal_sum':'d*(d+1)/8','extra_factor_endpoint_reciprocal_sum':'(d*d+3*d+8)/8',
        'extra_factor_endpoint_gap_to_P':'(d-8)/8','endpoint_gap_at194':qs(Q(194-8,8)),
        'algebraic_monotonicity_binding':'Existing symbolic derivative/endpoint identities in INDEPENDENT-ALGEBRA/ORIGINAL-ALL-DEGREE-GAIN-BRIDGE-v2; lower start checked exactly.'},
    'core_floor':'429/160','uniform_error_strict_upper':'21/10','whole_margin':'93/160','gap_above_half':'13/160',
    'prospective_original_bound':'H_m >=_c S*a_(2m+1)(4S)*(1+S/(m+2))/(2m), every m>=96; G strengthening via full positive J gain.',
    'actual_degree':'T degree2m+2; H/G degree2m+3 and zero constant; no quotient deletion or extra target-factor omission.',
    'failures':list(failures)})

# Preserve every failed slot as well as successful complete arrays; do not sweep.
status='PASS_PROPOSED_THRESHOLD96_ARITHMETIC_ONLY' if not failures else 'FAILED_THRESHOLD96_PRESERVED'
finish={'schema':'a81-original-gain-threshold96-result/v1','identity':'public-threshold96','status':status,**bindings,
    'majorants':majorants,'bridge':bridge,'failures':failures,'threshold_sweep':False,'expected_SOURCE_arrays_read':False,
    'provider_programs_read_or_executed':False,'quotient_theorem_adoption':False,'scientific_adoption':False,'scalar_LR_calls':0,'original_enumeration':False,
    'changed_proof_statement':'Uniform original-only H/G raw-gain reserve starts m>=96 if root adopts; finite join becomes transitionsm3..95 with complete endpointsm3..96. Existing H3 exception remains.',
    'self_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'seconds':time.monotonic()-start,'python':sys.executable,'declared_Sage_slots':1,
    'stop':'Root mathematical judgment, independent gate/adoption and finite integration remain separate.'}
put('RESULT-v1.json',finish)
print(json.dumps({'status':status,'failures':len(failures),'bounds':count,'slots':slots,'finite_degrees':len(finite),
    'maximum_degree':maxrow['d'],'maximum_bound':maxrow['B_d'],'R0':qs(R96[0]),'Jbar0':qs(J96[0]),'U194_exact':qs(U194),
    'U194_informational':float(U194),'ratio194_exact':qs(ratio194),'ratio194_informational':float(ratio194),'seconds':finish['seconds'],'self_peak_rss_bytes':finish['self_peak_rss_bytes']}),flush=True)
sys.exit(0 if not failures else 1)
