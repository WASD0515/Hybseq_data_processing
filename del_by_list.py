import os
import shutil

def remove_species_from_FNA(genes_file_path, species_to_remove, output_path):
    """
    根据物种清单从 genes 文件中删除对应的物种及其序列。
    """
    print(f"Processing file: {genes_file_path}...")  # 调试输出
    try:
        with open(genes_file_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        seq_name = ""
        seq_data = []

        for line in lines:
            if line.startswith(">"):  # 判断是否为序列头（label）
                # 如果当前物种的标签不在待删除清单中，保留它
                if seq_name and seq_name[1:].split()[0] not in species_to_remove:
                    new_lines.append(seq_name + "".join(seq_data) + "\n")
                seq_name = line
                seq_data = []
            else:
                seq_data.append(line.strip())  # 收集序列数据

        # 处理最后一个序列
        if seq_name and seq_name[1:].split()[0] not in species_to_remove:
            new_lines.append(seq_name + "".join(seq_data) + "\n")

        # 如果有处理后的数据，则保存到 output_path
        if new_lines:
            with open(output_path, 'w') as f:
                f.writelines(new_lines)
            print(f"Processed and saved: {output_path}")
            return True
        else:
            print(f"No valid sequences found in {genes_file_path}.")
            return False  # 没有有效序列时返回 False
    except Exception as e:
        print(f"Error processing {genes_file_path}: {e}")
        return False


def process_genes_and_lists(genes_dir, list_dir, output_dir):
    """
    遍历 genes 和 list 文件夹中的文件，删除对应的物种，并保存处理后的文件。
    """
    # 如果输出目录不存在，创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # 获取 genes 和 list 文件夹中的文件列表
    list_files = set(os.listdir(list_dir))
    genes_files = set(os.listdir(genes_dir))

    print(f"List directory contents: {list_files}")
    print(f"Genes directory contents: {genes_files}")

    for genes_file in genes_files:
        if genes_file.endswith(".FNA"):
            list_file = genes_file.replace(".FNA", ".txt")  # 对应的 list 文件

            print(f"Checking if {list_file} exists in the list directory...")

            if list_file in list_files:
                # 如果对应的 list 文件存在，读取物种清单
                species_list_path = os.path.join(list_dir, list_file)
                with open(species_list_path, 'r') as f:
                    species_to_remove = set(line.strip() for line in f.readlines())  # 物种清单

                genes_file_path = os.path.join(genes_dir, genes_file)
                output_file_path = os.path.join(output_dir, f"processed_{genes_file}")
                
                # 根据物种清单，处理 genes 文件
                success = remove_species_from_FNA(genes_file_path, species_to_remove, output_file_path)
                
                if not success:
                    # 如果没有要删除的物种，直接复制 genes 文件到 processed 文件夹
                    shutil.copy(genes_file_path, output_dir)
                    print(f"Copied without changes: {genes_file_path}")
            else:
                # 如果没有对应的 list 文件，直接复制 genes 文件到 processed 文件夹
                genes_file_path = os.path.join(genes_dir, genes_file)
                shutil.copy(genes_file_path, output_dir)
                print(f"Copied without list file: {genes_file_path}")
        else:
            print(f"Skipping non-.FNA file: {genes_file}")  # 调试输出


# 设置目录路径
current_directory = os.getcwd()  # 获取当前工作目录
genes_directory = os.path.join(current_directory, 'genes')  # genes 文件夹路径
list_directory = os.path.join(current_directory, 'list')  # list 文件夹路径
output_directory = os.path.join(current_directory, 'processed')  # processed 文件夹路径

# 打印目录路径，确保路径正确
print(f"Genes directory: {genes_directory}")
print(f"List directory: {list_directory}")
print(f"Output directory: {output_directory}")

# 执行处理
process_genes_and_lists(genes_directory, list_directory, output_directory)
