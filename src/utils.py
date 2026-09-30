import json
import pandas as pd
import plotly
import plotly.express as px

def generate_analytics_charts():
    df = pd.read_csv('data/student_data.csv')

    # Chart 1
    fig1 = px.box(
        df, x='performance', y='study_hours', color='performance',
        title="Study Hours Distribution by Performance Tier",
        category_orders={"performance": ["At Risk", "Average", "Good", "Excellent"]}
    )

    # Chart 2
    corr = df.drop(columns=['student_id', 'performance'], errors='ignore').corr()
    fig2 = px.imshow(
        corr, text_auto=True, title="Academic Factors Correlation Matrix",
        color_continuous_scale="Viridis"
    )

    # Chart 3
    fig3 = px.scatter(
        df, x='attendance', y='internal_score', color='performance',
        size='study_hours', hover_data=['previous_gpa'],
        title="Attendance vs Internal Score (Bubble Size = Daily Study Hours)"
    )

    # Apply auto-scaling layout adjustments to all figures
    for fig in [fig1, fig2, fig3]:
        fig.update_layout(
            autosize=True,
            height=None,
            width=None,
            margin=dict(l=40, r=40, t=50, b=40)
        )

    chart1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    chart2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    chart3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return chart1, chart2, chart3