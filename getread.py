import pyfastx
from collections import defaultdict
import gzip
import argparse
import time

def fastq_grep():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument( "--input", action="store", dest="seqname", required=True,help="File of allValidPairs")
	parser.add_argument( "--r1", action="store", dest="r1seq", required=True,help="File of r1 seq(gzip)")
	parser.add_argument( "--r2", action="store", dest="r2seq", required=True,help="File of r2 seq(gzip)")
	parser.add_argument( "--header",type=str, dest="header", required=True,help="Type of fq header")
	args = parser.parse_args()
	seqname = args.seqname
	r1seq = args.r1seq
	r2seq = args.r2seq
	header = args.header
	myname = defaultdict(int)
	with open(seqname) as IN:
		for i in IN:
			myname[i.strip()]=1
	vaild_len = len(myname)
	count = 0
	print_len = vaild_len // 100 #per 1/100 print progress
	with gzip.open(filename='valid_R1.fastq.gz',compresslevel=6,mode='wt') as OUT1,gzip.open(filename='valid_R2.fastq.gz',compresslevel=6,mode='wt') as OUT2:
		for r1,r2 in zip(pyfastx.Fastq(r1seq,build_index=False,full_name=True),pyfastx.Fastq(r2seq,build_index=False,full_name=True)):
			if header =='new':
				tmp_r1_name = r1[0].rstrip('1').rstrip('/')
			else:
				tmp_r1_name = r1[0].split()[0]
			if  myname[tmp_r1_name]==1:
				count += 1
				if count % print_len == 0:
					print(f'[{time.asctime(time.localtime(time.time()))}] {count/vaild_len*100}% done.\n')
				OUT1.write("@"+r1[0]+"\n")
				OUT1.write(r1[1]+"\n")
				OUT1.write("+"+"\n")
				OUT1.write(r1[2]+"\n")
				OUT2.write("@"+r2[0]+"\n")
				OUT2.write(r2[1]+"\n")
				OUT2.write("+"+"\n")
				OUT2.write(r2[2]+"\n")
			else:
				pass
if __name__=="__main__":
	fastq_grep()
