import pandas as pd


def load_data(url):
    """Cargo el CSV desde la URL y devuelvo un DataFrame."""
    return pd.read_csv(url)


def clean_column_names(df):
    """Ejercicio 1: nombres en minúsculas, espacios por _ y st por state."""
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.rename(columns={"st": "state"})
    return df


def clean_invalid_values(df):
    """Ejercicio 2: unifico los valores incoherentes."""
    df = df.copy()
    df["gender"] = df["gender"].replace({"Femal": "F", "female": "F", "Male": "M"})
    df["state"] = df["state"].replace({"AZ": "Arizona", "Cali": "California", "WA": "Washington"})
    df["education"] = df["education"].replace({"Bachelors": "Bachelor"})
    df["customer_lifetime_value"] = df["customer_lifetime_value"].str.replace("%", "")
    df["vehicle_class"] = df["vehicle_class"].replace(
        {"Sports Car": "Luxury", "Luxury SUV": "Luxury", "Luxury Car": "Luxury"}
    )
    return df


def format_data_types(df):
    """Ejercicio 3: paso a número CLV y open complaints (número del medio)."""
    df = df.copy()
    df["customer_lifetime_value"] = pd.to_numeric(df["customer_lifetime_value"])
    df["number_of_open_complaints"] = pd.to_numeric(
        df["number_of_open_complaints"].str.split("/").str[1]
    )
    return df


def handle_nulls(df):
    """Ejercicio 4: borro filas vacías, relleno nulos y paso números a enteros."""
    df = df.copy()
    df = df.dropna(how="all")
    df["gender"] = df["gender"].fillna(df["gender"].mode()[0])
    df["customer_lifetime_value"] = df["customer_lifetime_value"].fillna(
        df["customer_lifetime_value"].median()
    )
    columnas_numericas = df.select_dtypes(include="number").columns
    df[columnas_numericas] = df[columnas_numericas].astype(int)
    return df


def handle_duplicates(df):
    """Ejercicio 5: borro duplicados y reinicio el índice."""
    df = df.drop_duplicates(keep="first")
    df = df.reset_index(drop=True)
    return df


def main(url):
    """Ejecuto todos los pasos de limpieza en orden y devuelvo la tabla limpia."""
    df = load_data(url)
    df = clean_column_names(df)
    df = clean_invalid_values(df)
    df = format_data_types(df)
    df = handle_nulls(df)
    df = handle_duplicates(df)
    return df