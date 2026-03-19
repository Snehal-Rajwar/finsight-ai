import pandas as pd
import numpy as np

def detect_anomalies(df):
    """
    Detects unusually large transactions using Z-score statistics.
    """
    df['amount_abs'] = df['amount'].abs()
    flagged_list = []
    
    print(f"Total transactions: {len(df)}")
    print(f"Categories: {df['category'].unique()}")

    for category in df['category'].unique():
        group = df[df['category'] == category].copy()
        
        print(f"\nCategory: {category}, Count: {len(group)}")
        
        if len(group) < 2:
            print(f"  Skipped - only {len(group)} transaction")
            continue
        
        mean = group['amount_abs'].mean()
        std = group['amount_abs'].std()
        
        print(f"  Mean: ${mean:.2f}, Std: ${std:.2f}")
        
        if std == 0:
            print(f"  Skipped - std is 0")
            continue
        
        group['z_score'] = (group['amount_abs'] - mean) / std
        
        print(f"  Z-scores: {group['z_score'].values}")
        
        flagged = group[group['z_score'] > 1.0]
        
        if not flagged.empty:
            print(f"  FLAGGED {len(flagged)} transactions!")
            flagged_list.append(flagged)
    
    if flagged_list:
        return pd.concat(flagged_list)
    
    print("\nNo anomalies found")
    return pd.DataFrame()