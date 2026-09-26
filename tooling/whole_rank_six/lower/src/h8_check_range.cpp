// A17 bounded-range adapter retaining the accepted A16 mathematical kernel.
// Only authenticated DATA are consumed; no provider program is linked.
#define main geometric_entry_point_unused
#include "check_geometry.cpp"
#undef main
#include <gmpxx.h>
#include <functional>
#include <map>
#include <set>
#include <sstream>
using Big=mpz_class; using Rat=mpq_class; using Exponent=std::array<int,7>;
constexpr int ORDER=8; constexpr long SCALE=362880;
struct Homogeneous { Big denominator; std::vector<Big> coefficients; };
using Jet=std::vector<Homogeneous>;
struct Type { int k,index; uint32_t id; Subset ids{}; int gram[7][7]{},basis[7][7]{}; std::vector<int> axes; std::vector<std::array<int,7>> numerator; };
struct Child { int k,index; uint32_t id; std::vector<int> positions,omitted; };
struct Denominator { std::array<Big,9> values{}; Big scale=1; };
struct Checker {
 std::array<Bytes,8> types,lookup,profiles,maps,nidx,npts;
 std::array<std::map<uint32_t,Jet>,8> cache;
 std::array<std::set<uint32_t>,8> certified;
 std::map<uint32_t,Homogeneous> legacy7;
 std::vector<Exponent> monomials[8][9];
 std::map<std::vector<long>,Denominator> denominators;
 std::string mutation;
 bool mutation_applied=false;
 Checker(const std::string& root,const std::string& sources,int level,uint32_t begin,uint32_t end,bool measure,const std::string& barrier,const std::string& control):mutation(control) {
  std::ifstream listing(sources);need(bool(listing),"source list");
  for(int k=1;k<=7;++k) {
   for(int d=0;d<=ORDER-k;++d) { Exponent e{}; std::function<void(int,int)> f=[&](int p,int left) { if(p==k-1){e[p]=left;monomials[k][d].push_back(e);return;}for(int v=0;v<=left;++v){e[p]=v;f(p+1,left-v);} };f(0,d);need(monomials[k][d].size()==C[k+d-1][d],"homogeneous dimension"); }
   auto stem=root+"/U02/DATA/q"+std::to_string(k);
   types[k]=read(stem+".types"); profiles[k]=read(stem+".profiles"); maps[k]=read(stem+"-ALL.map");
   need(types[k].size()%73==0&&profiles[k].size()==(k+4)*count(k)&&maps[k].size()==6*C[42][k],"geometry populations");
   if(k<7){lookup[k]=read(stem+".lookup");need(lookup[k].size()==8*C[42][k],"lookup population");}
   nidx[k]=read(root+"/NUMERATORS/q"+std::to_string(k)+".nidx");npts[k]=read(root+"/NUMERATORS/q"+std::to_string(k)+".npts");
   need(nidx[k].size()==8*(count(k)+1)&&le(nidx[k].data()+8*count(k),8)*4==npts[k].size(),"numerator storage");
   int got;std::string path,index;need(bool(listing>>got>>path>>index)&&got==k,"source list order");
   if(k>=level&&(measure||k>level))continue;
   std::ifstream f(path);std::string magic,line,tail;int header_k,zero;uint64_t rows,slots;
   need(bool(std::getline(f,line)),"layer header missing");std::istringstream header(line);
   need(bool(header>>magic>>header_k>>zero>>rows>>slots)&&magic=="P31LAYER8"&&header_k==k&&zero==0&&rows==count(k)&&slots==C[7][k-1],"layer header");need(!(header>>tail),"header tail");
   uint32_t first=k<level?0:begin,last=k<level?count(k):end;need(first<last&&last<=count(k),"nonempty source range");
   if(k==level){auto offsets=read(index);need(offsets.size()==8*(count(k)+1),"range offsets length");auto offset=le(offsets.data()+8ull*first,8);need(offset>=uint64_t(f.tellg()),"range offset header");f.seekg(offset);need(bool(f),"range seek");}
   for(uint32_t tid=first;tid<last;++tid){need(bool(std::getline(f,line)),"missing layer row");std::istringstream row(line);uint64_t id;Homogeneous h;
    need(bool(row>>id>>h.denominator)&&id==tid&&h.denominator>0,"row identity or denominator");Big common=h.denominator;h.coefficients.reserve(slots);
    for(uint64_t j=0;j<slots;++j){Big value;need(bool(row>>value),"malformed coefficient");mpz_gcd(common.get_mpz_t(),common.get_mpz_t(),value.get_mpz_t());h.coefficients.push_back(std::move(value));}
    need(!(row>>tail)&&common==1,"canonical row or coefficient tail");Jet jet;jet.push_back(std::move(h));cache[k].emplace(tid,std::move(jet));
   }
   if(last==count(k))need(!std::getline(f,line),"layer trailing rows");
  }
  std::string tail;need(!(listing>>tail),"source list tail");
  if(!measure){std::ifstream proof(barrier);std::string magic;int through;need(bool(proof>>magic>>through)&&magic=="A17_CERTIFIED_LOWER"&&through==level-1,"lower certificate header");
   for(int k=1;k<level;++k){int got;uint64_t population;need(bool(proof>>got>>population)&&got==k&&population==count(k)&&cache[k].size()==population,"complete lower population");for(uint32_t id=0;id<population;++id)certified[k].insert(id);}
   need(!(proof>>tail),"lower certificate tail");
  }
 }
 size_t count(int k)const{return types[k].size()/73;}
 Rat evaluate(const Homogeneous& h,int k,int degree,const std::vector<long>& w)const {
  Big powers[7][8];for(int i=0;i<k;++i){powers[i][0]=1;for(int j=1;j<=degree;++j)powers[i][j]=powers[i][j-1]*w[i];}
  Big sum=0;for(size_t slot=0;slot<h.coefficients.size();++slot){if(h.coefficients[slot]==0)continue;Big value=h.coefficients[slot];for(int i=0;i<k;++i)value*=powers[i][monomials[k][degree][slot][i]];sum+=value;}
  Rat result(sum,h.denominator);result.canonicalize();return result;
 }
 Type get(int k,uint32_t id) {
  Type t{};t.k=k;t.id=id;auto p=types[k].data()+73ull*id;t.index=p[0];auto ordinal=le(p+57,4);need(ordinal<C[42][k]&&t.index>0,"type witness");auto original=unrank(ordinal,k);uint32_t permutation=le(p+61,4);unsigned used=0;
  auto profile=profiles[k].data()+(k+4)*size_t(id);uint64_t box=1;need(maps[k][6ull*ordinal+4]==t.index,"type image index");
  for(int j=0;j<k;++j){int pos=(permutation>>(3*j))&7;need(pos<k&&!(used&(1u<<pos)),"canonical permutation");used|=1u<<pos;t.ids[j]=original[pos];int subindex=1;
   if(k>1){Subset child{};int at=0;for(int q=0;q<k;++q)if(q!=pos)child[at++]=original[q];subindex=maps[k-1][6ull*rankof(child,k-1)+4];}
   need(subindex>0&&t.index%subindex==0&&profile[pos]==t.index/subindex,"primitive axis index");t.axes.push_back(profile[pos]);box*=profile[pos];}
  need(permutation>>(3*k)==0,"permutation tail");int off=1;
  for(int i=0;i<k;++i)for(int j=0;j<=i;++j){int v=int(p[off++])-4;need(v==H[t.ids[i]][t.ids[j]],"witness Gram");t.gram[i][j]=t.gram[j][i]=v;}
  need(detgram(t.ids,k)>0,"independent positive Gram");long determinant=1;
  for(int i=0;i<k;++i)for(int j=0;j<=i;++j){t.basis[i][j]=p[off++];if(i==j){need(t.basis[i][j]>0,"image basis diagonal");determinant*=t.basis[i][j];}}
  need(determinant==t.index,"image basis determinant");
  for(int c=0;c<10;++c){long coordinates[7]{};for(int i=0;i<k;++i){long value=N[t.ids[i]][c];for(int j=0;j<i;++j)value-=t.basis[i][j]*coordinates[j];need(value%t.basis[i][i]==0,"full image lattice");coordinates[i]=value/t.basis[i][i];}}
  auto start=le(nidx[k].data()+8ull*id,8),end=le(nidx[k].data()+8ull*(id+1),8);need(start<=end&&4*end<=npts[k].size(),"numerator slice");need(box%t.index==0&&end-start==box/t.index&&end-start==le(profile+k,4),"complete numerator cardinality");uint32_t previous=0;
  for(uint64_t at=start;at<end;++at){uint32_t code=le(npts[k].data()+4*at,4);
   if(mutation=="numerator"&&!mutation_applied&&end-start>1&&at==start){++code;mutation_applied=true;}
   need(code<box&&(at==start||previous<code),"distinct ordered numerator points");previous=code;auto remaining=code;std::array<int,7> point{};long coordinates[7]{};
   for(int i=0;i<k;++i){point[i]=remaining%t.axes[i];remaining/=t.axes[i];long value=point[i];for(int j=0;j<i;++j)value-=t.basis[i][j]*coordinates[j];need(value%t.basis[i][i]==0,"numerator lattice membership");coordinates[i]=value/t.basis[i][i];}need(remaining==0,"numerator radix");t.numerator.push_back(point);}
  return t;
 }
 std::vector<Child> children(const Type&t) {
  std::vector<Child> out;for(int mask=1;mask<(1<<t.k)-1;++mask){std::vector<std::pair<int,int>> chosen;Child ch{};
   for(int j=0;j<t.k;++j)if(mask&(1<<j))chosen.push_back({t.ids[j],j});else ch.omitted.push_back(j);std::sort(chosen.begin(),chosen.end());ch.k=chosen.size();Subset s{};for(int j=0;j<ch.k;++j)s[j]=chosen[j].first;
   auto p=lookup[ch.k].data()+8ull*rankof(s,ch.k);ch.id=le(p,4);need(ch.id<count(ch.k),"proper type ID");ch.index=types[ch.k][73ull*ch.id];uint32_t code=le(p+4,4);unsigned used=0;
   for(int j=0;j<ch.k;++j){int at=(code>>(3*j))&7;need(at<ch.k&&!(used&(1u<<at)),"proper canonical transport");used|=1u<<at;ch.positions.push_back(chosen[at].second);}need(code>>(3*ch.k)==0,"proper permutation tail");
   if(mutation=="permutation"&&!mutation_applied&&ch.k>=2&&t.gram[ch.positions[0]][ch.positions[0]]!=t.gram[ch.positions[1]][ch.positions[1]]){std::swap(ch.positions[0],ch.positions[1]);mutation_applied=true;}
   auto raw=types[ch.k].data()+73ull*ch.id;int off=1;for(int i=0;i<ch.k;++i)for(int j=0;j<=i;++j)need(int(raw[off++])-4==t.gram[ch.positions[i]][ch.positions[j]],"proper transported Gram");
   need(certified[ch.k].count(ch.id)&&cache[ch.k].count(ch.id),"uncertified h8 proper child");out.push_back(std::move(ch));}
  need(out.size()==size_t((1<<t.k)-2),"complete proper subsets");return out;
 }
 const Denominator& denominator(const Type&t,const std::vector<long>&c) {
  std::vector<long> key;for(int i=0;i<t.k;++i)key.push_back(t.axes[i]*c[i]);auto found=denominators.find(key);if(found!=denominators.end())return found->second;
  Denominator d;d.values[0]=1;
  for(long value:key){need(value>0,"generic positive covector");std::array<Big,9> next{},factor{};Big power=1;long factorial=1;
   for(int h=0;h<=ORDER;++h){power*=value;factorial*=h+1;need(SCALE%factorial==0,"9 factorial denominator scale");factor[h]=-power*(SCALE/factorial);}
   if(mutation=="series8"){factor[8]=0;mutation_applied=true;}
   for(int h=0;h<=ORDER;++h)for(int j=0;j<=h;++j)next[h]+=d.values[j]*factor[h-j];d.values=std::move(next);d.scale*=SCALE;}
  if(denominators.size()>=8192)denominators.clear(); // Bounded exact memoization.
  return denominators.emplace(key,std::move(d)).first->second;
 }
 void check(const Type&t,const Jet&current,const std::vector<Child>&children,const std::vector<long>&c) {
  std::vector<long>w(t.k,0);for(int i=0;i<t.k;++i)for(int j=0;j<t.k;++j)w[i]+=t.gram[i][j]*c[j];std::array<Big,9> moments{};
  for(const auto&point:t.numerator){long linear=0;for(int i=0;i<t.k;++i)linear+=c[i]*point[i];Big power=1;for(int h=0;h<=ORDER;++h){moments[h]+=power;power*=linear;}}
  const auto&den=denominator(t,c);std::array<Rat,9> numerator{},faces{};long factorial=1;
  for(int h=0;h<=ORDER;++h){if(h)factorial*=h;numerator[h]=Rat(moments[h]*den.scale,Big(factorial));numerator[h].canonicalize();}
  // D(z) Q(z)=N(z): triangular division needs all nine entries, but
  // [z^8]Q depends on only the new homogeneous top layer of each proper face.
  std::array<Rat,9> quotient{};
  for(int h=0;h<=ORDER;++h){Rat value=numerator[h];for(int j=1;j<=h;++j)value-=den.values[j]*quotient[h-j];quotient[h]=value/den.values[0];}
  Rat predicted=quotient[ORDER];
  for(const auto&ch:children){std::vector<long>arg;for(int p:ch.positions)arg.push_back(w[p]);Big divisor=t.index;for(int p:ch.omitted)divisor*=c[p];Rat factor((t.k-ch.k)%2?-ch.index:ch.index,divisor);factor.canonicalize();
   predicted-=factor*evaluate(cache[ch.k].at(ch.id)[0],ch.k,ORDER-ch.k,arg);}
  need(predicted==evaluate(current[0],t.k,ORDER-t.k,w),"H8 top-layer forward identity k="+std::to_string(t.k)+" type="+std::to_string(t.id));
 }
};
int main(int argc,char**argv){try {
 need(argc==11,"data sources lower-proof output mode k begin end control expected-population");
 std::string root=argv[1],sources=argv[2],barrier=argv[3],mode=argv[5],control=argv[9];int k=std::stoi(argv[6]);uint32_t begin=std::stoul(argv[7]),end=std::stoul(argv[8]);bool measure=mode=="measure";
 need(mode=="verify"||measure,"mode");need(k>=1&&k<=7,"level");need(control=="none"||control=="coefficient"||control=="permutation"||control=="numerator"||control=="series8","control");
 need(measure?(k==7&&begin==0&&end==0&&control=="none"):(begin<end&&end-begin<=10000),"bounded nonempty range");
 auto started=std::chrono::steady_clock::now();init(root+"/U02/DATA");Checker a(root,sources,k,begin,end,measure,barrier,control);auto loaded=std::chrono::steady_clock::now();need(a.count(k)==std::stoul(argv[10]),"expected population");
 if(measure){uint64_t rows=0,slots=0;for(int j=1;j<k;++j){rows+=a.cache[j].size();slots+=a.cache[j].size()*C[7][j-1];}std::cout<<"{\"status\":\"MEASURED_LOWER_CACHE_NO_CREDIT\",\"lower_types\":"<<rows<<",\"lower_slots\":"<<slots<<",\"loading_seconds\":"<<std::chrono::duration<double>(loaded-started).count()<<"}"<<std::endl;return 0;}
 need(a.cache[k].size()==end-begin,"current range exact size");std::ofstream rows(argv[4]);need(bool(rows),"per-type output");uint64_t points=0;
 for(uint32_t id=begin;id<end;++id){auto ts=std::chrono::steady_clock::now();auto&current=a.cache[k].at(id);auto t=a.get(k,id);auto children=a.children(t);
  if(control=="coefficient"&&!a.mutation_applied){current[0].coefficients[0]+=current[0].denominator;a.mutation_applied=true;}
  auto prepared=std::chrono::steady_clock::now();uint64_t tg=0;std::set<std::vector<long>> sites;std::vector<long>c(k,1);std::function<void(int,int)> visit=[&](int at,int left){if(at==k){need(sites.insert(c).second,"distinct determining sites");a.check(t,current,children,c);++tg;return;}for(int v=0;v<=left;++v){c[at]=1+v;visit(at+1,left-v);}};visit(1,ORDER-k);need(tg==C[7][k-1],"complete H8 determining dimension");
  for(int challenge=0;challenge<2;++challenge){for(int i=0;i<k;++i)c[i]=challenge?2*i+3:i+2;need(sites.insert(c).second,"distinct unused sites");a.check(t,current,children,c);}
  auto stopped=std::chrono::steady_clock::now();points+=t.numerator.size();rows<<"{\"k\":"<<k<<",\"id\":"<<id<<",\"index\":"<<t.index<<",\"numerator_points\":"<<t.numerator.size()<<",\"new_slots\":"<<C[7][k-1]<<",\"determining_sites\":"<<tg<<",\"unused_sites\":2,\"proper_children\":"<<children.size()<<",\"prepare_seconds\":"<<std::chrono::duration<double>(prepared-ts).count()<<",\"check_seconds\":"<<std::chrono::duration<double>(stopped-prepared).count()<<"}\n";
 }
 rows.close();need(bool(rows),"per-type output complete");need(control=="none","mutation unexpectedly passed or did not apply");
 std::cout<<"{\"status\":\"PASS_EXACT_H8_RANGE\",\"k\":"<<k<<",\"begin\":"<<begin<<",\"end\":"<<end<<",\"types\":"<<end-begin<<",\"new_coefficient_slots\":"<<(end-begin)*C[7][k-1]<<",\"determining_sites\":"<<(end-begin)*C[7][k-1]<<",\"unused_sites\":"<<2*(end-begin)<<",\"numerator_points\":"<<points<<",\"loading_seconds\":"<<std::chrono::duration<double>(loaded-started).count()<<",\"checking_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-loaded).count()<<",\"whole_LR_calls\":0}"<<std::endl;return 0;
 }catch(const std::exception&e){std::cerr<<"REFUSED: "<<e.what()<<std::endl;return 2;}}
