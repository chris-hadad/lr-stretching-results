// A54 independent edge-support predicate. No native/provider implementation used.
// Row elimination uses gcd-normalized integer rows, then exact back substitution.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
using I=int64_t; using U=uint64_t; namespace fs=std::filesystem;
void require(bool b,const char*s){if(!b)throw std::runtime_error(s);}
I exact(__int128 x){require(x>INT64_MIN&&x<=INT64_MAX,"integer range");return I(x);}
struct Mapping {int fd;size_t size;const unsigned char* p; explicit Mapping(const fs::path&f){fd=open(f.c_str(),O_RDONLY);require(fd>=0,"open input");struct stat s{};require(fstat(fd,&s)==0&&s.st_size>0,"input stat");size=s.st_size;p=(const unsigned char*)mmap(nullptr,size,PROT_READ,MAP_PRIVATE,fd,0);require(p!=MAP_FAILED,"input mapping");}~Mapping(){munmap((void*)p,size);close(fd);}};
U readle(const unsigned char*p,int count){U n=0;for(int i=count-1;i>=0;--i)n=(n<<8)|p[i];return n;}
U choose[43][10]; int normals[42][10];std::vector<int> branches[42];
using Bits=std::array<U,3>;Bits tight[45]{};int physical[45];size_t nrays;
std::array<int,9> decode(U ordinal){require(ordinal<choose[42][9],"ordinal bounds");std::array<int,9>s{};int next=0;U original=ordinal;for(int j=0;j<9;++j){while(ordinal>=choose[41-next][8-j]){ordinal-=choose[41-next][8-j];++next;require(next<42,"unrank bounds");}s[j]=next++;}require(!ordinal,"ordinal residual");U ranked=choose[42][9]-1;for(int j=0;j<9;++j)ranked-=choose[41-s[j]][9-j];require(ranked==original,"ordinal roundtrip");return s;}
std::array<I,10> kernel(const std::array<int,9>&s){I a[9][10]{};int piv[9]{},rank=0;bool isp[10]{};for(int r=0;r<9;++r)for(int c=0;c<10;++c)a[r][c]=normals[s[r]][c];
 for(int col=0;col<10&&rank<9;++col){int r=rank;while(r<9&&!a[r][col])++r;if(r==9)continue;for(int c=0;c<10;++c)std::swap(a[r][c],a[rank][c]);piv[rank]=col;isp[col]=true;
  for(int k=rank+1;k<9;++k){if(!a[k][col])continue;I g=std::gcd(a[rank][col],a[k][col]),x=a[rank][col]/g,y=a[k][col]/g;I common=0;for(int c=col;c<10;++c){a[k][c]=exact((__int128)x*a[k][c]-(__int128)y*a[rank][c]);common=std::gcd(common,a[k][c]);}if(common>1)for(int c=col+1;c<10;++c)a[k][c]/=common;require(a[k][col]==0,"elimination");}++rank;
 }
 require(rank==9,"independent nine normals");std::array<I,10>w{};int freecol=0;while(isp[freecol])++freecol;w[freecol]=1;
 for(int r=8;r>=0;--r){int p=piv[r];__int128 sum=0;for(int c=p+1;c<10;++c)sum+=(__int128)a[r][c]*w[c];I total=exact(sum),g=std::gcd(a[r][p],total),scale=a[r][p]/g;for(int c=0;c<10;++c)w[c]=exact((__int128)w[c]*scale);w[p]=-total/g;I common=0;for(I x:w)common=std::gcd(common,x);require(common>0,"nonzero null vector");if(common>1)for(I&x:w)x/=common;
 }
 for(int r:s){__int128 sum=0;for(int c=0;c<10;++c)sum+=(__int128)normals[r][c]*w[c];require(sum==0,"exact null identity");}return w;
}
bool branch_possible(const Bits&survivors,U span){for(int r=0;r<45;++r)if(!(span&(U(1)<<r))){bool some=false;for(int k=0;k<3;++k)some|=(survivors[k]&~tight[r][k])!=0;if(!some)return false;}return true;}
int main(int argc,char**argv){try{require(argc==7,"usage geometry q9 source-class begin end output-directory");auto started=std::chrono::steady_clock::now();for(int n=0;n<=42;++n){choose[n][0]=1;for(int k=1;k<=9;++k)choose[n][k]=n?choose[n-1][k-1]+choose[n-1][k]:0;}
 std::ifstream in(argv[1]);int nnormal,nrow;in>>nnormal>>nrow>>nrays;require(nnormal==42&&nrow==45&&nrays>0&&nrays<=192,"geometry shape");for(auto&r:normals)for(int&x:r)require(bool(in>>x),"normal input");for(int r=0;r<45;++r){require(bool(in>>physical[r])&&physical[r]>=0&&physical[r]<42,"row map");branches[physical[r]].push_back(r);}for(auto&v:branches)require(v.size()>=1&&v.size()<=2,"complete original branches");for(size_t j=0;j<nrays;++j){U mask;require(bool(in>>mask)&&mask<(U(1)<<45),"ray mask");for(int r=0;r<45;++r)if(mask&(U(1)<<r))tight[r][j/64]|=U(1)<<(j%64);}std::string extra;require(!(in>>extra)&&in.eof(),"geometry tail");
 Mapping q9(argv[2]),source(argv[3]);require(q9.size==8ull*27230728&&source.size==27230728,"complete source file sizes");U begin=std::stoull(argv[4]),end=std::stoull(argv[5]);require(begin<end&&end<=27230728,"explicit interval");fs::path out(argv[6]);require(fs::is_directory(out)&&!fs::exists(out/"RETAIN.u8")&&!fs::exists(out/"RESULT.json"),"fresh output");std::ofstream retained(out/"RETAIN.u8",std::ios::binary);U counts[3]{},tested=0,kept=0,mismatch=0,weighted=0,first_mismatch=UINT64_MAX;
 for(U row=begin;row<end;++row){auto p=q9.p+8*row;U ordinal=readle(p,4);require(row==0||ordinal>readle(p-8,4),"strict source row order");require(source.p[row]<=2,"classification range");require(p[6]>0&&6%p[6]==0,"source orbit multiplicity");auto s=decode(ordinal);auto w=kernel(s);U span=0;for(int r=0;r<45;++r){__int128 dot=0;for(int c=0;c<10;++c)dot+=(__int128)normals[physical[r]][c]*w[c];if(dot==0)span|=U(1)<<r;}
  int twins=0;for(int n:s)twins+=branches[n].size()==2;bool possible=false;for(int branch=0;branch<(1<<twins);++branch){Bits survivors{};for(size_t j=0;j<nrays;++j)survivors[j/64]|=U(1)<<(j%64);int bit=0;for(int n:s){int select=branches[n].size()==2?((branch>>bit++)&1):0;int r=branches[n][select];for(int k=0;k<3;++k)survivors[k]&=tight[r][k];}possible|=branch_possible(survivors,span);++tested;}
  ++counts[source.p[row]];kept+=possible;if(possible)weighted+=6/p[6];bool differs=possible!=(source.p[row]>=1);mismatch+=differs;if(differs&&first_mismatch==UINT64_MAX)first_mismatch=row;retained.put(possible?1:0);
 }
 retained.close();require(bool(retained),"retained output complete");double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();std::ofstream result(out/"RESULT.json");result<<"{\"schema\":\"astra054-independent-edge-predicate/v1\",\"status\":\""<<(mismatch?"MISMATCH":"PASS")<<"\",\"begin\":"<<begin<<",\"end\":"<<end<<",\"rows\":"<<end-begin<<",\"branches_checked\":"<<tested<<",\"retained\":"<<kept<<",\"retained_original_multiplicity\":"<<weighted<<",\"source_classes\":["<<counts[0]<<','<<counts[1]<<','<<counts[2]<<"],\"mismatches\":"<<mismatch<<",\"first_mismatch\":"<<(first_mismatch==UINT64_MAX?"null":std::to_string(first_mismatch))<<",\"seconds\":"<<seconds<<"}\n";result.close();require(bool(result),"result output complete");std::cout<<"rows="<<end-begin<<" retained="<<kept<<" branches="<<tested<<" mismatches="<<mismatch<<" seconds="<<seconds<<'\n';return mismatch?1:0;
 }catch(const std::exception&e){std::cerr<<"REFUSED: "<<e.what()<<'\n';return 2;}}
