from typing import Dict, List, Any
from itertools import permutations
import pandas as pd
import re
import polyline
from geopy.distance import geodesic

def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    """
    Reverses the input list by groups of n elements.
    """
    # Your code here
    length = len(lst)
    for i in range(0, length, n):
        end = min(i + n, length) 
        group = lst[i:end]
        for j in range(len(group)):
            lst[i + j] = group[len(group) - 1 - j]
    return lst


def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    """
    Groups the strings by their length and returns a dictionary.
    """
    # Your code here
    result = {}
    for string in lst:
        length = len(string)
        if length not in result:
            result[length] = []
        result[length].append(string)
    return dict(sorted(result.items()))

def flatten_dict(nested_dict: Dict[str, Any], sep: str = '.') -> Dict[str, Any]:
    """
    Flattens a nested dictionary into a single-level dictionary with dot notation for keys.
    
    :param nested_dict: The dictionary object to flatten
    :param sep: The separator to use between parent and child keys (defaults to '.')
    :return: A flattened dictionary
    """
    # Your code here
    def _flatten(current, parent_key=''):
        items = []
        if isinstance(current, dict):
            for k, v in current.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                items.extend(_flatten(v, new_key).items())
        elif isinstance(current, list):
            for i, v in enumerate(current):
                new_key = f"{parent_key}[{i}]"
                items.extend(_flatten(v, new_key).items())
        else:
            items.append((parent_key, current))
        return dict(items)
    
    return _flatten(nested_dict)

def unique_permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list that may contain duplicates.
    
    :param nums: List of integers (may contain duplicates)
    :return: List of unique permutations
    """
    # Your code here
    return list(map(list, set(permutations(nums))))
    


def find_all_dates(text: str) -> List[str]:
    """
    This function takes a string as input and returns a list of valid dates
    in 'dd-mm-yyyy', 'mm/dd/yyyy', or 'yyyy.mm.dd' format found in the string.
    
    Parameters:
    text (str): A string containing the dates in various formats.

    Returns:
    List[str]: A list of valid dates in the formats specified.
    """
    # Regular expression to match the date formats: dd-mm-yyyy, mm/dd/yyyy, yyyy.mm.dd
    date_pattern = r'\b\d{2}-\d{2}-\d{4}\b|\b\d{2}/\d{2}/\d{4}\b|\b\d{4}\.\d{2}\.\d{2}\b'
    
    # Find all matches using re.findall
    return re.findall(date_pattern, text)

    pass

def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    """
    Converts a polyline string into a DataFrame with latitude, longitude, and distance between consecutive points.
    
    Args:
        polyline_str (str): The encoded polyline string.

    Returns:
        pd.DataFrame: A DataFrame containing latitude, longitude, and distance in meters.
    """
    coordinates = polyline.decode(polyline_str)
    df = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
    df['distance'] = 0.0
    
    for i in range(1, len(df)):
        prev_point = (df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude'])
        current_point = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])
        df.loc[i, 'distance'] = geodesic(prev_point, current_point).meters
    
    return df


def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Rotate the given matrix by 90 degrees clockwise, then multiply each element 
    by the sum of its original row and column index before rotation.
    
    Args:
    - matrix (List[List[int]]): 2D list representing the matrix to be transformed.
    
    Returns:
    - List[List[int]]: A new 2D list representing the transformed matrix.
    """
    n = len(matrix)
    rotated_matrix = [[matrix[n - j - 1][i] for j in range(n)] for i in range(n)]
    final_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated_matrix[i]) - rotated_matrix[i][j] 
            col_sum = sum(rotated_matrix[k][j] for k in range(n)) - rotated_matrix[i][j]  
            final_matrix[i][j] = row_sum + col_sum
    
    return final_matrix



def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    full_week = set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    full_day_range = pd.date_range("00:00:00", "23:59:59", freq="S")  
    grouped = df.groupby(['id', 'id_2'])

    result = {}
    
    for (id_val, id2_val), group in grouped:
        days_covered = set(group['startDay'])
        missing_days = full_week - days_covered
        time_coverage_correct = True
        
        for day in full_week:
            day_group = group[group['startDay'] == day]
            if not day_group.empty:
                time_ranges = pd.date_range(day_group['startTime'].min(), day_group['endTime'].max(), freq="S")
                if len(time_ranges) != len(full_day_range):
                    time_coverage_correct = False
        
        result[(id_val, id2_val)] = len(missing_days) > 0 or not time_coverage_correct
    
    return pd.Series(result)
