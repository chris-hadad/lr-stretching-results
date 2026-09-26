// Campaign-owned indexed q8 contraction. Provider programs remain inert.
// Proper geometric transport is reused from the fully accepted c3 certificate.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fcntl.h>
#include <fstream>
#include <functional>
#include <gmpxx.h>
#include <iostream>
#include <list>
#include <map>
#include <memory>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <unistd.h>
#include <unordered_map>
#include <vector>
using Z=mpz_class; using Q=mpq_class; using Clock=std::chrono::steady_clock;
using Vec=std::array<int,8>; using Mat=std::array<Vec,8>;
constexpr uint32_t counts[]={0,4,36,386,4279,39908,293306,1651060};
uint64_t choose[43][9]{};
void need(bool v,const std::string&s){if(!v)throw std::runtime_error(s);}
double seconds(Clock::time_point t){return std::chrono::duration<double>(Clock::now()-t).count();}
uint64_t le(const unsigned char*p,int n){uint64_t x=0;for(int i=n-1;i>=0;--i)x=(x<<8)|p[i];return x;}
uint64_t be(const unsigned char*p,int n){uint64_t x=0;for(int i=0;i<n;++i)x=(x<<8)|p[i];return x;}
long exactlong(__int128 x){need(x>=INT64_MIN&&x<=INT64_MAX,"integer width");return long(x);}
long floordiv(long a,long b){long q=a/b,r=a%b;return q-(r<0);}
Q rat(const Z&a,const Z&b){Q q(a,b);q.canonicalize();return q;}
struct Mapped {
 int fd=-1; size_t size=0; const unsigned char*p=nullptr;
 explicit Mapped(const std::string&s){fd=open(s.c_str(),O_RDONLY);need(fd>=0,"open "+s);struct stat st{};need(fstat(fd,&st)==0&&st.st_size>0,"stat "+s);size=st.st_size;void*v=mmap(nullptr,size,PROT_READ,MAP_PRIVATE,fd,0);need(v!=MAP_FAILED,"mmap "+s);p=static_cast<unsigned char*>(v);}
 ~Mapped(){if(p)munmap(const_cast<unsigned char*>(p),size);if(fd>=0)close(fd);}
 Mapped(const Mapped&)=delete; Mapped&operator=(const Mapped&)=delete;
};
Vec unrank(uint32_t r,int k){Vec s{};int low=0;for(int j=0;j<k;++j){while(r>=choose[41-low][k-j-1]){r-=choose[41-low][k-j-1];++low;need(low<42,"unrank overflow");}s[j]=low++;}need(r==0,"unrank remainder");return s;}
uint32_t rankof(const Vec&s,int k){uint64_t r=choose[42][k]-1;for(int j=0;j<k;++j)r-=choose[41-s[j]][k-j];need(r<choose[42][k],"rank range");return uint32_t(r);}
struct Parent {uint32_t id,ordinal,permutation,orbits,originals;int index;Vec ids{};Mat gram{},lattice{};};
struct Child {uint32_t type;int mask,k,index;Vec positions{};};
struct Polynomial {Z denominator;std::vector<Z> coefficients;};
struct Root {Q value;Vec axes{};uint64_t box,points;};
struct Metrics {double geometry=0,transport=0,decode=0,root=0,proper=0,comparison=0,serialization=0;};
struct Engine {
 int normals[42][10]{};int atlasgram[42][42]{};
 std::unique_ptr<Mapped> parents;std::unique_ptr<Mapped> types[8],lookups[8],layers[8],offsets[8];
 std::vector<Vec> exponents[8];size_t capacity;
 std::list<std::pair<uint64_t,Polynomial>> lru;
 std::unordered_map<uint64_t,decltype(lru.begin())> cache;
 std::map<std::vector<int>,Root> roots;
 uint64_t hits=0,misses=0,evictions=0,root_hits=0,root_misses=0,transported=0;
 bool cache_mutated=false;std::string control;
 Engine(const std::string&geometry,const std::string&source,const std::string&index,size_t cap,std::string mutation):capacity(cap),control(std::move(mutation)){
  need(capacity>=1&&capacity<=131072,"bounded decoded cache");
  for(int n=0;n<=42;++n){choose[n][0]=1;for(int k=1;k<=8;++k)choose[n][k]=n?choose[n-1][k-1]+choose[n-1][k]:0;}
  std::ifstream f(geometry+"/atlas.txt");for(auto&r:normals)for(int&v:r)need(bool(f>>v),"atlas normal");int x;for(int i=0;i<312;++i)need(bool(f>>x),"atlas actions");std::string tail;need(!(f>>tail),"atlas tail");
  for(int i=0;i<42;++i)for(int j=0;j<42;++j)for(int c=0;c<10;++c)atlasgram[i][j]+=normals[i][c]*normals[j][c];
  parents=std::make_unique<Mapped>(source+"/U07/DATA/COLLATION/merge-02-00.types");need(parents->size==6958562ull*126,"complete q8 type population");
  for(int k=1;k<=7;++k){std::string q="q"+std::to_string(k);types[k]=std::make_unique<Mapped>(geometry+"/"+q+".types");lookups[k]=std::make_unique<Mapped>(geometry+"/"+q+".lookup");offsets[k]=std::make_unique<Mapped>(index+"/"+q+".offsets");
   std::string folder=k<=5?"U06/DATA/LAYER8":k==6?"U08/DATA/COMPLETE":"U09/DATA/COMPLETE";layers[k]=std::make_unique<Mapped>(source+"/"+folder+"/"+q+".layer8");
   need(types[k]->size==73ull*counts[k]&&lookups[k]->size==8ull*choose[42][k]&&offsets[k]->size==8ull*(counts[k]+1),"proper population dimensions");need(le(offsets[k]->p+8ull*counts[k],8)==layers[k]->size,"terminal layer offset");
   auto begin=le(offsets[k]->p,8);need(begin<layers[k]->size,"layer header bound");std::istringstream in(std::string(reinterpret_cast<const char*>(layers[k]->p),begin));std::string magic;uint32_t kk,lo,hi,slots;need(bool(in>>magic>>kk>>lo>>hi>>slots)&&magic=="P31LAYER8"&&kk==uint32_t(k)&&lo==0&&hi==counts[k]&&slots==choose[7][k-1]&&!(in>>tail),"h8 header");
   Vec e{};std::function<void(int,int)> visit=[&](int p,int left){if(p==k-1){e[p]=left;exponents[k].push_back(e);return;}for(int v=0;v<=left;++v){e[p]=v;visit(p+1,left-v);}};visit(0,8-k);need(exponents[k].size()==choose[7][k-1],"full h8 homogeneous space");
  }
 }
 Parent parent(uint32_t id){need(id<6958562,"parent id");Parent t{};t.id=id;auto p=parents->p+126ull*id;t.index=be(p,2);need(t.index>0&&t.index<=16,"root index");int off=2;for(int i=0;i<8;++i)for(int j=0;j<=i;++j)t.gram[i][j]=t.gram[j][i]=int(p[off++])-4;for(int i=0;i<8;++i)for(int j=0;j<=i;++j){t.lattice[i][j]=be(p+off,2);off+=2;}
  t.ordinal=le(p+110,4);t.permutation=le(p+114,4);t.orbits=le(p+118,4);t.originals=le(p+122,4);need(t.ordinal<choose[42][8]&&t.orbits>0&&t.originals>=t.orbits,"original support record");auto original=unrank(t.ordinal,8);unsigned seen=0;
  for(int i=0;i<8;++i){int pos=(t.permutation>>(3*i))&7;need(!(seen&(1u<<pos)),"parent permutation");seen|=1u<<pos;t.ids[i]=original[pos];}need(t.permutation>>24==0,"parent permutation tail");
  long determinant=1;for(int i=0;i<8;++i){need(t.lattice[i][i]>0,"root diagonal");determinant*=t.lattice[i][i];for(int j=0;j<8;++j)need(t.gram[i][j]==atlasgram[t.ids[i]][t.ids[j]],"root Gram transport");}need(determinant==t.index,"root lattice determinant");
  // A fresh image-index elimination plus full lattice inclusion verifies equality.
  long image[8][10]{};for(int i=0;i<8;++i)for(int c=0;c<10;++c)image[i][c]=normals[t.ids[i]][c];long image_index=1;
  for(int c=0;c<8;++c){int p=c;while(p<10&&!image[c][p])++p;need(p<10,"root independent image");for(int i=0;i<8;++i)std::swap(image[i][p],image[i][c]);for(int j=c+1;j<10;++j)while(image[c][j]){long q=image[c][c]/image[c][j];for(int i=0;i<8;++i){long v=exactlong((__int128)image[i][c]-(__int128)q*image[i][j]);image[i][c]=image[i][j];image[i][j]=v;}}image_index=exactlong((__int128)image_index*std::abs(image[c][c]));}need(image_index==t.index,"root original image index");
  for(int c=0;c<10;++c){long coords[8]{};for(int i=0;i<8;++i){long v=normals[t.ids[i]][c];for(int j=0;j<i;++j)v-=t.lattice[i][j]*coords[j];need(v%t.lattice[i][i]==0,"root original image membership");coords[i]=v/t.lattice[i][i];}}
  return t;
 }
 std::array<Child,254> children(const Parent&t){std::array<Child,254> out{};for(int mask=1;mask<255;++mask){auto&ch=out[mask-1];ch.mask=mask;std::vector<std::pair<int,int>> chosen;for(int j=0;j<8;++j)if(mask>>j&1)chosen.push_back({t.ids[j],j});std::sort(chosen.begin(),chosen.end());ch.k=chosen.size();Vec ids{};for(int j=0;j<ch.k;++j)ids[j]=chosen[j].first;auto ordinal=rankof(ids,ch.k);auto p=lookups[ch.k]->p+8ull*ordinal;ch.type=le(p,4);uint32_t code=le(p+4,4);need(ch.type<counts[ch.k],"proper lookup type");auto type=types[ch.k]->p+73ull*ch.type;ch.index=type[0];need(ch.index>0,"proper image index");unsigned used=0;for(int j=0;j<ch.k;++j){int at=(code>>(3*j))&7;need(at<ch.k&&!(used&(1u<<at)),"proper canonical permutation");used|=1u<<at;ch.positions[j]=chosen[at].second;}need(code>>(3*ch.k)==0,"proper transport tail");int off=1;for(int i=0;i<ch.k;++i)for(int j=0;j<=i;++j)need(t.gram[ch.positions[i]][ch.positions[j]]==int(type[off++])-4,"certified proper Gram transport");++transported;
  }return out;
 }
 const Polynomial& polynomial(int k,uint32_t id){uint64_t key=(uint64_t(k)<<32)|id;auto it=cache.find(key);if(it!=cache.end()){++hits;lru.splice(lru.begin(),lru,it->second);return it->second->second;}++misses;auto begin=le(offsets[k]->p+8ull*id,8),end=le(offsets[k]->p+8ull*(id+1),8);need(begin<end&&end<=layers[k]->size,"selected layer offsets");const char* cursor=reinterpret_cast<const char*>(layers[k]->p+begin);const char* finish=reinterpret_cast<const char*>(layers[k]->p+end);auto skip=[&](){while(cursor<finish&&(*cursor==' '||*cursor=='\n'||*cursor=='\r'||*cursor=='\t'))++cursor;};auto integer=[&](){skip();need(cursor<finish,"complete h8 token");const char* start=cursor;bool negative=*cursor=='-';if(negative)++cursor;need(cursor<finish&&*cursor>='0'&&*cursor<='9',"exact integer token");bool zero=*cursor=='0';++cursor;while(cursor<finish&&*cursor>='0'&&*cursor<='9'){need(!zero,"canonical integer digits");++cursor;}need(cursor==finish||*cursor==' '||*cursor=='\n'||*cursor=='\r'||*cursor=='\t',"integer token boundary");need(!negative||!zero,"canonical integer zero");Z value;if(cursor-start==1&&zero)return value;std::string token(start,cursor-start);need(mpz_set_str(value.get_mpz_t(),token.c_str(),10)==0,"GMP integer parse");return value;};Polynomial row;Z actual=integer();row.denominator=integer();need(actual==id&&row.denominator>0,"exact h8 row");Z gcd=row.denominator;row.coefficients.reserve(exponents[k].size());for(size_t j=0;j<exponents[k].size();++j){Z value=integer();mpz_gcd(gcd.get_mpz_t(),gcd.get_mpz_t(),value.get_mpz_t());row.coefficients.push_back(std::move(value));}skip();need(gcd==1&&cursor==finish,"canonical h8 row tail");if(cache.size()==capacity){cache.erase(lru.back().first);lru.pop_back();++evictions;}lru.emplace_front(key,std::move(row));cache[key]=lru.begin();return lru.front().second;
 }
 Q evaluate(const Polynomial&row,const Child&ch,const Vec&w){long powers[8][8]{};auto positions=ch.positions;if(control=="transport")std::sort(positions.begin(),positions.begin()+ch.k);for(int i=0;i<ch.k;++i){powers[i][0]=1;for(int h=1;h<=8-ch.k;++h)powers[i][h]=exactlong((__int128)powers[i][h-1]*w[positions[i]]);}Z total=0;for(size_t j=0;j<row.coefficients.size();++j){long v=1;for(int i=0;i<ch.k;++i)v=exactlong((__int128)v*powers[i][exponents[ch.k][j][i]]);if(!v)continue;Z coefficient=row.coefficients[j];if(control=="cache-coefficient"&&!cache_mutated){++coefficient;cache_mutated=true;}if(v>0)mpz_addmul_ui(total.get_mpz_t(),coefficient.get_mpz_t(),v);else mpz_submul_ui(total.get_mpz_t(),coefficient.get_mpz_t(),-v);}return rat(total,row.denominator);}
 Root root(const Parent&t,const Vec&c){std::vector<int>key;for(int i=0;i<8;++i){for(int j=0;j<=i;++j)key.push_back(t.lattice[i][j]);key.push_back(c[i]);}auto old=roots.find(key);if(old!=roots.end()){++root_hits;return old->second;}++root_misses;Root root{};root.box=1;std::vector<Vec>states(t.index);for(int i=0;i<t.index;++i){int rem=i;for(int j=0;j<8;++j){states[i][j]=rem%t.lattice[j][j];rem/=t.lattice[j][j];}need(rem==0,"quotient state count");}int steps[8][16]{};for(int j=0;j<8;++j){for(int state=0;state<t.index;++state){auto v=states[state];++v[j];for(int col=0;col<8;++col){long q=floordiv(v[col],t.lattice[col][col]);for(int r=col;r<8;++r)v[r]-=q*t.lattice[r][col];}int next=0,mul=1;for(int r=0;r<8;++r){need(v[r]>=0&&v[r]<t.lattice[r][r],"quotient residue");next+=v[r]*mul;mul*=t.lattice[r][r];}steps[j][state]=next;}int state=steps[j][0],order=1;while(state){state=steps[j][state];++order;need(order<=t.index,"finite axis order");}root.axes[j]=order;root.box*=order;}
  need(root.box%t.index==0&&root.box<=8957952,"whole q8 axis box bound");root.points=root.box/t.index;need(root.points<=823543,"whole q8 numerator bound");
  // Group-algebra dynamic programming counts every original-image numerator.
  int height=0;std::vector<std::vector<uint64_t>>hist(t.index,std::vector<uint64_t>(1));hist[0][0]=1;for(int j=0;j<8;++j){int nextheight=height+(root.axes[j]-1)*c[j];std::vector<std::vector<uint64_t>>next(t.index,std::vector<uint64_t>(nextheight+1));for(int state=0;state<t.index;++state){int target=state;for(int a=0;a<root.axes[j];++a){for(int h=0;h<=height;++h)next[target][h+a*c[j]]+=hist[state][h];target=steps[j][target];}}hist=std::move(next);height=nextheight;}
  need(std::accumulate(hist[0].begin(),hist[0].end(),uint64_t(0))==root.points,"complete root numerator cardinality");std::array<Q,9>series{};for(int h=0;h<=height;++h){Z power=1;for(int degree=0;degree<=8;++degree){series[degree]+=Z(static_cast<unsigned long>(hist[0][h]))*power;power*=h;}}long factorial=1;for(int h=0;h<=8;++h){if(h)factorial*=h;series[h]/=factorial;}
  for(int j=0;j<8;++j){long a=root.axes[j]*c[j];Z cube=Z(a)*a*a,p5=cube*a*a,p7=p5*a*a;std::array<Q,9>factor{};factor[0]=rat(-1,a);factor[1]=rat(1,2);factor[2]=rat(-a,12);factor[4]=rat(cube,720);factor[6]=rat(-p5,30240);factor[8]=control=="eighth"?Q(0):rat(p7,1209600);std::array<Q,9>next{};for(int h=0;h<=8;++h)for(int v=0;v<=h;++v)next[h]+=series[v]*factor[h-v];series=std::move(next);}root.value=series[8];if(roots.size()==4096)roots.erase(roots.begin());roots.emplace(std::move(key),root);return root;
 }
};
int main(int argc,char**argv){try{
 need(argc==10,"geometry source offsets expected output cache repeats covector control");std::string output=argv[5],site=argv[8],control=argv[9];need(site=="unit"||site=="spread","covector mode");need(control=="none"||control=="transport"||control=="cache-coefficient"||control=="eighth"||control=="omit-term","control mode");size_t capacity=std::stoull(argv[6]);int repeats=std::stoi(argv[7]);need(repeats>=1&&repeats<=32,"bounded repetitions");
 struct Expected {uint32_t id;int index;Q alpha;};std::vector<Expected>expected;std::ifstream in(argv[4]);uint32_t tid;int index;std::string value;while(in>>tid>>index>>value){Expected e{tid,index,Q(value)};e.alpha.canonicalize();need(expected.empty()||expected.back().id<tid,"strict panel order");expected.push_back(std::move(e));}need(in.eof()&&expected.size()>0&&expected.size()<=4096,"exact expected panel");
 need(access(output.c_str(),F_OK)!=0,"output already exists");auto start=Clock::now();Engine engine(argv[1],argv[2],argv[3],capacity,control);double preparation=seconds(start);std::ofstream out(output);need(bool(out),"output open");Metrics total{};uint64_t compared=0;auto bench=Clock::now();
 for(int repeat=0;repeat<repeats;++repeat)for(const auto&e:expected){Metrics m{};auto t=Clock::now();auto parent=engine.parent(e.id);need(parent.index==e.index,"expected original index");m.geometry=seconds(t);t=Clock::now();auto children=engine.children(parent);m.transport=seconds(t);Vec c{},w{};for(int i=0;i<8;++i)c[i]=site=="unit"?1:i+2;for(int i=0;i<8;++i)for(int j=0;j<8;++j)w[i]+=parent.gram[i][j]*c[j];t=Clock::now();auto root=engine.root(parent,c);m.root=seconds(t);Q alpha=root.value;int terms=0;bool omitted=false;
  for(const auto&ch:children){t=Clock::now();const auto&row=engine.polynomial(ch.k,ch.type);m.decode+=seconds(t);t=Clock::now();Q v=engine.evaluate(row,ch,w);long denominator=parent.index;for(int j=0;j<8;++j)if(!(ch.mask>>j&1))denominator=exactlong((__int128)denominator*c[j]);Q term=rat(ch.k%2?-ch.index:ch.index,denominator)*v;if(control=="omit-term"&&!omitted&&term!=0)omitted=true;else alpha-=term;++terms;m.proper+=seconds(t);}
  need(terms==254,"all 254 proper terms");t=Clock::now();need(alpha==e.alpha,"authenticated independent scalar mismatch at type "+std::to_string(e.id)+" control "+control);m.comparison=seconds(t);++compared;t=Clock::now();out<<"{\"type_id\":"<<e.id<<",\"repeat\":"<<repeat<<",\"index\":"<<parent.index<<",\"original_ordinal\":"<<parent.ordinal<<",\"original_permutation\":"<<parent.permutation<<",\"orbits\":"<<parent.orbits<<",\"originals\":"<<parent.originals<<",\"proper_terms\":"<<terms<<",\"alpha\":\""<<alpha<<"\",\"root\":\""<<root.value<<"\",\"axis_box\":"<<root.box<<",\"numerator_points\":"<<root.points<<",\"geometry_seconds\":"<<m.geometry<<",\"transport_seconds\":"<<m.transport<<",\"decode_seconds\":"<<m.decode<<",\"root_seconds\":"<<m.root<<",\"proper_seconds\":"<<m.proper<<",\"comparison_seconds\":"<<m.comparison<<"}\n";m.serialization=seconds(t);total.geometry+=m.geometry;total.transport+=m.transport;total.decode+=m.decode;total.root+=m.root;total.proper+=m.proper;total.comparison+=m.comparison;total.serialization+=m.serialization;
 }
 out.close();need(bool(out),"output complete");rusage usage{};getrusage(RUSAGE_SELF,&usage);std::cout<<"{\"status\":\"PASS_NATIVE_INDEXED_Q8_REUSED_PANEL\",\"unique_types\":"<<expected.size()<<",\"repeats\":"<<repeats<<",\"scalar_comparisons\":"<<compared<<",\"proper_terms\":"<<254*compared<<",\"covector\":\""<<site<<"\",\"decoded_cache_capacity\":"<<capacity<<",\"cache_hits\":"<<engine.hits<<",\"cache_misses\":"<<engine.misses<<",\"cache_evictions\":"<<engine.evictions<<",\"root_hits\":"<<engine.root_hits<<",\"root_misses\":"<<engine.root_misses<<",\"preparation_seconds\":"<<preparation<<",\"geometry_seconds\":"<<total.geometry<<",\"transport_seconds\":"<<total.transport<<",\"decode_seconds\":"<<total.decode<<",\"root_seconds\":"<<total.root<<",\"proper_seconds\":"<<total.proper<<",\"comparison_seconds\":"<<total.comparison<<",\"serialization_seconds\":"<<total.serialization<<",\"arithmetic_wall_seconds\":"<<seconds(bench)<<",\"total_seconds\":"<<seconds(start)<<",\"peak_rss_bytes\":"<<usage.ru_maxrss<<",\"new_scientific_types\":0,\"global_h8_adopted\":false}"<<std::endl;return 0;
 }catch(const std::exception&e){std::cerr<<"REFUSED: "<<e.what()<<std::endl;return 2;}}
