#include "helperFunctions.h"


string checkFlush(std::vector<int> realHand, std::vector<int> suitsHand){
    //the std::vector that gets passed in is already sorted and has already been divided by 13
    int count = 1, currMax = 1;
    int prev = suitsHand[0];
    int flushSuit = -1;
    for(int i = 1;i<suitsHand.size();i++){
        if(suitsHand[i] == prev){
            count++;
            if(count == 5) flushSuit = prev;
            if(count > currMax) currMax = count;
        }
        else{
            count = 1;
        }
        prev = suitsHand[i];
    }
    string toReturn = "";
    if(currMax < 5) return "-1";
    for(int i = realHand.size()-1;i>=0;i--){
        if(realHand[i]/13 == flushSuit){
            toReturn.push_back('0' + (char) (realHand[i]%13));
        }
    }
    return toReturn;
}
string checkStraight(std::vector<int> numsHand){
    for(int i = 0;i<numsHand.size();i++){
        if(numsHand[i] == 12) numsHand.push_back(-1);
    }
    sort(numsHand.begin(),numsHand.end());
    int count = 1, currMax = 1;
    int prev = numsHand[numsHand.size()-1];
    string toReturn = "";
    bool isAnAce = false;
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == 12) isAnAce = true;
        if(numsHand[i] == prev-1){
            count++;
            toReturn += (char) numsHand[i];
            if(count > currMax) currMax = count;
            if(count == 5) return toReturn;
        }
        else{
            count = 1;
            toReturn = "";
        }
        prev = numsHand[i];
    }
    return "-1";
}
string checkPair(std::vector<int> numsHand){
    int prev = numsHand[numsHand.size()-1];
    string highCards = "";
    string pair = "";
    bool theresAPair = false;
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev){
            pair += (char) numsHand[i];
            theresAPair = true;
        }
        else if(highCards.length() < 3 ){
            if(pair.length() > 0){
                if((char) prev !=  pair[0]){
                    highCards += (char) prev;
                }
            }
            else{
                highCards += (char) prev;
            }
            
        }
        prev = numsHand[i];
    }
    if(theresAPair) return pair + highCards;
    return "-1";
}
string checkQuads(std::vector<int> numsHand){
    int count = 1, currMax = 1;
    int prev = numsHand[numsHand.size()-1];
    string highCard = "";
    string quadCard = "";
    bool hitQuads = false;
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev){
            count++;
            if(count == 4){
                hitQuads = true;
                quadCard = (char) numsHand[i];
            } 
        }
        else{
            if(highCard.length() == 0){
                if(quadCard.length() > 0){
                    if((char) prev != highCard[0]){
                        highCard += (char) prev;
                    }
                }
                else{
                    highCard += (char) prev;
                }
            }
            count = 1;
        }
        prev = numsHand[i];
    }
    if(hitQuads) return quadCard + highCard;
    return "-1";
}
string checkTwoPair(std::vector<int> numsHand){
    int prev = numsHand[numsHand.size()-1];
    string highCard = "";
    string pair1 = "";
    string pair2 = "";
    bool hitTwoPair = false;
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev){
            if(pair1.length() == 0){
                pair1 += (char) numsHand[i];
            }
            else{
                if(numsHand[i] != pair1[0]){
                    pair2 += (char) numsHand[i];
                    hitTwoPair = true;
                }
            }
        }
        else{
            if(highCard.length() == 0){
                if(pair1.length() == 0){
                    highCard += (char) prev;
                }
                else{
                    if(pair2.length() == 0){
                         if((char) prev != pair1[0]){
                            highCard += (char) prev;
                         }
                    }
                    else{
                        if((char) prev != pair1[0] && (char) prev != pair2[0]){
                            highCard += (char) prev;
                        }
                    }
                }
            }
        }
        prev = numsHand[i];
    }
    if(hitTwoPair) return pair1 + pair2 + highCard;
    return "-1";
}
string checkStraightFlush(std::vector<int> realHand){
    std::vector<std::vector<int>> numsBySuits(4,std::vector<int>());
    for(int i = 0;i<realHand.size();i++){
        int num = realHand[i]%13;
        int suit = realHand[i]/13;
        numsBySuits[suit].push_back(num);
        if(num == 12) numsBySuits[suit].push_back(-1);
    }
    for(int i = 0;i<numsBySuits.size();i++){
        if(numsBySuits[i].size() < 5) continue;
        sort(numsBySuits[i].begin(),numsBySuits[i].end());
        int prev = numsBySuits[i][numsBySuits.size()-1];

        for(int j = numsBySuits.size()-2;j>=0;j--){
            string toReturn = checkStraight(numsBySuits[i]);
            if(toReturn != "-1") return toReturn;
        }
    }
    return "-1";
}
string checkTrips(std::vector<int> numsHand){
    int count = 1;
    int prev = numsHand[numsHand.size()-1];
    string highCards = "";
    string trips = "";
    bool theresTrips = false;
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev){
            count++;
            if(count == 3){
                trips += (char) numsHand[i];
                theresTrips = true;
            }
        }
        else if(highCards.length() < 2){
            if(trips.length() > 0){
                if((char) prev !=  trips[0]){
                    highCards += (char) prev;
                }
            }
            count = 1;
        }
        else{
            highCards += (char) prev;
            count = 1;
        }
        prev = numsHand[i];
    }
    if(theresTrips) return trips + highCards;
    return "-1";
}
string checkFullHouse(std::vector<int> numsHand){
    std::map<int, int> cardCount;
    std::vector<int> threeOfAKind;
    std::vector<int> pair;

    for (int card : numsHand) {
        cardCount[card]++;
    }

    for (const auto& entry : cardCount) {
        int card = entry.first;
        int count = entry.second;

        if (count >= 3) {
            threeOfAKind.push_back(card);
        }
        else if (count == 2) {
            pair.push_back(card);
        }
    }

    if (!threeOfAKind.empty()) {
        sort(threeOfAKind.begin(), threeOfAKind.end(), std::greater<int>());
        int maxThree = threeOfAKind[0];
        threeOfAKind.clear();

        if (!pair.empty()) {
            int smallThree = pair.back();
            pair.pop_back();
            pair.push_back(smallThree);
        }

        if (!pair.empty()) {
            return std::to_string(maxThree) + std::to_string(maxThree) + std::to_string(maxThree) + std::to_string(pair[0]) + std::to_string(pair[0]);
        }
    }

    return "-1";
}
bool checkFlushDraw(std::vector<int> floppedHand){
    std::vector<int> suits(4,0);
    for(int i = 0;i<floppedHand.size();i++){
        suits[floppedHand[i] / 13]++;
    }
    for(int i = 0;i<4;i++){
        if(suits[i] == 4){
            if((floppedHand[0]/4 == i && floppedHand[0]-(13*i) >= 8) || (floppedHand[1]/4 == i && floppedHand[1]-(13*i) >= 8)) return true;
        }
    }
    return false;
}
