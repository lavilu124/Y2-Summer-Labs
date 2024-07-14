import random

temperatures = []
for i in range(7):
	temperatures.append(random.randint(26, 41))

days_of_the_week = ["Sunday","Monday", "Tuesday", "Wednsday", "Thirsday", "Friday", "Saturday"]

good_days_count = []
for i in range(7):
	if temperatures[i] % 2 == 0:
		good_days_count.append(days_of_the_week[i])

high = 0
low = 0

for i in range(7):
	if temperatures[i] > temperatures[high]:
		high = i
	if temperatures[i] < temperatures[low]:
		low = i

highest_temp = temperatures[high]
highest_temp_day = days_of_the_week[high]

lowest_temp = temperatures[low]
lowest_temp_day = days_of_the_week[low]

avreg = 0

for i in temperatures:
	avreg += i

avreg /= 7

above_avreg = []
for i in range(7):
	if temperatures[i] > avreg:
		above_avreg.append(days_of_the_week[i])


for i in range(7):
	print(days_of_the_week[i], " : ", temperatures[i])

print("shally had", len(good_days_count), "good days")

print("the hottest temperature was: ", highest_temp, "on a ", highest_temp_day)
print("the coldest temperature was: ", lowest_temp, "on a ", lowest_temp_day)

print("the avreg temp was: ", avreg)
print("the days with above abreg are: ", above_avreg)

sorted_list = temperatures
for i in range(7):
	for j in range(i, 7):
		if temperatures[j] < temperatures[i]:
			temp_var = temperatures[i]
			temperatures[i] = temperatures[j]
			temperatures[j] = temp_var

print("sorted_list is: ", sorted_list) 
