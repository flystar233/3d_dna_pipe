import sys
def length_fa(faname,out):
    with open(faname,'rt') as IN, open(out,'wt') as OUT:
        Dict = {}
        result=[]
        for line in IN:
            if line[0] == '>':
                key = line[1:-1]
                Dict[key] = []
            else:
                Dict[key].append(line.strip("\n"))
        for key, value in Dict.items():
            Dict[key] = ''.join(value)
        for key, value in Dict.items():                 
            tmp_result = key+"\t"+str(len(value))
            result.append(tmp_result)
        result = "\n".join(result)
        OUT.write(result)
if (len(sys.argv)==3):
    length_fa(sys.argv[1],sys.argv[2])
else:
    print("Usage: python fa_length.py test.fa out.txt")

