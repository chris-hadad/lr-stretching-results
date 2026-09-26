#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Vec=std::array<long,6>;
struct Tree {std::array<unsigned,5> masks; Vec q; std::array<mpq_class,11> f;};
void need(bool x,const char* m){if(!x)throw std::runtime_error(m);}
std::vector<Tree> load(const char* path){
  std::ifstream in(path);std::string tag;unsigned n;in>>tag>>n;
  need(in.good()&&tag=="A19TREE1"&&n==1296,"tree header");
  std::vector<Tree> trees(n);
  for(auto& t:trees){
    for(auto& m:t.masks){in>>m;need(m>0&&m<63,"proper cut");}
    for(auto& q:t.q){in>>q;need(q>-100000000&&q<100000000,"bounded exact q");}
    need(t.q[5]==0,"normalized q");
    for(auto& f:t.f){std::string s;in>>s;need(in.good(),"truncated tree");f=mpq_class(s);f.canonicalize();}
  }
  std::string extra;need(!(in>>extra),"extra tree data");return trees;
}
std::array<long,64> subsets(const Vec& a){
  std::array<long,64> out{};
  for(unsigned m=1;m<64;++m){unsigned bit=__builtin_ctz(m);out[m]=out[m&(m-1)]+a[bit];}
  return out;
}
long dot(const Vec& a,const Vec& b){
  __int128 z=0;for(unsigned i=0;i<6;++i)z+=(__int128)a[i]*b[i];
  need(z>-( (__int128)1<<60)&&z<((__int128)1<<60),"exact dot width");return(long)z;
}
mpq_class polynomial(const Tree& t,long x,bool derivative){
  mpq_class value=0;
  if(derivative){for(int j=10;j>=1;--j)value=value*x+j*t.f[j];}
  else {for(int j=10;j>=0;--j)value=value*x+t.f[j];}
  return value;
}
struct Perm {std::array<unsigned,6> p;int sign;};
std::vector<Perm> permutations(){
  std::array<unsigned,6> p={0,1,2,3,4,5};std::vector<Perm> out;
  do{unsigned inv=0;for(unsigned i=0;i<6;++i)for(unsigned j=i+1;j<6;++j)inv+=p[i]>p[j];out.push_back({p,inv%2?-1:1});}while(std::next_permutation(p.begin(),p.end()));
  need(out.size()==720,"complete Weyl group");return out;
}
int main(int argc,char** argv){try{
  need(argc==5,"usage tree-file cases-file output mode");std::string mode=argv[4];
  need(mode=="correct"||mode=="zero-rho"||mode=="omit-identity"||mode=="drop-tied-cuts","mode");
  auto started=std::chrono::steady_clock::now();auto trees=load(argv[1]);auto perms=permutations();
  Vec zeta={1,1,1,1,1,-5};auto zs=subsets(zeta);
  std::ifstream cases(argv[2]);std::ofstream out(argv[3]);need(cases.good()&&out.good(),"case/output open");
  out<<"{\n\"mode\":"<<std::quoted(mode)<<",\n\"cases\":[\n";
  std::string label;bool first=true;unsigned count=0;
  while(cases>>label){
    need(label.find_first_not_of("abcdefghijklmnopqrstuvwxyz0123456789-")==std::string::npos,"case label");
    Vec lam,mu,nu;for(Vec* a:{&lam,&mu,&nu}){
      for(auto& x:*a){cases>>x;need(cases.good()&&x>=0&&x<=1000000,"bounded partition input");}
      need(std::is_sorted(a->rbegin(),a->rend()),"partition order");
    }
    long balance=0;for(unsigned i=0;i<6;++i)balance+=mu[i]+nu[i]-lam[i];need(balance==0,"balanced whole boundary");
    mpq_class value=0;std::array<mpq_class,18> gradient{};unsigned long admitted=0,selected=0,nonzero=0,tied=0;
    auto start=std::chrono::steady_clock::now();
    for(unsigned pi=0;pi<perms.size();++pi)for(unsigned qi=0;qi<perms.size();++qi){
      if(mode=="omit-identity"&&pi==0&&qi==0)continue;
      const auto& p=perms[pi];const auto& q=perms[qi];Vec gamma{},delta{};
      long gs=0,ds=0;bool support=true;
      for(unsigned i=0;i<6;++i){
        gamma[i]=mu[p.p[i]]+nu[q.p[i]]-lam[i];
        delta[i]=mode=="zero-rho"?0:2*(long)i-(long)p.p[i]-(long)q.p[i];
        gs+=gamma[i];ds+=delta[i];
        if(i<5&&(gs<0||(gs==0&&ds<0))){support=false;break;}
      }
      if(!support)continue;need(gs==0&&ds==0,"root trace");++admitted;
      auto sg=subsets(gamma),sd=subsets(delta);
      for(const auto& t:trees){bool use=true;bool tie=false;
        for(auto mask:t.masks){
          long g=sg[mask],d=sd[mask];
          if(mode=="drop-tied-cuts"&&g==0){use=false;break;}
          if(g<0||(g==0&&(d<0||(d==0&&zs[mask]<0)))){use=false;break;}
          tie|=g==0;
        }
        if(!use)continue;++selected;tied+=tie;long slope=dot(t.q,gamma);if(slope)++nonzero;
        mpq_class coefficient=polynomial(t,dot(t.q,delta),true);
        mpq_class signed_coefficient=coefficient*(p.sign*q.sign);
        for(unsigned i=0;i<6;++i){gradient[i]-=signed_coefficient*t.q[i];gradient[6+p.p[i]]+=signed_coefficient*t.q[i];gradient[12+q.p[i]]+=signed_coefficient*t.q[i];}
        mpq_class term=coefficient*slope;
        if(p.sign*q.sign>0)value+=term;else value-=term;
      }
    }
    double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    if(!first)out<<",\n";first=false;++count;
    out<<"{\"id\":"<<std::quoted(label)<<",\"c1\":"<<std::quoted(value.get_str())<<",\"weyl_pairs_considered\":518400,\"admitted_pairs\":"<<admitted<<",\"selected_tree_terms\":"<<selected<<",\"nonzero_slope_terms\":"<<nonzero<<",\"terms_with_tied_cuts\":"<<tied<<",\"seconds\":"<<std::setprecision(17)<<elapsed<<",\"gradient\":[";for(unsigned i=0;i<18;++i){if(i)out<<",";out<<std::quoted(gradient[i].get_str());}out<<"]}";
    out.flush();std::cout<<label<<" c1="<<value<<" seconds="<<elapsed<<std::endl;
    if(mode=="correct"&&value<0){out<<"\n],\n\"candidate_interrupt\":true,\"case_count\":"<<count<<"}\n";out.close();return 3;}
  }
  need(cases.eof()&&count>0,"case roster");
  out<<"\n],\n\"case_count\":"<<count<<",\n\"elapsed_seconds\":"<<std::setprecision(17)<<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<"\n}\n";
  return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<std::endl;return 2;}}
