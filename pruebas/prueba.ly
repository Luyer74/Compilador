func int : duplicate(int : x){
  ret x * 2;
}


main {
  int : a[10];
  int : i = 0;
  out("Hola mundo!");

  fill("arange", a);

  while(i < len(a)){
    out(duplicate(a[i]));
    i = i + 1;
  }
}