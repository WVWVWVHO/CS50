import cs50
import sys

def main():
    # if there are more or less than two arguments in the command line, return ERROR
    if len(sys.argv) != 2:
        print("ERROR")
        exit(1)
        
    # change the inputted variable from a string to an integer  
    k = int(sys.argv[1])
    
    # ask user to input the plaintext
    print("plaintext: ", end="")
    p = cs50.get_string()
    
    # convert the plaintext to ciphertext
    print("ciphertext: ", end="")
    for i in range(len(p)):
        
        # if the character is a letter convert it, using k
        if str.isalpha(p[i]):
            if str.isupper(p[i]):
                c = ord(p[i]) - 65
                c = (c+k) % 26
                c = c + 65
                print(chr(c), end="")
            
            else:
                c = ord(p[i]) - 97
                c = (c+k) % 26
                c = c + 97
                print(chr(c), end="")
        
        # if the character is not a letter just return it
        else:
            print(p[i], end="")
            
    print()
    exit(0)
    
if __name__ == "__main__":
    main()