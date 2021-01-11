## 第一步
hic-pro 处理原始hic数据，得到有效片段。（没有改动）
## 第二步
python 重写getread.pl。

与原代码相比，在同样的运行时间下，增加了对 fastq 文件新旧 2 种 ID 的兼容和程序进度提示。fastq 文件新 ID 示例:`@V300075059L2C001R0020000012/1` ，旧 ID：`@A00838:157:H2Y5TDSXY:4:1101:1398:1000 2:N:0:ATTCAGAA+CCTATCCT`

### 使用方法
```
sh getread.sh rawdata_allValidPairs CL10_1.fq.gz CL10_2.fq.gz #建议qsub提交任务
```
## 第三步
3d-dna 本就是一套用 sh、perl、python、awk 编写的流程。

在最新版本中，3d-dna 所依赖的 juicer 开始使用 bwa 双端比对，3d-dna 不再要求输入预估的染色体数目。在原接口流程中（由 liuqun@genomics.cn 编写），程序一直会监测 juicer 生成的文件，如果程序开始生成 inter.hic，则 qdel 任务，并开始运行3d-dna。这样就存在了如果不是nohup提交任务，如果关掉 ssh 集群连接，则任务将会失败。

在原流程的基础上修改了代码，以适应新 juicer+3d-dna 参数，并直接生成 juicer 和 3d-dna程序所需代码， 当juicer 生成 merged_nodups.txt 文件后（即开始生成 inter.hic 时），可以杀死 juicer任务，开始运行 3d-dna。在运行过程中，可以把 0.hic(1.hic,2.hic,polished.hic 等等hic文件)和 0.asm(1.asm,2,asm 等等asm文件)导出到 juicerbox 中查看具体情况，通常情况下 0.hic 会挂载最多的原始基因组序列，rawchrom.hic 会确定最好的染色体边界。选择一个进行人工 review 热图，确定染色体边界之后导出 review.assembly 文件。然后再到集群运行 3d-dna review 程序得到最终的hic组装结果。
### 使用方法
```
python juicer_3d_dna_pipe.py --fq *.gz --ref refer.fa --res_name MboI --n_cpus 8
bash run-asm-pipeline-post-review.sh --sort-output  -r test.review.assembly contig.fa  ./merged_nodups.txt
```
## 脚本存放
`/ldfssz1/MS_OP/USER/xutengfei1/script_py/hic_scr`
`/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/3d-dna_bin`
