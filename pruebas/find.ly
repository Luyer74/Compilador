main {
  int : i = 0;
  int : size;
  int : arr[100];
  int : ans = 0;

  fill("random", arr);
  size = len(arr);
  out("Looking for 101/n");
  arr[72] = 101;
  while(i < size){
    if(arr[i] == 101){
      ans = i;
    }
    i = i + 1;
  }
  out("found in index: ", ans);
}