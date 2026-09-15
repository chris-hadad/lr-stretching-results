// Exact image-lattice Euler-Maclaurin recurrence; see ../PROOF.md.
// Reverse subset adjoint elimination + integer-scaled Todd polynomials.
// Every proper face, finite numerator and degree-six Bernoulli term is retained.
#define main independent_types_frozen_entrypoint
#include "type_check.cpp"
#undef main
#include <gmpxx.h>
#include <climits>
#include <cstring>
#include <unordered_map>
using Z=mpz_class;
using Q=mpq_class;
constexpr I TD[7]={1,2,12,24,720,1440,60480};
constexpr I FAC[7]={1,1,2,6,24,120,720};
struct ImagePod {
    int q=0,tid=0,index=0;
    int gram[6][6]{},h[6][6]{},ids[6]{},axis[6]{};
    I adj[6][6]{},det=0;
    std::uint32_t count=0;
};
struct Image {ImagePod p;std::vector<std::array<std::int16_t,6>> points;};
struct Support {std::uint32_t mask=0;int type=0;std::uint8_t order[6]{};};
struct Catalog {
    std::vector<Image> images;
    std::unordered_map<std::uint32_t,Support> supports;
    std::vector<std::array<I,7>> normals;
};
Z big(__int128 value) {
    if(value>=LONG_MIN && value<=LONG_MAX)return Z((long)value);
    bool neg=value<0;unsigned __int128 u=neg?-value:value;
    std::uint64_t limbs[2]{std::uint64_t(u),std::uint64_t(u>>64)};
    Z result;mpz_import(result.get_mpz_t(),2,-1,sizeof(limbs[0]),0,0,limbs);
    if(neg)result=-result;return result;
}
Q fraction(const Z& numerator,const Z& denominator) {
    need(denominator!=0,"Zero rational denominator");Q r(numerator,denominator);r.canonicalize();return r;
}
Q fraction(I numerator,I denominator) {return fraction(Z((long)numerator),Z((long)denominator));}
std::string bits_path(const std::string& root,int q,const std::string& suffix) {
    return root+"/q"+std::to_string(q)+suffix;
}
std::vector<Image> read_images(const std::string& root,int q,int start=0,int stop=INT_MAX) {
    std::ifstream keys(bits_path(root,q,".keys.tsv")),raw(bits_path(root,q,".types.txt"));
    need(bool(keys)&&bool(raw),"Cannot read authenticated image inputs");
    std::vector<Image> result;std::string key,line;int tid=0;
    while(std::getline(keys,key)) {
        need(bool(std::getline(raw,line)),"Truncated raw type inputs");
        if(tid>=stop)break;
        if(tid++<start)continue;
        Image image;auto& p=image.p;p.q=q;p.tid=tid-1;
        auto tab=key.find('\t'),colon=key.find(':'),bar=key.find('|');
        need(integer(key.substr(0,tab))==p.tid && integer(key.substr(tab+1,colon-tab-1))==q,"Type/key identity mismatch");
        auto g=csv(key.substr(colon+1,bar-colon-1)),h=csv(key.substr(bar+1));
        need(g.size()==std::size_t(q*(q+1)/2)&&h.size()==std::size_t(q*q),"Image key dimensions");
        int k=0;for(int i=0;i<q;i++)for(int j=i;j<q;j++)p.gram[i][j]=p.gram[j][i]=int(g[k++]);
        k=0;for(int i=0;i<q;i++)for(int j=0;j<q;j++)p.h[i][j]=int(h[k++]);
        std::istringstream row(line);std::string tag;int rq,d;
        need(bool(row>>tag>>rq>>d>>p.index)&&tag=="t"+std::to_string(p.tid)&&rq==q&&d==7,"Raw type identity mismatch");
        Matrix values{};for(int i=0;i<q;i++)for(int j=0;j<7;j++)need(bool(row>>values[i][j]),"Truncated normal representative");
        std::string extra;need(!(row>>extra),"Trailing representative bytes");
        // IDs are resolved after loading the 32 original rows.
        for(int i=0;i<q;i++)p.ids[i]=-1;
        // Keep original row coefficients temporarily in adj; prepare overwrites it.
        for(int i=0;i<q;i++)for(int j=0;j<6;j++)p.adj[i][j]=values[i][j];
        // The seventh coordinate is carried in axis until resolution.
        for(int i=0;i<q;i++)p.axis[i]=int(values[i][6]);
        result.push_back(std::move(image));
    }
    need(tid>=start,"Type start beyond input");return result;
}
void load_normals(Catalog& catalog,const std::string& root) {
    std::ifstream source(root+"/normals.txt");int n,d;
    need(bool(source>>n>>d)&&n==32&&d==7,"Original normal header");
    catalog.normals.resize(32);for(auto& row:catalog.normals)for(I& x:row)need(bool(source>>x),"Truncated original normals");
}
void resolve_ids(Image& image,const Catalog& catalog) {
    auto& p=image.p;std::uint32_t mask=0;
    for(int i=0;i<p.q;i++) {
        std::array<I,7> row{};for(int j=0;j<6;j++)row[j]=p.adj[i][j];row[6]=p.axis[i];
        int id=0;while(id<32&&row!=catalog.normals[id])id++;
        need(id<32&&!(mask&(std::uint32_t(1)<<id)),"Representative original-normal identity");
        p.ids[i]=id;mask|=std::uint32_t(1)<<id;
    }
}
void prepare_image(Image& image,const Catalog& catalog) {
    auto& p=image.p;const int q=p.q;Matrix g{};I index=1;
    for(int i=0;i<q;i++) {
        need(p.h[i][i]>0,"Nonpositive image diagonal");index*=p.h[i][i];
        for(int j=0;j<q;j++) {
            I actual=0;for(int k=0;k<7;k++)actual+=catalog.normals[p.ids[i]][k]*catalog.normals[p.ids[j]][k];
            need(actual==p.gram[i][j],"Raw representative Gram drift");g[i][j]=actual;
            need(j<=i||p.h[i][j]==0,"Image basis not lower triangular");
        }
    }
    need(index==p.index&&index>=1&&index<=8,"Image index outside independently checked range");
    p.det=determinant(g,q);need(p.det>0,"Gram metric not positive definite");
    for(int i=0;i<q;i++)for(int j=0;j<q;j++) {
        if(q==1){p.adj[i][j]=1;continue;}
        Matrix minor{};int r=0;
        for(int u=0;u<q;u++)if(u!=j){int c=0;for(int v=0;v<q;v++)if(v!=i)minor[r][c++]=g[u][v];r++;}
        p.adj[i][j]=((i+j)%2?-1:1)*determinant(minor,q-1);
    }
    for(int i=0;i<q;i++)for(int j=0;j<q;j++) {
        __int128 value=0;for(int k=0;k<q;k++)value+=__int128(p.gram[i][k])*p.adj[k][j];
        need(value==(i==j?p.det:0),"Exact Gram inverse identity failed");
    }
    std::uint32_t mask=0;for(int i=0;i<q;i++)mask|=std::uint32_t(1)<<p.ids[i];
    I product_axis=1;
    for(int i=0;i<q;i++) {
        auto smaller=mask^(std::uint32_t(1)<<p.ids[i]);I projected=1;
        if(smaller){auto it=catalog.supports.find(smaller);need(it!=catalog.supports.end(),"Missing independent projected image");projected=catalog.images[it->second.type].p.index;}
        need(index%projected==0,"Nonintegral primitive axis ratio");p.axis[i]=int(index/projected);product_axis*=p.axis[i];
    }
    need(product_axis%index==0,"Nonintegral numerator cardinality");
    I expected=product_axis/index;need(expected>=1&&expected<=32768,"Numerator exceeds proved full q<=6 index<=8 bound");
    image.points.clear();image.points.reserve(expected);I coefficients[6]{};std::array<std::int16_t,6> point{};
    auto enumerate=[&](auto&& self,int i)->void {
        if(i==q){image.points.push_back(point);return;}
        I offset=0;for(int j=0;j<i;j++)offset+=p.h[i][j]*coefficients[j];
        I residue=offset%p.h[i][i];if(residue<0)residue+=p.h[i][i];
        for(I x=residue;x<p.axis[i];x+=p.h[i][i]) {
            point[i]=std::int16_t(x);coefficients[i]=(x-offset)/p.h[i][i];self(self,i+1);
        }
    };
    enumerate(enumerate,0);need(I(image.points.size())==expected,"Full finite numerator cardinality mismatch");p.count=image.points.size();
}
template<class T>void write_pod(std::ostream& out,const T& x){out.write(reinterpret_cast<const char*>(&x),sizeof(x));need(bool(out),"Cache write failed");}
template<class T>void read_pod(std::istream& in,T& x){in.read(reinterpret_cast<char*>(&x),sizeof(x));need(bool(in),"Truncated cache");}
void build_catalog(const std::string& root,const std::string& verified,const std::string& output) {
    Catalog catalog;load_normals(catalog,root);
    I support_counts[6]{},type_counts[6]{},numerators=0,max_numerator=0;
    for(int q=1;q<=5;q++) {
        int offset=catalog.images.size();auto images=read_images(root,q);
        for(auto& image:images){resolve_ids(image,catalog);catalog.images.push_back(std::move(image));}type_counts[q]=images.size();
        std::ifstream rows(verified+"/q"+std::to_string(q)+".verified.tsv");std::string line;
        need(bool(std::getline(rows,line)),"Missing independent assignment header");
        while(std::getline(rows,line)) {
            std::istringstream fields(line);Support support;int rank,index,tid;std::string order;
            need(bool(fields>>support.mask>>rank>>index>>tid>>order),"Malformed independent assignment");
            if(!index){need(tid==-1&&rank<q,"Dependent assignment conflict");continue;}
            need(rank==q&&tid>=0&&tid<int(images.size()),"Independent assignment type bound");support.type=offset+tid;
            std::replace(order.begin(),order.end(),',',' ');std::istringstream perm(order);std::uint32_t check=0;
            for(int i=0;i<q;i++){int id;need(bool(perm>>id)&&id>=0&&id<32,"Invalid explicit permutation");support.order[i]=id;check|=std::uint32_t(1)<<id;}
            need(check==support.mask&&catalog.images[support.type].p.index==index,"Explicit image assignment identity mismatch");
            need(catalog.supports.emplace(support.mask,support).second,"Repeated independent support");support_counts[q]++;
        }
        for(int at=offset;at<int(catalog.images.size());at++) {
            prepare_image(catalog.images[at],catalog);numerators+=catalog.images[at].p.count;max_numerator=std::max<I>(max_numerator,catalog.images[at].p.count);
        }
    }
    std::ifstream exists(output);need(!exists.good(),"Cache output already exists");std::ofstream out(output,std::ios::binary);
    const std::uint64_t magic=0x3156425649413031ULL;write_pod(out,magic);
    std::uint32_t count=catalog.images.size(),supports=catalog.supports.size();write_pod(out,count);write_pod(out,supports);
    for(auto& image:catalog.images){write_pod(out,image.p);for(auto& point:image.points)write_pod(out,point);}
    std::vector<std::uint32_t> masks;for(auto& kv:catalog.supports)masks.push_back(kv.first);std::sort(masks.begin(),masks.end());
    for(auto mask:masks)write_pod(out,catalog.supports.at(mask));out.close();need(bool(out),"Cache close failed");
    std::cout<<"{\"status\":\"PASS\",\"cached_types\":"<<count<<",\"cached_independent_supports\":"<<supports<<",\"full_numerator_points\":"<<numerators<<",\"maximum_numerator\":"<<max_numerator<<",\"image_pod_bytes\":"<<sizeof(ImagePod)<<",\"support_pod_bytes\":"<<sizeof(Support)<<"}\n";
}
Catalog read_catalog(const std::string& file,const std::string& root) {
    Catalog result;load_normals(result,root);std::ifstream input(file,std::ios::binary);std::uint64_t magic;std::uint32_t n,m;
    read_pod(input,magic);need(magic==0x3156425649413031ULL,"Cache magic mismatch");read_pod(input,n);read_pod(input,m);
    need(n==88196&&m==180549,"Cache full-support populations mismatch");result.images.resize(n);result.supports.reserve(m*2);
    for(auto& image:result.images){read_pod(input,image.p);need(image.p.q>=1&&image.p.q<=5&&image.p.count>=1&&image.p.count<=32768,"Cached image bound");image.points.resize(image.p.count);for(auto& point:image.points)read_pod(input,point);}
    for(std::uint32_t at=0;at<m;at++){Support row;read_pod(input,row);need(row.type>=0&&row.type<int(n),"Cache type ID bound");need(result.supports.emplace(row.mask,row).second,"Duplicate cache support");}
    char extra;need(!input.get(extra)&&input.eof(),"Trailing cache bytes");return result;
}
using Poly=std::array<Z,7>;
Poly multiply(const Poly& a,const Poly& b,int degree) {
    Poly answer{};
    for(int i=0;i<=degree;i++)if(a[i]!=0)for(int j=0;j+i<=degree;j++)if(b[j]!=0) {
        need(TD[i+j]%(TD[i]*TD[j])==0,"Todd scaling divisor invariant");
        answer[i+j]+=a[i]*b[j]*(long)(TD[i+j]/(TD[i]*TD[j]));
    }
    return answer;
}
struct Context {const Image* image=nullptr;int order[6]{};Z v[6];Q inverse_c[6];};
Poly normalized_discrete(const Context& context,int degree,const std::string& mutation) {
    const auto& image=*context.image;const auto& p=image.p;Poly todd{};todd[0]=1;
    for(int i=0;i<p.q;i++) {
        Z b=context.v[i]*p.axis[i], b2=b*b;Poly factor{};factor[0]=1;factor[1]=-b;
        if(degree>=2)factor[2]=b2;if(degree>=4)factor[4]=-b2*b2;
        if(degree>=6&&mutation!="omit-b6")factor[6]=2*b2*b2*b2;
        todd=multiply(todd,factor,degree);
    }
    Poly moments{};
    for(std::size_t at=0;at<image.points.size();at++) {
        if(mutation=="omit-numerator"&&at>0)continue;
        Z projection=0;for(int i=0;i<p.q;i++)projection+=context.v[i]*image.points[at][i];
        Z power=1;for(int k=0;k<=degree;k++){moments[k]+=power;power*=projection;}
    }
    for(int k=0;k<=degree;k++)moments[k]*=(long)(TD[k]/FAC[k]);
    return multiply(todd,moments,degree);
}
struct Value {Q alpha;int base=0;I face_terms=0,numerator_visits=0;std::vector<Q> poles;};
Value evaluate(const Image& full,const Catalog& catalog,int first_base,const std::string& mutation) {
    const int q=full.p.q,all=(1<<q)-1;std::array<Context,64> context;
    int global_to_local[32];std::fill(global_to_local,global_to_local+32,-1);
    for(int i=0;i<q;i++)global_to_local[full.p.ids[i]]=i;
    for(int mask=1;mask<=all;mask++) {
        auto& item=context[mask];
        if(mask==all) {item.image=&full;for(int i=0;i<q;i++)item.order[i]=full.p.ids[i];}
        else {
            std::uint32_t global=0;for(int i=0;i<q;i++)if(mask&(1<<i))global|=std::uint32_t(1)<<full.p.ids[i];
            auto found=catalog.supports.find(global);need(found!=catalog.supports.end(),"Missing proper-face original image");
            item.image=&catalog.images[found->second.type];for(int i=0;i<item.image->p.q;i++)item.order[i]=found->second.order[i];
        }
    }
    Value answer;
    for(int base=first_base;base<=first_base+961;base++) {
        I powers[6]{1};for(int i=1;i<q;i++)powers[i]=narrow(__int128(powers[i-1])*base);
        bool good=true;
        for(int mask=1;mask<=all;mask++) {
            auto& item=context[mask];const auto& p=item.image->p;
            for(int i=0;i<p.q;i++) {
                __int128 numerator=0;
                for(int j=0;j<p.q;j++){int at=global_to_local[item.order[j]];need(at>=0,"Proper-face permutation leaves original subset");numerator+=__int128(p.adj[i][j])*powers[at];}
                item.v[i]=big(numerator);if(item.v[i]==0)good=false;
            }
        }
        if(good){answer.base=base;break;}
    }
    need(answer.base>0,"No generic compatible direction in finite root bound");
    for(int mask=1;mask<=all;mask++) {
        auto& item=context[mask];for(int i=0;i<item.image->p.q;i++)item.inverse_c[global_to_local[item.order[i]]]=fraction(Z((long)-item.image->p.det),item.v[i]);
    }
    // Adjoint elimination. Every proper-face coefficient is applied once.
    std::array<Q,64> weight{};weight[all]=1;
    for(int mask=all;mask>=1;mask--) {
        const auto& item=context[mask];std::array<Q,64> products{};products[0]=1;
        for(int removed=1;removed<=all;removed++)if((removed&mask)==removed) {
            int bit=__builtin_ctz(unsigned(removed));products[removed]=products[removed^(1<<bit)]*item.inverse_c[bit];
        }
        for(int remain=(mask-1)&mask;;remain=(remain-1)&mask) {
            answer.face_terms++;
            if(mutation!="omit-proper-face"||remain==0) {
                I index=remain?context[remain].image->p.index:1;
                weight[remain]-=weight[mask]*fraction(index,item.image->p.index)*products[mask^remain];
            }
            if(remain==0)break;
        }
    }
    std::array<Q,7> final{};final[0]=weight[0];
    for(int mask=1;mask<=all;mask++) {
        const auto& item=context[mask];const auto& p=item.image->p;
        answer.numerator_visits+=item.image->points.size();
        Poly coefficients=normalized_discrete(item,q,mutation);Z denominator=1;
        for(int i=0;i<p.q;i++)denominator*=p.axis[i]*item.v[i];
        std::array<Z,7> det_powers{};det_powers[0]=1;for(int k=1;k<=q;k++)det_powers[k]=det_powers[k-1]*(long)p.det;
        for(int k=0;k<=q;k++) {
            Z numerator=coefficients[k], divisor=denominator*(long)TD[k];
            if(p.q%2)numerator=-numerator;
            if(p.q>=k)numerator*=det_powers[p.q-k];else divisor*=det_powers[k-p.q];
            final[k]+=weight[mask]*fraction(numerator,divisor);
        }
    }
    for(int k=0;k<q;k++)answer.poles.push_back(final[k]);answer.alpha=final[q];return answer;
}
void print_numerator(std::ostream& output,const Image& image) {
    const auto& p=image.p;output<<p.tid<<'\t'<<p.index<<'\t';
    for(int i=0;i<p.q;i++)output<<(i?",":"")<<p.ids[i];output<<'\t';
    for(int i=0;i<p.q;i++)output<<(i?",":"")<<p.axis[i];output<<'\t';
    for(int i=0;i<p.q;i++)for(int j=0;j<p.q;j++)output<<p.h[i][j]<<',';output<<'\t';
    for(const auto& point:image.points){for(int i=0;i<p.q;i++)output<<(i?",":"")<<point[i];output<<';';}output<<'\n';
}
int main(int argc,char** argv) {
    try {
        if(argc==5&&std::string(argv[1])=="prepare"){build_catalog(argv[2],argv[3],argv[4]);return 0;}
        need(argc==10,"Usage: bv evaluate DATA CACHE Q START STOP OUT_PREFIX FIRST_BASE MUTATION");
        need(std::string(argv[1])=="evaluate","Unknown operation");
        const int q=int(integer(argv[4])),start=int(integer(argv[5])),stop=int(integer(argv[6])),base=int(integer(argv[8]));
        need(q>=1&&q<=6&&start>=0&&stop>start&&base>=2&&base<=100,"Requested value slice outside scope");
        std::string mutation=argv[9];need(mutation=="none"||mutation=="omit-b6"||mutation=="omit-numerator"||mutation=="omit-proper-face","Unknown mutation");
        auto begin=std::chrono::steady_clock::now();Catalog catalog=read_catalog(argv[3],argv[2]);auto originals=read_images(argv[2],q,start,stop);
        need(int(originals.size())==stop-start,"Raw type slice is incomplete");
        std::string prefix=argv[7];std::ifstream old(prefix+".values.tsv");need(!old.good(),"Value output already exists");
        std::ofstream values(prefix+".values.tsv"),numerators(prefix+".numerators.tsv");need(bool(values)&&bool(numerators),"Cannot create owned value outputs");
        values<<"type_id\talpha\tgeneric_base\tindex\tnumerator_count\tproper_face_terms\tfull_numerator_visits\tpoles\n";
        numerators<<"type_id\tindex\tordered_original_normal_ids\tprimitive_axes\timage_basis\tfull_numerator\n";
        I total_visits=0,face_terms=0;int nonzero_poles=0,max_numerator=0,max_base=0;
        for(auto& image:originals) {
            resolve_ids(image,catalog);prepare_image(image,catalog);Value result=evaluate(image,catalog,base,mutation);
            bool poles=false;for(const auto& value:result.poles)if(value!=0)poles=true;nonzero_poles+=poles;
            values<<image.p.tid<<'\t'<<result.alpha<<'\t'<<result.base<<'\t'<<image.p.index<<'\t'<<image.p.count<<'\t'<<result.face_terms<<'\t'<<result.numerator_visits<<'\t';
            for(const auto& value:result.poles)values<<value<<',';values<<'\n';print_numerator(numerators,image);
            total_visits+=result.numerator_visits;face_terms+=result.face_terms;max_numerator=std::max(max_numerator,int(image.p.count));max_base=std::max(max_base,result.base);
            if((image.p.tid-start+1)%1000==0){values.flush();numerators.flush();need(bool(values)&&bool(numerators),"Value checkpoint flush failed");}
            if(mutation=="none")need(!poles,"Exact full pole cancellation failed at type "+std::to_string(image.p.tid));
        }
        values.close();numerators.close();need(bool(values)&&bool(numerators),"Value output completion failed");
        double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
        std::cout<<"{\"status\":\"COMPLETE\",\"q\":"<<q<<",\"start\":"<<start<<",\"stop\":"<<stop<<",\"types\":"<<originals.size()<<",\"nonzero_pole_rows\":"<<nonzero_poles<<",\"maximum_full_numerator\":"<<max_numerator<<",\"numerator_point_visits\":"<<total_visits<<",\"proper_face_terms\":"<<face_terms<<",\"maximum_generic_base\":"<<max_base<<",\"mutation\":\""<<mutation<<"\",\"seconds\":"<<seconds<<"}\n";return 0;
    } catch(const std::exception& error){std::cerr<<"REFUSED: "<<error.what()<<'\n';return 2;}
}
