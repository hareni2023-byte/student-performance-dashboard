import pandas as pd
import numpy as np
import joblib

def evaluate():
    try:
        # Load pre-calculated metrics saved by train_models.py
        metrics = joblib.load('models/metrics.pkl')
        
        print("\n" + "=" * 80)
        print(f"{'MODEL NAME':<30} | {'ACCURACY':<10} | {'PRECISION':<10} | {'RECALL':<10} | {'F1-SCORE':<10}")
        print("=" * 80)
        
        for name, m in metrics.items():
            acc = f"{m.get('accuracy', 0):.2f}%"
            prec = f"{m.get('precision', 0):.2f}%"
            rec = f"{m.get('recall', 0):.2f}%"
            f1 = f"{m.get('f1_score', 0):.2f}%"
            print(f"{name:<30} | {acc:>10} | {prec:>10} | {rec:>10} | {f1:>10}")
            
        print("=" * 80 + "\n")
        
    except FileNotFoundError:
        print("[ERROR] 'models/metrics.pkl' not found. Run 'python src/train_models.py' first.")

if __name__ == '__main__':
    evaluate()