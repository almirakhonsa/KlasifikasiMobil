import csv

data = []
with open('car.csv', 'r') as filecsv:
    datafile = csv.reader(filecsv)
    for i in datafile:
        data.append(i)

def getCount(data, col, value): # untuk menghitung value pada variabel
	total = 0
	for i in data:
		if i[col] == value: total += 1
	return total

def prior(data, value): # prior sudah di laplace
	totValue = getCount(data, 6, value)
	prior = (totValue + 1)/(len(data)+4)
	return prior

def smoothing(data, col, v1): # laplace likelihood
	unacc = 0; acc = 0; good = 0; vgood = 0
	for i in data:
		if i[col] == v1 and i[6] == 'unacc': unacc += 1
		elif i[col] == v1 and i[6] == 'acc': acc += 1
		elif i[col] == v1 and i[6] == 'good': good += 1
		elif i[col] == v1 and i[6] == 'vgood': vgood += 1
		else: 0 
	return [unacc+1, acc+1, good+1, vgood+1] #laplce per value

def likelihood(col, v1, v2, v3, v4): # mengoutputkan nilai likelihood unacc, acc, good, vgood dari masing-masing value
	if v4 == " ": value = [v1, v2, v3]
	else: value = [v1, v2, v3, v4]
	
	like = [smoothing(data, col, value[i]) for i in range(len(value))]
	
	m = []
	for i in range(0,4): 
		x = 0
		for j in range(len(like)):
			x += (like[j][i])
		m.append(x)

	nilai = {}
	for i in range(len(like)):
		n = []
		for j in range(len(m)):
			n.append(like[i][j]/m[j])
		nilai[value[i]] = n
	return nilai

def posterior(v1, v2, v3, v4, v5, v6):
	value = [v1, v2, v3, v4, v5, v6]
	buying = likelihood(0,"vhigh", "high", "med", "low")
	main = likelihood(1,"vhigh", "high", "med", "low")
	doors = likelihood(2,"2", "4", "3", "5more")
	persons = likelihood(3,"2", "4", "more", " ")
	lug_boot = likelihood(4,"small", "med", "big", " ")
	safety = likelihood(5,"low", "med", "high", " ")
	
	unacc = prior(data, "unacc")
	acc = prior(data, "acc")
	good = prior(data, "good")
	vgood = prior(data, "vgood")

	p_unacc = unacc * buying[v1][0] * main[v2][0] * doors[v3][0] * persons[v4][0] * lug_boot[v5][0] * safety[v6][0]
	p_acc = acc * buying[v1][1] * main[v2][1] * doors[v3][1] * persons[v4][1] * lug_boot[v5][1] * safety[v6][1]
	p_good = good * buying[v1][2] * main[v2][2] * doors[v3][2] * persons[v4][2] * lug_boot[v5][2] * safety[v6][2]
	p_vgood = vgood * buying[v1][3] * main[v2][3] * doors[v3][3] * persons[v4][3] * lug_boot[v5][3] * safety[v6][3]

	if p_unacc>p_acc and p_unacc>p_good and p_unacc>p_vgood: x = "unacc"
	elif p_acc>p_unacc and p_acc>p_good and p_acc>p_vgood: x = "acc"
	elif p_good>p_acc and p_good>p_unacc and p_good>p_vgood: x = "good"
	elif p_vgood>p_acc and p_vgood>p_good and p_vgood >p_unacc: x = ("vgood")
	else: print (" nothing")
	return x

def write(data):
	x = [posterior(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5]) for i in range(len(data))]
	with open("2.csv","w", newline='' ) as f:
		writer = csv.writer(f)
		writer.writerow(x)
	return 'Done'

test = []
with open('2.csv', 'r') as filecsv:
    datafile = csv.reader(filecsv)
    for i in datafile:
        test.append(i)

def accuracy(data):
	total = 0
	for i in range(len(data)):
		if data[i][0] == data[i][1]:
			print ("Data ke-", i, ": True")
			total += 1
		else:
			print ("Data ke-", i, ": False")
	result = (total/1728)*100
	print ("Akurasi : ", result,"%")

print (accuracy(test))