import pandas as pd
import os


# Function to process all CSV files in a directory
def process_all_csv_files(directory):
    results = []

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)

            # Read the CSV file
            data = pd.read_csv(file_path)

            # Compute the average of C_abundance and T_abundance across all rows
            C_abundance_average = data['C_abundance'].mean()
            T_abundance_average = data['T_abundance'].mean()

            # Add the result for this file
            results.append({
                'name': filename.replace('.csv', ''),  # Use the file name without the extension
                'C_abundance_average': C_abundance_average,
                'T_abundance_average': T_abundance_average
            })

    # Create a DataFrame for all results
    result_df = pd.DataFrame(results)

    # Save the results to a new CSV file
    output_path = os.path.join(directory, 'average.csv')  # Define the output path
    result_df.to_csv(output_path, index=False)

    print(f"Averages saved to {output_path}")


# Example usage
directory_path = '../band200_result/'  # Replace with the directory path containing your CSV files
process_all_csv_files(directory_path)
