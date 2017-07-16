import cs50

def main():
    
    # ask for the amount of change
    while True:
        print("How much change is owned?")
        change = cs50.get_float()
        if change > 0:
            break
    
    # change  the double floating point dollar value to a integer value in cents
    cents = change * 100
    
    # k is the minimum amount of coins needed
    k = 0
    
    # number of $0.25 coins needed
    k += cents//25
    cents = cents%25

    # number of $0.10 coins needed
    k += cents//10
    cents = cents%10
    
    # number of $0.05 coins needed
    k += cents//5
    cents = cents%5
    
    # number of $0.01 coins needed
    k += cents//1
    cents = cents%1
     
    # print the number of coins needed    
    print(int(k))
        
    
if __name__ == "__main__":
    main()