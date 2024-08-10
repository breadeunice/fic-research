import pandas as pd

# Load the CSV file into a DataFrame
filename = "results\enhypen_ao3_works2024.08.09_21"
df = pd.read_csv(filename)

# Function to count words in a string
def count_words(s):
    return len(str(s).split())

# Apply the function to each cell in the DataFrame and sum the results
total_words = df.applymap(count_words).sum().sum()

print(f"Total number of words in the {filename}: {total_words}")

# Use a lambda function to count words in each row
df['word_count'] = df.apply(lambda row: sum(len(str(cell).split()) for cell in row), axis=1)

# Calculate the average word count per row
average_words_per_row = df['word_count'].mean()

print(f"Average number of words per row: {average_words_per_row:.2f}")