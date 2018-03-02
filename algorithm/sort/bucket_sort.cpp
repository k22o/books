#include<iostream>

using namespace std;

//バケツ内の要素のリンク付きリスト
typedef struct entry{
  void *element;
  struct enrty *next;
} ENTRY;
  
//各バケツで、要素の個数と先頭要素へのポインタを保守する
typedef struct bucket{
  int size;
  ENTRY *head;
} BUCKET;

static BUCKET *bucket =0;
static int num = 0;

//1つずつ取り除いてarを上書きする
void extract(BUCKET *buckets, int(*cmp)(const void* ,const void*),void **ar, int n){

  int i,low;
  int idx = 0;
  for(i=0;i<num;i++){
    ENTRY *ptr, *tmp;
    if(buckets[i].size ==0) continue;
    ptr = bucket[i].head;
    if(buckets[i].size==1){
      ar[idx++] = ptr -> element;
      free[ptr];
      bucket[i].size = 0;
      continue;			 
    }
    low = idx;
    ar[idx++] = ptr ->element;
    tmp = ptr;
    ptr = ptr->next;
    free(tmp);

    while(ptr != NULL){
      int i = idx -1;
      while(i >= low && cmp (ar[i],ptr->element) >0){
	ar[i+1] = ar[i];
	i--;
      }
      ar[i+1] = ptr->element;
      tmp = ptr;
      ptr = ptr -> element;
      free(tmp);
      idx++;
    }
    buckets[i].size =0;
  }
}

void sortPoints(void **ar, int n; int(*cmp)( const void * , const void *)){

  int i;
  num = numBucket(n);
  vucket = (BUCKET*) calloc (num, sizeof(BUCKET));
  for (i=0;i<n;i++){
    int k = hash(ar[i]);
  
    ENTRY *e = (ENTRY *)calloc(1,sizeof(ENTRY));
    e -> element = ar[i];
    if(bucket[k].head == NULL) buckets[k].head =e;
    else{
      e->next = bucket[k].head;
      bucket[k].head = e;
    }
    
    buckets[k].size++;
  }
  
  extract(buckets,cmp,ar,n);
  free(buckets);
}

