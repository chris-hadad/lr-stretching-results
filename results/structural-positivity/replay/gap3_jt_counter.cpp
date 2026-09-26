// Complete root-derived Jacobi--Trudi / three-column matrix counter.
// Checked signed 128-bit arithmetic; the approved scope has total degree <=90,
// at most 15 matrix entries, at most 496 first states and all 120 permutations.
// One request: GAP3JT1 id MODE max_work milliseconds max_cells <payload>.
// FAMILY x y t; PROFILE/TERMS t alpha[5] beta[6]; MATRIX n c[3] r[n].
// SIGNS and ARITH (ADD/SUB/MUL a b) are self-authored fixture interfaces.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using I=__int128_t;
using U=__uint128_t;
using Degree=std::array<int,5>;
struct Refusal : std::runtime_error { using std::runtime_error::runtime_error; };
static I add(I a,I b) { I z;if (__builtin_add_overflow(a,b,&z)) throw Refusal("REFUSED_OVERFLOW");return z; }
static I sub(I a,I b) { I z;if (__builtin_sub_overflow(a,b,&z)) throw Refusal("REFUSED_OVERFLOW");return z; }
static I mul(I a,I b) { I z;if (__builtin_mul_overflow(a,b,&z)) throw Refusal("REFUSED_OVERFLOW");return z; }
static std::string decimal(I value) {
    bool negative=value<0;
    U magnitude=negative ? static_cast<U>(-(value+1))+1 : static_cast<U>(value);
    std::string out;
    do { out.push_back(static_cast<char>('0'+magnitude%10));magnitude/=10; } while (magnitude);
    if (negative) out.push_back('-');
    std::reverse(out.begin(),out.end());return out;
}
static I exact(std::istream& in) {
    std::string word;if (!(in>>word) || word.empty()) throw Refusal("REFUSED_INPUT");
    bool negative=word[0]=='-';std::size_t start=negative ? 1 : 0;
    if (start==word.size()) throw Refusal("REFUSED_INPUT");
    I result=0;
    for (std::size_t i=start;i<word.size();++i) {
        if (word[i]<'0' || word[i]>'9') throw Refusal("REFUSED_INPUT");
        result=mul(result,10);
        result=negative ? sub(result,word[i]-'0') : add(result,word[i]-'0');
    }
    return result;
}
static int small(std::istream& in) {
    I n=exact(in);
    if (n<std::numeric_limits<int>::min() || n>std::numeric_limits<int>::max())
        throw Refusal("REFUSED_OVERFLOW");
    return static_cast<int>(n);
}
struct Budget {
    std::uint64_t work=0,limit,cells;
    std::chrono::steady_clock::time_point end;
    Budget(I maximum,int ms,I cap) {
        if (maximum<=0 || maximum>std::numeric_limits<std::int64_t>::max()
            || ms<=0 || ms>100000 || cap<=0 || cap>1000000) throw Refusal("REFUSED_LIMITS");
        limit=static_cast<std::uint64_t>(maximum);cells=static_cast<std::uint64_t>(cap);
        end=std::chrono::steady_clock::now()+std::chrono::milliseconds(ms);
    }
    void check() const {
        if (std::chrono::steady_clock::now()>=end) throw Refusal("REFUSED_TIME");
    }
    void tick() {
        if (work==limit) throw Refusal("REFUSED_WORK");
        ++work;if ((work&1023)==0) check();
    }
};
struct Perm { std::array<int,5> p;int sign; };
static std::vector<Perm> permutations() {
    std::array<int,5> p{{0,1,2,3,4}};std::vector<Perm> result;
    do {
        int inversions=0;
        for (int i=0;i<5;++i) for (int j=i+1;j<5;++j) inversions+=p[i]>p[j];
        result.push_back({p,inversions%2 ? -1 : 1});
    } while (std::next_permutation(p.begin(),p.end()));
    if (result.size()!=120) throw Refusal("REFUSED_INTERNAL_PERMUTATIONS");
    return result;
}

// D[p,q] is the sum along p+q=constant from its smallest p through this p.
// H_n*f(i,j) is one closed interval on this diagonal, with ALL exponent splits.
static I window(const std::vector<I>& diagonal,int h,int w,int i,int j,int n) {
    if (i<0 || j<0 || n<0 || i>=h || j>=w) return 0;
    int lo=std::max(0,n-j),hi=std::min(n,i);
    if (lo>hi) return 0;
    int ph=i-lo,qh=j-n+lo,pl=i-hi,ql=j-n+hi;
    I answer=diagonal[static_cast<std::size_t>(ph*w+qh)];
    if (pl>0 && ql+1<w) answer=sub(answer,diagonal[static_cast<std::size_t>((pl-1)*w+ql+1)]);
    return answer;
}
static I matrices(const std::vector<int>& rows,const std::array<int,3>& columns,Budget& budget) {
    if (rows.size()>5) throw Refusal("REFUSED_SCOPE");
    int total=0,goal=0;
    for (int r:rows) { if (r<0) return 0;if (r>90) throw Refusal("REFUSED_SCOPE");total+=r; }
    for (int c:columns) { if (c<0) return 0;if (c>90) throw Refusal("REFUSED_SCOPE");goal+=c; }
    if (total!=goal) return 0;
    if (goal>90) throw Refusal("REFUSED_SCOPE");
    int h=columns[0]+1,w=columns[1]+1;
    std::size_t cells=static_cast<std::size_t>(h*w);
    if (cells>budget.cells) throw Refusal("REFUSED_TABLE_SIZE");
    std::vector<I> f(cells),diagonal(cells),next(cells);f[0]=1;
    int degree=0;
    for (int r:rows) {
        budget.check();if (r==0) continue;
        for (int i=0;i<h;++i) for (int j=0;j<w;++j) {
            budget.tick();auto k=static_cast<std::size_t>(i*w+j);
            diagonal[k]=f[k];
            if (i>0 && j+1<w) diagonal[k]=add(diagonal[k],diagonal[static_cast<std::size_t>((i-1)*w+j+1)]);
        }
        for (int i=0;i<h;++i) for (int j=0;j<w;++j) {
            budget.tick();auto k=static_cast<std::size_t>(i*w+j);
            next[k]=add(sub(f[k],window(diagonal,h,w,i,j,r+1)),window(diagonal,h,w,i-1,j-1,r));
        }
        // Invert (1-x)(1-y) by the ENTIRE 2D prefix. No third-margin filter is
        // applied to the RHS or during inversion; negative RHS entries survive.
        for (int i=0;i<h;++i) for (int j=0;j<w;++j) {
            budget.tick();auto k=static_cast<std::size_t>(i*w+j);
            if (i) next[k]=add(next[k],next[static_cast<std::size_t>((i-1)*w+j)]);
            if (j) next[k]=add(next[k],next[static_cast<std::size_t>(i*w+j-1)]);
            if (i && j) next[k]=sub(next[k],next[static_cast<std::size_t>((i-1)*w+j-1)]);
            if (next[k]<0) throw Refusal("REFUSED_INTERNAL_NEGATIVE_MATRIX_COEFFICIENT");
        }
        degree+=r;f.swap(next);
    }
    // Exact total degree fixes the third column at the final coefficient.
    if (degree!=goal) throw Refusal("REFUSED_INTERNAL_TOTAL_DEGREE");
    budget.check();return f[static_cast<std::size_t>(columns[0]*w+columns[1])];
}
struct Roster {
    std::map<Degree,I> weights;
    std::uint64_t states=0,admitted=0,terms=0,zero_terms=0;
};
static Roster roster(const Degree& alpha,const std::array<int,6>& beta,int t,
                     const std::vector<Perm>& ps,Budget& budget) {
    if (t<0 || t>10) throw Refusal("REFUSED_SCOPE");
    int sa=0,sb=0;
    for (int i=0;i<5;++i) {
        if (alpha[i]<0 || alpha[i]>90 || t*alpha[i]>90 || (i && alpha[i]>alpha[i-1]))
            throw Refusal("REFUSED_SHAPE_SCOPE");
        sa+=alpha[i];
    }
    for (int i=0;i<6;++i) {
        if (beta[i]<0 || beta[i]>90 || t*beta[i]>90 || (i && beta[i]>beta[i-1]))
            throw Refusal("REFUSED_CONTENT_SCOPE");
        sb+=beta[i];
    }
    if (sa!=sb || alpha[0]+alpha[1]+alpha[2]-beta[0]-beta[1]-beta[2]!=3)
        throw Refusal("REFUSED_NOT_BALANCED_GAP3");
    int deficit=3*t,tail=t*(beta[3]+beta[4]+beta[5]);
    if (tail>90) throw Refusal("REFUSED_SCOPE");
    Roster out;
    for (int u1=0;u1<=deficit;++u1) for (int u2=0;u2<=deficit-u1;++u2) {
        budget.tick();++out.states;
        int u3=deficit-u1-u2;
        Degree eta{{t*alpha[0]-u1,t*alpha[1]-u2,t*alpha[2]-u3,0,0}};
        if (eta[2]<0 || eta[0]<eta[1] || eta[1]<eta[2]) continue;
        int m=std::min({eta[0]-eta[1],eta[1]-eta[2],eta[0]-t*beta[0],t*beta[2]-eta[2]});
        if (m<0) continue;
        ++out.admitted;
        for (const auto& p:ps) {
            budget.tick();++out.terms;Degree r;bool zero=false;int sum=0;
            for (int i=0;i<5;++i) {
                r[i]=t*alpha[i]-eta[p.p[i]]-i+p.p[i];
                zero=zero || r[i]<0;sum+=r[i];
            }
            if (zero) { ++out.zero_terms;continue; }
            if (sum!=tail) throw Refusal("REFUSED_INTERNAL_DETERMINANT_DEGREE");
            std::sort(r.begin(),r.end());
            out.weights[r]=add(out.weights[r],mul(p.sign,m+1));
        }
    }
    if (out.terms!=120*out.admitted) throw Refusal("REFUSED_INTERNAL_INCOMPLETE_DETERMINANT");
    budget.check();return out;
}
static void emit_terms(std::ostream& out,const Roster& r) {
    out<<"[";bool first=true;
    for (const auto& item:r.weights) {
        if (item.second==0) continue;
        if (!first) out<<",";
        first=false;out<<"{\"rows\":[";
        for (int i=0;i<5;++i) { if (i) out<<",";out<<item.first[i]; }
        out<<"],\"weight\":\""<<decimal(item.second)<<"\"}";
    }
    out<<"]";
}
int main() {
    std::string protocol,id="invalid",mode;
    auto started=std::chrono::steady_clock::now();std::uint64_t work=0;
    try {
        if (!(std::cin>>protocol>>id>>mode) || protocol!="GAP3JT1") throw Refusal("REFUSED_INPUT");
        if (id.empty() || id.size()>128 || id.find_first_not_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:_-.")!=std::string::npos)
            throw Refusal("REFUSED_ID");
        I cap=exact(std::cin);int ms=small(std::cin);I cells=exact(std::cin);
        Budget budget(cap,ms,cells);auto ps=permutations();I answer=0;std::ostringstream detail;
        try {
            if (mode=="SIGNS") {
                detail<<",\"permutation_roster\":[";
                for (std::size_t i=0;i<ps.size();++i) {
                    if (i) detail<<",";
                    detail<<"{\"permutation\":[";
                    for (int j=0;j<5;++j) { if (j) detail<<",";detail<<ps[i].p[j]; }
                    detail<<"],\"sign\":"<<ps[i].sign<<"}";
                }
                detail<<"]";
            } else if (mode=="ARITH") {
                std::string operation;std::cin>>operation;I a=exact(std::cin),b=exact(std::cin);
                if (operation=="ADD") answer=add(a,b);
                else if (operation=="SUB") answer=sub(a,b);
                else if (operation=="MUL") answer=mul(a,b);
                else throw Refusal("REFUSED_INPUT");
            } else if (mode=="MATRIX") {
                int n=small(std::cin);
                if (n<0 || n>5) throw Refusal("REFUSED_SCOPE");
                std::array<int,3> columns;
                for (int& x:columns) x=small(std::cin);
                std::vector<int> rows(static_cast<std::size_t>(n));
                for (int& x:rows) x=small(std::cin);
                answer=matrices(rows,columns,budget);
            } else if (mode=="FAMILY" || mode=="PROFILE" || mode=="TERMS") {
                Degree alpha;std::array<int,6> beta;int t;
                if (mode=="FAMILY") {
                    int x=small(std::cin),y=small(std::cin);t=small(std::cin);
                    if (!((y==0 && x>=0 && x<=2) || (x==1 && y==1))) throw Refusal("REFUSED_PARENT_SCOPE");
                    alpha={{2*x+5+2*y,x+4+2*y,3+2*y,2+2*y,1+y}};
                    int large=x+3+2*y,small_value=y+2;
                    beta={{large,large,large,small_value,small_value,small_value}};
                } else {
                    t=small(std::cin);
                    for (int& x:alpha) x=small(std::cin);
                    for (int& x:beta) x=small(std::cin);
                }
                auto r=roster(alpha,beta,t,ps,budget);std::size_t nonzero=0;
                for (const auto& item:r.weights) if (item.second) ++nonzero;
                detail<<",\"simplex_states\":"<<r.states<<",\"admitted_states\":"<<r.admitted
                      <<",\"determinant_terms\":"<<r.terms<<",\"literal_zero_terms\":"<<r.zero_terms
                      <<",\"nonzero_sorted_degree_terms\":"<<nonzero;
                if (mode=="TERMS") { detail<<",\"terms\":";emit_terms(detail,r); }
                else {
                    std::array<int,3> columns{{t*beta[3],t*beta[4],t*beta[5]}};
                    for (const auto& item:r.weights) {
                        budget.check();if (!item.second) continue;
                        I count=matrices(std::vector<int>(item.first.begin(),item.first.end()),columns,budget);
                        answer=add(answer,mul(item.second,count));
                    }
                    if (answer<0) throw Refusal("REFUSED_INTERNAL_NEGATIVE_WHOLE_COUNT");
                }
            } else throw Refusal("REFUSED_MODE");
            std::string extra;if (std::cin>>extra) throw Refusal("REFUSED_EXTRA_INPUT");
            budget.check();work=budget.work;
        } catch (...) { work=budget.work;throw; }
        double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();
        std::cout<<"{\"id\":\""<<id<<"\",\"status\":\"COMPLETE\",\"count\":";
        if (mode=="TERMS" || mode=="SIGNS") std::cout<<"null";else std::cout<<"\""<<decimal(answer)<<"\"";
        std::cout<<",\"mode\":\""<<mode<<"\",\"work\":"<<work
                 <<",\"permutations\":120,\"even_permutations\":60,\"odd_permutations\":60"
                 <<",\"elapsed_seconds\":"<<elapsed<<detail.str()<<"}\n";
        return 0;
    } catch (const Refusal& error) {
        if (id.empty() || id.size()>128 || id.find_first_not_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:_-.")!=std::string::npos) id="invalid";
        std::cout<<"{\"id\":\""<<id<<"\",\"status\":\""<<error.what()<<"\",\"count\":null,\"work\":"<<work<<"}\n";
        return 2;
    } catch (const std::bad_alloc&) {
        std::cout<<"{\"id\":\"invalid\",\"status\":\"REFUSED_MEMORY\",\"count\":null}\n";return 2;
    }
}
