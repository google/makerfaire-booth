#include <algorithm>

#include <iostream>
#include <vector>
std::vector<std::vector<int> > cart_product (const std::vector<std::vector<int> >& v) {
  std::vector<std::vector<int> > s = {{}};
  for (const auto& u : v) {
    std::vector<std::vector<int> > r;
    for (const auto& x : s) {
      for (const auto y : u) {
	r.push_back(x);
	r.back().push_back(y);
      }
    }
    s = std::move(r);
  }
  return s;
}
int main(void) {
  const std::vector<int> v = { 0, 1, 2, 3, 4, 5, 6 };
  
  const std::vector<std::vector<int> > v2(8, v);
  auto result = cart_product(v2);
  sort(result.begin(), result.end());
  for(int i = 0; i < result.size(); ++i) {
    std::cout << result[i][0] << result[i][1] << result[i][2] << result[i][3] << result[i][4] << result[i][5] << result[i][6] << result[i][7] << std::endl;
  }
}
