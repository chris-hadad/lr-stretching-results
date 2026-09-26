// Root independent full-field readback from bounded-distribution counts.
// No provider source is compiled, imported, or executed.
#include <gmpxx.h>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <chrono>
#include <stdexcept>
#include <algorithm>
#include <iomanip>
#include <sstream>
using Z=mpz_class; using V=std::vector<Z>;using M=std::vector<V>;
void need(bool b,const std::string&s){if(!b)throw std::runtime_error(s);}
Z cube(const Z&z){return z*z*z;}
struct Distribution{
 int r,x,n;V cumulative,cube_prefix;
 Distribution(int rr,int xx):r(rr),x(xx),n(2*rr*xx){
  V d(1,Z(1));
  for(int layer=0;layer<r;++layer){V e(d.size()+2*x);Z window=0;
   for(int k=0;k<(int)e.size();++k){if(k<(int)d.size())window+=d[k];if(k-2*x-1>=0&&k-2*x-1<(int)d.size())window-=d[k-2*x-1];e[k]=window;}d.swap(e);
  }
  cumulative.resize(n+1);cube_prefix.resize(n+1);Z c=0,p=0;
  for(int k=0;k<=n;++k){c+=d[k];cumulative[k]=c;p+=cube(c);cube_prefix[k]=p;}
 }
 Z sum(int k)const{return k<0?Z(0):cumulative[std::min(k,n)];}
 Z count(int a)const{
  need(a>=0,"negative width");const int center=a+r*x;
  int stop=std::min(2*a,center-1);Z half=stop<0?Z(0):cube_prefix[std::min(stop,n)];
  if(stop>n)half+=(stop-n)*cube(cumulative[n]);
  for(int k=2*a+1;k<center;++k)half+=cube(sum(k)-sum(k-2*a-1));
  return 2*half+cube(sum(center)-sum(center-2*a-1));
 }
};
Z evaluate(const M&a,int D,int w,int z){Z v=0;for(int i=D;i>=0;--i){Z row=0;for(int j=D-i;j>=0;--j)row=row*z+a[i][j];v=v*w+row;}return v;}
int main(int argc,char**argv){try{
 need(argc==6,"usage: verifier DATA RMIN RMAX OUT STRIP");int strip=std::stoi(argv[5]);need(strip==2||strip==3,"strip");std::string root=argv[1];int rmin=std::stoi(argv[2]),rmax=std::stoi(argv[3]);need(rmin>=strip&&rmax<=43&&rmin<=rmax,"frozen finite range");
 std::ofstream out(argv[4]);need(bool(out),"output unavailable");out<<"{\"schema\":\"astra053-independent-third-strip-fields/v1\",\"fields\":[";bool first=true;auto start=std::chrono::steady_clock::now();long all=0,pos=0,zeros=0,holdouts=0;
 for(int r=rmin;r<=rmax;++r){auto st=std::chrono::steady_clock::now();int D=3*r+1,slots=(D+1)*(D+2)/2;Z fact=1;for(int i=2;i<=D;++i)fact*=i;
  std::ostringstream suffix;suffix<<std::setw(2)<<std::setfill('0')<<r;
  std::ifstream f(root+"/FIELD-r"+suffix.str()+".txt"),s(root+"/SYMBOLIC-r"+suffix.str()+".txt");need(bool(f)&&bool(s),"missing finite field");
  std::string tag;int rr,dd,n;Z den;f>>tag>>rr>>dd>>den;need(tag=="SLR042_U12_FIELD_V1"&&rr==r&&dd==D&&den==fact,"field header");f>>tag>>n;need(tag=="COUNTS"&&n==slots,"count roster");
  M counts(D+1,V(D+1)),coeff(D+1,V(D+1));int ii,jj;Z v;
  for(int i=0;i<=D;++i)for(int j=0;j<=D-i;++j){f>>ii>>jj>>v;need(ii==i&&jj==j,"ordered determining lattice");counts[i][j]=v;}
  f>>tag>>n;need(tag=="COEFFICIENTS"&&n==slots,"coefficient roster");int rp=0,rz=0;
  for(int i=0;i<=D;++i)for(int j=0;j<=D-i;++j){f>>ii>>jj>>v;need(ii==i&&jj==j,"ordered monomial lattice");need(v>=0,"negative source coefficient");coeff[i][j]=v;if(v>0)++rp;else ++rz;}
  need(coeff[0][0]==fact,"ordinary constant");
  int sp,sz;long ops;s>>tag>>rr>>dd>>sp>>sz>>ops;need(tag=="SLR042_U12_SYMBOLIC_V1"&&rr==r&&dd==D&&sp==rp&&sz==rz,"symbolic header");
  for(int i=0;i<=D;++i)for(int j=0;j<=D-i;++j){s>>ii>>jj>>v;need(ii==i&&jj==j&&v==coeff[i][j],"complete second organization differs");}need(!(s>>tag),"symbolic suffix");
  // Every determining WHOLE count, independent of the source tail formula.
  for(int x=0;x<=D;++x){Distribution distribution(r,x);for(int w=0;w<=x;++w){int z=x-w,a=(r-strip)*w+(r-strip+1)*z;need(distribution.count(a)==counts[w][z],"complete original-equivalent count differs");}}
  // Convert ordinary powers to falling factorials by two exact Stirling transforms.
  M stir(D+1,V(D+1)),comb(D+1,V(D+1));stir[0][0]=comb[0][0]=1;
  for(int a=1;a<=D;++a){comb[a][0]=comb[a][a]=1;for(int b=1;b<=a;++b){stir[a][b]=stir[a-1][b-1]+b*stir[a-1][b];if(b<a)comb[a][b]=comb[a-1][b-1]+comb[a-1][b];}}
  M tmp(D+1,V(D+1)),fall(D+1,V(D+1));V factorial(D+1,Z(1));for(int i=1;i<=D;++i)factorial[i]=factorial[i-1]*i;
  for(int i=0;i<=D;++i)for(int b=0;b<=D-i;++b)for(int a=i;a<=D-b;++a)tmp[i][b]+=coeff[a][b]*stir[a][i];
  for(int i=0;i<=D;++i)for(int j=0;j<=D-i;++j){for(int b=j;b<=D-i;++b)fall[i][j]+=tmp[i][b]*stir[b][j];fall[i][j]*=factorial[i]*factorial[j];}
  // Integer Pascal transform in each axis evaluates every determining site.
  M atw(D+1,V(D+1));
  for(int w=0;w<=D;++w)for(int j=0;j<=D-w;++j)for(int i=0;i<=w;++i)atw[w][j]+=fall[i][j]*comb[w][i];
  for(int w=0;w<=D;++w)for(int z=0;z<=D-w;++z){Z value=0;for(int j=0;j<=z;++j)value+=atw[w][j]*comb[z][j];need(value==counts[w][z]*fact,"monomial field not equal to complete counts");}
  f>>tag>>n;need(tag=="HOLDOUTS"&&n==6,"holdout roster");for(int h=0;h<n;++h){f>>ii>>jj>>v;need(ii+jj>D,"holdout inside determining set");Distribution distribution(r,ii+jj);int a=(r-strip)*ii+(r-strip+1)*jj;need(distribution.count(a)==v,"unused whole-count holdout");need(evaluate(coeff,D,ii,jj)==v*fact,"unused polynomial holdout");}
  int fp,fz,fn;f>>tag>>fp>>fz>>fn;need(tag=="POSITIVITY"&&fp==rp&&fz==rz&&fn==0,"positivity header");need(!(f>>tag),"field suffix");
  need((r==strip&&rz==6)||(r>strip&&rz==0),"rank-drop zero pattern");
  if(r==strip){for(int i=3*r-1;i<=D;++i)need(coeff[i][0]==0,"trimmed zero layer");need(coeff[3*r-2][0]>0,"actual trimmed degree");}
  for(int j=0;j<=D;++j)need(coeff[0][j]>0,"positive upper edge");if(r>strip)for(int i=0;i<=D;++i)need(coeff[i][0]>0,"positive lower edge");
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count();
  if(!first)out<<",";first=false;out<<"{\"r\":"<<r<<",\"degree\":"<<D<<",\"slots\":"<<slots<<",\"positive\":"<<rp<<",\"zeros\":"<<rz<<",\"whole_count_holdouts\":6,\"seconds\":"<<sec<<"}";out.flush();
  all+=slots;pos+=rp;zeros+=rz;holdouts+=6;std::cout<<"r="<<r<<" slots="<<slots<<" seconds="<<sec<<std::endl;
 }
 double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();out<<"],\"slots\":"<<all<<",\"positive\":"<<pos<<",\"zeros\":"<<zeros<<",\"holdouts\":"<<holdouts<<",\"seconds\":"<<seconds<<",\"provider_code_executed\":false,\"claim\":\"Exact complete polynomial fields conditional on independently reviewed original map and degree theorem\"}\n";
 return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<std::endl;return 2;}}
