function change = algorithm4(A, B, C, sourcerack, targetrack, sku)
C2 = C;
C2(sku,sourcerack) = 0;
C2(sku,targetrack) = 1;
B2 = A * C2;
change = sum(sum(B2>0)) - sum(sum(B>0));
