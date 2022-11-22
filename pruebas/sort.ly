main {
  int : arr[100];
  int : i = 0;
  int : j = 0;
  int : size;
  int : temp;

  fill("random", arr);
  size = len(arr);

  out("unsorted/n");
  while(i < size){
    out(arr[i]);
    i = i + 1;
  }

  i = 0;
  while(i < size - 1){
    j = 0;
    while(j < size - i - 1){
      if(arr[j] > arr[j + 1]){
        temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
      }
      j = j + 1;
    }
    i = i + 1;
  }
  out("/n");
  out("sorted/n");
  i = 0;
  while(i < size){
    out(arr[i]);
    i = i + 1;
  }
}