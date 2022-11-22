func int : fact(int : n){
  if(n == 0){
    ret 1;
  }
  ret n * fact(n - 1);
}

main{
  out(fact(5));
}