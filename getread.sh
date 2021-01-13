#!/bin/sh
(($# == 3)) || { echo -e "\nUsage: $0 rawdata_allValidPairs fq1.gz fq2.gz\n"; exit; }
file=$1
fq1=$2
fq2=$3
sign=`head -1 $file |grep "/"`
sign_fq=`zcat $fq1|head -1|grep "/"` 
if [ ! -n "$sign" ]; then  
  cut -f 1 $file > fastq.name 
else  
  cut -f 1 -d "/" $file > fastq.name
fi
if [ ! -n "$sign_fq" ]; then  
  /zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/miniconda3/bin/python /ldfssz1/MS_OP/USER/xutengfei1/script_py/hic_scr/getread.py --input fastq.name --r1 $fq1 --r2 $fq2 --header old
else  
  /zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/miniconda3/bin/python /ldfssz1/MS_OP/USER/xutengfei1/script_py/hic_scr/getread.py --input fastq.name --r1 $fq1 --r2 $fq2 --header new
fi
