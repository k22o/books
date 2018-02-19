#include<iostream>
#include<vector>

using namespace std;

/*線形探索は、検索のアルゴリズムの一つ。 リストや配列に入ったデータに対する検索を行うにあたって、 先頭から順に比較を行い、それが見つかれば終了する。
n個のデータからm個のデータを検索する場合、時間計算量はO(nm) 、空間計算量はO(1) である。(wikipedia)*/

int find(vector<int> N, int value){
  for(int i=0;i<N.size();i++){
    if(N[i]==value) return i;
  }
  return -1;
}

int main(){
  vector<int> N{2,4,5,7,1,3,6};
  int ans = find(N,10);
  if( ans != -1)  cout << "index:"<< ans << endl;
  else cout << "can't find" << endl;
  
  return 0;
}
