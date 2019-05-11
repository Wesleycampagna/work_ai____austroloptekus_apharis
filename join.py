str1 = ' de'
str2 = ' ia'

str3 = 'Trabalho '
str4 = 'final'

#str3 = str3.concat([str3, str4, str1, str2])

str3 = '{}{}{}{}'.format(str3, str4, str1, str2)

print(str3)
