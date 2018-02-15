#include<iostream>
#include<vector>

using namespace std;

/*一番小さい(大きい)ものを1番目と入れ替えて…を繰り返す. O(N^2)*/

void show_data(vector<int> N){
  for(int i=0; i<N.size(); i++){
    cout << N[i] << " ";
  }
  cout << endl;
}


vector<int> selectionSort(vector<int> N){
  int i,j,min,tmp;
  int len = N.size();

  for(i=0; i<len; i++){
    min = i;

    for(j=i+1; j<len ; j++){
      if(N[j] < N[min]){
	min = j;
      }
    }

    if(min != i){
      tmp = N[i];
      N[i] = N[min];
      N[min] = tmp;
    }
    show_data(N);
  }
  return N;
}

int main(){
  vector<int> N{6,2,3,4,5};
  int len = N.size();
  N = selectionSort(N);
  show_data(N);

  return 0;
}
