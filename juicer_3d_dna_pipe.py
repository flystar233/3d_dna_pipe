#coding=utf8

'''
Created by xutengfei <xutengfei1@genomics.cn> on 2020.12.29.
__author__ = "<xutengfei1@genomics.cn>"
__version__ = "v1.0"
'''

import re,os
import argparse
import textwrap

parser = argparse.ArgumentParser(description=textwrap.dedent('''
==============================================================
        	Juicer&3d-dna pipeline v1.0
        	   xutengfei1@genomics.cn
--------------------------------------------------------------
'''), formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("--fq",dest="fq",help="Valid fastq(getreads.pl && cat),*_R*.fastq(.gz),[R]",required=True,nargs="+")
parser.add_argument("--ref",dest="reference",help="Path of the Reference sequence file,[R]",required=True)
parser.add_argument("--res_name",dest="res_name",help="Restriction site name,[default:\"MboI\"]",default="MboI",type=str,choices=["HindIII","MboI","DpnII","NcoI"])
parser.add_argument("--n_cpus",dest="n_cpus",help="The required cpu numbers,[int,default=1]",default=1,type=int)
args = parser.parse_args()
print(args)
########################check##########################
assert os.path.exists(args.reference),"Please check Reference file"
for fq in args.fq:
	assert os.path.isfile(fq),"Please check fastq file"
	assert re.match(r".*_R.\.fastq\.*",fq),"The fastq file name is error"
########################mkdir#########################
if not os.path.exists("01.Juicer"):
	os.mkdir("01.Juicer")
if not os.path.exists("02.3d_dna"):
	os.mkdir("02.3d_dna")
if not os.path.exists("01.Juicer/genome"):
	os.mkdir("01.Juicer/genome")
if not os.path.exists("01.Juicer/fastq"):
	os.mkdir("01.Juicer/fastq")
######################get parameter####################
reference = os.path.abspath(args.reference)
ref_base = os.path.basename(reference)
fastqs = args.fq
n_cpus = args.n_cpus
res_name = args.res_name
####################fastq&&genome########################
os.system("echo \"export PATH=/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/bwa-0.7.17:\$PATH\" > 01.Juicer/shell.sh")
os.system(f"ln -s {reference} 01.Juicer/genome/")
for fq in fastqs:
	fq_path = os.path.abspath(fq)
	os.system(f"ln -s {fq_path} 01.Juicer/fastq/")
########################bwa index########################
bwa_final = reference+".sa"
if os.path.isfile(bwa_final):
	os.system("ln -s %s{.amb,.ann,.bwt,.pac,.sa} 01.Juicer/genome/"%(reference))
else:
	os.system(f"echo \"bwa index genome/{ref_base}\" >> 01.Juicer/shell.sh")

########################MboI.txt &length#################
os.system(f"echo \"python /zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/HIC_Juicer_3d/generate_site_positions.py {res_name} genome/{ref_base} genome/{ref_base}  \" >> 01.Juicer/shell.sh")
chrom_size = "genome/"+ref_base+".size.txt"
os.system(f"echo \"python /ldfssz1/MS_OP/USER/xutengfei1/script_py/fa_length.py genome/{ref_base}  genome/{ref_base}.size.txt\">>01.Juicer/shell.sh")
res_file = "genome/" + ref_base + "_" + res_name + ".txt"
########################Juicer############################
p_now = os.getcwd()
os.system("mkdir 01.Juicer/tmp")
juicer_tmpdir = os.path.abspath("01.Juicer/tmp")

with open("01.Juicer/shell.sh","a") as f:
    f.write(r'export JAVA_TOOL_OPTIONS="-Djava.io.tmpdir=%s -XX:ParallelGCThreads=%d"'%(juicer_tmpdir,int(n_cpus)) + "\n" + 
        r"export TMPDIR=%s"%(juicer_tmpdir) + "\n" +
        r"/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/juicer-1.6/scripts/juicer.sh -z %s -p %s -y %s -s %s -d %s -D /zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/juicer-1.6 -t %s"%("genome/" + ref_base,chrom_size,res_file,res_name,p_now+"/01.Juicer",n_cpus)) 
    f.write("\n")
os.chdir("01.Juicer/")
os.chdir("../")
########################3d-dna############################
os.system("mkdir 02.3d_dna/tmp")
dna_tmpdir = os.path.abspath("02.3d_dna/tmp")

merged_nodups = p_now+'/01.Juicer/aligned/merged_nodups.txt'
with open("02.3d_dna/shell.sh","w") as f:
    f.write(r"export TMPDIR=%s"%(dna_tmpdir) + "\n" +
                r"export PYTHONPATH=/hwfssz1/ST_OCEAN/USER/liuqun/lib/python_2.7:$PYTHONPATH;" + "\n" +
                r"export PATH=/share/app/python-2.7.10/bin:/hwfssz1/ST_OCEAN/USER/liuqun/software/gawk-4.0.2/bin:/hwfssz1/ST_OCEAN/USER/liuqun/software/coreutils-8.11/bin:/hwfssz1/ST_OCEAN/USER/liuqun/software/parallel-20150322/bin:$PATH" + "\n" +
                r"/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/3d-dna_bin/run-asm-pipeline.sh -m haploid -r 3 %s %s"%(reference,merged_nodups)) 
    f.write("\n")

os.chdir("02.3d_dna")
