import csv
import os

# 定义输入文件名和输出文件夹路径
input_file = 'paralog_report.tsv'
output_folder = '.'  # 输出文件夹为当前目录

# 读取TSV文件并处理
def process_tsv(input_filename, output_folder):
    # 使用csv模块读取TSV文件
    with open(input_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        
        # 跳过标题行，获取基因名称和物种名称
        headers = next(reader)
        gene_names = headers[1:]  # 基因名称从第二列开始
        species_name = headers[0]  # 第一列是物种名称

        # 遍历每行数据
        for row in reader:
            species_values = row[1:]  # 从第二列开始是基因的值
            for gene_index, gene_value in enumerate(species_values):
                if float(gene_value) > 1:
                    gene_name = gene_names[gene_index]
                    output_filename = f"{gene_name}.txt"
                    output_filepath = os.path.join(output_folder, output_filename)

                    # 写入物种名称到对应的基因文件中
                    with open(output_filepath, 'a') as output_file:  # 'a'模式用于追加
                        output_file.write(f"{row[0]}\n")  # 写入第一列的物种名称

# 调用函数处理文件
process_tsv(input_file, output_folder)

print("基因对应的物种记录文件已生成。")