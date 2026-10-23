#include <bits/stdc++.h>
using namespace std;
int main(){ int n; cin>>n; int best=INT_MIN, cur=0; for(int i=0;i<n;i++){ int x; cin>>x; cur=max(x,cur+x); best=max(best,cur);} cout<<best<<"\n"; }
