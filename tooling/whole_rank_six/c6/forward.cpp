// Forward Euler--Maclaurin recurrence, independent of the Python projection.
#define main inherited_local_values_main
#include "local_values.cpp"
#undef main
#include <fstream>
#include <functional>
int main(int argc, char **argv) {
  try {
    require(argc == 2, "atlas input required");
    std::ifstream in(argv[1]); int count, dim;
    require(bool(in >> count >> dim) && count == 42 && dim == 10, "atlas dimensions");
    IntMatrix normals(count, Row(dim));
    for (auto &r: normals) for (auto &v: r) require(bool(in >> v), "short atlas");
    std::string rest; require(!(in >> rest), "trailing atlas");
    for(int q=4;q<=4;++q) {
      std::vector<int> ids;
      std::function<void(int)> visit=[&](int start) {
        if(int(ids.size())!=q) {
          for(int i=start;i<count;++i){ids.push_back(i);visit(i+1);ids.pop_back();}
          return;
        }
        IntMatrix n;for(int i:ids)n.push_back(normals[i]);
        try{(void)image_index(n);}catch(const std::runtime_error &e){
          require(std::string(e.what())=="dependent input normals", "unexpected index error");
          return;
        }
        auto r=evaluate(n);
        for(size_t i=0;i<ids.size();++i){if(i)std::cout<<',';std::cout<<ids[i];}
        std::cout<<' '<<r.alpha<<' '<<r.index<<'\n';
      };visit(0);
    }
    return 0;
  }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
