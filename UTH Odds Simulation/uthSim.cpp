#include <iostream>
#include <map>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <stack>

using namespace std;

const long long SIMS = 1500;
int BANKROLL = 21000;
int NUMPLAYERS = 8;
int MAXSTACK = 2000;
int NUMCARDS = 52;
int BETINCREMENTS = 5;
int MAXBETINCREMENT = 10;
map<string,int> handRankings;

void dealCards(vector<int>&, vector<int>&, int);
pair<int,string> handValue(vector<int>, vector<int>);



string checkFlush(vector<int> realHand, vector<int> suitsHand){
    //the vector that gets passed in is already sorted and has already been divided by 13
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
            count = 0;
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
string checkStraight(vector<int> numsHand){
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

    //check for ace low straight

    return "-1";
}
string checkPair(vector<int> numsHand){
    int prev = numsHand[numsHand.size()-1];
    string highCards = "";
    string pair = "";
    bool theresAPair = false;
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev){
            pair += (char) numsHand[i];
            theresAPair = true;
        }
        else if(highCards.length() < 3 && pair.length() >0 && ((char) prev) !=  pair[0]){
            highCards += (char) prev;
        }
        prev = numsHand[i];
    }
    if(theresAPair) return pair + highCards;
    return "-1";
}
string checkQuads(vector<int> numsHand){
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
                
        }
        prev = numsHand[i];
    }
    if(hitQuads) return quadCard + highCard;
    return "-1";
}
string checkTwoPair(vector<int> numsHand){
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
string checkStraightFlush(vector<int> realHand){
    int count = 1, currMax = 1;
    int startIndex = -1;
    int prev = realHand[realHand.size()-1];
    for(int i = realHand.size()-2;i>=0;i--){
        if(realHand[i] == prev-1){
            count++;
            currMax = max(count,currMax);
            if(startIndex == -1) startIndex = i+1;
        }
        else{
            count = 1;
            startIndex = -1;
        }
    }
    if(currMax >=0){
        string toReturn = "";
        for(int i = 0;i<5;i++) toReturn += (realHand[startIndex-i]%13);
    }
    else return "-1";
}
string checkTrips(vector<int> numsHand){
    int count = 1, currMax = 1;
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
        else if(highCards.length() < 2 && trips.length() > 0 && ((char) prev) !=  trips[0]){
            highCards += (char) prev;
            count = 1;
        }
        prev = numsHand[i];
    }
    if(theresTrips) return trips + highCards;
    return "-1";
}
string checkFullHouse(vector<int> numsHand){
    int prev = numsHand[numsHand.size()-1];
    string card1 = "";
    string card2 = "";
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev){
            if(card1.length() >= 0 && card1[0] == (char) numsHand[i]){
                card1 += (char) prev;
            }
            else if(card2.length() >= 0 && card2[0] == (char) numsHand[i]){
                card2 += (char) prev;
            }
            else if(card1.length() == 0){
                card1 += (char) prev;
                card1 += (char) prev;
            }
            else{
                card2 += (char) prev;
                card2 += (char) prev;
            }
        }
        prev = numsHand[i];
    }

    if(card1.length()+card2.length() >=5){
        if(card1.length() == card2.length()){
            if(card1 > card2) return card1 + card2.substr(1);
            else return card2 + card1.substr(1);
        }
        else if(card1.length() > card2.length()){
            return card1 + card2;
        }
        else{
            return card2 + card1;
        }
    }
    return "-1";
}

int main(){
    // vector<int> playerStks;
    // long int totalOnTable = 0;
    // for(int i = 0;i<NUMPLAYERS;i++){
    //     int x = rand() * MAXSTACK;
    //     playerStks.push_back(x);
    //     totalOnTable += x;
    // }
    // vector<vector<int>> playerHands(NUMPLAYERS, vector<int>());
    // vector<vector<int>> playerBets(NUMPLAYERS, vector<int>(3,0));
    // vector<int> dealerHand;
    // vector<int> table;
    // for(int i = 0;i<SIMS;++i){
    //     //place player initial bets (trips and anti/blind)
    //     for(int j = 0;j<NUMPLAYERS;j++){
    //         playerBets[j][0] = (rand() * MAXBETINCREMENT) * BETINCREMENTS;//assign the trips bet
    //         playerBets[j][1] = (rand() * MAXBETINCREMENT) * BETINCREMENTS;//assign the ante and blind bet
    //     }
    //     //deal all the cards
    //     vector<int> cardsDealt(NUMCARDS,0);
    //     dealCards(cardsDealt,table,5);
    //     dealCards(cardsDealt,dealerHand,2);
    //     for(int j = 0;j<NUMPLAYERS;j++){
    //         dealCards(cardsDealt, playerHands[i], 2);
    //     }
    //     //pay out players
    //     pair<int,string> dH = handValue(table, dealerHand);
    //     for(int j = 0;j<NUMPLAYERS;j++){
    //         //figure out when/if the player bets
    //         //figure out who has a better hand, player or dealer
    //         pair<int,string> pH = handValue(table, playerHands[i]);
            
    //         //adjust player stack accordingly
    //     }
    // }
    vector<int> flush = {};
    vector<int> suitsHand = {};
    cout << checkStraight(flush, suitsHand) << endl;
    return 0;
}

void dealCards(vector<int>& cD, vector<int>& cards, int numCards){
    for(int i = 0;i<numCards;i++){
        int x;
        do x = rand() * NUMCARDS;
        while(cD[x]);
        cards.push_back(x);
        cD[x] = 1;
    }
}

pair<int,string> handValue(vector<int> table, vector<int> holeCards){
    vector<int> sevenCardHand = table;
    sevenCardHand.insert(sevenCardHand.end(), holeCards.begin(), holeCards.end());
    vector<int> suitsHand = sevenCardHand;
    vector<int> numsHand = sevenCardHand;
    for(int i = 0;i<7;i++){
        suitsHand[i] /= 13;
        numsHand[i] %= 13;
    }
    sort(sevenCardHand.begin(),sevenCardHand.end());
    sort(suitsHand.begin(),suitsHand.end());
    sort(numsHand.begin(),numsHand.end());
    string tieBreaker;

    //check for straight flush return 8
    if((tieBreaker = checkStraightFlush(sevenCardHand)) != "-1") return make_pair(8, tieBreaker);
    //check for quads return 7
    if((tieBreaker = checkQuads(sevenCardHand)) != "-1") return make_pair(7, tieBreaker);
    //check for boat return 6
    if((tieBreaker = checkFullHouse(sevenCardHand)) != "-1") return make_pair(6, tieBreaker);
    //check for flush return 5
    if((tieBreaker = checkFlush(sevenCardHand, suitsHand)) != "-1") return make_pair(5, tieBreaker);
    //check for straight return 4
    if((tieBreaker = checkStraight(numsHand)) != "-1") return make_pair(4, tieBreaker);
    //check for trips return 3
    if((tieBreaker = checkTrips(numsHand)) != "-1") return make_pair(3, tieBreaker);
    //check for twopair return 2
    if((tieBreaker = checkTwoPair(numsHand)) != "-1") return make_pair(2, tieBreaker);
    //check for pair return 1
    if((tieBreaker = checkPair(numsHand)) != "-1") return make_pair(1, tieBreaker);
    //return 0 which high card
    string toReturn = "";
    for(int i = 0;i<5;i++){
        toReturn += numsHand[numsHand.size()-1-i];
    }
    return make_pair(0,toReturn);
}