func int : fibo(int : n){
  int : a = 0;
  int : b = 1;
  int : c;
  int : i = 2;
  if(n <= 1){
    ret n;
  }
  while(i <= n){
    c = a + b;
    a = b;
    b = c;
    i = i + 1;
  }
  ret b;
}

main {
  out(fibo(9));
}