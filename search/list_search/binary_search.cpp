#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;

/*ソート済み配列に対して行う*/

//key:探す値
int binary_search(vector<int>N, int key, int imin, int imax){
  if(imax < imin) return 10000;
  else{
    int imid = imin + (imax -imin)/2;
    if(N[imid] > key){
      return binary_search(N,key,imin,imid-1);
    }
    else if(N[imid] < key){
      return binary_search(N,key,imid+1,imax);
    }
    else{
      return imid;
    }
  }
}


int main(){
  //vector<int>N{3,1,4,6,9,10,2};
  //sort(N.begin(),N.end());
  vector<int>N{1,2,3,4,6,9,10};

  int ans = binary_search(N,10,0,N.size()-1);
  if(ans != 10000){
    cout << "index:"<< ans <<endl;
  }
  else{
    cout << "can't find" << endl;
  }
  
  return 0;
}
