main {
  int : mat[2,4];
  int : arr[3];
  int : i = 0;
  int : j = 0;
  int : cont = 1;
  arr[2] = 1;
  while(i < 2){
    j = 0;
    while(j < 4){
      mat[i, j] = cont;

      j = j + 1;
      cont = cont + 1;
    }
    i = i + 1;
  }
  i = 0;
  j = 0;
  while(i < 2){
    j = 0;
    while(j < 4){
      out(mat[i, j]);
      j = j + 1;
    }
    out("/n");
    i = i + 1;
  }
  out(mat[arr[2], 2]);
}