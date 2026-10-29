def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

    print(f"CSV saved: {file_path}")