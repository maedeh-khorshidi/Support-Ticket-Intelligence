import pandas as pd

from app.config import RAW_DATA_FILE


def load_data() -> pd.DataFrame:
    """Load the raw customer-support dataset."""

    if not RAW_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{RAW_DATA_FILE}"
        )

    return pd.read_csv(RAW_DATA_FILE)


def show_shape(df: pd.DataFrame) -> None:
    """Show number of rows and columns."""

    print("\n" + "=" * 70)
    print("DATASET SIZE")
    print("=" * 70)

    rows, columns = df.shape

    print(f"Rows    : {rows:,}")
    print(f"Columns : {columns}")


def show_columns(df: pd.DataFrame) -> None:
    """Show column names and data types."""

    print("\n" + "=" * 70)
    print("COLUMNS")
    print("=" * 70)

    info = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str).values,
        "non_null": df.notna().sum().values,
        "unique": df.nunique(dropna=True).values,
    })

    print(info.to_string(index=False))


def show_missing_values(df: pd.DataFrame) -> None:
    """Show missing values for every column."""

    print("\n" + "=" * 70)
    print("MISSING VALUES")
    print("=" * 70)

    missing = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percent": (
            df.isna().mean() * 100
        ).round(2),
    })

    missing = missing.sort_values(
        "missing_count",
        ascending=False,
    )

    print(missing.to_string())


def show_duplicates(df: pd.DataFrame) -> None:
    """Show exact and text-based duplicate rows."""

    print("\n" + "=" * 70)
    print("DUPLICATES")
    print("=" * 70)

    exact_duplicates = df.duplicated().sum()

    print(
        f"Exact duplicate rows: "
        f"{exact_duplicates:,}"
    )

    text_columns = [
        column
        for column in ["subject", "body"]
        if column in df.columns
    ]

    if text_columns:
        text_duplicates = df.duplicated(
            subset=text_columns
        ).sum()

        print(
            f"Duplicate tickets using "
            f"{text_columns}: "
            f"{text_duplicates:,}"
        )


def show_categorical_distribution(
    df: pd.DataFrame,
    column: str,
) -> None:
    """Show frequency and percentage of a categorical column."""

    if column not in df.columns:
        return

    print("\n" + "=" * 70)
    print(f"{column.upper()} DISTRIBUTION")
    print("=" * 70)

    distribution = (
        df[column]
        .value_counts(dropna=False)
        .rename("count")
        .to_frame()
    )

    distribution["percentage"] = (
        distribution["count"]
        / len(df)
        * 100
    ).round(2)

    print(distribution.to_string())


def show_text_statistics(
    df: pd.DataFrame,
    column: str,
) -> None:
    """Show character-length statistics for a text column."""

    if column not in df.columns:
        return

    text = df[column].fillna("").astype(str)

    lengths = text.str.len()

    print("\n" + "=" * 70)
    print(f"{column.upper()} LENGTH")
    print("=" * 70)

    print(f"Mean   : {lengths.mean():.2f}")
    print(f"Median : {lengths.median():.2f}")
    print(f"Min    : {lengths.min():,}")
    print(f"Max    : {lengths.max():,}")

    print("\nPercentiles:")
    print(
        lengths.quantile(
            [0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
        ).to_string()
    )


def show_samples(
    df: pd.DataFrame,
    n: int = 5,
) -> None:
    """Show a few representative ticket samples."""

    columns = [
        column
        for column in [
            "subject",
            "body",
            "queue",
            "priority",
            "type",
            "language",
        ]
        if column in df.columns
    ]

    print("\n" + "=" * 70)
    print("SAMPLE TICKETS")
    print("=" * 70)

    samples = df[columns].sample(
        n=min(n, len(df)),
        random_state=42,
    )

    for index, (_, row) in enumerate(
        samples.iterrows(),
        start=1,
    ):
        print(f"\n--- Ticket {index} ---")

        for column in columns:
            value = row[column]

            if pd.isna(value):
                value = "<NULL>"

            print(f"{column}: {value}")


def show_class_counts(df: pd.DataFrame) -> None:
    """Show the main target-label distributions."""

    for column in [
        "queue",
        "priority",
        "type",
        "language",
    ]:
        show_categorical_distribution(
            df,
            column,
        )


def main() -> None:
    print(f"Loading dataset from:\n{RAW_DATA_FILE}")

    df = load_data()

    show_shape(df)
    show_columns(df)
    show_missing_values(df)
    show_duplicates(df)

    show_class_counts(df)

    for column in [
        "subject",
        "body",
        "answer",
    ]:
        show_text_statistics(
            df,
            column,
        )

    show_samples(df)


if __name__ == "__main__":
    main()