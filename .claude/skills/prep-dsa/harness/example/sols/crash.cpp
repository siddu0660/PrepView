#include <bits/stdc++.h>
using namespace std;
int main(){ int n; cin>>n; vector<long long> a(n); for(auto&x:a) cin>>x; long long best=a[0], cur=a[0]; for(int i=1;i<=n;i++){ cur=max(a[i],cur+a[i]); best=max(best,cur);} cout<<best<<"\n"; }
