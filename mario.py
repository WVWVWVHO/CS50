import cs50

def main():
    # ask for an height between the 1 and 23
    while True:
        print("Height: ")
        height = cs50.get_int()
        if height > 0 and height < 23:
            break

    # print the whole piramid
    for i in range(height):

        # print the spaces before the #'s  
        for k in range(height-i+1):
            print(" ", end="")

        # print first #'s
        for j in range(i+1):
            print("#", end="")
            
        # print the two spaces        
        print("  ", end="")

        # print the last #'s            
        for z in range(i+1):
            print("#", end="")

        # print a last return            
        print()

if __name__ == "__main__":
    main()