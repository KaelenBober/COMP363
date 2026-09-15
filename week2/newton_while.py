def newton_sqrt(a):
    """Calculate the square root of a number using Newton's method."""
    # Guard statements to handle edge cases
    if a < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    elif a == 0:
        return 0

    # Initial guess and parameters for convergence
    x = a / 2.0  
    # Define the tolerance level for convergence
    epsilon = 0.0001 
    # Define a maximum number of iterations to prevent infinite loops 
    stop_after = 1_000  
    # Initialize the iteration count
    iterations_count = 0

    while abs(x * x - a) > epsilon and iterations_count < stop_after:
        # Update guess using Newton's formula:
        x = (x + a / x) / 2.0
        iterations_count += 1
    # Done
    return x

newton_sqrt(4)
