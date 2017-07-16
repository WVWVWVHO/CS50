import cs50
import math


def main():
    # ask credit card number 
    print("Credit Card number: ", end="")
    cc = cs50.get_int()
    c  = math.floor(math.log10(cc))+1

    # if the credit card number is shorter than 13 return INVALID
    # if the credit card number is longer  than 16 return INVALID
    if c<13 or c>16:
        print("INVALID")
        exit(0)
    
    # make string of the long_long
    s = str(cc)
    
    # temporary variables
    sum1 = 0
    sum2 = 0
    sum3 = sum1 + sum2
    
    # sum of the 'second to last' numbers
    for i in range(c-2, -1, -2):
        if int(s[i])*2 < 10:
            sum1 = int(s[i])*2 + sum1
        else:
            sum1 = int(s[i])*2 - 10 + 1 + sum1
    
    # sum of the 'last' numbers
    for i in range(c-1, -1, -2):
        sum2 = int(s[i]) + sum2
        
    # check if sum3 ends with a 0
    if sum3%10 == 0:
        two = int(s[0])*10 + int(s[1])
    
        # check if the card is from AMEX
        if two==34 or two==37:
            print("AMEX")
        
        # check if the card is from MASTERCARD
        elif two>=51 and two <= 55:
            print("MASTERCARD")
        
        # check if the card is from VISA
        elif int(s[0]) == 4:
            print("VISA")
            
        else:
            print("INVALID")
    
    else:
        print("NOT RECOGNIZED CARD")
    

if __name__ == "__main__":
    main()