// Complete unsigned four-row/five-column table counts from homogeneous-series
// multiplication. No signed character formula or provider program is used.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using U=unsigned __int128;
void need(bool value,const char* message){if(!value)throw std::runtime_error(message);}
std::string decimal(U value){if(!value)return "0";std::string s;while(value){s.push_back('0'+value%10);value/=10;}std::reverse(s.begin(),s.end());return s;}
void add(U& a,U b){need(~U(0)-a>=b,"unsigned count overflow");a+=b;}
U count(std::array<int,4> rows,const std::array<int,5>& columns,std::uint64_t& additions,std::size_t& largest){
    for(int a:rows)need(a>=0&&a<=200,"row bound");
    for(int a:columns)need(a>=0&&a<=64,"column bound");
    need(std::accumulate(rows.begin(),rows.end(),0)==std::accumulate(columns.begin(),columns.end(),0),"unbalanced margins");
    std::sort(rows.begin(),rows.end());
    const int A=rows[0],B=rows[1],C=rows[2];
    need(A<=32&&B<=32&&C<=32,"retained row capacity bound");
    const std::size_t strideC=1,strideB=C+1,strideA=(B+1)*strideB,size=(A+1)*strideA;
    std::vector<U> previous(size);previous[0]=1;
    for(int cap:columns){
        const std::size_t cells=(cap+1)*size;
        need(cells<=1000000,"state allocation exceeds one million cells");
        largest=std::max(largest,cells);
        std::vector<U> next(cells);
        // The factor (1-w)^-1 copies the old polynomial into every grade.
        for(int m=0;m<=cap;++m)std::copy(previous.begin(),previous.end(),next.begin()+m*size);
        // Each recurrence multiplies by one entire geometric factor
        // (1-w*x_i)^-1, retaining every nonnegative allocation exactly once.
        for(int axis=0;axis<3;++axis){
            const std::size_t stride=axis==0?strideA:axis==1?strideB:strideC;
            for(int m=1;m<=cap;++m)for(int a=0;a<=A;++a)for(int b=0;b<=B;++b)for(int c=0;c<=C;++c){
                const int coordinate=axis==0?a:axis==1?b:c;
                if(coordinate==0)continue;
                const std::size_t at=m*size+a*strideA+b*strideB+c;
                add(next[at],next[at-size-stride]);++additions;
            }
        }
        std::copy(next.begin()+cap*size,next.end(),previous.begin());
    }
    return previous.back();
}
int main(int argc,char**argv){try{
    need(argc==2,"expected input path");std::ifstream in(argv[1]);need(bool(in),"cannot open input");
    std::string label;
    while(in>>label){int t;need(bool(in>>t)&&t>=0&&t<=14,"missing or invalid original grade");
        std::array<int,4> r;std::array<int,5> c;
        for(int&v:r)need(bool(in>>v)&&v>=0&&v<=14,"base row outside control contract");
        for(int&v:c)need(bool(in>>v)&&v>=0&&v<=4,"base column outside control contract");
        need(std::accumulate(r.begin(),r.end(),0)==std::accumulate(c.begin(),c.end(),0),"unbalanced original margins");
        for(int&v:r)v*=t;for(int&v:c)v*=t;
        std::uint64_t operations=0;std::size_t largest=0;U value=count(r,c,operations,largest);
        std::cout<<label<<' '<<t<<' '<<decimal(value)<<' '<<operations<<' '<<largest<<'\n'<<std::flush;
    }
    need(in.eof(),"trailing invalid input");return 0;
}catch(const std::exception&e){std::cerr<<"REFUSED: "<<e.what()<<'\n';return 2;}}
