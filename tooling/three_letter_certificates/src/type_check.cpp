// Exhaustive verification of original normal subsets and complete lattice/metric types.
// Index: gcd of ALL maximal minors by fraction-free determinants.
// Image lattice: exact lower-triangular solves for all seven normal columns,
// together with independently established equal indices. No Hermite algorithm.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using I = long long;
using Mask = std::uint64_t;
using Matrix = std::array<std::array<I, 7>, 6>;
void need(bool ok, const std::string& message) { if (!ok) throw std::runtime_error(message); }
I narrow(__int128 value) {
    need(value > -(__int128(1)<<60) && value < (__int128(1)<<60), "Exact arithmetic range exceeded");
    return I(value);
}
I integer(const std::string& token) {
    std::size_t used=0; I value=std::stoll(token,&used);
    need(used==token.size(),"Trailing integer data"); return value;
}
std::vector<I> csv(const std::string& text) {
    need(!text.empty() && text.back()==',',"Missing terminal key comma");
    std::vector<I> result; std::size_t at=0;
    while(at<text.size()) {
        auto end=text.find(',',at); need(end!=std::string::npos && end>at,"Malformed key integer list");
        result.push_back(integer(text.substr(at,end-at))); at=end+1;
    }
    return result;
}
I determinant(Matrix a,int q) {
    I previous=1, sign=1;
    for(int k=0;k<q-1;k++) {
        int pivot=k; while(pivot<q && !a[pivot][k]) pivot++;
        if(pivot==q) return 0;
        if(pivot!=k) {std::swap(a[pivot],a[k]);sign=-sign;}
        const I value=a[k][k];
        for(int i=k+1;i<q;i++) for(int j=k+1;j<q;j++) {
            __int128 numerator=__int128(a[i][j])*value-__int128(a[i][k])*a[k][j];
            need(numerator%previous==0,"Nonexact Bareiss division");
            a[i][j]=narrow(numerator/previous);
        }
        for(int i=k+1;i<q;i++) a[i][k]=0;
        previous=value;
    }
    return sign*a[q-1][q-1];
}
bool advance(std::vector<int>& choice,int n) {
    for(int i=int(choice.size())-1;i>=0;i--) if(choice[i]<n-int(choice.size())+i) {
        choice[i]++; for(int j=i+1;j<int(choice.size());j++) choice[j]=choice[j-1]+1;
        return true;
    }
    return false;
}
std::vector<std::vector<int>> columns(int q) {
    std::vector<std::vector<int>> result; std::vector<int> ids(q);
    std::iota(ids.begin(),ids.end(),0);
    do {result.push_back(ids);} while(advance(ids,7));
    return result;
}
I minor_gcd(const Matrix& rows,int q,I& count) {
    I divisor=0;
    for(const auto& selected:columns(q)) {
        Matrix square{};
        for(int i=0;i<q;i++) for(int j=0;j<q;j++) square[i][j]=rows[i][selected[j]];
        divisor=std::gcd(divisor,std::abs(determinant(square,q))); count++;
    }
    return divisor;
}
int exact_rank(Matrix a,int q) {
    int rank=0;
    for(int col=0;col<7 && rank<q;col++) {
        int pivot=rank; while(pivot<q && !a[pivot][col]) pivot++;
        if(pivot==q) continue;
        std::swap(a[pivot],a[rank]);
        for(int i=rank+1;i<q;i++) if(a[i][col]) {
            I factor=a[i][col], value=a[rank][col], divisor=0;
            for(int j=col+1;j<7;j++) {
                a[i][j]=narrow(__int128(value)*a[i][j]-__int128(factor)*a[rank][j]);
                divisor=std::gcd(divisor,std::abs(a[i][j]));
            }
            a[i][col]=0;
            if(divisor) for(int j=col+1;j<7;j++) a[i][j]/=divisor;
        }
        rank++;
    }
    return rank;
}
struct Type {
    int gram[6][6]{}, h[6][6]{};
    I index=0, multiplicity=0;
    Mask representative_mask=0;
    bool representative_loaded=false, representative_seen=false;
};
bool columns_in_image(const Matrix& rows,const Type& type,int q) {
    for(int col=0;col<7;col++) {
        I coefficients[6]{};
        for(int i=0;i<q;i++) {
            __int128 residual=rows[i][col];
            for(int j=0;j<i;j++) residual-=__int128(type.h[i][j])*coefficients[j];
            if(residual%type.h[i][i]) return false;
            coefficients[i]=narrow(residual/type.h[i][i]);
        }
    }
    return true;
}
I choose(int n,int q) {I x=1;for(int k=1;k<=q;k++)x=x*(n-k+1)/k;return x;}
void self_test() {
    Matrix a{}; a[0][0]=2; a[1][1]=3;
    need(determinant(a,2)==6,"Determinant diagonal control");
    std::swap(a[0],a[1]); need(determinant(a,2)==-6,"Determinant sign control");
    a[1]=a[0]; need(determinant(a,2)==0 && exact_rank(a,2)==1,"Dependent rank control");
    a={};a[0][0]=2;a[1][1]=1;I minors=0;
    need(minor_gcd(a,2,minors)==2 && minors==21,"Rectangular maximal-minor control");
    Type correct,wrong; correct.h[0][0]=2;correct.h[1][1]=1;
    wrong.h[0][0]=1;wrong.h[1][1]=2;
    need(columns_in_image(a,correct,2),"Correct image basis rejected");
    need(!columns_in_image(a,wrong,2),"Same-index incorrect image basis accepted");
    std::cout<<"{\"status\":\"PASS\",\"controls\":6,\"same_index_wrong_lattice_rejected\":true}\n";
}
int main(int argc,char** argv) {
    I completed=0, representative_checks=0, minor_count=0, permutations_tested=0;
    int active_q=0;
    auto started=std::chrono::steady_clock::now();
    try {
        if(argc==2 && std::string(argv[1])=="--self-test") {self_test();return 0;}
        need(argc==8,"Usage: independent_types NORMALS Q ROSTER KEYS TYPES OUT_PREFIX MAX_TYPES");
        const int q=int(integer(argv[2]));active_q=q;
        need(q>=1 && q<=6,"Order outside fixed scope");
        const I max_types=integer(argv[7]);need(max_types==choose(32,q),"Type admission bound must equal full subset count");
        std::ifstream source(argv[1]);int n,d;need(bool(source>>n>>d) && n==32 && d==7,"Normal header mismatch");
        std::array<std::array<I,7>,32> normals{};
        for(auto& row:normals)for(auto& value:row){need(bool(source>>value),"Truncated normals");need(std::abs(value)<=2,"Normal coefficient bound");}
        std::string extra;need(!(source>>extra),"Trailing normal data");
        for(int i=0;i<32;i++)for(int j=0;j<i;j++)need(normals[i]!=normals[j],"Duplicate original normal");
        I gram[32][32]{};
        for(int i=0;i<32;i++)for(int j=0;j<32;j++)for(int k=0;k<7;k++)gram[i][j]+=normals[i][k]*normals[j][k];
        std::ifstream keys(argv[4]);need(bool(keys),"Cannot read keys");
        std::vector<Type> types;std::set<std::string> unique_keys;std::string line;
        while(std::getline(keys,line)) {
            auto tab=line.find('\t'), colon=line.find(':'), bar=line.find('|');
            need(tab!=std::string::npos && colon!=std::string::npos && bar!=std::string::npos && tab<colon && colon<bar,"Malformed key line");
            need(integer(line.substr(0,tab))==I(types.size()),"Noncontiguous key type IDs");
            need(integer(line.substr(tab+1,colon-tab-1))==q,"Key order mismatch");
            auto g=csv(line.substr(colon+1,bar-colon-1)), h=csv(line.substr(bar+1));
            need(g.size()==std::size_t(q*(q+1)/2) && h.size()==std::size_t(q*q),"Key dimensions mismatch");
            std::ostringstream normalized;for(I x:g)normalized<<x<<',';normalized<<'|';for(I x:h)normalized<<x<<',';
            need(unique_keys.insert(normalized.str()).second,"Duplicate full Gram and image key");
            Type type;int at=0;
            for(int i=0;i<q;i++)for(int j=i;j<q;j++) {need(std::abs(g[at])<=28,"Gram entry bound");type.gram[i][j]=type.gram[j][i]=int(g[at++]);}
            at=0;type.index=1;
            for(int i=0;i<q;i++)for(int j=0;j<q;j++) {
                I value=h[at++];need(std::abs(value)<=13824,"Image basis entry bound");type.h[i][j]=int(value);
                if(j>i)need(value==0,"Image basis not lower triangular");
                if(j==i){need(value>0,"Image basis diagonal not positive");type.index=narrow(__int128(type.index)*value);}
            }
            for(int i=0;i<q;i++)for(int j=0;j<i;j++)need(type.h[i][j]>=0 && type.h[i][j]<type.h[i][i],"Image basis not row-reduced");
            types.push_back(type);need(I(types.size())<=max_types,"Too many types");
        }
        need(keys.eof() && !types.empty(),"Key read incomplete or empty");
        std::ifstream representatives(argv[5]);need(bool(representatives),"Cannot read representatives");
        std::map<Mask,int> representative_owners;int next_type=0;
        while(std::getline(representatives,line)) {
            std::istringstream row(line);std::string tag;int rq,rd;I index;
            need(bool(row>>tag>>rq>>rd>>index),"Malformed representative header");
            need(tag=="t"+std::to_string(next_type) && rq==q && rd==7 && next_type<int(types.size()),"Representative identity mismatch");
            Matrix values{};Mask mask=0;
            for(int i=0;i<q;i++) {
                for(int j=0;j<7;j++)need(bool(row>>values[i][j]),"Truncated representative");
                int id=0;while(id<32 && values[i]!=normals[id])id++;
                need(id<32 && !(mask&(Mask(1)<<id)),"Representative is not a distinct original-normal subset");mask|=Mask(1)<<id;
            }
            need(!(row>>extra),"Trailing representative data");
            Type& type=types[next_type];
            I actual=minor_gcd(values,q,minor_count);
            need(actual>0 && actual==index && actual==type.index,"Representative image index mismatch at type "+std::to_string(next_type));
            for(int i=0;i<q;i++)for(int j=0;j<q;j++) {
                I entry=0;for(int k=0;k<7;k++)entry+=values[i][k]*values[j][k];
                need(entry==type.gram[i][j],"Representative Gram mismatch at type "+std::to_string(next_type));
            }
            need(columns_in_image(values,type,q),"Representative full image lattice mismatch at type "+std::to_string(next_type));
            need(representative_owners.emplace(mask,next_type).second,"Repeated representative subset");
            type.representative_mask=mask;type.representative_loaded=true;next_type++;representative_checks++;
        }
        need(representatives.eof() && next_type==int(types.size()),"Representative coverage mismatch");
        std::ifstream roster(argv[3]);need(bool(roster),"Cannot read original roster");
        std::string output=std::string(argv[6])+".verified.tsv";
        FILE* verified=std::fopen(output.c_str(),"wx");need(verified,"Cannot exclusively create assignment certificate");
        std::fprintf(verified,"mask\trank\timage_index\ttype_id\tordered_original_normal_ids_zero_based\n");
        std::map<I,I> ranks,indices;I independent=0,dependent=0,all_column_memberships=7*representative_checks;
        std::vector<int> ids(q);std::iota(ids.begin(),ids.end(),0);
        do {
            Mask mask=0;Matrix values{};for(int i=0;i<q;i++){mask|=Mask(1)<<ids[i];values[i]=normals[ids[i]];}
            need(bool(std::getline(roster,line)),"Missing subset at ordinal "+std::to_string(completed));
            std::istringstream fields(line);Mask old_mask;I old_index;int tid;
            need(bool(fields>>old_mask>>old_index>>tid) && !(fields>>extra),"Malformed roster row at ordinal "+std::to_string(completed));
            need(old_mask==mask,"Missing, duplicated, or reordered original mask at ordinal "+std::to_string(completed));
            I index=minor_gcd(values,q,minor_count);
            need(index==old_index,"Original image index mismatch at mask "+std::to_string(mask));
            int rank=index?q:exact_rank(values,q);need((rank==q)==bool(index),"Rank and maximal-minor disagreement");ranks[rank]++;
            if(!index) {
                need(tid==-1,"Dependent subset assigned to a type at mask "+std::to_string(mask));dependent++;
                std::fprintf(verified,"%llu\t%d\t0\t-1\t-\n",(unsigned long long)mask,rank);
            } else {
                need(tid>=0 && tid<int(types.size()),"Invalid independent type assignment");Type& type=types[tid];
                need(type.index==index,"Assigned image index differs at mask "+std::to_string(mask));
                int order[6]{};bool used[6]{};
                auto match=[&](auto&& self,int position)->bool {
                    if(position==q) {
                        permutations_tested++;Matrix arranged{};
                        for(int i=0;i<q;i++)arranged[i]=values[order[i]];
                        return columns_in_image(arranged,type,q);
                    }
                    for(int candidate=0;candidate<q;candidate++)if(!used[candidate] && gram[ids[candidate]][ids[candidate]]==type.gram[position][position]) {
                        bool same=true;
                        for(int before=0;before<position;before++)if(gram[ids[candidate]][ids[order[before]]]!=type.gram[position][before])same=false;
                        if(!same)continue;order[position]=candidate;used[candidate]=true;
                        if(self(self,position+1))return true;used[candidate]=false;
                    }
                    return false;
                };
                need(match(match,0),"No admissible Gram and full-image permutation at mask "+std::to_string(mask));
                independent++;indices[index]++;type.multiplicity++;all_column_memberships+=7;
                auto owner=representative_owners.find(mask);
                if(owner!=representative_owners.end()) {need(owner->second==tid,"Representative original subset has wrong assigned type");type.representative_seen=true;}
                std::fprintf(verified,"%llu\t%d\t%lld\t%d\t",(unsigned long long)mask,q,index,tid);
                for(int i=0;i<q;i++)std::fprintf(verified,"%s%d",i?",":"",ids[order[i]]);
                std::fprintf(verified,"\n");
            }
            completed++;
            if(completed%100000==0) {need(std::fflush(verified)==0,"Certificate flush failed");std::cout<<"{\"progress_q\":"<<q<<",\"subsets\":"<<completed<<"}\n"<<std::flush;}
        } while(advance(ids,32));
        need(!std::getline(roster,line) && roster.eof(),"Trailing roster rows or read failure");
        need(completed==choose(32,q),"Exhaustive subset population mismatch");
        need(std::fclose(verified)==0,"Certificate close failed");
        FILE* checked_types=std::fopen((std::string(argv[6])+".types-verified.tsv").c_str(),"wx");need(checked_types,"Cannot exclusively create type certificate");
        std::fprintf(checked_types,"type_id\trepresentative_mask\timage_index\tassignment_multiplicity\n");
        for(int tid=0;tid<int(types.size());tid++) {
            const auto& type=types[tid];need(type.representative_loaded && type.representative_seen && type.multiplicity>0,"Uncovered type or representative");
            std::fprintf(checked_types,"%d\t%llu\t%lld\t%lld\n",tid,(unsigned long long)type.representative_mask,type.index,type.multiplicity);
        }
        need(std::fclose(checked_types)==0,"Type certificate close failed");
        double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();
        std::cout<<"{\"status\":\"PASS\",\"q\":"<<q<<",\"total\":"<<completed<<",\"independent\":"<<independent<<",\"dependent\":"<<dependent<<",\"types\":"<<types.size()<<",\"representatives_checked\":"<<representative_checks<<",\"maximal_minor_determinants\":"<<minor_count<<",\"full_image_column_memberships\":"<<all_column_memberships<<",\"gram_matching_permutations_tested\":"<<permutations_tested<<",\"seconds\":"<<seconds<<",\"ranks\":{";
        bool first=true;for(auto [rank,count]:ranks){if(!first)std::cout<<',';std::cout<<'"'<<rank<<"\":"<<count;first=false;}
        std::cout<<"},\"indices\":{";first=true;for(auto [index,count]:indices){if(!first)std::cout<<',';std::cout<<'"'<<index<<"\":"<<count;first=false;}
        std::cout<<"}}\n";return 0;
    } catch(const std::exception& exc) {
        std::cerr<<"REFUSED q="<<active_q<<" verified_subsets="<<completed<<" verified_representatives="<<representative_checks<<" maximal_minor_determinants="<<minor_count<<": "<<exc.what()<<'\n';
        return 2;
    }
}
