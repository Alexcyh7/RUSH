import subprocess
import os
from multiprocessing import Pool
import itertools
import re

def run_process(args):
    output_dir = args[-1]
    summary_file_path = os.path.join(output_dir, 'summary.txt')
    try:
        with open(summary_file_path, 'r') as summary_file:
            lines = summary_file.readlines()
            precision = float(lines[1].strip())  # Read precision from the second line
            recall = float(lines[2].strip())  # Read recall from the third line
            f1 = 0
            if (precision + recall) != 0:
                f1 = 2 * (precision * recall) / (precision + recall)  # Calculate F1 score
            
            # Output the results
            print(f"{precision:.2f} {recall:.2f} {f1:.2f}")
            # You can also write these results to a file if needed
    except FileNotFoundError:
        print(f"File not found: {summary_file_path}")

def construct_output_directory(base_dir, input_path, time_slice, half_life, retirement, application):
    output_dir = f"{base_dir}{input_path}/{time_slice}_{half_life}_{retirement}/{application}"
    return output_dir

def main():
    input_file_data = [
        # ('bayc', 1650364600),
        # ('terraforms', 1650620294),
        ('meebits', 1651992148),
        # ('artblock', 1651907349),
        # ('dot', 1642688831),
        # ('ios', 954388451),
        # ('adr', 954112538),
        # Add more pairs as needed
    ]  

    group_list = [
        # (3600, 1, 4),
        # (1800, 2, 8),
        # (900, 4, 16),
        # (450, 8, 32),
        # (225, 16, 64),
        # (112, 32, 128),
        # (56, 64, 236),
        (3600, 1, 16),
        (1800, 2, 16),
        (900, 4, 16),
        (450, 8, 16),
        (225, 16, 16),
        (112, 32, 16),
        (56, 64, 16),


        # (60, 1, 16),
        # (30, 2, 16),
        # (12, 4, 16),
        # (6, 8, 16),
        # (3, 16, 16),
        # (1, 32, 16),
       # ... other groups ...
    ]

    data_directory = "/data/yuhang/rush/"
    application = 'rush'

    args_list = []
    for (input_path, start_time), (time_slice_length, half_life_ratio, retirement_ratio) in itertools.product(input_file_data, group_list):
        input_file1 = f"{data_directory}{input_path}/static.txt"
        input_file2 = f"{data_directory}{input_path}/increment.txt"
        output_dir = construct_output_directory(data_directory, input_path, time_slice_length, half_life_ratio, retirement_ratio, application)
        args = [input_file1, input_file2, start_time, time_slice_length, half_life_ratio, retirement_ratio, output_dir]
        run_process(args)

    # with Pool() as pool:
        # pool.map(run_process, args_list)

if __name__ == "__main__":
    main()
