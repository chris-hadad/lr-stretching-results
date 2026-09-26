"""Unchanged mathematical/input functions from the accepted independent checker."""
from math import comb
from exact import need, integer
PARENTS = {"P00": (0, 0), "P10": (1, 0), "P20": (2, 0), "P11": (1, 1)}

def family(x,y):
    need(type(x) is int and type(y) is int and x>=0 and y>=0,"Invalid integer quadrant parameter")
    alpha=[2*x+5+2*y,x+4+2*y,3+2*y,2+2*y,1+y]
    beta=[x+3+2*y]*3+[y+2]*3
    lam=[sum(beta[i:]) for i in range(6)]
    return {"x":x,"y":y,"alpha":alpha,"beta":beta,
            "bare_triple":{"lambda":lam,"mu":lam[1:],"nu":alpha}}


def gt_hypotheses(parent):
    a,b=parent["alpha"],parent["beta"]
    need(len(a)==5 and len(b)==6 and all(type(x) is int and x>0 for x in a+b),"Wrong strict GT shapes")
    need(all(a[i]>a[i+1] for i in range(4)) and b==sorted(b,reverse=True) and sum(a)==sum(b),"GT partition/trace hypotheses fail")
    gaps=[sum(a[:k])-sum(b[:k]) for k in range(1,5)]
    need(all(x>0 for x in gaps) and gaps[2]==3,"Strict dominance/gap-three premise fails")
    ceil=lambda x,y:(x+y-1)//y
    costs=[ceil(5,b[-1]),*(ceil(2,a[i]-a[i+1]) for i in range(4)),ceil(2,a[-1]),
           *(ceil(k*(6-k),gaps[k-1]) for k in range(1,5))]
    degree=(5-1)*6-5*6//2+1
    need(degree==10 and max(costs)==3,"Parent outside the fixed degree/codegree premise")
    return {"dimension":degree,"codegree":3,"dominance_gaps":gaps,"staircase_costs":costs,
            "lattice":"saturated Z^10, conditional on the explicitly cited strict weighted-GT theorem",
            "known_values":{"-2":0,"-1":0,"0":1},"determining_positive_grades":list(range(1,9)),
            "unused_positive_grades":[9,10]}


def query(parent,grade,max_work,milliseconds,max_cells):
    need(parent in PARENTS and type(grade) is int and 1<=grade<=10,"Out-of-roster parent/grade")
    need(type(max_work) is int and 0<max_work<2**63 and type(milliseconds) is int and 0<milliseconds<=100000
         and type(max_cells) is int and 0<max_cells<=1000000,"Invalid explicit counter limit")
    x,y=PARENTS[parent]
    return f"GAP3JT1 {parent}:t{grade} FAMILY {max_work} {milliseconds} {max_cells} {x} {y} {grade}\n"


def complete_counter_record(counter,identity,grade):
    need(counter["id"]==identity and counter["status"]=="COMPLETE" and counter["mode"]=="FAMILY",
         "Wrong complete counter object")
    value=integer(counter["count"])
    states,admitted,terms,zero,distinct=(integer(counter[k]) for k in
        ("simplex_states","admitted_states","determinant_terms","literal_zero_terms","nonzero_sorted_degree_terms"))
    need(value>=0 and integer(counter["permutations"])==120
         and integer(counter["even_permutations"])==integer(counter["odd_permutations"])==60
         and states==comb(3*grade+2,2) and 0<=admitted<=states and terms==120*admitted
         and 0<=zero<=terms and 0<=distinct<=terms-zero,"Incomplete state/permutation/term roster or scalar")
    return value
