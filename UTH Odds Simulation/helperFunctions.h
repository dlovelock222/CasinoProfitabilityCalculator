#pragma once

#include <map>
#include <vector>
#include <stack>
#include <string>

std::string checkFlush(std::vector<int> realHand, std::vector<int> suitsHand);
std::string checkStraight(std::vector<int> numsHand);
std::string checkPair(std::vector<int> numsHand);
std::string checkQuads(std::vector<int> numsHand);
std::string checkTwoPair(std::vector<int> numsHand);
std::string checkStraightFlush(std::vector<int> realHand);
std::string checkTrips(std::vector<int> numsHand);
std::string checkFullHouse(std::vector<int> numsHand);