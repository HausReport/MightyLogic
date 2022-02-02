

points = [0,20,50,110,185,260,380,500,650,850,
          1050,1250,1550,1850,2150,2500,2850,
          3250,3650,4100,4800,5900,7200,8600,
          9900,11200,12200,13200,14100,15000, 16000, 17500]

test = 12324

for i in range(len(points)):
    print(str(i))
    if points[i] <= test < points[i + 1]:
        league = 30-i
        perc = (test - points[i]) /(points[i+1] - points[i])
        print(f'League {league}, percent {perc}')
        break
