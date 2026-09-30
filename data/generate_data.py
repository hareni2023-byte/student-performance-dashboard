import pandas as pd
import numpy as np
import random

np.random.seed(42)

def generate_tier(n, perf_label, att_range, study_range, score_range, gpa_range):
    return pd.DataFrame({
        'student_id': range(np.random.randint(1000, 9000), np.random.randint(1000, 9000) + n),
        'attendance': np.random.uniform(*att_range, n),
        'study_hours': np.random.uniform(*study_range, n),
        'assignment_score': np.random.uniform(*score_range, n),
        'internal_score': np.random.uniform(*score_range, n),
        'previous_gpa': np.random.uniform(*gpa_range, n),
        'participation_score': np.random.uniform(*score_range, n),
        'assignments_completed': np.random.randint(0, 15, n),
        'performance': [perf_label] * n
    })

# Generate exactly 50 of each tier to force perfect distribution
df_excellent = generate_tier(50, 'Excellent', (85, 100), (4.5, 6.0), (85, 100), (8.5, 10.0))
df_good = generate_tier(50, 'Good', (70, 85), (3.0, 4.5), (70, 85), (7.0, 8.5))
df_average = generate_tier(50, 'Average', (50, 70), (1.5, 3.0), (50, 70), (5.0, 7.0))
df_at_risk = generate_tier(50, 'At Risk', (20, 50), (0.0, 1.5), (20, 50), (2.0, 5.0))

df = pd.concat([df_excellent, df_good, df_average, df_at_risk]).sample(frac=1).reset_index(drop=True)
df.to_csv('data/student_data.csv', index=False)
print("[SUCCESS] Generated perfectly balanced dataset.")