// Session-authored exact geometry checker. Only data schemas are inherited.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using Bytes=std::vector<unsigned char>;
using Subset=std::array<int,7>;
uint64_t C[43][8];int N[42][10],G[6][42],Q[6][10],H[42][42];
void need(bool v,const std::string&m){if(!v)throw std::runtime_error(m);}
uint64_t le(const unsigned char*p,int n){uint64_t x=0;for(int i=n-1;i>=0;--i)x=(x<<8)|p[i];return x;}
int16_t i16(const unsigned char*p){return static_cast<int16_t>(le(p,2));}
int32_t i32(const unsigned char*p){return static_cast<int32_t>(le(p,4));}
Bytes read(const std::string&p){std::ifstream f(p,std::ios::binary);need(bool(f),"open "+p);f.seekg(0,std::ios::end);auto n=f.tellg();need(n>=0,"size");Bytes b(static_cast<size_t>(n));f.seekg(0);if(n)f.read(reinterpret_cast<char*>(b.data()),n);need(bool(f),"read "+p);return b;}
uint32_t rankof(const Subset&s,int k){uint64_t r=C[42][k]-1;for(int j=0;j<k;++j)r-=C[41-s[j]][k-j];return r;}
Subset unrank(uint32_t r,int k){Subset s{};int low=0;for(int j=0;j<k;++j){while(r>=C[41-low][k-j-1]){r-=C[41-low][k-j-1];++low;need(low<42,"unrank overflow");}s[j]=low++;}need(r==0,"unrank residual");return s;}
void next(Subset&s,int k){int j=k-1;while(j>=0&&s[j]==42-k+j)--j;if(j<0)return;++s[j];while(++j<k)s[j]=s[j-1]+1;}
long long checked(__int128 x){need(x>=INT64_MIN&&x<=INT64_MAX,"integer width");return static_cast<long long>(x);}
long long detgram(const Subset&s,int k){long long a[7][7]{};for(int i=0;i<k;++i)for(int j=0;j<k;++j)a[i][j]=H[s[i]][s[j]];long long prev=1;int sign=1;for(int c=0;c<k-1;++c){int p=c;while(p<k&&!a[p][c])++p;if(p==k)return 0;if(p!=c){for(int j=0;j<k;++j)std::swap(a[p][j],a[c][j]);sign=-sign;}auto pivot=a[c][c];for(int i=c+1;i<k;++i){for(int j=c+1;j<k;++j){auto num=(__int128)a[i][j]*pivot-(__int128)a[i][c]*a[c][j];need(num%prev==0,"Bareiss exact division");a[i][j]=checked(num/prev);}a[i][c]=0;}prev=pivot;}return sign*a[k-1][k-1];}
long long imageindex(const Subset&s,int k){long long a[7][10]{};for(int i=0;i<k;++i)for(int j=0;j<10;++j)a[i][j]=N[s[i]][j];long long d=1;for(int c=0;c<k;++c){int p=c;while(p<10&&!a[c][p])++p;if(p==10)return 0;for(int i=0;i<k;++i)std::swap(a[i][p],a[i][c]);for(int j=c+1;j<10;++j)while(a[c][j]){auto q=a[c][c]/a[c][j];for(int i=0;i<k;++i){auto v=checked((__int128)a[i][c]-(__int128)q*a[i][j]);a[i][c]=a[i][j];a[i][j]=v;}}d=checked((__int128)d*std::abs(a[c][c]));}return d;}
void init(const std::string&d){for(int n=0;n<=42;++n){C[n][0]=1;for(int k=1;k<=7;++k)C[n][k]=n?C[n-1][k-1]+C[n-1][k]:0;}std::ifstream f(d+"/atlas.txt");for(auto&r:N)for(int&v:r)need(bool(f>>v),"normal");for(auto&r:G)for(int&v:r)need(bool(f>>v),"action");for(auto&r:Q)for(int&v:r)need(bool(f>>v),"coordinate action");std::string tail;need(!(f>>tail),"atlas tail");for(int g=0;g<6;++g){std::array<int,42>a;std::copy(G[g],G[g]+42,a.begin());std::sort(a.begin(),a.end());for(int i=0;i<42;++i)need(a[i]==i,"normal permutation");std::array<int,10>q;std::copy(Q[g],Q[g]+10,q.begin());std::sort(q.begin(),q.end());for(int i=0;i<10;++i)need(q[i]==i,"coordinate permutation");for(int i=0;i<42;++i)for(int j=0;j<10;++j)need(N[G[g][i]][Q[g][j]]==N[i][j],"actual integral isometry");for(int h=0;h<6;++h){int matches=0;for(int t=0;t<6;++t){bool ok=true;for(int i=0;i<42;++i)ok&=G[t][i]==G[g][G[h][i]];matches+=ok;}need(matches==1,"group closure");}}for(int i=0;i<42;++i)for(int j=0;j<42;++j)for(int c=0;c<10;++c)H[i][j]+=N[i][c]*N[j][c];}
void topology(const std::string&d,int k,uint32_t begin,uint32_t end){
 auto map=read(d+"/q"+std::to_string(k)+"-ALL.map"),lookup=read(d+"/q"+std::to_string(k)+".lookup"),types=read(d+"/q"+std::to_string(k)+".types");
 need(map.size()==6*C[42][k]&&lookup.size()==8*C[42][k]&&types.size()%73==0&&begin<end&&end<=C[42][k],"length/range");
 size_t nt=types.size()/73;for(size_t t=0;t<nt;++t){auto p=types.data()+73*t;int off=1+k*(k+1)/2;long long index=1;for(int i=0;i<k;++i)for(int j=0;j<=i;++j){int v=p[off++];if(i==j){need(v>0,"HNF diagonal");index*=v;}else need(v<p[1+k*(k+1)/2+i*(i+1)/2+i],"HNF residue");}need(index==p[0],"HNF determinant");for(;off<57;++off)need(p[off]==0,"type key padding");}
 uint64_t indep=0,dep=0,reps=0,dep_reps=0,rankchecks=0,latticechecks=0;auto s=unrank(begin,k);
 for(uint32_t ord=begin;ord<end;++ord,next(s,k)){
  need(rankof(s,k)==ord,"successor rank");uint32_t best=UINT32_MAX;unsigned mask=0;
  for(int g=0;g<6;++g){Subset t{};for(int j=0;j<k;++j)t[j]=G[g][s[j]];std::sort(t.begin(),t.begin()+k);uint32_t r=rankof(t,k);if(r<best){best=r;mask=1u<<g;}else if(r==best)mask|=1u<<g;}
  auto m=map.data()+6ull*ord;unsigned index=m[4];need(le(m,4)==best&&m[5]==mask,"orbit/group mask at "+std::to_string(ord));need(map[6ull*best+4]==index,"orbit index transfer");
  if(best==ord){auto determinant=detgram(s,k),idx=imageindex(s,k);need(determinant>=0&&determinant<=16384,"Gram determinant bound");need((determinant==0)==(idx==0)&&idx==index,"independent rank/index at "+std::to_string(ord));++rankchecks;if(index)++reps;else ++dep_reps;}
  auto lk=lookup.data()+8ull*ord;uint32_t id=le(lk,4),code=le(lk+4,4);
  if(!index){++dep;need(id==UINT32_MAX&&code==0,"dependent lookup");continue;}++indep;
  need(id<nt,"type range");auto p=types.data()+73ull*id;need(p[0]==index,"type index");Subset t{};unsigned seen=0;for(int i=0;i<k;++i){int q=(code>>(3*i))&7;need(q<k&&!(seen&(1u<<q)),"row permutation");seen|=1u<<q;t[i]=s[q];}need((code>>(3*k))==0,"permutation tail");
  int off=1;for(int i=0;i<k;++i)for(int j=0;j<=i;++j)need(H[t[i]][t[j]]==int(p[off++])-4,"Gram transport at "+std::to_string(ord));
  if(index!=1){int b[7][7]{};for(int i=0;i<k;++i)for(int j=0;j<=i;++j)b[i][j]=p[off++];for(int c=0;c<10;++c){long long x[7]{};for(int i=0;i<k;++i){long long v=N[t[i]][c];for(int j=0;j<i;++j)v-=b[i][j]*x[j];need(v%b[i][i]==0,"full image lattice membership");x[i]=v/b[i][i];}}++latticechecks;}
 }
 std::cout<<"{\"status\":\"PASS_EXACT_TOPOLOGY_RANGE\",\"k\":"<<k<<",\"begin\":"<<begin<<",\"end\":"<<end<<",\"originals\":"<<end-begin<<",\"independent\":"<<indep<<",\"dependent\":"<<dep<<",\"independent_representatives\":"<<reps<<",\"dependent_representatives\":"<<dep_reps<<",\"representative_rank_and_index_checks\":"<<rankchecks<<",\"nonunit_original_lattice_checks\":"<<latticechecks<<",\"complete_stabilizer_masks_checked\":true,\"scalar_values_recomputed\":false}"<<std::endl;
}
void oper(const std::string&d,uint32_t end){
 auto kernels=read(d+"/ALL.kernels"),join6=read(d+"/q6.join"),map7=read(d+"/q7-ALL.map");need(kernels.size()==675721ull*165&&join6.size()==675721ull*12,"kernel population");
 std::vector<int32_t> repr(C[42][6],-1);std::vector<int16_t> basis(675721ull*40);std::vector<unsigned> uses(675721,0);
 for(uint32_t r=0;r<675721;++r){auto p=kernels.data()+165ull*r;auto ord=le(p,4);need(le(join6.data()+12ull*r,4)==ord&&ord<C[42][6]&&repr[ord]<0,"kernel order");repr[ord]=r;auto s=unrank(ord,6);for(int i=0;i<40;++i)basis[40ull*r+i]=i16(p+5+2*i);for(int i=0;i<6;++i)for(int j=0;j<4;++j){long long z=0;for(int c=0;c<10;++c)z+=N[s[i]][c]*basis[40ull*r+4*c+j];need(z==0,"NM=0");}for(int i=0;i<4;++i)for(int j=0;j<4;++j){long long z=0;for(int c=0;c<10;++c)z+=i16(p+85+2*(10*i+c))*basis[40ull*r+4*c+j];need(z==(i==j),"AM=I");}}
 auto join7=read(d+"/q7.join");need(join7.size()==2999563ull*12,"parent rows");std::vector<uint32_t> starts={0,10000,260000,510000,760000,1010000,1260000,1510000,1760000,2010000,2260000,2510000,2760000,2999563};
 uint64_t occurrences=0,nonzeros=0;uint32_t row=0;unsigned largest=0;std::vector<std::pair<uint32_t,int>> terms,combined;terms.reserve(168);combined.reserve(168);
 for(size_t sh=0;sh+1<starts.size()&&row<end;++sh){char suffix[50];std::snprintf(suffix,sizeof(suffix),"/incidence-%07u.rows",starts[sh]);auto saved=read(d+suffix);size_t pos=0;while(pos<saved.size()&&row<end){need(pos+6<=saved.size(),"row header");uint32_t ord=le(saved.data()+pos,4);int nnz=le(saved.data()+pos+4,2);pos+=6;need(le(join7.data()+12ull*row,4)==ord,"operator original ordinal");auto s=unrank(ord,7);terms.clear();combined.clear();for(int g=0;g<6;++g){Subset t{};for(int j=0;j<7;++j)t[j]=G[g][s[j]];std::sort(t.begin(),t.end());for(int del=0;del<7;++del){Subset face{};int at=0;for(int j=0;j<7;++j)if(j!=del)face[at++]=t[j];int r=repr[rankof(face,6)];if(r<0)continue;++occurrences;++uses[r];int u[4]{},gcd=0;for(int j=0;j<4;++j){for(int c=0;c<10;++c)u[j]+=N[t[del]][c]*basis[40ull*r+4*c+j];gcd=std::gcd(gcd,std::abs(u[j]));}need(gcd>0&&gcd*kernels[165ull*r+4]==map7[6ull*ord+4],"primitive index divisor");for(int j=0;j<4;++j)if(u[j]){int v=u[j]/gcd;largest=std::max(largest,unsigned(std::abs(v)));terms.push_back({4u*unsigned(r)+unsigned(j),v});}}}
 std::sort(terms.begin(),terms.end());for(auto term:terms){if(!combined.empty()&&combined.back().first==term.first)combined.back().second+=term.second;else combined.push_back(term);}combined.erase(std::remove_if(combined.begin(),combined.end(),[](auto x){return x.second==0;}),combined.end());need(combined.size()==unsigned(nnz),"operator nonzero count row "+std::to_string(row));need(pos+8ull*nnz<=saved.size(),"operator payload");for(int j=0;j<nnz;++j){need(le(saved.data()+pos,4)==combined[j].first&&i32(saved.data()+pos+4)==combined[j].second,"operator entry row "+std::to_string(row));pos+=8;}nonzeros+=nnz;++row;}
 if(row==starts[sh+1])need(pos==saved.size(),"row shard tail");}
 need(row==end,"operator coverage");unsigned lo=*std::min_element(uses.begin(),uses.end()),hi=*std::max_element(uses.begin(),uses.end());if(end==2999563)need(lo>0,"unused support");
 std::cout<<"{\"status\":\"PASS_EXACT_GEOMETRIC_OPERATOR\",\"rows\":"<<row<<",\"kernels\":675721,\"NM_entries\":16217304,\"AM_entries\":10811536,\"primitive_incidences\":"<<occurrences<<",\"nonzeros\":"<<nonzeros<<",\"largest_primitive_coordinate\":"<<largest<<",\"minimum_support_uses\":"<<lo<<",\"maximum_support_uses\":"<<hi<<",\"all_coefficients_compared\":true,\"support_map_used_for_assembly\":false}"<<std::endl;
}
int main(int argc,char**argv){try{need(argc>=4,"usage");std::string mode=argv[1],d=argv[2];init(d);if(mode=="topology"){need(argc==6,"topology arguments");topology(d,std::stoi(argv[3]),std::stoul(argv[4]),std::stoul(argv[5]));}else if(mode=="operator"){need(argc==4,"operator arguments");oper(d,std::stoul(argv[3]));}else throw std::runtime_error("mode");return 0;}catch(const std::exception&e){std::cerr<<"REFUSED: "<<e.what()<<std::endl;return 2;}}
