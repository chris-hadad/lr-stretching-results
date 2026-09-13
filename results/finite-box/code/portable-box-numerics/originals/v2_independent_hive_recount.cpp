// Independently written complete bounded integer H-system counter.
// Protocol: RECOUNT1 id n m max_states milliseconds, n pairs lo hi,
// then m rows c a_1 ... a_n, each meaning c + sum(a_j*x_j) >= 0.
// Overflow or any resource limit refuses the entire request, never a partial sum.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using I = __int128_t;
using U = __uint128_t;
using Row = std::vector<I>;

struct Refusal : std::runtime_error { using std::runtime_error::runtime_error; };

I add(I x, I y) { I z; if (__builtin_add_overflow(x,y,&z)) throw Refusal("REFUSED_OVERFLOW"); return z; }
I sub(I x, I y) { I z; if (__builtin_sub_overflow(x,y,&z)) throw Refusal("REFUSED_OVERFLOW"); return z; }
I mul(I x, I y) { I z; if (__builtin_mul_overflow(x,y,&z)) throw Refusal("REFUSED_OVERFLOW"); return z; }
U add_count(U x, U y) { U z; if (__builtin_add_overflow(x,y,&z)) throw Refusal("REFUSED_OVERFLOW"); return z; }
U mul_count(U x, U y) { U z; if (__builtin_mul_overflow(x,y,&z)) throw Refusal("REFUSED_OVERFLOW"); return z; }
I absolute(I x) { return x < 0 ? sub(0,x) : x; }
I gcd128(I a, I b) { a=absolute(a); b=absolute(b); while (b) { I r=a%b; a=b; b=r; } return a; }
I floor_div(I x, I positive) {
    if (positive <= 0) throw Refusal("REFUSED_INPUT");
    I q=x/positive, r=x%positive; return r < 0 ? sub(q,1) : q;
}
I ceil_div(I x, I positive) {
    if (positive <= 0) throw Refusal("REFUSED_INPUT");
    I q=x/positive, r=x%positive; return r > 0 ? add(q,1) : q;
}
std::int64_t narrow(I x) {
    if (x < std::numeric_limits<std::int64_t>::min() || x > std::numeric_limits<std::int64_t>::max())
        throw Refusal("REFUSED_OVERFLOW");
    return static_cast<std::int64_t>(x);
}
std::string decimal(U x) {
    if (!x) return "0";
    std::string s;
    while (x) { s.push_back(static_cast<char>('0'+x%10)); x/=10; }
    std::reverse(s.begin(),s.end()); return s;
}

struct State {
    std::vector<std::int64_t> lo,hi;
    std::vector<Row> rows;
    bool full_box=false;
};

struct Counter {
    std::uint64_t visited=0, row_work=0, hits=0, max_states;
    std::size_t memo_bytes=0;
    std::chrono::steady_clock::time_point start, deadline;
    std::unordered_map<std::string,U> memo;
    Counter(std::uint64_t cap, std::uint64_t milliseconds) : max_states(cap) {
        start=std::chrono::steady_clock::now();
        deadline=start+std::chrono::milliseconds(milliseconds);
    }
    void check_time() const {
        if (std::chrono::steady_clock::now() >= deadline) throw Refusal("REFUSED_TIME");
    }
    void work() {
        if (row_work == std::numeric_limits<std::uint64_t>::max()) throw Refusal("REFUSED_WORK");
        ++row_work;
        if ((row_work & 255) == 0) check_time();
    }
    double seconds() const {
        return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    }
    bool propagate(State& s) {
        const std::size_t n=s.lo.size();
        for (std::size_t j=0;j<n;++j) if (s.lo[j]>s.hi[j]) return false;
        bool changed=true;
        while (changed) {
            check_time(); changed=false;
            for (const Row& r:s.rows) {
                work(); I maximum=r[0];
                for (std::size_t j=0;j<n;++j)
                    maximum=add(maximum,mul(r[j+1],r[j+1]>=0 ? s.hi[j] : s.lo[j]));
                if (maximum<0) return false;
                for (std::size_t j=0;j<n;++j) {
                    const I a=r[j+1];
                    if (!a) continue;
                    const I rest=sub(maximum,mul(a,a>0 ? s.hi[j] : s.lo[j]));
                    if (a>0) {
                        I lower=ceil_div(sub(0,rest),a);
                        if (lower>s.hi[j]) return false;
                        if (lower>s.lo[j]) { s.lo[j]=narrow(lower); changed=true; }
                    } else {
                        I upper=floor_div(rest,sub(0,a));
                        if (upper<s.lo[j]) return false;
                        if (upper<s.hi[j]) { s.hi[j]=narrow(upper); changed=true; }
                    }
                }
            }
        }
        return true;
    }
    void canonicalize(State& s) {
        // Substitute fixed variables and translate all surviving variables to
        // start at zero. A row is removed only after its exact minimum on the
        // current enclosing integer box proves it nonnegative everywhere.
        // Every remaining binding mixed row is retained.
        std::vector<std::size_t> active;
        State out;
        out.full_box=true;
        for (std::size_t j=0;j<s.lo.size();++j) if (s.lo[j]!=s.hi[j]) {
            active.push_back(j); out.lo.push_back(0);
            out.hi.push_back(narrow(sub(s.hi[j],s.lo[j])));
        }
        for (const Row& r:s.rows) {
            work(); I constant=r[0],minimum=r[0];
            for (std::size_t j=0;j<s.lo.size();++j) {
                constant=add(constant,mul(r[j+1],s.lo[j]));
                minimum=add(minimum,mul(r[j+1],r[j+1]>=0 ? s.lo[j] : s.hi[j]));
            }
            if (minimum<0) out.full_box=false;
            else continue; // Exact box-valid redundancy certificate, including mixed rows.
            Row next{constant}; I g=0;
            for (auto j:active) { next.push_back(r[j+1]); g=gcd128(g,r[j+1]); }
            if (!g) {
                if (constant<0) throw Refusal("REFUSED_INTERNAL");
                continue; // This full original row is now a verified true constant.
            }
            // Exact integer equivalence: c+g*a*x>=0 iff floor(c/g)+a*x>=0.
            next[0]=floor_div(next[0],g);
            for (std::size_t j=1;j<next.size();++j) next[j]/=g;
            out.rows.push_back(std::move(next));
        }
        std::sort(out.rows.begin(),out.rows.end());
        out.rows.erase(std::unique(out.rows.begin(),out.rows.end()),out.rows.end());
        s=std::move(out);
    }
    static void append(std::string& out, U value, unsigned bytes) {
        for (unsigned j=0;j<bytes;++j) { out.push_back(static_cast<char>(value & 255)); value>>=8; }
    }
    std::string key(const State& s) {
        std::string result;
        append(result,s.lo.size(),8); append(result,s.rows.size(),8);
        for (auto hi:s.hi) append(result,static_cast<U>(hi),8);
        for (const Row& row:s.rows) {
            append(result,static_cast<U>(row[0]),16);
            for (std::size_t j=1;j<row.size();++j)
                append(result,static_cast<std::uint64_t>(narrow(row[j])),8);
        }
        return result;
    }
    U remember(std::string key, U count) {
        // Stopping memo insertion is exact; it never changes the count or
        // supplies an incomplete cached result. Memory is an optional shortcut.
        const std::size_t cost=key.size()+160;
        if (cost <= 64*1024*1024 && memo_bytes <= 64*1024*1024-cost) {
            auto inserted=memo.emplace(std::move(key),count);
            if (inserted.second) memo_bytes+=cost;
        }
        return count;
    }
    U solve(State s, unsigned depth=0) {
        check_time();
        if (visited>=max_states) throw Refusal("REFUSED_WORK");
        ++visited;
        if (depth>256) throw Refusal("REFUSED_DEPTH");
        if (!propagate(s)) return 0;
        canonicalize(s);
        const std::size_t n=s.lo.size();
        if (!n) return 1;
        if (s.rows.empty() || s.full_box || n==1) {
            U total=1;
            for (auto hi:s.hi) total=mul_count(total,static_cast<U>(hi)+1);
            return total;
        }
        std::string identity=key(s);
        auto found=memo.find(identity);
        if (found!=memo.end()) { ++hits; return found->second; }
        // Factor only connected components of the NONZERO SUPPORTS of every
        // remaining complete row. A mixed row joins all of its variables.
        std::vector<std::size_t> parent(n);
        std::iota(parent.begin(),parent.end(),0);
        auto root=[&](std::size_t j) { while (parent[j]!=j) j=parent[j]; return j; };
        for (const Row& row:s.rows) {
            std::size_t first=n;
            for (std::size_t j=0;j<n;++j) if (row[j+1]) {
                if (first==n) first=j;
                else parent[root(j)]=root(first);
            }
        }
        std::vector<std::vector<std::size_t>> groups(n);
        for (std::size_t j=0;j<n;++j) groups[root(j)].push_back(j);
        std::size_t component_count=0;
        for (const auto& group:groups) component_count+=!group.empty();
        if (component_count>1) {
            U total=1;
            for (const auto& group:groups) if (!group.empty()) {
                State child;
                for (auto j:group) { child.lo.push_back(0); child.hi.push_back(s.hi[j]); }
                for (const Row& row:s.rows) {
                    bool belongs=false;
                    for (auto j:group) belongs=belongs || row[j+1]!=0;
                    if (!belongs) continue;
                    Row projected{row[0]};
                    for (auto j:group) projected.push_back(row[j+1]);
                    child.rows.push_back(std::move(projected));
                }
                total=mul_count(total,solve(std::move(child),depth+1));
                if (!total) break; // A complete zero factor proves the full count zero.
            }
            return remember(std::move(identity),total);
        }
        const std::size_t variable=std::min_element(s.hi.begin(),s.hi.end())-s.hi.begin();
        const std::int64_t middle=s.hi[variable]/2;
        State right=s;
        s.hi[variable]=middle;
        right.lo[variable]=middle+1;
        U left_count=solve(std::move(s),depth+1);
        U right_count=solve(std::move(right),depth+1);
        return remember(std::move(identity),add_count(left_count,right_count));
    }
};

bool valid_id(const std::string& id) {
    if (id.empty() || id.size()>160) return false;
    for (unsigned char ch:id)
        if (!((ch>='A'&&ch<='Z')||(ch>='a'&&ch<='z')||(ch>='0'&&ch<='9')||ch=='_'||ch=='-'||ch==':'||ch=='.')) return false;
    return true;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::string protocol,id;
    while (std::cin>>protocol) {
        std::size_t n,m;
        std::uint64_t cap,milliseconds;
        if (!(std::cin>>id>>n>>m>>cap>>milliseconds) || protocol!="RECOUNT1" || !valid_id(id)
            || n>64 || m>10000 || cap==0 || cap>static_cast<std::uint64_t>(std::numeric_limits<std::int64_t>::max())
            || milliseconds==0 || milliseconds>110000) {
            std::cout<<"{\"status\":\"REFUSED_INPUT\",\"count\":null}"<<std::endl; return 2;
        }
        State state;
        state.lo.resize(n); state.hi.resize(n);
        for (std::size_t j=0;j<n;++j) if (!(std::cin>>state.lo[j]>>state.hi[j])) {
            std::cout<<"{\"status\":\"REFUSED_INPUT\",\"count\":null}"<<std::endl; return 2;
        }
        state.rows.resize(m,Row(n+1));
        for (auto& row:state.rows) for (auto& value:row) {
            std::int64_t input;
            if (!(std::cin>>input)) { std::cout<<"{\"status\":\"REFUSED_INPUT\",\"count\":null}"<<std::endl; return 2; }
            value=input;
        }
        Counter counter(cap,milliseconds);
        std::string status="complete",count;
        try { count=decimal(counter.solve(std::move(state))); }
        catch (const Refusal& error) { status=error.what(); }
        catch (const std::bad_alloc&) { status="REFUSED_MEMORY"; }
        std::cout<<"{\"id\":\""<<id<<"\",\"status\":\""<<status<<"\",\"count\":";
        if (status=="complete") std::cout<<'"'<<count<<'"'; else std::cout<<"null";
        std::cout<<",\"visited_states\":"<<counter.visited<<",\"row_work\":"<<counter.row_work
                 <<",\"memo_hits\":"<<counter.hits<<",\"elapsed_seconds\":"<<counter.seconds()<<"}"<<std::endl;
    }
    return 0;
}
