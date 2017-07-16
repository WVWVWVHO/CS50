import cs50
import sys

def main():
    # if there are more or less than two arguments in the command line, return ERROR
    if len(sys.argv) != 2:
        print("ERROR")
        exit(1)
    
    # if there is a character that is NOT a letter, return ERROR
    for i in range(len(sys.argv[1])):
        if not str.isalpha(sys.argv[1][i]):
            print("ERROR")
            exit(1)
    
        
    # call the key 'k' from now on and call the position of the current letter in the key 'kk'
    k = sys.argv[1]
    kk = 0
    
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
                d = ord(str.lower(k[kk])) - 97
                c = (c+d) % 26
                c = c + 65
                print(chr(c), end="")
                kk += 1
                kk = kk%len(k)
            
            else:
                c = ord(p[i]) - 97
                d = ord(str.lower(k[kk])) - 97
                c = (c+d) % 26
                c = c + 97
                print(chr(c), end="")
                kk += 1
                kk = kk%len(k)
        
        # if the character is not a letter just return it
        else:
            print(p[i], end="")
            
    print()
    exit(0)
    
if __name__ == "__main__":
    main()