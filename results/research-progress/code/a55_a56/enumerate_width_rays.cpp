// Independent subset-pair roster and fraction-free determinant ray check.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>
using V=std::vector<long long>;
long long determinant(long long a[5][5],int n){
 long long den=1,sign=1;
 for(int k=0;k<n-1;++k){int r=k;while(r<n&&a[r][k]==0)++r;if(r==n)return 0;if(r!=k){for(int j=0;j<n;++j)std::swap(a[r][j],a[k][j]);sign=-sign;}
  long long p=a[k][k];for(int i=k+1;i<n;++i)for(int j=k+1;j<n;++j){long long v=a[i][j]*p-a[i][k]*a[k][j];if(v%den)std::abort();a[i][j]=v/den;}for(int i=k+1;i<n;++i)a[i][k]=0;den=p;
 }return sign*a[n-1][n-1];
}
int main(int argc,char**argv){if(argc!=3)return 2;int n=std::atoi(argv[1]);if(n<2||n>5)return 2;auto start=std::chrono::steady_clock::now();std::set<V> hs;
 for(int a=1;a<(1<<n);++a)for(int b=1;b<(1<<n);++b)if(!(a&b)){V h(n);for(int j=0;j<n;++j)h[j]=((a>>j)&1)-((b>>j)&1);auto it=std::find_if(h.begin(),h.end(),[](long long x){return x;});if(*it>0)hs.insert(h);}
 for(int j=0;j<n;++j){V h(n);h[j]=1;hs.insert(h);}std::vector<V> H(hs.begin(),hs.end());std::vector<int> pick(n-1);std::iota(pick.begin(),pick.end(),0);std::set<V> rays;long long checked=0,ranked=0,positive=0;
 do{++checked;V r(n);long long gcd=0;int sign=0;bool mixed=false;
  for(int j=0;j<n;++j){long long a[5][5]{};for(int i=0;i<n-1;++i){int k2=0;for(int k=0;k<n;++k)if(k!=j)a[i][k2++]=H[pick[i]][k];}r[j]=(j%2?-1:1)*determinant(a,n-1);gcd=std::gcd(gcd,std::abs(r[j]));if(r[j]){int s=r[j]>0?1:-1;if(sign&&s!=sign)mixed=true;sign=s;}}
  if(gcd){++ranked;if(!mixed){++positive;for(auto&x:r)x=x*sign/gcd;std::sort(r.begin(),r.end());rays.insert(r);}}
  int j=n-2;while(j>=0&&pick[j]==(int)H.size()-(n-1-j))--j;if(j<0)break;++pick[j];for(int k=j+1;k<n-1;++k)pick[k]=pick[k-1]+1;
 }while(true);
 std::ofstream out(argv[2]);out<<"{\"n\":"<<n<<",\"normal_count\":"<<H.size()<<",\"intersection_tests\":"<<checked<<",\"full_rank_intersections\":"<<ranked<<",\"nonnegative_intersections\":"<<positive<<",\"sorted_primitive_rays\":[";bool comma=false;for(const V&r:rays){if(comma)out<<",";comma=true;out<<"[";for(int j=0;j<n;++j){if(j)out<<",";out<<r[j];}out<<"]";}double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();out<<"],\"seconds\":"<<sec<<"}\n";std::cout<<"{\"ray_orbits\":"<<rays.size()<<",\"intersection_tests\":"<<checked<<",\"seconds\":"<<sec<<"}\n";
}
