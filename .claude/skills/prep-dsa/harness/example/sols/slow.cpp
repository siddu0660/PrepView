#include <bits/stdc++.h>
using namespace std;
int main(){ int n; cin>>n; vector<long long> a(n); for(auto&x:a) cin>>x; long long best=LLONG_MIN; for(int i=0;i<n;i++){ long long s=0; for(int j=i;j<n;j++){ s+=a[j]; best=max(best,s);} } cout<<best<<"\n"; }
