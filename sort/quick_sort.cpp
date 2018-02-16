#include<iostream>
#include<vector>

using namespace std;

/*中央の値との大小で並び替えののち、左右でソート*/

void show_data(vector<int>N){
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

vector<int> quickSort(vector<int>N,int left, int right){
  int i,j;
  int pivot;
  i=left;
  j=right;
  pivot = N[(left+right)/2];

  while(1){
    while(N[i] < pivot){
      i++;
    }
    while(pivot < N[j]){
      j--;
    }
    if(i>=j) break;

    swap(N[i],N[j]);
    i++;
    j--;
    
  }
  show_data(N);

  if(left < i-1){//基準値の左に2つ以上の要素があれば
    N = quickSort(N,left, i-1);//左の配列をquick sort
  }
  if(right > j+1){//基準値の右に2つ以上の要素があれば
    N = quickSort(N,j+1,right);//右の配列をquick sort
  }
  return N;
}


int main(){
  vector<int> N{1,4,5,2,10,6,7};
  N = quickSort(N,0,N.size()-1);
  show_data(N);
  return 0;	
		
}
