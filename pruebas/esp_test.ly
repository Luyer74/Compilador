main {
  int : arr[100];
  float : ans;
  fill("random", arr);

  ans = mean(arr);
  out(ans);
  ans = std(arr);
  out(ans);
  ans = min(arr);
  out(ans);
  ans = max(arr);
  out(ans);
}