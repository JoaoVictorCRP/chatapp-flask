args = {
    '1':'oi'
}

if args['1'] == None:
    args['1'].append('foo')
else:
    args['1'] = [222]

print(args)