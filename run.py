import alocacaoArtigos as al
import sys

def err ():
    print('don\'t exists this parameter configuration')

if len(sys.argv) is 1:
    al.alocacaoArtigos()

if len(sys.argv) is 2:
    if float(sys.argv[1]) is not None:
        al.alocacaoArtigos(crossoverrate=float(sys.argv[1]))
    else:
        al.alocacaoArtigos(inputpath=sys.argv[1])

elif len(sys.argv) is 3:
    if float(sys.argv[1]) and float(sys.argv[2]):
        al.alocacaoArtigos(crossoverrate=float(sys.argv[1]), mutationrate=float(sys.argv[2]))
    else: err()

elif len(sys.argv) is 4:
    if float(sys.argv[1]) and float(sys.argv[2]) and int(sys.argv[3]):
        al.alocacaoArtigos(crossoverrate=float(sys.argv[1]), mutationrate=float(sys.argv[2]), maxgen=int(sys.argv[3]))
    else: err()

elif len(sys.argv) is 5:
    if float(sys.argv[1]) and float(sys.argv[2]) and int(sys.argv[3]):
        al.alocacaoArtigos(crossoverrate=float(sys.argv[1]), mutationrate=float(sys.argv[2]), 
            maxgen=int(sys.argv[3]), inputpath=sys.argv[4])
    else: err()
else:
    err()