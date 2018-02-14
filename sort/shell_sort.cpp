#include<iostream>

using namespace std;

/*要素を分割して、insert sortを行う。*/

void show_data(int N[], int len){

  for(int i=0; i<len; i++){
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
void insertSort(int N[], int gap, int len){
  int i,j,tmp;

  for(i=gap; i<len; i++){
    for(j= i-gap; j>=0 ; j -=gap){
      if(N[j] <= N[j+gap]) break;
      else{
	swap(&N[j],&N[j+gap]);
	show_data(N,len);
      }
    }
  }
}

//シェルソート
void shellSort(int N[], int len){
  int gap;
  for(gap = len/2; gap>0 ; gap/=2){
    insertSort(N,gap,len);
  }
}

int main(){

  int N[] = {5,10,6,9,1,3,2,11};
  int len = 8;
  shellSort(N,len);
  show_data(N,len);
  return 0;
}
