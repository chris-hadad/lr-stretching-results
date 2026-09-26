// Complete extension coverage from a separately verified full q7 roster.
#include "../astra019-2026-09-18/field/common_v1.hpp"
using Bits = std::vector<unsigned char>;
void setbit(Bits& b,uint32_t n){need(!(b[n/8]&(1u<<(n%8))),"duplicate orbit");b[n/8]|=1u<<(n%8);}
bool contains(const Bits&b,uint32_t n){return b[n/8]&(1u<<(n%8));}
Row extend(Row s,int k,int n){s[k]=n;std::sort(s.begin(),s.begin()+k+1);return s;}
int main(int argc,char**argv){try{
 need(argc==6,"atlas geometry q7-kernels cache q9");init(argv[1]);
 auto start=std::chrono::steady_clock::now();Sources seven(argv[2],argv[3]);Cache eight(argv[4]);Map nine(argv[5]);
 need(nine.n==8ull*FIELD_ROWS,"complete q9 shape");Bits b8((C[42][8]+7)/8),b9((C[42][9]+7)/8);
 std::vector<uint32_t> ordinal8(SUPPORTS,UINT32_MAX);uint64_t original8=0,original9=0;
 for(uint32_t k=0;k<SUPPORTS;++k){uint32_t ord=le(eight.lookup.p+8ull*k,4),row=le(eight.lookup.p+8ull*k+4,4);
  need(row<SUPPORTS&&ordinal8[row]==UINT32_MAX&&ord<C[42][8],"q8 lookup bijection/range");
  if(k)need(ord>le(eight.lookup.p+8ull*(k-1),4),"q8 sorted lookup");
  ordinal8[row]=ord;setbit(b8,ord);auto s=unrank(ord,8);auto orbit=canonical(s,8);
  need(orbit.ordinal==ord,"q8 canonical orbit");original8+=6/orbit.stabilizer;
  auto p=eight.get(row);auto im=imageof(s,8);need(im.index>0&&im.index==I(le(p+80,2)),"q8 independent image index");
  for(int i=0;i<8;++i)for(int j=0;j<2;++j){I value=0;for(int c=0;c<10;++c)value+=I(N[s[i]][c])*small(p+2*(2*c+j));need(value==0,"q8 original NM zero");}
  for(int i=0;i<2;++i)for(int j=0;j<2;++j){I value=0;for(int c=0;c<10;++c)value+=I(small(p+40+2*(10*i+c)))*small(p+2*(2*c+j));need(value==(i==j),"q8 full saturated kernel");}
 }
 uint32_t at=0;for(auto&part:seven.joins){Map map(part.first);for(uint64_t j=0;j<part.second;++j){need(at<SUPPORTS&&le(map.p+12*j,4)==ordinal8[at],"q8 source join alignment");++at;}}need(at==SUPPORTS,"all source joins");
 for(uint32_t row=0;row<FIELD_ROWS;++row){auto p=nine.p+8ull*row;auto rec=readrecord(p);need(rec.ordinal<C[42][9]&&rec.ones<=1,"q9 record fields");if(row)need(rec.ordinal>le(p-8,4),"q9 sorted unique");
  setbit(b9,rec.ordinal);auto s=unrank(rec.ordinal,9);auto orbit=canonical(s,9);auto im=imageof(s,9);
  need(orbit.ordinal==rec.ordinal&&orbit.stabilizer==rec.stabilizer&&im.index>0&&im.index==rec.index&&im.ones==bool(rec.ones),"q9 independent original image and orbit");original9+=6/rec.stabilizer;
 }
 uint64_t ext8=0,weighted8=0,ext9=0,weighted9=0;
 for(uint32_t row=0;row<OLD_SUPPORTS;++row){auto p=seven.get(row);auto s=unrank(le(p,4),7);auto im=imageof(s,7);auto orbit=canonical(s,7);need(im.index>0&&im.index==p[4],"independent q7 premise and index");
  for(int n=0;n<42;++n){if(std::binary_search(s.begin(),s.begin()+7,n))continue;I v[3]{};for(int c=0;c<10;++c)for(int j=0;j<3;++j)v[j]+=I(N[n][c])*small(p+5+2*(3*c+j));
   if(v[0]||v[1]||v[2]){auto parent=canonical(extend(s,7,n),8);need(contains(b8,parent.ordinal),"omitted q8 independent extension");++ext8;weighted8+=6/orbit.stabilizer;}
  }
 }
 need(weighted8==8*original8,"complete q7-q8 weighted incidence identity");
 std::cerr<<"q8 complete "<<SUPPORTS<<" originals "<<original8<<"\n"<<std::flush;
 for(uint32_t row=0;row<SUPPORTS;++row){auto s=unrank(ordinal8[row],8);auto orbit=canonical(s,8);auto p=eight.get(row);
  for(int n=0;n<42;++n){if(std::binary_search(s.begin(),s.begin()+8,n))continue;I v[2]{};for(int c=0;c<10;++c)for(int j=0;j<2;++j)v[j]+=I(N[n][c])*small(p+2*(2*c+j));
   if(v[0]||v[1]){auto parent=canonical(extend(s,8,n),9);need(contains(b9,parent.ordinal),"omitted q9 independent extension");++ext9;weighted9+=6/orbit.stabilizer;}
  }
 }
 need(weighted9==9*original9,"complete q8-q9 weighted incidence identity");
 std::cout<<"{\"status\":\"PASS_COMPLETE_EXTENSIONS_GIVEN_COMPLETE_Q7\",\"q7\":"<<OLD_SUPPORTS<<",\"q8\":"<<SUPPORTS<<",\"q9\":"<<FIELD_ROWS<<",\"original_q8\":"<<original8<<",\"original_q9\":"<<original9<<",\"extensions8\":"<<ext8<<",\"weighted8\":"<<weighted8<<",\"extensions9\":"<<ext9<<",\"weighted9\":"<<weighted9<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
 return 0;
 }catch(const std::exception&e){std::cerr<<"REFUSED: "<<e.what()<<'\n';return 2;}}
