#include<iostream>
#include<algorithm>
#include<vector>

using namespace std;

/*桁の順にソートを行っていく*/

//桁数を算出する
int digit(vector<int> N){
  int q=1;
  int r=1;
  int max_value = *max_element(N.begin(),N.end());
  while(r!=0){
    r = max_value / (pow(10,q));
    q++;
  }
  return q-1;
}

void show_data(vector<int> N){
  int len = N.size();
  for(int i=0; i<len; i++){
    cout << N[i] << " ";
  }
  cout << endl;
}

vector<int> radix_sort(vector<int> N){
  int i,j,k;
  int len = N.size();
  vector<int> rad(len);
  vector<int> y(len);
  int m=1;
  int cnt=1;
  int r= digit(N);//桁数
  cout << r << endl;
  
  while(cnt<=r){
    for(i=0;i<len;i++){
      rad[i] = (N[i]/m) % 10 ;//基数の取り出し
    }
      k=0;
      for(i=0;i<=9;i++){
	for(j=0; j<len; j++){
	  if(rad[j] == i){
	    y[k++]=N[j];//基数の小さいものを取り出してyに
	  }
	}	
      }
      for(i=0;i<len;i++) N[i] =y[i];
      show_data(N);
      m *=10;
      cnt +=1;
  }
  return N;
}


int main(){
  vector<int> N{10,44,52,21,69};
  int len = N.size();
  N = radix_sort(N);
  show_data(N);
  return 0;
}
