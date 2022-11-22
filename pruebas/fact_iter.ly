main {
  int : fact = 1;
  int : n = 5;
  while(n > 0){
    fact = fact * n;
    n = n - 1;
  }
  out(fact);
}