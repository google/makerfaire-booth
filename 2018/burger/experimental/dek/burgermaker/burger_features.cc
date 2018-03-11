#include <msgpack.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>

using namespace std;

enum BurgerElement {
  empty,
  crown,
  lettuce,
  tomato,
  cheese,
  patty,
  heel,
};

MSGPACK_ADD_ENUM(your_enum);

class BurgerElementCounts {
private:
  map<int, int> counts;
public:
  BurgerElementCounts(string burger) {
    for(auto &it : burger) {
      int i = it-48;
      counts[i]++;
    }
  }
  MSGPACK_DEFINE(counts);
};

class BurgerFeatures {
private:
  BurgerElementCounts counts;
  bool non_empty_sequential_duplicates;
public:
  BurgerFeatures(string burger): counts(BurgerElementCounts(burger)), non_empty_sequential_duplicates(false) {
    char prev = '\0';
    for(auto &it : burger) {
      if (it != '0' && it == prev) {
	non_empty_sequential_duplicates = true;
	break;
      }
    }
  }
  MSGPACK_DEFINE(counts, non_empty_sequential_duplicates);
};

int main() {

  ifstream file("burgers.csv");
  string row_index;
  string burger;
  map<string, BurgerFeatures> burger_features_map;
  while(file.good()) {
    getline(file, row_index, ',');
    getline(file, burger, '\n') ;
    burger_features_map.insert(make_pair(burger, BurgerFeatures(burger)));
  }

  std::ofstream ofs("./burger_features.dat");
  msgpack::pack(ofs, burger_features_map);
}
