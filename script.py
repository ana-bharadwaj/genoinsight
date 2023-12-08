#Function to read samples from a text file
def read_samples(file_path):
    with open(file_path, 'r') as file:
        samples = set(line.strip() for line in file)
    return samples

#Input file paths
text1_file = 'text1.txt'
text2_file = 'text2.txt'

#Read samples from the input files
text1_samples = read_samples(text1_file)
text2_samples = read_samples(text2_file)

#Find common samples
common_samples = text1_samples.intersection(text2_samples)

#Remove common samples from text1
text1_samples = text1_samples - common_samples

#Count the remaining unique samples in text1
num_remaining_samples = len(text1_samples)

#Write remaining samples to a new output file
output_file = 'remaining_samples.txt'
with open(output_file, 'w') as file:
    for sample in text1_samples:
        file.write(sample + '\n')

print(f"Common samples have been removed from text1.txt")
print(f"Remaining samples have been written to {output_file}")
print(f"Number of remaining samples in text1: {num_remaining_samples}")
