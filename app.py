import random

def random_list(n):
  return [random.randint(1 , 100) for i in range(n)]

def selection_sort(unsorted):
  LENGTH = len(unsorted)
  i = 0
  while i < LENGTH-1:
    min = i
    j = i + 1
    
    while j < LENGTH :
      if unsorted[j] < unsorted[min]:
        min = j
      j += 1
      
    if min != i:
      unsorted[i], unsorted[min] = unsorted[min], unsorted[i]
      
    i +=1
  return unsorted
