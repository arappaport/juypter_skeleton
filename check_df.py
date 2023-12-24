import pandas as pd
import logging

LOGGER = logging.getLogger(__name__)
LOGGER = logging.getLogger('arappaport')
LOGGER.debug("log level = %s", str(LOGGER.getEffectiveLevel()))


def fix_empty_cells(df:pd.DataFrame, inplace:bool=False)->pd.DataFrame:
    """
    Update all empty cells to be None.
    Empty can be:
       - empty string
       - whitespace only string
    :param df:  dataframe
    :param inplace:  if True, changes are made to df parameter.
    :return: Updated dataframe with all empty cells changed to None's
    """

    df = df.copy() if inplace == True else df

    string_cols = df.select_dtypes(include=['object'])
    df[string_cols.columns] = string_cols.apply(lambda x: x.str.strip())
    df.replace('', None, inplace=True)
    return df

def check_df(df :pd.DataFrame, required_columns :[str ] =None, required_values :[str ] =None , )->str:
    """
    Check and clean values in dataframe. Original df is returned unchanged or throws exception
    :param df:   raw dataframe.
    :param required_columns: optional - Names of df columns that must be present - even if empty
    :param required_values: optional - Names of df columns that must have values.  Error if any of them have missing values.
    :return:  Str. Either None or string containing error message. 
    """
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            return f"Invalid CSV. Missing required columns: {', '.join(missing_cols)}"

    if required_values:
        df_req = df[required_values]

        num_null = df_req.isnull().sum().sum()
        LOGGER.debug("Num empty required cells in dataframe: %d", num_null)

        if num_null > 0:
            err = {row :required_values[col] for row, col in zip(*df_req.isnull().values.nonzero())}
            msg = f"Data error. Dataframe contained {num_null} empty cells in required columns {required_columns}. The returned list shows the row index and column names of the FIRST ERROR IN ROWS with blanks.  {err}"
            return msg
    return None