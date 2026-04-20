# Sorting Assignment

## Student Name
Lee Dotan

## Selected Algorithms
- Insertion Sort
- Merge Sort
- Quick Sort

## Result 1

![Result 1](result1.png)

This figure shows the running times of the three algorithms on random arrays with sizes 500, 1000, 3000, 5000, and 7000.

As the array size increases, the running time of Insertion Sort grows much faster than the other two algorithms.

Merge Sort and Quick Sort remain much faster on random arrays, so their running times look almost zero on the graph compared to Insertion Sort. This does not mean their running time is actually zero, but only that it is much smaller on the same scale.

## Result 2

![Result 2](result2.png)

This figure shows the running times of the same algorithms on nearly sorted arrays with 5% noise.

Compared to result1, the running time of Insertion Sort is much lower in this experiment. This happens because Insertion Sort works more efficiently when the array is already close to being sorted.

Merge Sort and Quick Sort are still efficient, and their running times remain relatively low as the array size grows.

The running times changed because in result2 the input arrays were nearly sorted, while in result1 the arrays were completely random.
