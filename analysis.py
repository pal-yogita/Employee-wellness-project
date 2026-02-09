# File Path: employee_wellness_project/analysis.py
# This file contains all data analysis and plotting functions for the web app.

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# Define our custom color palette
THEME_COLORS = {
    'primary': '#4A5568',
    'accent1': '#38B2AC', # Teal
    'accent2': '#A0AEC0', # Gray
    'accent3': '#E53E3E', # Red for contrast if needed
}
# Load the cleaned dataset, our single source of truth for all functions.
df = pd.read_csv('cleaned_employee_data.csv')


# -------------------------------------------------------------------- #
# --- PRESENTER 1: THE HR GENERALIST ---
# -------------------------------------------------------------------- #

def plot_q1_demographics() -> tuple[go.Figure, go.Figure]:
    """
    Answers Q1: What is the overall demographic profile (Age & Gender)?
    Generates an age histogram and a gender pie chart.
    """
    # Gender Distribution
    gender_counts = df['Gender'].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title='Gender Distribution of Workforce',
        hole=0.3
    )
    
    # Age Distribution
    fig_age = px.histogram(
        df,
        x='Age',
        title='Age Distribution of Workforce',
        labels={'Age': 'Employee Age'},
        nbins=10
    )
    fig_age.update_layout(bargap=0.1)
    
    return fig_gender, fig_age

def plot_q2_workplace_landscape() -> tuple[go.Figure, go.Figure]:
    """
    Answers Q2: What is the workplace landscape?
    Generates charts for company size and tech company split.
    """
    # Company Size
    order = ['5-Jan', '25-Jun', '26-100', '100-500', '500-1000', 'More than 1000']
    size_counts = df['no_employees'].value_counts().reindex(order)
    fig_size = px.bar(
        x=size_counts.index,
        y=size_counts.values,
        title='Company Size Distribution',
        labels={'x': 'Number of Employees', 'y': 'Count'}
    )
    
    # Tech Company Split
    tech_counts = df['tech_company'].value_counts()
    fig_tech = px.pie(
        names=tech_counts.index,
        values=tech_counts.values,
        title='Is the Company Primarily a Tech Company?',
        hole=0.3
    )
    
    return fig_size, fig_tech

def plot_q3_family_history() -> go.Figure:
    """
    Answers Q3: Is there a baseline mental health risk based on family history?
    Generates a pie chart for family history of mental illness.
    """
    history_counts = df['family_history'].value_counts()
    fig_history = px.pie(
        names=history_counts.index,
        values=history_counts.values,
        title='Family History of Mental Illness',
        hole=0.3,
        color_discrete_sequence=[THEME_COLORS['accent1'], THEME_COLORS['accent2']] # <-- ADD THIS LINE
    )
    return fig_history


# -------------------------------------------------------------------- #
# --- PRESENTER 2: THE BENEFITS SPECIALIST ---
# -------------------------------------------------------------------- #

def plot_q4_formal_support() -> go.Figure:
    """
    Answers Q4: How comprehensive is our formal support (Benefits vs. Wellness Programs)?
    Generates side-by-side pie charts for benefits and wellness programs.
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Does Employer Provide<br>Mental Health Benefits?', 'Is There a Formal<br>Wellness Program?'),
        specs=[[{'type':'domain'}, {'type':'domain'}]]
    )
    
    benefits_counts = df['benefits'].value_counts()
    fig.add_trace(go.Pie(labels=benefits_counts.index, values=benefits_counts.values, name="Benefits"), 1, 1)
    
    wellness_counts = df['wellness_program'].value_counts()
    fig.add_trace(go.Pie(labels=wellness_counts.index, values=wellness_counts.values, name="Wellness"), 1, 2)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(title_text="Coverage of Formal Mental Health Support Systems")
    return fig

def plot_q5_care_options_by_size() -> go.Figure:
    """
    Answers Q5: Are employees aware of care options, and how does this vary by company size?
    Generates a grouped bar chart of care options awareness by company size.
    """
    grouped = df.groupby('no_employees')['care_options'].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
    fig = px.bar(
        grouped,
        x='no_employees', y='percentage', color='care_options',
        title='Awareness of Care Options by Company Size',
        labels={'no_employees': 'Company Size', 'percentage': 'Percentage of Employees'},
        barmode='group',
        category_orders={'no_employees': ['5-Jan', '25-Jun', '26-100', '100-500', '500-1000', 'More than 1000']}
    )
    return fig

def plot_q6_leave_vs_treatment() -> go.Figure:
    """
    Answers Q6: How accessible is taking medical leave, and does this impact treatment rates?
    Generates a chart showing treatment rates based on ease of taking medical leave.
    """
    leave_treatment_dist = pd.crosstab(df['leave'], df['treatment'], normalize='index').mul(100).reset_index()
    leave_treatment_dist = leave_treatment_dist.sort_values(by='Yes', ascending=False)
    fig = px.bar(
        leave_treatment_dist,
        x='leave', y='Yes',
        title='Treatment Rate by Ease of Taking Medical Leave',
        labels={'leave': 'Ease of Taking Medical Leave', 'Yes': 'Treatment Rate (%)'}
    )
    return fig


# -------------------------------------------------------------------- #
# --- PRESENTER 3: THE LEAD ANALYST ---
# -------------------------------------------------------------------- #

def plot_q7_treatment_vs_family_history() -> go.Figure:
    """
    Answers Q7: What is the overall treatment rate, and how does family_history amplify this?
    Generates a pie chart for the overall rate and a bar chart for the comparison.
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Overall Treatment Rate', 'Treatment Rate by Family History'),
        specs=[[{'type':'domain'}, {'type':'bar'}]]
    )
    treatment_counts = df['treatment'].value_counts()
    fig.add_trace(go.Pie(labels=treatment_counts.index, values=treatment_counts.values, name="Overall"), 1, 1)
    
    fh_dist = pd.crosstab(df['family_history'], df['treatment'], normalize='index').mul(100)
    fig.add_trace(go.Bar(x=fh_dist.index, y=fh_dist['Yes'], name='Sought Treatment'), 1, 2)
    
    fig.update_traces(hole=.4, selector=dict(type='pie'))
    fig.update_yaxes(title_text="Treatment Rate (%)", row=1, col=2)
    fig.update_layout(title_text="Impact of Family History on Seeking Treatment", showlegend=False)
    return fig

def plot_q8_work_interference_vs_treatment() -> go.Figure:
    """
    Answers Q8: How strongly does work_interference predict who gets help?
    Generates a bar chart showing treatment rate by level of work interference.
    """
    wi_dist = pd.crosstab(df['work_interfere'], df['treatment'], normalize='index').mul(100)
    wi_dist = wi_dist.sort_values(by='Yes', ascending=False)
    fig = px.bar(
        wi_dist,
        x=wi_dist.index, y='Yes',
        title='Treatment Rate by Perceived Work Interference',
        labels={'x': 'Level of Work Interference', 'Yes': 'Treatment Rate (%)'}
    )
    return fig

def plot_q9_gender_disparity_under_interference() -> go.Figure:
    """
    Answers Q9: Is there a gender disparity in treatment among those whose work is affected?
    Generates a bar chart of treatment rates by gender for a filtered subset.
    """
    affected_df = df[df['work_interfere'] != 'Never']
    gender_dist = pd.crosstab(affected_df['Gender'], affected_df['treatment'], normalize='index').mul(100)
    gender_dist = gender_dist.sort_values(by='Yes', ascending=False)
    fig = px.bar(
        gender_dist,
        x=gender_dist.index, y='Yes', color=gender_dist.index,
        title='Treatment Rate by Gender (for employees with work interference)',
        labels={'x': 'Gender', 'Yes': 'Treatment Rate (%)'}
    )
    return fig


# -------------------------------------------------------------------- #
# --- PRESENTER 4: THE CULTURE OFFICER ---
# -------------------------------------------------------------------- #

def plot_q10_mental_vs_physical_consequences() -> go.Figure:
    """
    Answers Q10: Do employees expect more negative consequences for mental vs. physical health?
    Generates side-by-side pie charts for comparison.
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Consequences for<br>Mental Health', 'Consequences for<br>Physical Health'),
        specs=[[{'type':'domain'}, {'type':'domain'}]]
    )
    mental_counts = df['mental_health_consequence'].value_counts()
    fig.add_trace(go.Pie(labels=mental_counts.index, values=mental_counts.values, name="Mental"), 1, 1)
    
    phys_counts = df['phys_health_consequence'].value_counts()
    fig.add_trace(go.Pie(labels=phys_counts.index, values=phys_counts.values, name="Physical"), 1, 2)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(title_text="Perceived Negative Consequences: Mental vs. Physical Health")
    return fig

def plot_q11_fear_vs_treatment() -> go.Figure:
    """
    Answers Q11: Does fear of consequences stop people from getting treatment?
    Generates a bar chart comparing treatment rates.
    """
    fear_dist = pd.crosstab(df['mental_health_consequence'], df['treatment'], normalize='index').mul(100)
    fear_dist = fear_dist.sort_values(by='Yes', ascending=False)
    fig = px.bar(
        fear_dist,
        x=fear_dist.index, y='Yes',
        title='Impact of Fearing Consequences on Seeking Treatment',
        labels={'x': 'Fears Negative Consequences?', 'Yes': 'Treatment Rate (%)'}
    )
    return fig

def plot_q12_trust_circle() -> go.Figure:
    """
    Answers Q12: Who do employees trust? (Coworkers vs. Supervisors).
    Generates side-by-side bar charts for comparison.
    """
    category_order = ['Yes', 'Some of them', 'No']
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Willingness to Discuss<br>with Coworkers', 'Willingness to Discuss<br>with Supervisor')
    )
    coworker_counts = df['coworkers'].value_counts().reindex(category_order)
    fig.add_trace(go.Bar(x=coworker_counts.index, y=coworker_counts.values, name='Coworkers'), 1, 1)
    
    supervisor_counts = df['supervisor'].value_counts().reindex(category_order)
    fig.add_trace(go.Bar(x=supervisor_counts.index, y=supervisor_counts.values, name='Supervisor'), 1, 2)
    
    fig.update_layout(title_text="Whom Do Employees Trust with Mental Health Discussions?", showlegend=False)
    return fig


# -------------------------------------------------------------------- #
# --- PRESENTER 5: THE WORKPLACE ENVIRONMENT ANALYST ---
# -------------------------------------------------------------------- #

def plot_q13_seriousness_perception() -> go.Figure:
    """
    Answers Q13: Do employees feel their company takes mental health as seriously as physical health?
    Generates a pie chart to show the distribution of opinions.
    """
    seriousness_counts = df['mental_vs_physical'].value_counts()
    fig = px.pie(
        names=seriousness_counts.index,
        values=seriousness_counts.values,
        title='Is Mental Health Taken as Seriously as Physical Health?',
        hole=0.4
    )
    return fig

def plot_q14_witnessed_consequences_by_tech() -> go.Figure:
    """
    Answers Q14: Have employees witnessed negative consequences for others,
    and is this more common in tech companies?
    """
    witness_dist = pd.crosstab(df['tech_company'], df['obs_consequence'], normalize='index').mul(100)
    fig = px.bar(
        witness_dist,
        x=witness_dist.index, y='Yes',
        title='Percentage of Employees Who Witnessed Negative Consequences',
        labels={'x': 'Is it a Tech Company?', 'Yes': '% Who Witnessed Consequences'},
        color=witness_dist.index
    )
    return fig

def plot_q15_witnessing_vs_treatment() -> go.Figure:
    """
    Answers Q15: Does witnessing negative events correlate with a lower personal treatment rate?
    """
    witness_treatment_dist = pd.crosstab(df['obs_consequence'], df['treatment'], normalize='index').mul(100)
    fig = px.bar(
        witness_treatment_dist,
        x=witness_treatment_dist.index, y='Yes',
        title='Impact of Witnessing Consequences on Seeking Treatment',
        labels={'x': 'Have You Witnessed Negative Consequences?', 'Yes': 'Personal Treatment Rate (%)'},
        color=witness_treatment_dist.index
    )
    return fig


# -------------------------------------------------------------------- #
# --- PRESENTER 6: THE MODERN WORKPLACE STRATEGIST ---
# -------------------------------------------------------------------- #

def plot_q16_remote_work_vs_treatment() -> go.Figure:
    """
    Answers Q16: How does remote work affect the likelihood of seeking treatment?
    """
    remote_dist = pd.crosstab(df['remote_work'], df['treatment'], normalize='index').mul(100)
    fig = px.bar(
        remote_dist,
        x=remote_dist.index, y='Yes',
        title='Treatment Rate by Work Location',
        labels={'x': 'Works Remotely?', 'Yes': 'Treatment Rate (%)'},
        color=remote_dist.index
    )
    return fig

def plot_q17_remote_work_vs_leave() -> go.Figure:
    """
    Answers Q17: Do remote workers find it easier or harder to take medical leave?
    """
    leave_dist = df.groupby('remote_work')['leave'].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
    fig = px.bar(
        leave_dist,
        x='leave', y='percentage', color='remote_work', barmode='group',
        title='Perception of Leave Accessibility by Work Location',
        labels={'leave': 'Ease of Taking Medical Leave', 'percentage': 'Percentage of Employees'}
    )
    return fig

def plot_q18_summary_top_factors() -> go.Figure:
    """
    Answers Q18: What are the top 3 most significant factors?
    Calculates and plots the factors with the highest impact on seeking treatment.
    """
    factors = {}
    
    fh_crosstab = pd.crosstab(df['family_history'], df['treatment'], normalize='index')
    factors['Family History'] = fh_crosstab.loc['Yes', 'Yes'] - fh_crosstab.loc['No', 'Yes']
    
    wi_crosstab = pd.crosstab(df['work_interfere'], df['treatment'], normalize='index')
    factors['Work Interference (Often vs. Never)'] = wi_crosstab.loc['Often', 'Yes'] - wi_crosstab.loc['Never', 'Yes']
    
    fc_crosstab = pd.crosstab(df['mental_health_consequence'], df['treatment'], normalize='index')
    factors['Fearing Consequences'] = fc_crosstab.loc['Yes', 'Yes'] - fc_crosstab.loc['No', 'Yes']

    summary_df = pd.DataFrame.from_dict(factors, orient='index', columns=['ImpactScore'])
    summary_df = summary_df.sort_values('ImpactScore', ascending=True)
    summary_df['ImpactScore'] = summary_df['ImpactScore'] * 100

    fig = px.bar(
        summary_df,
        x='ImpactScore', y=summary_df.index, orientation='h',
        title='Most Influential Factors on Seeking Treatment',
        labels={'ImpactScore': 'Increase in Likelihood of Seeking Treatment (%)', 'y': 'Factor'}
    )
    return fig

# File Path: employee_wellness_project/analysis.py
# (Append this code to the existing file)


# -------------------------------------------------------------------- #
# --- KPI CALCULATION FUNCTIONS FOR SUMMARY DASHBOARD ---
# -------------------------------------------------------------------- #

def get_kpi_treatment_rate() -> str:
    """Calculates the overall treatment rate as a formatted string."""
    rate = df['treatment'].value_counts(normalize=True).loc['Yes'] * 100
    return f"{rate:.1f}%"

def get_kpi_family_history() -> str:
    """Calculates the percentage of employees with a family history."""
    rate = df['family_history'].value_counts(normalize=True).loc['Yes'] * 100
    return f"{rate:.1f}%"

def get_kpi_fear_consequences() -> str:
    """Calculates the percentage of employees who fear negative consequences."""
    rate = df['mental_health_consequence'].value_counts(normalize=True).loc['Yes'] * 100
    return f"{rate:.1f}%"

# -------------------------------------------------------------------- #
# --- ADDITIONAL FUNCTIONS FOR SUMMARY DASHBOARD ---
# -------------------------------------------------------------------- #

def plot_summary_benefits_vs_treatment() -> go.Figure:
    """
    Answers: Does offering benefits correlate with higher treatment rates?
    Generates a bar chart comparing treatment rates for employees with/without benefits.
    """
    # Calculate treatment rate based on whether the employer provides benefits
    benefits_dist = pd.crosstab(df['benefits'], df['treatment'], normalize='index').mul(100)
    
    fig = px.bar(
        benefits_dist,
        x=benefits_dist.index,
        y='Yes',
        title='Treatment Rate by Benefits Availability',
        labels={'x': 'Employer Provides Benefits?', 'Yes': 'Treatment Rate (%)'},
        color=benefits_dist.index,
        color_discrete_map={
            "Yes": THEME_COLORS['accent1'],
            "No": THEME_COLORS['accent2'],
            "Don't know": "#CCCCCC"
        }
    )
    return fig

# -------------------------------------------------------------------- #
# --- CONSOLIDATED TEST BLOCK ---
# --- Uncomment the functions you want to test ---
# -------------------------------------------------------------------- #
if __name__ == '__main__':
    print("Running analysis functions to generate test plots...")
    
    # --- Presenter 1 ---
    # fig1, fig2 = plot_q1_demographics()
    # fig1.show()
    # fig2.show()
    # fig3 = plot_q2_workplace_landscape()
    # fig3[0].show() # fig3 is a tuple of figures
    # fig3[1].show()
    # fig4 = plot_q3_family_history()
    # fig4.show()

    # --- Presenter 2 ---
    # fig5 = plot_q4_formal_support()
    # fig5.show()
    # fig6 = plot_q5_care_options_by_size()
    # fig6.show()
    # fig7 = plot_q6_leave_vs_treatment()
    # fig7.show()
    
    # --- Presenter 3 ---
    # fig8 = plot_q7_treatment_vs_family_history()
    # fig8.show()
    # fig9 = plot_q8_work_interference_vs_treatment()
    # fig9.show()
    # fig10 = plot_q9_gender_disparity_under_interference()
    # fig10.show()

    # --- Presenter 4 ---
    # fig11 = plot_q10_mental_vs_physical_consequences()
    # fig11.show()
    # fig12 = plot_q11_fear_vs_treatment()
    # fig12.show()
    # fig13 = plot_q12_trust_circle()
    # fig13.show()

    # --- Presenter 5 ---
    # fig14 = plot_q13_seriousness_perception()
    # fig14.show()
    # fig15 = plot_q14_witnessed_consequences_by_tech()
    # fig15.show()
    # fig16 = plot_q15_witnessing_vs_treatment()
    # fig16.show()

    # --- Presenter 6 ---
    # fig17 = plot_q16_remote_work_vs_treatment()
    # fig17.show()
    # fig18 = plot_q17_remote_work_vs_leave()
    # fig18.show()
    fig19 = plot_q18_summary_top_factors()
    fig19.show()

    print("Test plots generated.")

