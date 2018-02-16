#include<iostream>
#include<vector>

using namespace std;

/*要素を分割して、insert sortを行う。*/

void show_data(vector<int> N){
  for(int i=0; i<N.size(); i++){
    cout << N[i] << " ";
  }
  cout << endl;
}

void swap(int *p1, int *p2){
  int tmp;
  tmp = *p1;
  *p1 = *p2;
  *p2 = tmp;
}  

//挿入ソート
vector<int> insertSort(vector<int> N, int gap){
  int i,j,tmp;
  int len = N.size();
  for(i=gap; i<len; i++){
    for(j= i-gap; j>=0 ; j -=gap){
      if(N[j] <= N[j+gap]) break;
      else{
	swap(&N[j],&N[j+gap]);
	show_data(N);
      }
    }
  }
  return N;
}

//シェルソート
vector<int> shellSort(vector<int> N){
  int len = N.size();
  int gap;
  for(gap = len/2; gap>0 ; gap/=2){
    N = insertSort(N,gap);
  }
  return N;
}

int main(){

  vector<int> N {5,10,6,9,1,3,2,11};
  int len = N.size();
  N = shellSort(N);
  show_data(N);
  return 0;
}
