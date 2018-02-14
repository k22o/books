#include<iostream>

using namespace std;

/*隣同士を比較して並び替えるアルゴリズム。O(N^2)*/
int* bubbleSort_ascend(int *N, int len){
  int i,j,tmp;
  for (i=0;i<len;i++){
    for(j=len-1; j>i;j--){
	if(N[j] < N[j-1]){
	  tmp = N[j];
	  N[j] = N[j-1];
	  N[j-1] = tmp;
	}
      }
    }
  return N;
}

int* bubbleSort_decend(int *N, int len){
  int i,j,tmp;
  for (i=0;i<len;i++){
    for(j=len-1; j>i;j--){
	if(N[j] > N[j-1]){
	  tmp = N[j];
	  N[j] = N[j-1];
	  N[j-1] = tmp;
	}
      }
    }
  return N;
}


int main(){
  int N[5] = {6,2,3,4,5};
  int len = 5;
  int *ans = bubbleSort_ascend(N,len);

  for(int i=0; i<len; i++){
    cout << ans[i] << " ";
  }
  cout<<endl;

}
