import kociemba





''''
             |------------|
             |-U1--U2--U3-|
             |------------|
             |-U4--U5--U6-|
             |------------|
             |-U7--U8--U9-|
|------------|------------|------------|------------|
|-L1--L2--L3-|-F1--F2--F3-|-R1--R2--R3-|-B1--B2--B3-|
|------------|------------|------------|------------|
|-L4--L5--L6-|-F4--F5--F6-|-R4--R5--R6-|-B4--B5--B6-|
|------------|------------|------------|------------|
|-L7--L8--L9-|-F7--F8--F9-|-R7--R8--R9-|-B7--B8--B9-|
|------------|------------|------------|------------|
             |-D1--D2--D3-|
             |------------|
             |-D4--D5--D6-|
             |------------|
             |-D7--D8--D9-|
             |------------|

             
U - Orange
L - White
F - Green
R - Yellow
B - Blue
D - Red


Ask user to take pictures of each face based on the centers, 
since centers don't change; makes mapping easier

Map each face color to the corresponding ULFRBD value

Systems:

- mapping system (image color to location of face)
- image processor (take photo and extract color data)
- pass to k solver
- output graphics


'''



print(kociemba.solve('UUUUUUUUUFFFRRRRRRLLLFFFFFFDDDDDDDDDBBBLLLLLLRRRBBBBBB'))

# U R F D L B - Order to type pieces out for a scramble string