#include<iostream>

using namespace std;

/*一番小さい(大きい)ものを1番目と入れ替えて…を繰り返す. O(N^2)*/
int* selectionSort_ascend(int *N, int len){
  int i,j,min,tmp;

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

  }
  return N;
}

int* selectionSort_decend(int *N, int len){
  int i,j,max,tmp;

  for(i=0; i<len; i++){
    max = i;

    for(j=i+1; j<len ; j++){
      if(N[j] > N[max]){
	max = j;
      }
    }

    if(max != i){
      tmp = N[i];
      N[i] = N[max];
      N[max] = tmp;
    }

  }
  return N;
}


int main(){
  int N[5] = {6,2,3,4,5};
  int len = 5;
  int *ans = selectionSort_decend(N,len);

  for(int i=0; i<len; i++){
    cout << ans[i] << " ";
  }
  cout<<endl;
}
