import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console

# Initialize rich console
console = Console()

# Configuration
LOG_FILE = "cyber_warfare_log.txt"

def load_log_data():
    """Load log data from the log file into a pandas DataFrame."""
    try:
        data = []
        with open(LOG_FILE, "r") as log_file:
            for line in log_file:
                parts = line.strip().split(" ", 2)
                if len(parts) == 3:
                    timestamp, status, details = parts
                    data.append({"Timestamp": timestamp, "Status": status, "Details": details})
        return pd.DataFrame(data)
    except Exception as e:
        console.print(f"[red]Error loading log data: {e}")
        return pd.DataFrame()

def generate_metrics(df):
    """Generate metrics and display them using matplotlib."""
    if df.empty:
        console.print("[red]No data available to generate metrics.")
        return

    # Count occurrences of each status
    status_counts = df["Status"].value_counts()

    # Plot status distribution
    plt.figure(figsize=(10, 6))
    status_counts.plot(kind="bar", color=["green", "red", "yellow", "blue"])
    plt.title("Status Distribution")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Display top 5 details
    console.print("[blue]Top 5 Details:")
    top_details = df["Details"].value_counts().head(5)
    console.print(top_details)

def main():
    console.print("[blue]Loading log data and generating metrics...")
    df = load_log_data()
    generate_metrics(df)

if __name__ == "__main__":
    main()
