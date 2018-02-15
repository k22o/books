#include<iostream>
#include<vector>

using namespace std;

/*隣同士を比較して並び替えるアルゴリズム。O(N^2)*/

void show_data(vector<int> N){

  for(int i=0; i<N.size(); i++){
    cout << N[i] << " ";
  }
  cout << endl;
}

vector<int> bubbleSort(vector<int> N){
  int len = N.size();
  int i,j,tmp;
  for (i=0;i<len;i++){
    for(j=len-1; j>i;j--){
	if(N[j] < N[j-1]){
	  tmp = N[j];
	  N[j] = N[j-1];
	  N[j-1] = tmp;
	}
	show_data(N);
    }
  }
  return N;
}


int main(){
  vector<int> N{6,2,3,4,5};
  int len = N.size();
  N = bubbleSort(N);
  show_data(N);

  return 0;
}
