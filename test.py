ab = ['Saturday', 'Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', ]

days = ((a+1,ab[a%7]) for a in range(77))

for i in days:
    print(i)
