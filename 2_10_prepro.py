import re

# Specify the input and output file paths
input_file = 'brown.txt'
output_file = 'output.txt'

# Initialize an empty list to store the lowercase words
lowercase_words = []

# Open the input file
with open(input_file, 'r') as file:
    # Read lines from the file
    for line in file:
        # Use regex to find and extract words containing only alphabets
        words = re.findall(r'\b[a-zA-Z]+\b', line)
        # Convert each word to lowercase and add it to the list
        lowercase_words.extend([word.lower() for word in words])

# Join the lowercase words with spaces and create a single string
result_text = ' '.join(lowercase_words)

# Limit the result to a maximum of 50,000 characters
result_text = result_text[:50000]

# Write the result to the output file
with open(output_file, 'w') as file:
    file.write(result_text)