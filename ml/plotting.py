import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_volume_comparisons(df, model_name="Model", output_dir="graphs"):
    """
    Generates 3 bar graphs: all sites, busiest site, and quietest site comparison.

    Parameters:
        df (DataFrame): Must contain 'Site_ID', 'Actual_Volume', 'Predicted_Volume'
        model_name (str): e.g., 'LSTM', 'GRU'
        output_dir (str): Directory to save graphs
    """
    model_path = os.path.join(output_dir, model_name.lower())
    os.makedirs(model_path, exist_ok=True)

    # 1. All Sites
    plt.figure(figsize=(12, 6))
    grouped = df.groupby('Site_ID').mean()
    x = grouped.index.astype(str)
    actual = grouped['Actual_Volume']
    pred = grouped['Predicted_Volume']

    bar_width = 0.35
    index = range(len(x))

    plt.bar(index, actual, width=bar_width, label='Actual', color='skyblue')
    plt.bar([i + bar_width for i in index], pred, width=bar_width, label='Predicted', color='orange')
    plt.xticks([i + bar_width / 2 for i in index], x, rotation=90)
    plt.ylabel("Volume")
    plt.title(f"{model_name} - All Sites Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(model_path, "All_Sites.png"))
    plt.close()

    # 2. Busiest Site
    busiest = df.loc[df['Actual_Volume'].idxmax()]
    plt.figure()
    plt.bar(['Actual', 'Predicted'],
            [busiest['Actual_Volume'], busiest['Predicted_Volume']],
            color=['skyblue', 'orange'])
    plt.title(f"{model_name} - Busiest Site (ID: {int(busiest['Site_ID'])})")
    plt.ylabel("Volume")
    plt.tight_layout()
    plt.savefig(os.path.join(model_path, "Busiest_Site.png"))
    plt.close()

    # 3. Quietest Site
    quietest = df.loc[df['Actual_Volume'].idxmin()]
    plt.figure()
    plt.bar(['Actual', 'Predicted'],
            [quietest['Actual_Volume'], quietest['Predicted_Volume']],
            color=['skyblue', 'orange'])
    plt.title(f"{model_name} - Quietest Site (ID: {int(quietest['Site_ID'])})")
    plt.ylabel("Volume")
    plt.tight_layout()
    plt.savefig(os.path.join(model_path, "Quietest_Site.png"))
    plt.close()

    print(f" Graphs saved in {model_path}/")
