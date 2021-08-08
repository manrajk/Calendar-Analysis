def bubbleSort(arr):
    '''
    Sorted from largest length to smallest length
    '''

    n = len(arr)

    for i in range(0,n-1):
        for j in range(n-i-1):
            if len(arr[j]) < len(arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]

