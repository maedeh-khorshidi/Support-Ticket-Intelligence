
import pandas as pd

from app.config import (
    DATASET_NAME,
    TRAIN_DATA_URL,
    TEST_DATA_URL,
    RAW_DATA_DIR,
    RAW_TRAIN_FILE,
    RAW_TEST_FILE,
)


def download_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Download Banking77 train and test CSV files."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading dataset: {DATASET_NAME}")

    train_df = pd.read_csv(TRAIN_DATA_URL)
    test_df = pd.read_csv(TEST_DATA_URL)

    expected_columns = {"text", "category"}

    for name, data in [
        ("train", train_df),
        ("test", test_df),
    ]:
        if not expected_columns.issubset(data.columns):
            raise ValueError(
                f"Unexpected columns in {name}: "
                f"{data.columns.tolist()}"
            )

        if data["text"].isna().any() or data["category"].isna().any():
            raise ValueError(
                f"Missing text or label values in {name}."
            )

    train_df.to_csv(
        RAW_TRAIN_FILE, index=False, encoding="utf-8"
    )
    test_df.to_csv(
        RAW_TEST_FILE, index=False, encoding="utf-8"
    )

    print(f"Train shape: {train_df.shape}")
    print(f"Test shape: {test_df.shape}")
    print(f"Train saved to: {RAW_TRAIN_FILE}")
    print(f"Test saved to: {RAW_TEST_FILE}")

    print("\nTrain columns:", train_df.columns.tolist())
    print("Number of train classes:", train_df["category"].nunique())
    print("Number of test classes:", test_df["category"].nunique())

    return train_df, test_df


if __name__ == "__main__":
    download_dataset()
