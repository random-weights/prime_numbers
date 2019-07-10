# Prime Numbers

Prime numbers are those that are divisible ONLY by themselves and **1**.

If we want to find if **n** is a prime number, we have to check divisibility of **n** by all numbers between **2** and **n-1**.

#### For ex. is **17** a prime number? (Yes)

Check divisibility of **17** by all numbers between **2** and **16**.
>Is it really necessary to check 11,12,13,14,15,16?
>No, you need to check only upto ceil(17/2)