def museum_partial(C_full, w, v):
    # Number of items in the "museum". We are adjusting for 1-based indexing
    # by subtracting 1 from the length of the weights list.
    n = len(w) - 1
    # Initialize the dynamic programming table with zeros.
    # The table has (n+1) rows and (C_full+1) columns.
    # This takes care of initial conditions that require 0 in the
    # first row and first column.
    S = [[0 for _ in range(C_full + 1)] for _ in range(n + 1)]
    # Fill in the dynamic programming table using the recurrence relation.
    for i in range(1, n + 1):
        for r in range(1, C_full + 1):
            # Some verbose variables to help with readability of the recurrence relation.
            available_capacity = r
            weight_of_current_item = w[i]
            best_value_without_current_item = S[i - 1][available_capacity]
            if weight_of_current_item <= available_capacity:
                # We can include the current item in the optimal solution because
                # its weight is less than or equal to the available capacity. Just
                # because we can take it, doesn't mean we should. We need to compare
                # the value of taking it versus not taking it. We take the maximum
                # of the two options. (Only computed here, since the current item's
                # weight could otherwise exceed the available capacity and produce
                # a negative, out-of-range index below.)
                capacity_remaining_after_taking_current_item = (
                    available_capacity - weight_of_current_item
                )
                best_value_with_current_item = (
                    S[i - 1][capacity_remaining_after_taking_current_item] + v[i]
                )
                S[i][r] = max(
                    best_value_without_current_item, best_value_with_current_item
                )
            else:
                # We cannot include the current item in the optimal solution because
                # its weight is greater than the available capacity. Therefore, we
                # can only take the best value without including the current item.
                S[i][r] = best_value_without_current_item
    return S


def museum_traceback(S, w, C_full):
    # Number of items in the "museum". We are adjusting for 1-based indexing
    # by subtracting 1 from the length of the weights list.
    n = len(w) - 1
    # Initialize an empty list to store the selected items.
    selected_items = []
    # Start from the last item and the full capacity.
    i = n
    r = C_full
    # Trace back through the dynamic programming table to find which items were included.
    while i > 0 and r > 0:
        if S[i][r] != S[i - 1][r]:
            # This means that item i was included in the optimal solution.
            selected_items.append(i)
            # Reduce the remaining capacity by the weight of the included item.
            r -= w[i]
        # Move to the previous item.
        i -= 1
    return selected_items 


def complete_museum_heist(C_full, w, v):
    # Number of items in the "museum". We are adjusting for 1-based indexing
    # by subtracting 1 from the length of the weights list.
    n = len(w) - 1
    # First, compute the dynamic programming table.
    S = museum_partial(C_full, w, v)
    # Then, perform traceback to find the selected items.
    selected_items = museum_traceback(S, w, C_full)
    return (
        S[n][C_full],
        selected_items,
    )  # Return the maximum value and the list of selected items


# Demonstration of the complete museum heist function
if __name__ == "__main__":
    # Weights and values of the items from the companion slide deck. Since we use
    # 1-based indexing, we add a dummy value at index 0.
    w = [None, 3, 2, 1, 4]
    v = [None, 4, 3, 2, 5]
    # The maximum weight capacity of our get-away truck. Possible bug:
    # if C_full < smallest weight, we may run into an index error. This
    # will be fixed at later time. For now, chose a value for C_full such that
    # C_full is large enough to accommodate at least one item.
    C_full = 6
    # Items in the museum:
    n = len(w) - 1  # Adjust for 1-based indexing
 # Call the forward dynamic programming function.
    result = museum_partial(C_full, w, v)
    print(f"               The weights of the items are: {w[1:]} lbs")
    print(f"                The values of the items are: {v[1:]} million dollars")
    print(f"The maximum weight capacity of the truck is: {C_full} lbs")
    print(f"       The number of items in the museum is: {n}")
    print(
        f"          Max value that can be obtained is: {result[n][C_full]} million dollars"
    )
    print(f"\nDynamic programming table (S):\t{result[0]}")
    for i in range(1, len(result)):
        print(f"\t\t\t\t{result[i]}")

    # Call the complete museum heist function.
    max_value, selected_items = complete_museum_heist(C_full, w, v)
    print()
    print(f"          Items selected for the heist are: {selected_items}")