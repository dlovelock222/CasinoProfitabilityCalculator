#include <iostream>
#include <map>
#include <vector>
#include <cstdlib>
#include <algorithm>


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

int main(){
    vector<int> playerStks;
    long int totalOnTable = 0;
    for(int i = 0;i<NUMPLAYERS;i++){
        int x = rand() * MAXSTACK;
        playerStks.push_back(x);
        totalOnTable += x;
    }
    vector<vector<int>> playerHands(NUMPLAYERS, vector<int>());
    vector<vector<int>> playerBets(NUMPLAYERS, vector<int>(3,0));
    vector<int> dealerHand;
    vector<int> table;
    for(int i = 0;i<SIMS;++i){
        //place player initial bets (trips and anti/blind)
        for(int j = 0;j<NUMPLAYERS;j++){
            playerBets[j][0] = (rand() * MAXBETINCREMENT) * BETINCREMENTS;//assign the trips bet
            playerBets[j][1] = (rand() * MAXBETINCREMENT) * BETINCREMENTS;//assign the ante and blind bet
        }
        //deal all the cards
        vector<int> cardsDealt(NUMCARDS,0);
        dealCards(cardsDealt,table,5);
        dealCards(cardsDealt,dealerHand,2);
        for(int j = 0;j<NUMPLAYERS;j++){
            dealCards(cardsDealt, playerHands[i], 2);
        }
        //pay out players
        pair<int,string> dH = handValue(table, dealerHand);
        for(int j = 0;j<NUMPLAYERS;j++){
            //figure out when/if the player bets
            //figure out who has a better hand, player or dealer
            pair<int,string> pH = handValue(table, playerHands[i]);
            
            //adjust player stack accordingly
        }
    }
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
    if(currMax < 5) return toReturn;
    for(int i = realHand.size()-1;i>=0;i--){
        if(realHand[i]/13 == flushSuit){
            toReturn.push_back((char) realHand[i]);
        }
    }
    return toReturn;
}

string checkStraight(vector<int> realHand, vector<int> numsHand){
    int count = 0, currMax = 0;
    int prev = numsHand[numsHand.size()-1];
    string toReturn = "";
    for(int i = numsHand.size()-2;i>=0;i--){
        if(numsHand[i] == prev-1){
            count++;
            toReturn += (char) numsHand[i];
            if(count > currMax) currMax = count;
            
        }
        else{
            count = 0;
        }
        prev = numsHand[i];
    }
}
string checkPair(vector<int> hand){
    
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
    pair<string,string> toReturn;

    //check for straight flush
    
    //check for quads

    //check for boat

    //check for flush

    //check for straight

    //check for trips

    //check for twopair

    //check for pair

    //return which high card
}