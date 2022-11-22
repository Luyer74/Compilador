main {
  int : mat1[2,3];
  int : mat2[3,2];
  int : res[2,2];
  int : i = 0;
  int : j = 0;
  int : k = 0;

  mat1[0,0] = 1;
  mat1[0,1] = 2;
  mat1[0,2] = 3;
  mat1[1,0] = 4;
  mat1[1,1] = 5;
  mat1[1,2] = 6;
  mat2[0,0] = 10;
  mat2[0,1] = 11;
  mat2[1,0] = 20;
  mat2[1,1] = 21;
  mat2[2,0] = 30;
  mat2[2,1] = 31;

  while(i < 2){
    j = 0;
    while(j < 2){
      res[i, j] = 0;
      k = 0;
      while(k < 3){
        res[i, j] = res[i, j] + mat1[i, k] * mat2[k, j];
        k = k + 1;
      }
      j = j + 1;
    }
    i = i + 1;
  }

  i = 0;
  j = 0;

  while(i < 2){
    j = 0;
    while(j < 2){
      out(res[i, j]);
      j = j + 1;
    }
    out("/n");
    i = i + 1;
  }
}