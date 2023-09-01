#include <iostream>
#include <map>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <stack>
#include <random>

using namespace std;

const long long SIMS = 20;
int BANKROLL = 21000;
int NUMPLAYERS = 5;
int MAXSTACK = 2000;
int NUMCARDS = 52;
int BETINCREMENTS = 5;
int MAXBETINCREMENT = 10;
map<string,int> handRankings;
vector<string> numToCardConversion = 
{"2s","3s","4s","5s","6s","7s","8s","9s","10s","Js","Qs","Ks","As",
 "2d","3d","4d","5d","6d","7d","8d","9d","10d","Jd","Qd","Kd","Ad",
 "2c","3c","4c","5c","6c","7c","8c","9c","10c","Jc","Qc","Kc","Ac",
 "2h","3h","4h","5h","6h","7h","8h","9h","10h","Jh","Qh","Kh","Ah"
};
vector<string> numToHandConversion = {
    "high Card", "pair", "twoPair", "three of a kind", "straight", "flush", "full house", "quads", "straight flush"
};

void dealCards(vector<int>&, vector<int>&, int);
pair<int,string> handValue(vector<int>, vector<int>);


//all of these algos check whether or not the player/dealer has a given hand
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
    if(isAnAce){
        for(int i = 0;i<numsHand.size();i++){
            if(numsHand[i] == prev || numsHand[i] == prev+1){
                if(numsHand[i] == 5) return "5";
            }
            else break;
        }
    }
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
    vector<vector<int>> numsBySuits(4,vector<int>());
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
string checkTrips(vector<int> numsHand){
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
string checkFullHouse(vector<int> numsHand){
    int prev = numsHand[numsHand.size()-1];
    string card1 = "";
    string card2 = "";
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev){
            if(card1.length() == 0){
                card1 += (char) prev;
                card1 += (char) prev;
            }
            else if(card1.length() >= 0 && card1[0] == (char) numsHand[i]){
                card1 += (char) prev;
            }
            else if(card2.length() == 0){
                card2 += (char) prev;
                card2 += (char) prev;
            }
            else{
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
    vector<vector<int>> playerBets(NUMPLAYERS, vector<int>(3,0));
    auto rng = default_random_engine {};
    for(int i = 0;i<SIMS;++i){
        //place player initial bets (trips and anti/blind)
        // for(int j = 0;j<NUMPLAYERS;j++){
        //     playerBets[j][0] = (rand() * MAXBETINCREMENT) * BETINCREMENTS;//assign the trips bet
        //     playerBets[j][1] = (rand() * MAXBETINCREMENT) * BETINCREMENTS;//assign the ante and blind bet
        // }
        //deal all the cards
        vector<int> deck;
        for(int j = 0;j<52;j++) deck.push_back(j);
        
        shuffle(begin(deck), end(deck), rng);
        vector<int> dealerHand;
        vector<int> table;
        dealCards(deck,table,5);
        dealCards(deck,dealerHand,2);
        vector<vector<int>> playerHands(NUMPLAYERS, vector<int>());
        for(int j = 0;j<NUMPLAYERS;j++){
            dealCards(deck, playerHands[j], 2);
        }
        pair<int,string> dH = handValue(table, dealerHand);
        cout << "-----HAND #" << i << "-----" << endl;
        cout << "dealers hand: " << numToCardConversion[dealerHand[0]] + numToCardConversion[dealerHand[1]] << "---" << numToHandConversion[dH.first] << endl;
        cout << "table: ";
        for(int j = 0;j<table.size();j++){
            cout << numToCardConversion[table[j]];
        }
        cout << endl << endl;
        //pay out players
        for(int j = 0;j<NUMPLAYERS;j++){
            //figure out when/if the player bets
            //figure out who has a better hand, player or dealer
            pair<int,string> pH = handValue(table, playerHands[j]);
            cout << "player #" << j << "hand = " << numToCardConversion[playerHands[j][0]] + numToCardConversion[playerHands[j][1]] << endl;
            if(pH == dH){
                cout << "Player pushes with: " << numToHandConversion[pH.first] << endl;
            }
            else if(pH > dH){
                cout << "Player wins with: " << numToHandConversion[pH.first] << endl;
            }
            else{
                cout << "Player loses with: " << numToHandConversion[pH.first] << endl;
            }
            cout << endl;
        }
    }

    return 0;
}

void dealCards(vector<int>& deck, vector<int>& cards, int numCards){
    for(int i = 0;i<numCards;i++){
        int x = deck.back();
        cards.push_back(x);
        deck.pop_back();
    }
}

string convertTieBreaker(string s){
    string toReturn = "";
    for(int i = 0;i<s.size();i++){
        toReturn += s[i] + '0';
    }
    return toReturn;
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
    if((tieBreaker = checkStraightFlush(sevenCardHand)) != "-1") return make_pair(8, convertTieBreaker(tieBreaker));
    //check for quads return 7
    if((tieBreaker = checkQuads(sevenCardHand)) != "-1") return make_pair(7, convertTieBreaker(tieBreaker));
    //check for boat return 6
    if((tieBreaker = checkFullHouse(numsHand)) != "-1") return make_pair(6, convertTieBreaker(tieBreaker));
    //check for flush return 5
    if((tieBreaker = checkFlush(sevenCardHand, suitsHand)) != "-1") return make_pair(5, convertTieBreaker(tieBreaker));
    //check for straight return 4
    if((tieBreaker = checkStraight(numsHand)) != "-1") return make_pair(4, convertTieBreaker(tieBreaker));
    //check for trips return 3
    if((tieBreaker = checkTrips(numsHand)) != "-1") return make_pair(3, convertTieBreaker(tieBreaker));
    //check for twopair return 2
    if((tieBreaker = checkTwoPair(numsHand)) != "-1") return make_pair(2, convertTieBreaker(tieBreaker));
    //check for pair return 1
    if((tieBreaker = checkPair(numsHand)) != "-1") return make_pair(1, convertTieBreaker(tieBreaker));
    //return 0 which high card
    string toReturn = "";
    for(int i = 0;i<5;i++){
        toReturn += numsHand[numsHand.size()-1-i];
    }
    return make_pair(0,toReturn);
}