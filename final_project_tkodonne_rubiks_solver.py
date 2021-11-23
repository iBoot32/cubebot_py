"""
===============================================================================
ENGR 13300 Fall 2021

Program Description: Final Project: A Rubik's Cube solver using buffers and iterative piece solving
    

Assignment Information
    Assignment:     Python Final Individual Project Fall 2021
    Author:         Tom O'Donnell, tkodonne@purdue.edu
    Team ID:        LC3 - 03

Contributor:   
    
    My contributor(s) helped me:
    [] understand the assignment expectations without
        telling me how they will approach it.
    [] understand different ways to think about a solution
        without helping me plan my solution.
    [] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""
import math
from datetime import datetime

solved = False
cube_arr = []
setup = ""
sticker = 0
undo = ""
stick = ""

#define which stickers on cube belong to which pieces
pieces = {
    0: [0, 4, 17],
    1: [1, 13, 16],
    2: [2, 12, 9],
    3: [3, 5, 8],
    4: [20, 6, 11],
    5: [21, 15, 10],
    6: [22, 14, 19],
    7: [23, 7, 18]
    }

solved_cube = [
    'W','W','W','W','O','O','O','O','G','G','G','G','R','R','R','R','B','B','B','B','Y','Y','Y','Y']

# define which stickers we are swapping with based on the input sticker
# array is broken up into 6 layers, each representing a face of the cube
# and 4 sub-layers representing each piece on a layer
# so if we shoot to the 3rd sticker, we access swaps[2] since arrays are 0-indexed
swaps = [
    
    [], [1, 16, 13], [2, 12, 9], [3, 8, 5],
    [], [5, 3, 8], [6, 11, 20], [7, 23, 18],
    [8, 5, 3], [9, 2, 12], [10, 15, 21], [11, 20, 6],
    [12, 9, 2], [13, 1, 16], [14, 19, 22], [15, 21, 10],
    [16, 13, 1], [], [18, 7, 23], [19, 22, 14],
    [20, 6, 11], [21, 10, 15], [22, 14, 19], [23, 18, 7],
    
    ]


def check_if_solved(arr):
    
    for piece in (pieces):
        for sticker in (0, 2):
            if (arr[pieces[piece][sticker]] != solved_cube[pieces[piece][sticker]]):
                # if any sticker om the cube does not match sticker in same location of a solved cube
                # then the cube must be unsolved
                return False
                
            
def handle_twisted_buffer(arr):
    global sticker
    global cube_arr
    
    # if we're here, the buffer is either twisted in place or solved
    # how do we fix this?
    # the way i chose is to shoot the buffer to some random unsolved piece
    # so we have an unsolved piece in the buffer again, and continue as normal.
    
    for stick in range(0,24):
        if solved_cube[stick] != cube_arr[stick]:
            break;
            
    sticker = stick
    # voodoo magic time
    # we know which sticker we can shoot to, since we just iterated to find an unsolved one
    # but since we deal with solving pieces, we need to find a piece containing that sticker
    # if we take the ceil of the sticker / 4, we are given a piece containing that sticker, which is what we need
    pieceindexes = pieces[math.ceil(sticker / 4)]
    
    solve_piece(cube_arr[pieceindexes[0]] + cube_arr[pieceindexes[1]] + cube_arr[pieceindexes[2]], cube_arr)
        
    
    return
    
def update_cube_state(sticker):
    
    cube_arr[0], cube_arr[swaps[sticker][0]] = cube_arr[swaps[sticker][0]], cube_arr[0]
    cube_arr[4], cube_arr[swaps[sticker][1]] = cube_arr[swaps[sticker][1]], cube_arr[4]
    cube_arr[17], cube_arr[swaps[sticker][2]] = cube_arr[swaps[sticker][2]], cube_arr[17]
    
    return
    
        
    
def solve_piece(p, arr):
    global cube_arr
    # take a certain piece on the cube as input and determine where it belongs
    # determines the setup moves required to move the sticker to the swap location
    global setup
    global undo
    global sticker

    
    
    if "W" in p and "O" in p and "B" in p:
        # buff solved, however
        # we verified cube is not solved so that means 
        # we have a solved buffer yet other pieces not solved
        handle_twisted_buffer(arr)
        return
    elif "W" in p and "R" in p and "B" in p:
    # change this to an array of setups and undos so can access
        if p[0] == "W":
            setup = "R D'"
            undo = "D R'"
            sticker = 1
        elif p[0] == "R":
            setup = "R2"
            undo = "R2'"
            sticker = 13
        else:
            setup = "R' F"
            undo = "F' R"
            sticker = 16
    elif "W" in p and "R" in p and "G" in p:
        if p[0] == "W":
            setup = "F"
            undo = "F'"
            sticker = 2
        elif p[0] == "R":
            setup = "R'"
            undo = "R"
            sticker = 12
        else:
            setup = "F2 D"
            undo = "D' F2"
            sticker = 9
    elif "W" in p and "O" in p and "G" in p:
        if p[0] == "W":
            setup = "L D L'"
            undo = "L D' L"
            sticker = 3
        elif p[0] == "O":
            setup = "F2"
            undo = "F2"
            sticker = 5
        else:
            setup = "F' D"
            undo = "D' F"
            sticker = 8
    elif "Y" in p and "O" in p and "G" in p:
        if p[0] == "Y":
            setup = "F'"
            undo = "F"
            sticker = 20
        elif p[0] == "O":
            setup = "D2 R";
            undo = "R' D2"
            sticker = 6
        else:
            setup = "D"
            undo = "D'"
            sticker = 11
    elif "Y" in p and "O" in p and "B" in p:
        if p[0] == "Y":
            setup = "D F'"
            undo = "F D'"
            sticker = 23 
        elif p[0] == "O":
            setup = "D2";
            undo = "D2"
            sticker = 7
        else:
            setup = "D' R"
            undo = "R' D"
            sticker = 18
    elif "Y" in p and "G" in p and "R" in p:
        if p[0] == "Y":
            setup = "D' F'"
            undo = "F D"
            sticker = 21
        elif p[0] == "G":
            setup = "F D";
            undo = "D' F'"
            sticker = 10
        else:
            setup = ""
            undo = ""
            sticker = 15
    elif "Y" in p and "R" in p and "B" in p:
        if p[0] == "Y":
            setup = "D2 F'"
            undo = "F D2"
            sticker =  22
        elif p[0] == "R":
            setup = "R";
            undo = "R'"
            sticker = 14
        else:
            setup = "D'"
            undo = "D"
            sticker = 19
       
    # move piece to swap location, swap buffer and piece, undo setup moves.
    print(f'  {setup} R U\' R\' U\' R U R\' F\' R U R\' U\' R\' F R {undo}')
    update_cube_state(sticker)
    
    

def solve_cube(arr):
    global sticker
    global cube_arr
    
    print("")    
    print("   solution to your cube:")
    print("")
    
    #if cube not solved
    while(check_if_solved(arr) == False):
        #print('Cube not solved, solving')
        #print(arr)
        #print(arr[pieces[0][0]] + arr[pieces[0][1]] + arr[pieces[0][2]])
        
        #while(check_if_solved(arr) == False):
            # now we begin solving
            # this solving method is basically the Old Pochmnann method:
            # designate the top, back, left piece as a buffer through which all unsolved pieces will pass
            # begin by solving just the sticker in the buffer using "setup + Y perm + undo_setup".
            # (this swaps just that one corner with just one other)
            # so simply loop solving the buffer until all corners are solved
            
        solve_piece(arr[pieces[0][0]] + arr[pieces[0][1]] + arr[pieces[0][2]], arr)
        
    endtime = datetime.now()
    elapsed = endtime - starttime
    print("")
    print(f'   cube solved in {elapsed.microseconds / 1000000} seconds')
    print("   py_cubebot by tom o'donnell")
    print("   written for engr133 at purdue university")

def main():
    global cube_arr
    global starttime
    
    starttime = datetime.now()
    
    cube_str = input("Input cube state (type \"help\" for help): ")
    if cube_str == "help":
        print(f'\n ORDER TO INPUT YOUR CUBE: ')
        print(f' Example: WWWWOOOOGGGGRRRRBBBBYYYY')
        
        #print diagram of cube showing in what order to input cube's stickers
        print(r"""
		                 _________________ 
		                 |       |       |
		                 |   1   |   2   |
		                 |-------|-------|
		                 |   4   |   3   |
		                 |_______|_______|
    _________________    _________________    _________________    _________________ 
    |       |       |    |       |       |    |       |       |    |       |       |
	|   5   |   6   |    |   9   |   10  |	  |   13  |   14  |    |   17  |   18  |
	|-------|-------|    |-------|-------|	  |-------|-------|    |-------|-------|
	|   8   |   7   |    |   12  |   11  |	  |   16  |   15  |    |   20  |   19  |
	|_______|_______|    |_______|_______|	  |_______|_______|    |_______|_______|
                         _________________ 
		                 |       |       |
		                 |   21  |   22  |
		                 |-------|-------|
		                 |   24  |   23  |
		                 |_______|_______|


                """)
    else:
        #example could be WWWWOOOOGGGGRRRRBBBBYYYY, 
        #split cube_str by letters to get array with each element being 1 sticker
        cube_arr = [sticker for sticker in cube_str]
        
        #cube array is set up, now we call solving function while passing cube array
        solve_cube(cube_arr)


if __name__ == "__main__":
    main()