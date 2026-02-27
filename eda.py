import matplotlib
matplotlib.use("Qt5Agg")

import pandas as pd
import matplotlib.pyplot as plt
import sys

def generate_eda(file_path):
    # Load dataset
    df = pd.read_csv(file_path)

    print("Dataset Loaded Successfully!\n")
    print("Basic Info:")
    print(df.info())
    print("\nStatistical Summary:")
    print(df.describe())

    # -------------------------------
    # 1️⃣ Daily Phone Usage per Occupation
    # -------------------------------
    if "Occupation" in df.columns and "Daily_Phone_Hours" in df.columns:
        avg_phone = df.groupby("Occupation")["Daily_Phone_Hours"].mean()

        plt.figure()
        avg_phone.plot(kind="bar")
        plt.title("Average Daily Phone Usage per Occupation")
        plt.xlabel("Occupation")
        plt.ylabel("Average Daily Phone Hours")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # -------------------------------
    # 2️⃣ Stress Level per Occupation (Bar)
    # -------------------------------
    if "Occupation" in df.columns and "Stress_Level" in df.columns:
        avg_stress_occ = df.groupby("Occupation")["Stress_Level"].mean()

        plt.figure()
        avg_stress_occ.plot(kind="bar")
        plt.title("Average Stress Level per Occupation")
        plt.xlabel("Occupation")
        plt.ylabel("Average Stress Level")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # -------------------------------
    # 3️⃣ Stress Level by Age (Line)
    # -------------------------------
    if "Age" in df.columns and "Stress_Level" in df.columns:
        avg_stress_age = df.groupby("Age")["Stress_Level"].mean()

        plt.figure()
        avg_stress_age.plot()
        plt.title("Average Stress Level by Age")
        plt.xlabel("Age")
        plt.ylabel("Average Stress Level")
        plt.tight_layout()
        plt.show()

    # -------------------------------
    # 4️⃣ Caffeine Intake per Occupation
    # -------------------------------
    if "Occupation" in df.columns and "Caffeine_Intake_Cups" in df.columns:
        avg_caffeine = df.groupby("Occupation")["Caffeine_Intake_Cups"].mean()

        plt.figure()
        avg_caffeine.plot(kind="bar")
        plt.title("Average Caffeine Intake per Occupation")
        plt.xlabel("Occupation")
        plt.ylabel("Average Caffeine Intake (Cups)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    print("Columns in dataset:", df.columns)

    # -------------------------------
    # 🥧 Pie Chart – Stress Distribution
    # -------------------------------
    if "Stress_Level" in df.columns:
        stress_counts = df["Stress_Level"].value_counts().sort_index()

        plt.figure()
        plt.pie(
            stress_counts.values,
            labels=stress_counts.index,
            autopct="%1.1f%%"
        )
        plt.title("Stress Level Distribution")
        plt.show()


    # -------------------------------
    # 🥧 Pie Chart – Occupation Distribution
    # -------------------------------
    if "Occupation" in df.columns:
        occupation_counts = df["Occupation"].value_counts()

        plt.figure()
        plt.pie(
            occupation_counts.values,
            labels=occupation_counts.index,
            autopct="%1.1f%%"
        )
        plt.title("Occupation Distribution")
        plt.show()


    # -------------------------------
    # 7️⃣ Correlation Matrix
    # -------------------------------
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    if not numeric_df.empty:
        corr = numeric_df.corr()

        plt.figure()
        plt.imshow(corr)
        plt.title("Correlation Matrix")
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.colorbar()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python eda_program.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        generate_eda(file_path)