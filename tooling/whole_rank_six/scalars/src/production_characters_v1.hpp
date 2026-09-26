#pragma once
// Exact native character correction. Producer uses rational Galois traces;
// checker sums every character in one exact field and uses the reverse polar order.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <functional>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace a19char {
using Q=mpq_class;
using Matrix=std::vector<std::vector<Q>>;
using Normal=std::array<int,10>;
using Normals=std::array<Normal,9>;
using Theta=std::array<Q,9>;
using Element=std::vector<Q>;
inline void require(bool x,const char*message){if(!x)throw std::runtime_error(message);}
inline long factorial(int n){long v=1;for(int i=2;i<=n;++i)v*=i;return v;}
inline Q rational(long a,long b){Q x(a,b);x.canonicalize();return x;}
inline Q fractional(Q x){mpz_class quotient;mpz_fdiv_q(quotient.get_mpz_t(),x.get_num_mpz_t(),x.get_den_mpz_t());x-=quotient;return x;}
inline Matrix inverse(Matrix a){size_t n=a.size();for(size_t i=0;i<n;++i){require(a[i].size()==n,"square exact inverse");a[i].resize(2*n);a[i][n+i]=1;}
 for(size_t p=0;p<n;++p){size_t pivot=p;while(pivot<n&&a[pivot][p]==0)++pivot;require(pivot<n,"nonsingular exact inverse");std::swap(a[p],a[pivot]);Q d=a[p][p];for(Q&v:a[p])v/=d;for(size_t i=0;i<n;++i)if(i!=p){Q x=a[i][p];if(x!=0)for(size_t j=0;j<2*n;++j)a[i][j]-=x*a[p][j];}}
 Matrix out(n,std::vector<Q>(n));for(size_t i=0;i<n;++i)for(size_t j=0;j<n;++j)out[i][j]=a[i][j+n];return out;}
inline Matrix gram(const Normals&n){Matrix g(9,std::vector<Q>(9));for(int i=0;i<9;++i)for(int j=0;j<9;++j)for(int c=0;c<10;++c)g[i][j]+=n[i][c]*n[j][c];return g;}
struct Image {long basis[9][9]{};int index=1;bool ones=true;};
inline long checked_long(__int128 x){require(x>=INT64_MIN&&x<=INT64_MAX,"exact integer image arithmetic");return long(x);}
inline Image image(const Normals&n){long a[9][10]{};for(int i=0;i<9;++i){bool nonzero=false;for(int c=0;c<10;++c){require(std::abs(n[i][c])<=1,"signed unit original normal");a[i][c]=n[i][c];nonzero|=n[i][c]!=0;}require(nonzero,"primitive nonzero original normal");}
 Image result;for(int i=0;i<9;++i){int p=i;while(p<10&&!a[i][p])++p;require(p<10,"independent original parent");for(int r=0;r<9;++r)std::swap(a[r][i],a[r][p]);for(int c=i+1;c<10;++c)while(a[i][c]){long q=a[i][i]/a[i][c];for(int r=0;r<9;++r){long v=checked_long((__int128)a[r][i]-(__int128)q*a[r][c]);a[r][i]=a[r][c];a[r][c]=v;}}if(a[i][i]<0)for(int r=0;r<9;++r)a[r][i]=-a[r][i];result.index*=a[i][i];require(result.index>0&&result.index<=32,"complete domain image-index bound");}
 for(int i=0;i<9;++i)for(int j=0;j<9;++j)result.basis[i][j]=a[i][j];
 long coords[9]{};for(int i=0;i<9;++i){long value=1;for(int j=0;j<i;++j)value-=a[i][j]*coords[j];if(value%a[i][i]){result.ones=false;break;}coords[i]=value/a[i][i];}return result;}
inline std::vector<Theta> characters(const Normals&n,const Image&im){Matrix b(9,std::vector<Q>(9));for(int i=0;i<9;++i)for(int j=0;j<9;++j)b[i][j]=im.basis[i][j];auto inv=inverse(b);std::vector<Theta>out;std::array<long,9>rep{};
 std::function<void(int)>visit=[&](int at){if(at==9){Theta t{};for(int i=0;i<9;++i){for(int j=0;j<9;++j)t[i]+=inv[j][i]*rep[j];t[i]=fractional(t[i]);}out.push_back(t);return;}for(rep[at]=0;rep[at]<im.basis[at][at];++rep[at])visit(at+1);};visit(0);
 require(out.size()==size_t(im.index)&&std::set<Theta>(out.begin(),out.end()).size()==out.size(),"complete distinct character group");for(const auto&t:out)for(int c=0;c<10;++c){Q value=0;for(int i=0;i<9;++i)value+=t[i]*n[i][c];require(value.get_den()==1,"every character annihilates every original column");}return out;}
inline int mobius(int n){int sign=1;for(int p=2;p*p<=n;++p)if(n%p==0){n/=p;sign=-sign;if(n%p==0)return 0;}return n>1?-sign:sign;}
inline int ramanujan(int m,int power){int common=std::gcd(m,power),sum=0;for(int d=1;d<=common;++d)if(common%d==0)sum+=d*mobius(m/d);return sum;}
inline std::vector<long> cyclotomic(int m){require(m>=2&&m<=32,"bounded exact cyclotomic order");static std::map<int,std::vector<long>>cache{{1,{-1,1}}};auto old=cache.find(m);if(old!=cache.end())return old->second;std::vector<long>a(m+1);a[0]=-1;a[m]=1;
 for(int d=1;d<m;++d)if(m%d==0){auto b=d==1?cache.at(1):cyclotomic(d);std::vector<long>q(a.size()-b.size()+1);while(a.size()>=b.size()){size_t shift=a.size()-b.size();long v=a.back();q[shift]=v;for(size_t j=0;j<b.size();++j)a[shift+j]-=v*b[j];while(a.size()>1&&a.back()==0)a.pop_back();}require(a.size()==1&&a[0]==0,"exact cyclotomic polynomial division");a=std::move(q);while(a.size()>1&&a.back()==0)a.pop_back();}cache.emplace(m,a);return a;}
struct Field {
 int order,degree;std::vector<long>modulus;Element zero,one;std::vector<Element>roots,inverses;
 explicit Field(int m):order(m),modulus(cyclotomic(m)){degree=modulus.size()-1;int phi=0;for(int u=1;u<m;++u)phi+=std::gcd(u,m)==1;require(degree==phi,"complete cyclotomic degree");zero=Element(degree);one=zero;one[0]=1;Element z=reduce({0,1});roots.push_back(one);for(int i=1;i<m;++i)roots.push_back(multiply(roots.back(),z));require(multiply(roots.back(),z)==one,"exact root order");for(int d=1;d<m;++d)if(m%d==0)require(roots[d]!=one,"primitive exact root");
  for(int j=0;j<degree;++j){Element sum=zero;for(int u=1;u<m;++u)if(std::gcd(u,m)==1)add_to(sum,root(u*j));require(sum==scale(one,ramanujan(m,j)),"complete Galois trace on every field basis vector");}
  inverses.resize(m);for(int a=1;a<m;++a){Element sum=zero;for(int j=0;j<m;++j)add_to(sum,scale(root(a*j),rational(m-1-j,m)));require(multiply(subtract(one,root(a)),sum)==one,"exact analytic inverse");inverses[a]=std::move(sum);}}
 Element reduce(Element p)const{p.resize(std::max<size_t>(p.size(),degree));for(int i=int(p.size())-1;i>=degree;--i)if(p[i]!=0)for(int j=0;j<degree;++j)p[i-degree+j]-=p[i]*modulus[j];p.resize(degree);return p;}
 Element multiply(const Element&a,const Element&b)const{Element p(2*degree-1);for(int i=0;i<degree;++i)if(a[i]!=0)for(int j=0;j<degree;++j)if(b[j]!=0)p[i+j]+=a[i]*b[j];return reduce(std::move(p));}
 static void add_to(Element&a,const Element&b){for(size_t i=0;i<a.size();++i)a[i]+=b[i];}
 Element subtract(Element a,const Element&b)const{for(int i=0;i<degree;++i)a[i]-=b[i];return a;}
 Element scale(Element a,const Q&q)const{for(Q&v:a)v*=q;return a;}
 const Element&root(int a)const{return roots[(a%order+order)%order];}
 Q trace(const Element&a)const{Q value=0;for(int j=0;j<degree;++j)value+=a[j]*ramanujan(order,j);return value;}
};
inline const Field& field(int m){static std::map<int,Field>fields;auto found=fields.find(m);if(found==fields.end())found=fields.emplace(m,Field(m)).first;return found->second;}
inline std::vector<Q> bernoulli(int degree){std::vector<Q>b(degree+1);b[0]=1;for(int n=1;n<=degree;++n){long choose=1;for(int j=0;j<n;++j){if(j)choose=choose*(n+2-j)/j;b[n]-=choose*b[j];}b[n]/=n+1;}return b;}
struct Polar {
 Matrix q;bool reverse;std::map<int,Matrix>inverses;std::map<std::pair<int,int>,std::vector<std::pair<int,Q>>>projections;std::unordered_map<uint64_t,Q>memo;
 Polar(const Matrix&g,bool r):q(inverse(g)),reverse(r){}
 const std::vector<std::pair<int,Q>>&project(int mask,int j){auto key=std::make_pair(mask,j);auto hit=projections.find(key);if(hit!=projections.end())return hit->second;std::vector<int>ids;for(int i=0;i<9;++i)if(mask>>i&1)ids.push_back(i);
  if(!inverses.count(mask)){Matrix sub(ids.size(),std::vector<Q>(ids.size()));for(size_t i=0;i<ids.size();++i)for(size_t h=0;h<ids.size();++h)sub[i][h]=q[ids[i]][ids[h]];inverses.emplace(mask,inverse(std::move(sub)));}std::vector<std::pair<int,Q>>coeff;const auto&inv=inverses.at(mask);for(size_t i=0;i<ids.size();++i){Q value=0;for(size_t h=0;h<ids.size();++h)value+=inv[i][h]*q[ids[h]][j];coeff.emplace_back(ids[i],value);}return projections.emplace(key,std::move(coeff)).first->second;}
 Q contract(int mask,uint64_t powers){if(mask==0){require(powers==0,"degree-zero polar base");return 1;}uint64_t key=(powers<<9)|unsigned(mask);auto hit=memo.find(key);if(hit!=memo.end())return hit->second;int j=reverse?8:0;while(j>=0&&j<9&&((powers>>(4*j))&15)==0)j+=reverse?-1:1;require(j>=0&&j<9,"homogeneous polar numerator");require(!(mask>>j&1),"numerator denominator cancellation complete");Q value=0;for(const auto&[i,c]:project(mask,j))if(c!=0)value+=c*contract(mask^(1<<i),powers-(uint64_t(1)<<(4*j)));memo.emplace(key,value);return value;}
 Q term(int poles,uint64_t powers){int mask=0;uint64_t numerator=0;for(int i=0;i<9;++i){int a=(powers>>(4*i))&15;if(poles>>i&1){if(!a)mask|=1<<i;else numerator|=uint64_t(a-1)<<(4*i);}else numerator|=uint64_t(a)<<(4*i);}return contract(mask,numerator);}
};
struct CorrectionStats {uint64_t characters=0,orbits=0,terms=0,states=0;double character_seconds=0,numerator_seconds=0,projection_seconds=0;};
using Polynomial=std::map<uint64_t,Element>;
inline Polynomial polynomial(const Field&f,const std::array<int,9>&exponents,int index,int&poles){poles=0;for(int i=0;i<9;++i)if(exponents[i]==0)poles|=1<<i;int degree=__builtin_popcount(unsigned(poles));require(degree<=6,"primitive signed-unit support bound");auto b=bernoulli(degree);std::array<std::vector<Element>,9>factor;
 for(int i=0;i<9;++i){int a=exponents[i];factor[i].resize(degree+1);if(!a){for(int d=0;d<=degree;++d)factor[i][d]=f.scale(f.one,-b[d]/factorial(d));}else{factor[i][0]=f.inverses[a];auto ratio=f.multiply(f.root(a),f.inverses[a]);for(int d=1;d<=degree;++d){auto total=f.zero;for(int j=1;j<=d;++j)Field::add_to(total,f.scale(factor[i][d-j],rational(1,factorial(j))));factor[i][d]=f.multiply(ratio,total);}}}
 int sum=std::accumulate(exponents.begin(),exponents.end(),0);auto weight=f.scale(f.subtract(f.one,f.root(sum)),rational(1,index));require(weight!=f.zero,"surviving ones character");Polynomial result;
 std::function<void(int,int,uint64_t,const Element&)>visit=[&](int i,int left,uint64_t code,const Element&value){if(i==8){auto coefficient=f.multiply(weight,f.multiply(value,factor[i][left]));if(coefficient!=f.zero)result.emplace(code|(uint64_t(left)<<(4*i)),std::move(coefficient));return;}for(int d=0;d<=left;++d)if(factor[i][d]!=f.zero)visit(i+1,left-d,code|(uint64_t(d)<<(4*i)),f.multiply(value,factor[i][d]));};visit(0,degree,0,f.one);return result;}
inline double seconds(std::chrono::steady_clock::time_point t){return std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count();}
inline Q correction(const Normals&n,const Image&im,bool checker,CorrectionStats&stats){using Clock=std::chrono::steady_clock;auto stamp=Clock::now();auto roster=characters(n,im);stats.characters+=roster.size();std::set<Theta>surviving;for(const auto&t:roster){Q sum=0;for(const Q&v:t)sum+=v;if(fractional(sum)!=0)surviving.insert(t);}require(surviving.empty()==im.ones,"complete ones admission agrees with characters");stats.character_seconds+=seconds(stamp);if(surviving.empty())return 0;Polar projector(gram(n),checker);Q total=0;
 if(!checker){while(!surviving.empty()){Theta t=*surviving.begin();int order=1;for(const Q&v:t)order=std::lcm(order,int(v.get_den().get_si()));std::array<int,9>exponents{};for(int i=0;i<9;++i){Q a=t[i]*order;require(a.get_den()==1,"exact character phase denominator");exponents[i]=a.get_num().get_si();}size_t size=0;for(int u=1;u<order;++u)if(std::gcd(u,order)==1){Theta other{};for(int i=0;i<9;++i)other[i]=fractional(t[i]*u);require(surviving.erase(other)==1,"complete disjoint Galois orbit");++size;}const Field&f=field(order);require(size==size_t(f.degree),"full Galois orbit size");++stats.orbits;stamp=Clock::now();int poles;auto terms=polynomial(f,exponents,im.index,poles);std::vector<std::pair<uint64_t,Q>>rational_terms;for(const auto&[powers,value]:terms){Q c=f.trace(value);if(c!=0)rational_terms.emplace_back(powers,c);}stats.numerator_seconds+=seconds(stamp);stamp=Clock::now();for(const auto&[powers,c]:rational_terms)total+=c*projector.term(poles,powers);stats.terms+=rational_terms.size();stats.projection_seconds+=seconds(stamp);}}
 else{const Field&f=field(im.index);std::map<std::pair<int,uint64_t>,Element>sum;stamp=Clock::now();for(const auto&t:surviving){std::array<int,9>exponents{};for(int i=0;i<9;++i){Q a=t[i]*im.index;require(a.get_den()==1,"all character orders divide image index");exponents[i]=a.get_num().get_si();}int poles;auto terms=polynomial(f,exponents,im.index,poles);for(const auto&[powers,value]:terms){auto key=std::make_pair(poles,powers);auto hit=sum.find(key);if(hit==sum.end())sum.emplace(key,value);else Field::add_to(hit->second,value);}}stats.numerator_seconds+=seconds(stamp);stamp=Clock::now();for(const auto&[key,value]:sum){for(int j=1;j<f.degree;++j)require(value[j]==0,"complete individual-character sum is rational");if(value[0]!=0){total+=value[0]*projector.term(key.first,key.second);++stats.terms;}}stats.projection_seconds+=seconds(stamp);}
 stats.states+=projector.memo.size();return total/2;}
} // namespace a19char
