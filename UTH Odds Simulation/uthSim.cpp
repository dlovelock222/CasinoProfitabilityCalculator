#include <iostream>
#include <map>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <stack>
#include <random>
#include <string>
#include <ctime>
#include "helperFunctions.h"

using namespace std;

bool printing = false;
const int HANDSPERHOUR = 16;
const int HOURSPERNIGHT = 8;
const int NUMNIGHTS = 1000;
const int PUSHING = 4000;
const int NUMPLAYERS = 6;
const int MAXSTACK = 2000;
const int NUMCARDS = 52;
const int BETINCREMENTS = 5;
const int MAXBETINCREMENT = 10;
const int DROP = 3;
int numWins = 0, numLosses = 0, numDraws = 0, numFolds = 0;
int couldntCover = 0;
auto rng = default_random_engine {time(0)};
const vector<string> numToCardConversion = {
 "2s","3s","4s","5s","6s","7s","8s","9s","10s","Js","Qs","Ks","As",
 "2d","3d","4d","5d","6d","7d","8d","9d","10d","Jd","Qd","Kd","Ad",
 "2c","3c","4c","5c","6c","7c","8c","9c","10c","Jc","Qc","Kc","Ac",
 "2h","3h","4h","5h","6h","7h","8h","9h","10h","Jh","Qh","Kh","Ah"
};
const vector<string> numToHandConversion = {
    "high Card", "pair", "twoPair", "three of a kind", "straight", "flush", "full house", "quads", "straight flush", "royal flush"
};
vector<vector<int>> suitedRange{
    {0,0,0,0,0,0,0,0,0,0,0,4,4},
    {0,4,0,0,0,0,0,0,0,0,0,4,4},
    {0,0,4,0,0,0,0,0,0,0,0,4,4},
    {0,0,0,4,0,0,0,0,0,0,0,4,4},
    {0,0,0,0,4,0,0,0,0,0,0,4,4},
    {0,0,0,0,0,4,0,0,0,0,4,4,4},
    {0,0,0,0,0,0,4,0,0,0,4,4,4},
    {0,0,0,0,0,0,0,4,0,4,4,4,4},
    {0,0,0,0,0,0,0,0,4,4,4,4,4},
    {0,0,0,0,0,0,0,4,4,4,4,4,4},
    {0,0,0,0,4,4,4,4,4,4,4,4,4},
    {4,4,4,4,4,4,4,4,4,4,4,4,4},
    {4,4,4,4,4,4,4,4,4,4,4,4,4}
};
vector<vector<int>> nonSuitedRange{
    {0,0,0,0,0,0,0,0,0,0,0,0,4},
    {0,4,0,0,0,0,0,0,0,0,0,0,4},
    {0,0,4,0,0,0,0,0,0,0,0,0,4},
    {0,0,0,4,0,0,0,0,0,0,0,4,4},
    {0,0,0,0,4,0,0,0,0,0,0,4,4},
    {0,0,0,0,0,4,0,0,0,0,0,4,4},
    {0,0,0,0,0,0,4,0,0,0,4,4,4},
    {0,0,0,0,0,0,0,4,0,0,4,4,4},
    {0,0,0,0,0,0,0,0,4,4,4,4,4},
    {0,0,0,0,0,0,0,0,0,4,4,4,4},
    {0,0,0,0,0,0,0,4,4,4,4,4,4},
    {0,0,0,4,4,4,4,4,4,4,4,4,4},
    {4,4,4,4,4,4,4,4,4,4,4,4,4}
};
vector<vector<int>> suitedRange2{
    {0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,4,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,4,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,4,0,0,0,4,0},
    {0,0,0,0,0,0,0,0,4,4,4,4,4},
    {0,0,0,0,0,0,0,0,4,4,4,4,4},
    {0,0,0,0,0,0,0,0,4,4,4,4,4},
    {0,0,0,0,0,0,0,4,4,4,4,4,4},
    {0,0,0,0,0,0,0,0,4,4,4,4,4}
};
vector<vector<int>> nonSuitedRange2{
    {0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,4,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,4,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,4,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,4,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,4,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,4,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,4,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,4,0,0,4,4},
    {0,0,0,0,0,0,0,0,0,4,4,4,4},
    {0,0,0,0,0,0,0,0,0,4,4,4,4},
    {0,0,0,0,0,0,0,0,4,4,4,4,4},
    {0,0,0,0,0,0,0,0,4,4,4,4,4}
};

void dealCards(vector<int>&, vector<int>&, int);
void distributeCards(vector<int>&,vector<int>&,vector<vector<int>>&);
pair<int,string> handValue(vector<int>, vector<int>);
int calculatePreFlopBets(vector<vector<int>>&, vector<vector<int>>&);
int calculateFlopBets(vector<vector<int>>&, vector<int>, vector<vector<int>>&);
int calculateRiverBets(vector<vector<int>>&, vector<int>, vector<vector<int>>&);
int calculateHandProfit(vector<vector<int>>,pair<int,string>,vector<int>,vector<int>,vector<vector<int>>);
int placeBets(vector<vector<int>>&);
int adjustBankStack(int&,int);

int main(){
    // vector<int> playerHandsOverWholeSim = {0,0,0,0,0,0,0,0,0,0};
    // vector<int> dealerHandsOverWholeSim = {0,0,0,0,0,0,0,0,0,0};
    vector<int> playerStks(NUMPLAYERS,2000);
    vector<vector<int>> playerBets(NUMPLAYERS, vector<int>(3,0));
    int totalWagered = 0, totalProfit = 0, busts = 0, totalHandsPlayed = 0;
    for(int i = 0;i<NUMNIGHTS;i++){
        int bankStack = 2*PUSHING, moneyWagered = 0;
        bool busted = false, belowMin = false;
        int j;
        for(j = 0;j<HOURSPERNIGHT*HANDSPERHOUR && !busted && !belowMin;j++){
            int betBeforeCards = placeBets(playerBets);
            vector<int> dealerHand;
            vector<int> table;
            vector<vector<int>> playerHands(NUMPLAYERS, vector<int>());
            distributeCards(dealerHand,table,playerHands);
            int preFlopBets = calculatePreFlopBets(playerHands,playerBets);
            int flopBets = calculateFlopBets(playerHands, table, playerBets);
            int riverBets = calculateRiverBets(playerHands, table, playerBets);
            moneyWagered += betBeforeCards + preFlopBets + flopBets + riverBets;
            pair<int,string> dH = handValue(table, dealerHand);
            //dealerHandsOverWholeSim[dH.first]++;
            // if(printing){
            //     cout << "-----HAND #" << i << "-----" << endl;
            //     cout << "dealers hand: " << numToCardConversion[dealerHand[0]] + numToCardConversion[dealerHand[1]] << "---" << numToHandConversion[dH.first] << endl;
            //     cout << "table: ";
            //     for(int j = 0;j<table.size();j++){
            //         cout << numToCardConversion[table[j]];
            //     }
            //     cout << endl << endl;
            // }
            int roundProfit = calculateHandProfit(playerHands,dH,table,playerStks,playerBets);
            int postRoundSituation = adjustBankStack(bankStack,roundProfit);
            if(postRoundSituation == 1){
                busted = true;
            }
            else if(postRoundSituation == 2){
                belowMin = true;
            }
        }
        totalWagered += moneyWagered;
        totalProfit += (bankStack - (PUSHING*2));
        totalHandsPlayed += j;
        if(busted){
            cout << "NIGHT #" << i << ": WE BUSTED" << endl;
            busts++;
        }
        else if(belowMin){
            cout << "NIGHT #" << i << ": BELOW MIN :(" << (bankStack - (PUSHING*2)) << endl;
        }
        else{
            cout << "NIGHT #" << i << ": " << (bankStack - (PUSHING*2)) << endl;
        }
    }
    cout << "--------OVERALL STATS---------\n";
    cout << "\tPROFIT: " << totalProfit << endl;
    cout << "\tHOURLY: " << totalProfit / (totalHandsPlayed/HANDSPERHOUR) << endl;
    cout << "\tMoney Wagered: " << totalWagered << endl;
    cout << "\tBusts: " << busts << endl;
    cout << "\tCouldntCover: " << couldntCover << endl;
    cout << "\tTotal Drop: " << (DROP*totalHandsPlayed) << endl;

    return 0;
}

int placeBets(vector<vector<int>>& playerBets){
    int toReturn = 0;
    for(int k = 0;k<NUMPLAYERS;k++){
        toReturn += playerBets[k][0] = 20;
        toReturn += playerBets[k][1] = 10;
    }
    return toReturn;
}

int adjustBankStack(int& bankStack,int roundProfit){
    if(bankStack < PUSHING){
        //case 1: bankrupt
        if(roundProfit < bankStack*(-1)){
            bankStack = 0;
            couldntCover++;
            return 1;
        }
        else{
            bankStack += roundProfit;
        }
    }
    else{
        //case royal :(
        if(roundProfit < PUSHING*(-1)){
            bankStack -= PUSHING;
            couldntCover++;
        }
        else{
            bankStack += roundProfit;
        }
    }
    bankStack -= DROP;
    if(bankStack < PUSHING/2) return 2;
    return 3;
}

int calculatePreFlopBets(vector<vector<int>>& playerHands, vector<vector<int>>& playerBets){
    int toReturn = 0;
    for(int j = 0;j<NUMPLAYERS;j++){
        bool suited = (playerHands[j][0]/13 == playerHands[j][1]/13);//check whether or not the hand is suited
        if(suited){
            playerBets[j][2] = playerBets[j][0]*suitedRange2[playerHands[j][0]%13][playerHands[j][1]%13];
            toReturn += playerBets[j][0]*suitedRange2[playerHands[j][0]%13][playerHands[j][1]%13];
        } 
        else{
            playerBets[j][2] = playerBets[j][0]*nonSuitedRange2[playerHands[j][0]%13][playerHands[j][1]%13];
            toReturn += playerBets[j][0]*nonSuitedRange2[playerHands[j][0]%13][playerHands[j][1]%13];
        }
    }
    return toReturn;
}

int calculateFlopBets(vector<vector<int>>& playerHands, vector<int> table, vector<vector<int>>& playerBets){
    int toReturn = 0;
    for(int j = 0;j<NUMPLAYERS;j++){
        if(playerBets[j][2] == 0){
            vector<int> temp = playerHands[j];
            temp.insert(temp.end(),table.begin(),table.begin()+3);
            vector<int> numsHand;
            for(int k = 0;k<temp.size();k++){
                numsHand.push_back(temp[k]%13);
            }
            vector<int> numsOnBoard;
            for(int k = 2;k<5;k++) numsOnBoard.push_back(numsHand[k]);
            //check for flush draw
            if(checkFlushDraw(temp)){
                playerBets[j][2] = 2*playerBets[j][0];
                toReturn+= 2*playerBets[j][0];
            } 
            //check for 2 pair or better
            if(handValue(temp, vector<int>({})).first >=2){
                playerBets[j][2] = 2*playerBets[j][0];
                toReturn+= 2*playerBets[j][0];
            } 
            //check for pair of 3's or better with 1 in hole
            if(checkPair(numsOnBoard) == "-1" && checkPair(numsHand) != "-1"){
                playerBets[j][2] = 2*playerBets[j][0];
                toReturn+= 2*playerBets[j][0];
            }
        }
    }
    return toReturn;
}

int calculateRiverBets(vector<vector<int>>& playerHands, vector<int> table, vector<vector<int>>& playerBets){
    int toReturn = 0;
    for(int j = 0;j<NUMPLAYERS;j++){
        if(playerBets[j][2] == 0){
            vector<int> temp = playerHands[j];
            temp.insert(temp.end(),table.begin(),table.end());
            vector<int> numsHand;
            for(int k = 0;k<temp.size();k++){
                numsHand.push_back(temp[k]%13);
            }
            vector<int> numsOnBoard;
            for(int k = 2;k<7;k++) numsOnBoard.push_back(numsHand[k]);
            //check for 2 pair or better
            if(handValue(temp, vector<int>({})).first >=1){
                playerBets[j][2] = playerBets[j][0];
                toReturn += playerBets[j][0];
            } 
            //check for pair of with 1 in hole
            else if(checkPair(numsOnBoard) == "-1" && checkPair(numsHand) != "-1"){
                toReturn += playerBets[j][0];
                playerBets[j][2] = playerBets[j][0];
            } 
        }
    }
    return toReturn;
}

int calculateHandProfit(vector<vector<int>> playerHands,pair<int,string> dH,vector<int> table,vector<int> playerStks,vector<vector<int>> playerBets){
    const vector<double> payoutBlind = {0,0,0,0,1,1.5,3,10,50,500};
    const vector<int> payoutTrips = {-1,-1,-1,3,4,7,8,30,40,50};
    int toReturn = 0;
    for(int j = 0;j<playerHands.size();j++){
        pair<int,string> pH = handValue(table, playerHands[j]);
        int stackChange  = 0;
        //playerHandsOverWholeSim[pH.first]++;
        if(printing) cout << "player #" << j << "hand = " << numToCardConversion[playerHands[j][0]] + numToCardConversion[playerHands[j][1]] << endl;
        if(playerBets[j][2] == 0){
            numFolds++;
            stackChange -= playerBets[j][0]*2;
            if(printing) cout << "Player folds with: " << numToHandConversion[pH.first] << endl;
        }
        else if(pH == dH){
            numDraws++;
            if(printing) cout << "Player pushes with: " << numToHandConversion[pH.first] << endl; 
        }
        else if(pH > dH){
            numLosses++;
            stackChange  += playerBets[j][2];
            if(dH.first > 0){
                stackChange  += playerBets[j][0];
            } 
            stackChange  += playerBets[j][0]*payoutBlind[pH.first];
            if(printing) cout << "Player wins with: " << numToHandConversion[pH.first] << endl;
        }
        else{
            numWins++;
            stackChange -= (playerBets[j][0]*2 + playerBets[j][2]);
            if(printing)  cout << "Player loses with: " << numToHandConversion[pH.first] << endl;
        }
        stackChange += playerBets[j][1]*payoutTrips[pH.first];
        playerStks[j] += stackChange;
        toReturn -= stackChange;
        if(printing){
            cout << "stack size: " << playerStks[j] << endl;
            cout << "stack change: " << stackChange << endl;
        }
        playerBets[j].clear();
        if(printing) cout << endl;
    }
    return toReturn;
}

string convertTieBreaker(string s){
    string toReturn = "";
    for(int i = 0;i<s.size();i++){
        toReturn += s[i] + '0';
    }
    return toReturn;
}

void distributeCards(vector<int>& dealerHand,vector<int>& table,vector<vector<int>>& playerHands){
    vector<int> deck;
    for(int j = 0;j<52;j++) deck.push_back(j);
    shuffle(begin(deck), end(deck), rng);
    dealCards(deck,table,5);
    dealCards(deck,dealerHand,2);
    for(int j = 0;j<NUMPLAYERS;j++) dealCards(deck, playerHands[j], 2);
}

void dealCards(vector<int>& deck, vector<int>& cards, int numCards){
    for(int i = 0;i<numCards;i++){
        int x = deck.back();
        cards.push_back(x);
        deck.pop_back();
    }
}

pair<int,string> handValue(vector<int> table, vector<int> holeCards){
    vector<int> sevenCardHand = table;
    sevenCardHand.insert(sevenCardHand.end(), holeCards.begin(), holeCards.end());
    vector<int> suitsHand = sevenCardHand;
    vector<int> numsHand = sevenCardHand;
    for(int i = 0;i<sevenCardHand.size();i++){
        suitsHand[i] /= 13;
        numsHand[i] %= 13;
    }
    sort(sevenCardHand.begin(),sevenCardHand.end());
    sort(suitsHand.begin(),suitsHand.end());
    sort(numsHand.begin(),numsHand.end());
    string tieBreaker;

    //check for straight flush return 8
    if((tieBreaker = checkStraightFlush(sevenCardHand)) != "-1"){
        if(tieBreaker[0] + '0'== ';') return make_pair(9, convertTieBreaker(tieBreaker));
        else return make_pair(8, convertTieBreaker(tieBreaker));
    }
    //check for quads return 7
    if((tieBreaker = checkQuads(numsHand)) != "-1") return make_pair(7, convertTieBreaker(tieBreaker));
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