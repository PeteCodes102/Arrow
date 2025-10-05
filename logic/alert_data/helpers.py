import pandas as pd

# load trading view alert data
def load_data_from_csv(file_path: str) -> pd.DataFrame:
  """
  Loads data from a CSV file into a pandas DataFrame.

  Args:
    file_path: The path to the CSV file.

  Returns:
    A pandas DataFrame containing the data from the CSV file.
  """
  return pd.read_csv(file_path)