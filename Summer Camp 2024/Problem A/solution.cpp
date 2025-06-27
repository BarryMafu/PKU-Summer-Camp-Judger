#include<iostream>
#include<vector>

using namespace std;

class Solution {
    public:
        int calculate_coins(int k){
            int coins = 0;  // 金币数量
            int days = 0;   // 天数
            int i;          // 轮数，第i轮持续i天
            for(i = 1; days < k; i++){
                days += i;
                coins += i * i;
            }
            coins -= (days - k) * (i - 1); // 减去多余的金币数量
            return coins;
        }
};

int main(){
    Solution solution = Solution();

    int k;
    cin >> k;
    cout << solution.calculate_coins(k) << endl;

    return 0;
}