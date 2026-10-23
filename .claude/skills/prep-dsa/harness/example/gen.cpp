#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){ unsigned seed=atoi(argv[1]); int n=atoi(argv[2]); mt19937_64 r(seed*1000003ULL+n);
  long long M = n>1000 ? 1000000000LL : (seed%2 ? 5 : 1000000000LL);   // tiny values on small cases to force negatives/ties
  printf("%d\n",n); for(int i=0;i<n;i++){ long long v=(long long)(r()%(2*M+1))-M; if(n>1000) v = (long long)(r()%(M+1)); printf("%lld%c",v,i+1<n?' ':'\n'); } }
