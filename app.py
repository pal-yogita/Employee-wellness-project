# File Path: employee_wellness_project/app.py
# This is the main Flask application file.

from flask import Flask, render_template, url_for
import analysis as an # We import our analysis file and give it a shorter name 'an'

# Initialize the Flask application
app = Flask(__name__)

# --- Route for the Homepage / Presentation Lobby ---
@app.route('/')
def index():
    """
    This function renders the homepage of our application.
    It will list the 6 presenters and their questions.
    """
    # For now, we just render the template. We'll add more later.
    return render_template('index.html')

# --- Routes for each Presenter's Dashboard ---

@app.route('/presenter/1')
def presenter_1():
    """Dashboard for Presenter 1: The HR Generalist"""
    chart1, chart2 = an.plot_q1_demographics()
    chart3 = an.plot_q3_family_history()
    
    # Convert plotly figures to HTML
    chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn')
    chart2_html = chart2.to_html(full_html=False, include_plotlyjs='cdn')
    chart3_html = chart3.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('presenter_dashboard.html', 
                           presenter_name="The HR Generalist",
                           q1="What is our demographic profile?", 
                           q2="What is our workplace landscape?", 
                           q3="What is the baseline risk from family history?",
                           chart1=chart1_html, 
                           chart2=chart2_html, 
                           chart3=chart3_html)

@app.route('/presenter/2')
def presenter_2():
    """Dashboard for Presenter 2: The Benefits Specialist"""
    chart1 = an.plot_q4_formal_support()
    chart2 = an.plot_q5_care_options_by_size()
    chart3 = an.plot_q6_leave_vs_treatment()
    
    chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn')
    chart2_html = chart2.to_html(full_html=False, include_plotlyjs='cdn')
    chart3_html = chart3.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('presenter_dashboard.html',
                           presenter_name="The Benefits Specialist",
                           q1="How comprehensive is our formal support?",
                           q2="Are employees aware of care options?",
                           q3="How does leave accessibility impact treatment?",
                           chart1=chart1_html, 
                           chart2=chart2_html, 
                           chart3=chart3_html)

# We will continue this pattern for all 6 presenters...

@app.route('/presenter/3')
def presenter_3():
    """Dashboard for Presenter 3: The Lead Analyst"""
    chart1 = an.plot_q7_treatment_vs_family_history()
    chart2 = an.plot_q8_work_interference_vs_treatment()
    chart3 = an.plot_q9_gender_disparity_under_interference()

    chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn')
    chart2_html = chart2.to_html(full_html=False, include_plotlyjs='cdn')
    chart3_html = chart3.to_html(full_html=False, include_plotlyjs='cdn')
    
    return render_template('presenter_dashboard.html',
                           presenter_name="The Lead Analyst",
                           q1="How does family history impact treatment?",
                           q2="How does work interference predict treatment?",
                           q3="Is there a gender disparity in seeking help?",
                           chart1=chart1_html, 
                           chart2=chart2_html, 
                           chart3=chart3_html)

@app.route('/presenter/4')
def presenter_4():
    """Dashboard for Presenter 4: The Culture Officer"""
    chart1 = an.plot_q10_mental_vs_physical_consequences()
    chart2 = an.plot_q11_fear_vs_treatment()
    chart3 = an.plot_q12_trust_circle()

    chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn')
    chart2_html = chart2.to_html(full_html=False, include_plotlyjs='cdn')
    chart3_html = chart3.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('presenter_dashboard.html',
                           presenter_name="The Culture Officer",
                           q1="Is mental health stigma greater than physical?",
                           q2="Does fear of consequences prevent treatment?",
                           q3="Who do employees trust more: coworkers or supervisors?",
                           chart1=chart1_html, 
                           chart2=chart2_html, 
                           chart3=chart3_html)

@app.route('/presenter/5')
def presenter_5():
    """Dashboard for Presenter 5: The Workplace Environment Analyst"""
    chart1 = an.plot_q13_seriousness_perception()
    chart2 = an.plot_q14_witnessed_consequences_by_tech()
    chart3 = an.plot_q15_witnessing_vs_treatment()

    chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn')
    chart2_html = chart2.to_html(full_html=False, include_plotlyjs='cdn')
    chart3_html = chart3.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('presenter_dashboard.html',
                           presenter_name="The Workplace Environment Analyst",
                           q1="Is mental health taken seriously?",
                           q2="Are negative consequences witnessed more in tech?",
                           q3="Does witnessing negativity reduce treatment rates?",
                           chart1=chart1_html, 
                           chart2=chart2_html, 
                           chart3=chart3_html)

@app.route('/presenter/6')
def presenter_6():
    """Dashboard for Presenter 6: The Modern Workplace Strategist"""
    chart1 = an.plot_q16_remote_work_vs_treatment()
    chart2 = an.plot_q17_remote_work_vs_leave()
    chart3 = an.plot_q18_summary_top_factors()

    chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn')
    chart2_html = chart2.to_html(full_html=False, include_plotlyjs='cdn')
    chart3_html = chart3.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('presenter_dashboard.html',
                           presenter_name="The Modern Workplace Strategist",
                           q1="How does remote work affect treatment rates?",
                           q2="Does remote work impact taking leave?",
                           q3="What are the top 3 summary factors?",
                           chart1=chart1_html, 
                           chart2=chart2_html, 
                           chart3=chart3_html)

# File Path: employee_wellness_project/app.py
# (Append this code before the final 'if' block)


# --- Route for the Final Summary Dashboard ---
@app.route('/summary')
def summary():
    """Renders the comprehensive summary dashboard page."""
    
    # 1. Fetch KPIs
    kpi_treatment = an.get_kpi_treatment_rate()
    kpi_family_history = an.get_kpi_family_history()
    kpi_fear = an.get_kpi_fear_consequences()

    # 2. Fetch the 5 selected charts for the dashboard
    hero_chart = an.plot_q18_summary_top_factors()
    stigma_chart_1 = an.plot_q10_mental_vs_physical_consequences()
    stigma_chart_2 = an.plot_q15_witnessing_vs_treatment()
    drivers_chart_1 = an.plot_q8_work_interference_vs_treatment()
    drivers_chart_2 = an.plot_summary_benefits_vs_treatment() # Our new chart

    # 3. Convert all charts to HTML
    hero_html = hero_chart.to_html(full_html=False, include_plotlyjs='cdn')
    stigma_1_html = stigma_chart_1.to_html(full_html=False, include_plotlyjs='cdn')
    stigma_2_html = stigma_chart_2.to_html(full_html=False, include_plotlyjs='cdn')
    drivers_1_html = drivers_chart_1.to_html(full_html=False, include_plotlyjs='cdn')
    drivers_2_html = drivers_chart_2.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 4. Render the template with all the necessary data
    return render_template('summary_dashboard.html',
                           kpi_treatment=kpi_treatment,
                           kpi_family_history=kpi_family_history,
                           kpi_fear=kpi_fear,
                           hero_chart=hero_html,
                           stigma_chart_1=stigma_1_html,
                           stigma_chart_2=stigma_2_html,
                           drivers_chart_1=drivers_1_html,
                           drivers_chart_2=drivers_2_html
                           )

# This block allows us to run the app directly from the command line
if __name__ == '__main__':
    app.run(debug=True)