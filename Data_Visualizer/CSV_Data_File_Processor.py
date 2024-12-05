import pandas as pd
import os

# Function to process all files in the specified directory
def process_files(input_folder, output_file):
    summary_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".xlsx") or file_name.endswith(".csv"):
            file_path = os.path.join(input_folder, file_name)
            
            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                print(f"Skipping empty file: {file_name}")
                continue

            try:
                # Read the file based on its extension
                if file_name.endswith(".xlsx"):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)

                # Skip if DataFrame is empty
                if df.empty:
                    print(f"Skipping empty DataFrame in file: {file_name}")
                    continue

                # Select the last 50 rows (or fewer if less data is available)
                last_50_rows = df.tail(50)

                # Calculate mean for each column in the last 50 rows
                means = last_50_rows.mean().to_dict()
                means["Location"] = os.path.splitext(file_name)[0]  # Use file name as location identifier

                summary_data.append(means)

            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    # Create a DataFrame for the summary data and save to output CSV
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_file, index=False)
    print(f"Summary saved to {output_file}")

# Main execution
if __name__ == "__main__":
    input_folder = "./Data_Sets/Data_Set_1_2024_12_04"  # Current directory where the script is located
    output_file = "./Data_Sets/Data_Set_1_2024_12_04/Summary_last_50_means.csv"  # Output file to store results
    process_files(input_folder, output_file)
