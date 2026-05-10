def fix_legacy_columns(df):

    rename_map = {
        "timestamps": "timestamp",
        "date": "timestamp",
        "time": "timestamp"
    }

    return df.rename(columns=rename_map)