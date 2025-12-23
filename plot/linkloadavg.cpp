#include<iostream>
using namespace std;

int main(){
	int cnt = 0;
	double x;
	double sum = 0;
	while(cin>>x){
		cnt += 1;
		sum += x;
	}
	cout<<cnt<<" "<<sum / cnt<<'\n';
	return 0;
}
