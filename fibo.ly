func int : fibo (int : x){
  if(x <= 1){
    ret x;
  }
  ret fibo(x - 1) + fibo(x - 2);
}

main{
  int : ans;
  ans = fibo(20);
  out(ans);
}