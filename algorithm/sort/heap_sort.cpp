#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <time.h>
//http://capm-network.com/?tag=C%E8%A8%80%E8%AA%9E%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0-%E3%83%92%E3%83%BC%E3%83%97%E3%82%BD%E3%83%BC%E3%83%88

using namespace std;

void array_random_number(int N[], unsigned int size, unsigned int digit)
{
  int i;
  /* 起動毎に異なる乱数を発生させる */
  srand((unsigned int)time(NULL));
  for(i = 0; i < size; i++){
    N[i]=rand() % digit;
  }
}

void show_data(int N[], unsigned int len)
{
  for(int i = 0; i < len; i++){
    cout << N[i] << " ";
  }
  cout << endl;
}

void swap(int *i, int *j){
  int temp;
  temp = *i;
  *i   = *j;
  *j   = temp;
}

/*!
 * @brief          降順の半順序木（ヒープ）を作成する
 * @param[in/out]  array  整列する要素配列
 * @param[in]      left   根とみなす要素位置
 * @param[in]      right  配列上の子に該当する要素位置
 */

void down_heap(int N[], int left, int right)
{
  int child;
  int parent = left;
  int temp = N[left];  /* 根とみなす */
  int cl, cr;

  /* 子を持っている限り繰り返す */
  while(parent < (right + 1) / 2){
    cl = parent * 2 + 1;  /* 左の子 */
    cr = cl + 1;          /* 右の子 */

    /* 大きい方の子を選択する */
    if((cr <= right) && (N[cr] > N[cl])){
      child = cr;
    }else{
      child = cl;
    }

    /* 子の方が大きい場合には交換する */
    if(temp >= N[child]) break;
    N[parent] = N[child];
    parent = child;
  }
  N[parent] = temp;
}

void heapSort(int N[], unsigned int size)
{
  int i;

  /* 半順序木を構成する */
  for(i = (size - 1) / 2; i >= 0; i--){
    down_heap(N, i, size - 1);
  }
  cout << "[heap] :" ;
  show_data(N, size);

  /* ソート */
  for (i = size - 1; i > 0; i--) {
    /* 半順序木の根と末尾の要素を交換する */
    swap(&N[0], &N[i]);

    /* 根を外したデータ列で、半順序木を構成する */
    down_heap(N, 0, i - 1);
    cout << "[heap] :" ;
    show_data(N, i);
  }
}

int
main(void)
{
  int data[15];
  array_random_number(data, sizeof(data)/4, 100);

  cout << "[before]: ";
  show_data(data, sizeof(data)/4);

  heapSort(data, sizeof(data)/4);

  cout << "[after]: ";
  show_data(data, sizeof(data)/4);

  return 0;
}
