# CISC-121_Project

##Decomposition: What smaller steps form your chosen algorithm?
repeatedly find the smallest element in the unsorted part of the array and store its index, do this by iterating thourgh it with a pointer
establist another pointer that acts as the boundary between sorted and unsorted part of the array
after iterating through the unsorted part check if boundary is the smallest integer, if not swap the array[min] and array[boundary]
now move boundary by 1 and continue until the array is sorted
