#pragma once

#include <map>
#include <vector>
#include <stack>
#include <string>
#include <algorithm>
using namespace std;

string checkFlush(std::vector<int> realHand, std::vector<int> suitsHand);
string checkStraight(std::vector<int> numsHand);
string checkPair(std::vector<int> numsHand);
string checkQuads(std::vector<int> numsHand);
string checkTwoPair(std::vector<int> numsHand);
string checkStraightFlush(std::vector<int> realHand);
string checkTrips(std::vector<int> numsHand);
string checkFullHouse(std::vector<int> numsHand);
bool checkFlushDraw(std::vector<int> floppedHand);