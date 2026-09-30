import joblib

def check_all_accuracies():
    try:
        # Load the stored evaluation metrics generated during training
        metrics = joblib.load('models/metrics.pkl')
        
        print("=" * 60)
        print(f"{'MODEL NAME':<30} | {'ACCURACY':<10} | {'F1-SCORE':<10}")
        print("=" * 60)
        
        for model_name, scores in metrics.items():
            acc = scores.get('accuracy', 0)
            f1 = scores.get('f1_score', 0)
            print(f"{model_name:<30} | {acc:>8.2f}% | {f1:>8.2f}%")
            
        print("=" * 60)
        
    except FileNotFoundError:
        print("[ERROR] 'models/metrics.pkl' not found. Please run 'python src/train_models.py' first.")

if __name__ == '__main__':
    check_all_accuracies()