#pragma once
#define main field_unused_domain_main
#include "../domain/domain_v3.cpp"
#undef main
#include <gmpxx.h>
#include <cmath>
#include <cstring>
#include <memory>
#include <limits>
#include <iomanip>
#include <sstream>
using Z=mpz_class;using Q=mpq_class;
using Terms9=std::map<uint32_t,I>;
constexpr uint64_t FIELD_ROWS=27230728,FIELD_NNZ=321693368,FIELD_COORDS=20960436;
struct Cache{Map kernels,lookup;explicit Cache(const fs::path&p):kernels(p/"kernels82.bin"),lookup(p/"lookup8.bin"){need(kernels.n==82ull*SUPPORTS&&lookup.n==8ull*SUPPORTS,"complete cache source");}uint32_t find(uint32_t ord){uint32_t lo=0,hi=SUPPORTS;while(lo<hi){uint32_t mid=lo+(hi-lo)/2;if(le(lookup.p+8ull*mid,4)<ord)lo=mid+1;else hi=mid;}need(lo<SUPPORTS&&le(lookup.p+8ull*lo,4)==ord,"complete original face lookup");return le(lookup.p+8ull*lo+4,4);}const unsigned char*get(uint32_t row){need(row<SUPPORTS,"source support index");return kernels.p+82ull*row;}};
void cleanterms(Terms9&t){for(auto i=t.begin();i!=t.end();)if(!i->second)i=t.erase(i);else++i;}
Terms9 rowterms(const Row&s,I parent_index,Cache&cache,std::set<uint32_t>*used){Terms9 result;for(int deleted=0;deleted<9;++deleted){Row face{};int j=0;for(int i=0;i<9;++i)if(i!=deleted)face[j++]=s[i];uint32_t minimum=UINT32_MAX,ordinals[6];for(int g=0;g<6;++g){Row transformed{};for(int i=0;i<8;++i)transformed[i]=G[g][face[i]];std::sort(transformed.begin(),transformed.begin()+8);ordinals[g]=rankof(transformed,8);minimum=std::min(minimum,ordinals[g]);}uint32_t support=cache.find(minimum);if(used)used->insert(support);auto p=cache.get(support);I index=le(p+80,2);for(int g=0;g<6;++g)if(ordinals[g]==minimum){I v[2]{};for(int c=0;c<10;++c)for(int z=0;z<2;++z)v[z]+=I(N[G[g][s[deleted]]][c])*small(p+2*(2*c+z));I divisor=std::gcd(std::abs(v[0]),std::abs(v[1]));need(divisor>0&&parent_index%index==0&&divisor==parent_index/index,"complete original primitive quotient index");for(int z=0;z<2;++z)result[2*support+z]+=v[z]/divisor;}}cleanterms(result);return result;}
uint64_t number(const std::string&s){need(!s.empty()&&std::all_of(s.begin(),s.end(),[](char c){return c>='0'&&c<='9';}),"canonical integer");auto n=std::stoull(s);need(std::to_string(n)==s,"canonical integer spelling");return n;}
uint32_t u32arg(const std::string&s){auto value=number(s);need(value<=UINT32_MAX,"explicit uint32 range before narrowing");return uint32_t(value);}
Z positiveZ(const std::string&s){Z value;need(mpz_set_str(value.get_mpz_t(),s.c_str(),10)==0&&value>0&&value.get_str()==s,"canonical positive exact denominator");return value;}
Q rational(const std::string&s){Q q;need(mpq_set_str(q.get_mpq_t(),s.c_str(),10)==0&&q.get_den()>0,"valid exact rational");q.canonicalize();need(q.get_str()==s,"canonical exact rational");return q;}
Z big(__int128 v){bool negative=v<0;unsigned __int128 x=negative?static_cast<unsigned __int128>(-(v+1))+1:static_cast<unsigned __int128>(v);std::string s;do{s.push_back('0'+x%10);x/=10;}while(x);if(negative)s.push_back('-');std::reverse(s.begin(),s.end());return Z(s);}
void freshpath(const fs::path&p){need(!fs::exists(p),"fresh output identity");}
void rawwrite(const fs::path&p,const void*data,uint64_t bytes){freshpath(p);std::ofstream out(p,std::ios::binary);out.write((const char*)data,bytes);out.close();need(bool(out),"complete binary output");}
template<class T>void readvector(const fs::path&p,std::vector<T>&v,uint64_t n){need(fs::file_size(p)==n*sizeof(T),"exact binary file length: "+p.string());v.resize(n);std::ifstream f(p,std::ios::binary);if(n)need(bool(f.read((char*)v.data(),n*sizeof(T))),"complete binary read");char tail;need(!f.get(tail),"no binary tail");}
struct Matrix{std::string scope;uint32_t begin,end,coords;uint64_t nnz;std::vector<uint32_t>columns;std::vector<int8_t>values;std::vector<uint8_t>degrees;std::vector<uint16_t>norms;
 uint32_t rows()const{return end-begin;}
 explicit Matrix(const fs::path&p){std::ifstream f(p/"HEADER.txt");std::string magic,a,b,c,d,tail;need(bool(f>>magic>>scope>>a>>b>>c>>d)&&magic=="A19_MATRIX_V1"&&!(f>>tail),"complete matrix header");auto aa=number(a),bb=number(b),cc=number(c);nnz=number(d);need(aa<bb&&bb<=FIELD_ROWS&&cc>0&&cc<=FIELD_COORDS&&nnz<=FIELD_NNZ&&(scope=="original"||scope=="synthetic"),"matrix dimensions/scope");begin=aa;end=bb;coords=cc;need(scope!="original"||coords==FIELD_COORDS,"original global field dimension");readvector(p/"columns.u32",columns,nnz);readvector(p/"coefficients.i8",values,nnz);readvector(p/"degrees.u8",degrees,rows());readvector(p/"norms.u16",norms,rows());uint64_t at=0;for(uint32_t r=0;r<rows();++r){need(degrees[r]<=18&&(scope!="original"||degrees[r]>=2),"complete row degree bound");I norm=0;uint32_t previous=0;for(int j=0;j<degrees[r];++j){need(at<nnz&&columns[at]<coords&&(j==0||columns[at]>previous)&&values[at]!=0&&values[at]>=-38&&values[at]<=38,"sorted unique valid original matrix entry");previous=columns[at];norm+=I(values[at])*values[at];++at;}need(norm==norms[r]&&norm<=25992,"exact stored uint16 norm");}need(at==nnz,"complete matrix entry count");}
};
void matrixheader(const fs::path&out,const std::string&scope,uint32_t begin,uint32_t end,uint32_t coords,uint64_t nnz){freshpath(out/"HEADER.txt");std::ofstream f(out/"HEADER.txt");f<<"A19_MATRIX_V1 "<<scope<<' '<<begin<<' '<<end<<' '<<coords<<' '<<nnz<<'\n';f.close();need(bool(f),"matrix header output");}
struct RHS{std::string scope;uint32_t begin,end;Map text,offsets;RHS(const fs::path&p):text(p/"exact.tsv"),offsets(p/"offsets.u64"){std::ifstream f(p/"HEADER.txt");std::string magic,a,b,tail;need(bool(f>>magic>>scope>>a>>b)&&magic=="A19_RHS_V1"&&!(f>>tail),"complete RHS header");begin=u32arg(a);end=u32arg(b);need(begin<end&&end<=FIELD_ROWS&&(scope=="original"||scope=="synthetic")&&offsets.n==8ull*(end-begin+1)&&le(offsets.p,8)==0&&le(offsets.p+8ull*(end-begin),8)==text.n,"RHS source dimensions and terminal");}
 Q get(uint32_t row,uint32_t ordinal,uint32_t index){need(begin<=row&&row<end,"RHS exact row range");auto a=le(offsets.p+8ull*(row-begin),8),b=le(offsets.p+8ull*(row-begin+1),8);need(a<b&&b<=text.n&&b-a<=1048576,"bounded exact RHS record");std::istringstream f(std::string((const char*)text.p+a,b-a));std::string r,o,i,q,tail;need(bool(f>>r>>o>>i>>q)&&!(f>>tail)&&number(r)==row&&number(o)==ordinal&&number(i)==index,"exact original scalar identity");return rational(q);}
};
