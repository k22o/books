#include<iostream>

using namespace std;

/*適した位置に挿入していく。O(n^2)*/

//表示の関数
void show_data(int N[], int len){
  for(int i=0; i<len; i++){
    cout << N[i] << " ";
  }
  cout << endl;
}

//入れ替えの関数
void swap(int *p1, int *p2){
  int tmp;
  tmp = *p1;
  *p1 = *p2;
  *p2 = tmp;  
}

//昇順
void insertSort_ascend(int N[], int len){
  int i,j;
  for(i=1;i<len;i++){
    j=i;
    while(j>0 && (N[j-1] > N[j])){
	swap(&N[j-1], &N[j]);
	j -= 1;
	show_data(N,len);
    }
  }
}

//降順
void insertSort_decend(int N[], int len){
  int i,j;
  for(i=1;i<len;i++){
    j=i;
    while(j>0 && (N[j-1] < N[j])){
	swap(&N[j-1], &N[j]);
	j -= 1;
	show_data(N,len);

    }
  }
}




int main(){
  int N[5] = {4,10,5,1,8};
  int len = 5;
  insertSort_decend(N,len);
  show_data(N,len);
}
