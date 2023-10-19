import math
total = 9
grupo = math.ceil(total / 10)
#print(docs_per_task)
for i in range(10):
    start = i * grupo + 1 if i > 0 else i * grupo
    end = (i + 1) * grupo + 1 if (i + 1) * grupo < total else total
    print(str(start)+' '+str(end))