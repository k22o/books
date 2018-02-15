#include<iostream>
#include<stdlib.h>

using namespace std;

/*2つに分割して整列させて結合する。O(NlogN)*/
//https://www.codereading.com/algo_and_ds/algo/merge_sort.html


void mergeSort(int N[], int tmp[],int len);
void m_sort(int N[],int tmp[], int left, int right);
void merge(int N[], int tmp[], int left, int mid, int right);


void show_data(int N[], int len){

  for(int i=0; i<len; i++){
    cout << N[i] << " ";
  }
  cout << endl;
}

void mergeSort(int N[], int tmp[],int len){
  m_sort(N, tmp, 0, len - 1);
}

void m_sort(int N[], int tmp[], int left, int right){
  int mid;
  if (right > left){
      mid = (right + left) / 2; /* 配列を分割する位置 */
      m_sort(N, tmp, left, mid);
      m_sort(N, tmp, mid+1, right);
      merge(N, tmp, left, mid+1, right);
    }
}

void merge(int N[], int tmp[], int left, int mid, int right){
  int i, left_end, num_elements, tmp_pos;

  left_end = mid - 1;
  tmp_pos = left;
  num_elements = right - left + 1; /* 配列の要素数 */

  /* 2つのリストに要素が残っている */
  while ((left <= left_end) && (mid <= right)){
    if (N[left] <= N[mid]){
      tmp[tmp_pos] = N[left];
      tmp_pos = tmp_pos + 1;
      left = left +1;
    }
    else{
      tmp[tmp_pos] = N[mid];
      tmp_pos = tmp_pos + 1;
      mid = mid + 1;
    }
  }

  /* 左側のリスト */
  while (left <= left_end){
    tmp[tmp_pos] = N[left];
    left = left + 1;
    tmp_pos = tmp_pos + 1;
  }
  /* 右側のリスト */
  while (mid <= right){
    tmp[tmp_pos] = N[mid];
    mid = mid + 1;
    tmp_pos = tmp_pos + 1;
  }

  /* 昇順に整列するようひとつのリストにまとめる */
  for (i=0; i <= num_elements; i++) {
    N[right] = tmp[right];
    right = right - 1;
  }
}

int main(){
  int i;
  int N[] = {6,8,3,1,2,6,11,17,15,0};
  int len = 8;
  int tmp[len];

  mergeSort(N, tmp, len);
  show_data(N,len);

  return 0;
}
