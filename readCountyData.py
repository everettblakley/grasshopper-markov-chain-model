

path = r'C:\Users\evere\Documents\Grasshopper Research\Spreadsheets\Counties_Rank.csv'

xl = open(path, 'r').read().split('\n')

for line in xl:
    l = line.split(',')
    print "{0} & {1} & {2} & {3} \\\\".format(l[0], l[1], l[2], l[3])

