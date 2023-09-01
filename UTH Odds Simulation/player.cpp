#include <vector>

using namespace std;

class player {
    public:
        int getPreflopAction(vector<int>);
    private:
        vector<vector<int>> preflopRange;
};

int player::getPreflopAction(vector<int> hand){
    return preflopRange[hand[0]][hand[1]];
}
