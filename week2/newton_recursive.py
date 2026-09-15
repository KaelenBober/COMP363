def newton_sqrt(a,x=None, loops=0):
    """Calculate the square root of a number using Newton's method and Recursion."""
    # Guard statements to handle edge cases
    if a < 0:
        raise ValueError("There is no squareroot of negative numbers.")
    elif a == 0:
        return 0
    # Stops the code from running infinitely
    elif loops > 1000:
        return x

    # Only want to update x outside of recursion once
    if x == None:
        x = a/2
    
    # Define the tolerance level for convergence
    epsilon = 0.0001 
    # Base case, if my tolerance is less than epsilon, we have found the closest convergence
    if abs(x*x-a) < epsilon:
        return x
    # Recursive call after recalculating for new x
    return newton_sqrt(a, recalcuateX(a,x), loops+1)


        
# Recalculates and returns new x for recursion
def recalcuateX(a,x):
    x = (x + (a/x)) / 2.0
    return x
 

newton_sqrt(36)





