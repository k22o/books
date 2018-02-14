#include<iostream>

using namespace std;

/*隣同士を比較して並び替えるアルゴリズム。O(N^2)*/

void show_data(int N[], int len){

  for(int i=0; i<len; i++){
    cout << N[i] << " ";
  }
  cout << endl;
}

void bubbleSort_ascend(int *N, int len){
  int i,j,tmp;
  for (i=0;i<len;i++){
    for(j=len-1; j>i;j--){
	if(N[j] < N[j-1]){
	  tmp = N[j];
	  N[j] = N[j-1];
	  N[j-1] = tmp;
	}
	show_data(N,len);
    }
  }
}

void bubbleSort_decend(int *N, int len){
  int i,j,tmp;
  for (i=0;i<len;i++){
    for(j=len-1; j>i;j--){
	if(N[j] > N[j-1]){
	  tmp = N[j];
	  N[j] = N[j-1];
	  N[j-1] = tmp;
	}
	show_data(N,len);
      }
    }
}

int main(){
  int N[5] = {6,2,3,4,5};
  int len = 5;
  bubbleSort_ascend(N,len);
  show_data(N,len);

  return 0;
}
