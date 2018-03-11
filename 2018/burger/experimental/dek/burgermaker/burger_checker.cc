#include <msgpack.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>

using namespace std;

enum BurgerElements {
  EMPTY = '0',
  CROWN,
  LETTUCE,
  TOMATO,
  CHEESE,
  PATTY,
  HEEL,
};
  
bool check_burger(string burger, bool debug = false) {
  if (burger.length() != 8) {
    if (debug) cout << "Burger is wrong size" << endl;
    return false;
  }
  string::iterator crown_pos = burger.end();
  for (auto layer_it = burger.begin(); layer_it != burger.end(); ++layer_it) {
    if (*layer_it == EMPTY) continue;
    if (*layer_it == CROWN) {
      crown_pos = layer_it;
      break;
    }
    if (debug) cout << "Prefix elements must be empty or crown" << endl;
    return false;
  }
  
  if (crown_pos == burger.end()) {
    if (debug) cout << "Must have crown." << endl;
    return false;
  }

  if (burger[7] != HEEL) {
    if (debug) cout << "Burger must have heel bottom" << endl;
    return false;
  }

  if ((find(crown_pos+1, burger.end()-1, CROWN) != burger.end()-1) ||
      (find(crown_pos+1, burger.end()-1, HEEL) != burger.end()-1)) {
    if (debug) cout << "Cannot have internal buns" << endl;
    return false;
  }

  if ((find(crown_pos+1, burger.end(), EMPTY) != burger.end())) {
    if (debug) cout << "Cannot have internal or terminal empty" << endl;
    return false;
  }

  char prev = '\0';
  for(auto &it : burger) {
    if (it != '0' && it == prev) {
      if (debug) cout << "Cannot have sequential non-empty items" << endl;
      return  false;
    }
    prev = it;
  }

  if (burger.find(PATTY) == string::npos) {
    if (debug) cout << "Must have at least one patty." << endl;
    return false;
  }

  auto last_cheese_pos = burger.find_last_of(CHEESE);
  if (last_cheese_pos != string::npos) {
    auto last_patty_pos = burger.find_last_of(PATTY);
    if (last_patty_pos != string::npos && last_patty_pos < last_cheese_pos) {
      if (debug) cout << "Must have at least one patty after last cheese." << endl;
      return false;
    }
  }

  return true;
}

int main() {

  ifstream file("burgers.txt");
  string row_index;
  string burger;
  cout << boolalpha;
  while(file.good()) {
    getline(file, burger, '\n') ;
    if (!file.good()) break;
    cout << burger << " " << check_burger(burger) << endl;
  }

  // burger = "10000156";
  // cout << burger << endl;
  // check_burger(burger, true);
}
