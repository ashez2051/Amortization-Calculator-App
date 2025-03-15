import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
import numpy as np

# Set page configuration for a polished look
st.set_page_config(
    page_title="Elegant Loan Calculator",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💰"
)

# Custom CSS for modern UI design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2c3e50;
    }

    .main {
        padding: 2.5rem;
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.95);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }

    h1 {
        font-weight: 700;
        color: #1e3a8a;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        font-size: 2.5rem;
    }

    h2, h3 {
        color: #1e3a8a;
        font-weight: 600;
        margin-top: 1.5rem;
    }

    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 20px rgba(59, 130, 246, 0.5);
    }

    .stButton>button:active {
        transform: translateY(-1px);
    }

    .metric-card {
        background-color: white;
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
        border-left: 5px solid #3b82f6;
        margin-bottom: 24px;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }

    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3a8a;
    }

    .sidebar .stSelectbox label, .sidebar .stNumberInput label {
        font-weight: 600;
        color: #1e3a8a;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .stExpander {
        border-radius: 12px;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    /* Sidebar styling */
    .sidebar .stSelectbox, .sidebar .stNumberInput {
        background-color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    .sidebar [data-testid="stSidebarNav"] {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 1rem;
        border-radius: 12px;
    }

    /* Custom input field styling */
    input[type="number"] {
        border-radius: 8px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
    }

    input[type="number"]:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* Info box styling */
    .stAlert {
        background-color: rgba(59, 130, 246, 0.1);
        border-left: 5px solid #3b82f6;
        color: #1e3a8a;
        padding: 1.2rem;
        border-radius: 12px;
    }

    /* Additional UI elements */
    .nav-pill {
        display: inline-block;
        padding: 10px 20px;
        margin: 5px;
        background-color: #f8fafc;
        border-radius: 50px;
        color: #64748b;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .nav-pill:hover, .nav-pill.active {
        background-color: #3b82f6;
        color: white;
    }

    /* Table styling */
    table {
        border-radius: 12px;
        overflow: hidden;
    }

    thead tr th {
        background-color: #f1f5f9 !important;
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }

    tbody tr:nth-child(even) {
        background-color: #f8fafc !important;
    }

    </style>
""", unsafe_allow_html=True)

# Icon set for the app
icons = {
    "mortgage": "🏠",
    "car": "🚗",
    "personal": "💼",
    "education": "🎓",
    "payment": "💰",
    "term": "⏱️",
    "interest": "💹"
}

def calculate_amortization_schedule(principal, annual_rate, monthly_payment, extra_payment=0, start_date=None):
    monthly_rate = annual_rate / 100 / 12
    balance = principal
    schedule = []
    total_interest = 0
    month = 0
    current_date = start_date if start_date else date.today()

    while balance > 0:
        interest = balance * monthly_rate
        total_interest += interest
        principal_payment = monthly_payment + extra_payment - interest

        if principal_payment > balance:
            principal_payment = balance
            monthly_payment = interest + principal_payment

        balance -= principal_payment
        month += 1

        # Calculate date for this payment
        payment_date = current_date.replace(month=((current_date.month - 1 + month) % 12) + 1,
                                           year=current_date.year + ((current_date.month - 1 + month) // 12))

        schedule.append([
            month,
            payment_date.strftime("%b %Y"),
            round(monthly_payment + extra_payment, 2),
            round(interest, 2),
            round(principal_payment, 2),
            round(balance, 2)
        ])

    df = pd.DataFrame(
        schedule,
        columns=["Payment #", "Date", "Total Payment", "Interest", "Principal", "Remaining Balance"]
    )
    return df, month, total_interest

def plot_amortization(df, loan_type="mortgage"):
    # Create a custom color scheme based on loan type
    colors = {
        "mortgage": {"balance": "#3b82f6", "interest": "#ef4444"},
        "car": {"balance": "#10b981", "interest": "#f97316"},
        "personal": {"balance": "#8b5cf6", "interest": "#f43f5e"},
        "education": {"balance": "#06b6d4", "interest": "#a855f7"}
    }

    selected_colors = colors.get(loan_type, colors["mortgage"])

    # Create the figure
    fig = go.Figure()

    # Add traces with improved styling
    fig.add_trace(go.Scatter(
        x=df["Payment #"],
        y=df["Remaining Balance"],
        name="Remaining Balance",
        line=dict(color=selected_colors["balance"], width=4),
        fill='tozeroy',
        fillcolor=f"rgba({int(selected_colors['balance'][1:3], 16)}, {int(selected_colors['balance'][3:5], 16)}, {int(selected_colors['balance'][5:7], 16)}, 0.1)"
    ))

    fig.add_trace(go.Scatter(
        x=df["Payment #"],
        y=df["Interest"].cumsum(),
        name="Cumulative Interest",
        line=dict(color=selected_colors["interest"], width=4),
        fill='tozeroy',
        fillcolor=f"rgba({int(selected_colors['interest'][1:3], 16)}, {int(selected_colors['interest'][3:5], 16)}, {int(selected_colors['interest'][5:7], 16)}, 0.1)"
    ))

    # Update layout with more professional styling
    fig.update_layout(
        title=dict(
            text="Loan Amortization Visualization",
            font=dict(family="Poppins, sans-serif", size=24, color="#1e3a8a"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(
                text="Payment Number",
                font=dict(family="Poppins, sans-serif", size=14, color="#64748b")
            ),
            showgrid=True,
            gridcolor='rgba(220, 220, 220, 0.4)',
            zeroline=False,
            tickfont=dict(family="Poppins, sans-serif", size=12, color="#64748b")
        ),
        yaxis=dict(
            title=dict(
                text="Amount ($)",
                font=dict(family="Poppins, sans-serif", size=14, color="#64748b")
            ),
            showgrid=True,
            gridcolor='rgba(220, 220, 220, 0.4)',
            zeroline=False,
            tickfont=dict(family="Poppins, sans-serif", size=12, color="#64748b")
        ),
        legend=dict(
            y=1.02,
            x=1,
            xanchor='right',
            yanchor='bottom',
            orientation='h',
            font=dict(family="Poppins, sans-serif", size=14, color="#64748b")
        ),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=80, b=40),
        height=500
    )

    # Add custom hover template
    fig.update_traces(
        hovertemplate="<b>Payment #%{x}</b><br>Amount: $%{y:,.2f}<extra></extra>"
    )

    return fig

def plot_payment_breakdown(principal, total_interest):
    labels = ['Principal', 'Interest']
    values = [principal, total_interest]
    colors = ['#3b82f6', '#ef4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        textinfo='label+percent',
        marker=dict(colors=colors)
    )])

    fig.update_layout(
        title=dict(
            text="Total Payment Breakdown",
            font=dict(family="Poppins, sans-serif", size=20, color="#1e3a8a"),
            x=0.5,
            xanchor='center'
        ),
        legend=dict(
            font=dict(family="Poppins, sans-serif", size=14, color="#64748b")
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig

def plot_monthly_breakdown(monthly_payment, extra_payment=0):
    # Create data for the monthly payment breakdown
    payment_data = pd.DataFrame({
        'Category': ['Regular Payment', 'Extra Payment'],
        'Amount': [monthly_payment, extra_payment]
    })

    # Filter out zero values
    payment_data = payment_data[payment_data['Amount'] > 0]

    fig = px.bar(
        payment_data,
        x='Category',
        y='Amount',
        color='Category',
        color_discrete_map={
            'Regular Payment': '#3b82f6',
            'Extra Payment': '#10b981'
        },
        text_auto='.2f'
    )

    fig.update_layout(
        title=dict(
            text="Monthly Payment Breakdown",
            font=dict(family="Poppins, sans-serif", size=20, color="#1e3a8a"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="",
            showgrid=False
        ),
        yaxis=dict(
            title="Amount ($)",
            titlefont=dict(family="Poppins, sans-serif", size=14, color="#64748b")
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_traces(
        texttemplate='$%{text}',
        textposition='outside'
    )

    return fig

def plot_comparison(data, title="Payment Comparison"):
    fig = px.bar(
        data,
        x='Category',
        y='Amount',
        color='Category',
        color_discrete_map={
            'Old Payment': '#ef4444',
            'New Payment': '#3b82f6',
            'Old Interest': '#f97316',
            'New Interest': '#10b981'
        },
        text_auto='.2f'
    )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Poppins, sans-serif", size=20, color="#1e3a8a"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="",
            showgrid=False
        ),
        yaxis=dict(
            title="Amount ($)",
            titlefont=dict(family="Poppins, sans-serif", size=14, color="#64748b")
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_traces(
        texttemplate='$%{text}',
        textposition='outside'
    )

    return fig

def main():
    # App header with animation effect
    st.markdown("""
        <div style="text-align: center; animation: fadeIn 1.5s;">
            <h1>💰 Elegant Loan Amortization Calculator</h1>
            <p style="font-size: 1.2rem; color: #64748b; margin-bottom: 2rem;">
                Make informed financial decisions with our powerful visualization tools
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for organization
    tabs = st.tabs(["📊 Calculator"])

    # Define start_date at the beginning of the main function
    start_date = date.today().replace(day=1)

    with tabs[0]:
        with st.sidebar:
            st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h3 style="color: #1e3a8a;">⚙️ Loan Parameters</h3>
                </div>
            """, unsafe_allow_html=True)

            # Add loan type selector with icons
            loan_type = st.selectbox(
                "Loan Type",
                ["Mortgage Loan 🏠", "Auto Loan 🚗", "Personal Loan 💼", "Education Loan 🎓"],
                index=0,
                format_func=lambda x: x
            )
            loan_type_key = loan_type.split()[0].lower()

            # Add calculation mode selector
            option = st.selectbox(
                "Calculation Mode",
                [
                    f"{icons['payment']} Calculate Monthly Payment",
                    f"{icons['term']} Calculate Loan Term",
                    f"{icons['interest']} Calculate Interest Saved"
                ],
                help="Choose the type of calculation you want to perform."
            )
            option = option[2:]  # Remove the icon from the string

            # Add collapsible settings section
            with st.expander("Loan Basics", expanded=True):
                principal = st.number_input(
                    "Loan Amount ($)",
                    min_value=0.0,
                    value=250000.0 if loan_type_key == "mortgage" else
                          30000.0 if loan_type_key == "auto" else
                          15000.0 if loan_type_key == "personal" else 50000.0,
                    step=1000.0,
                    format="%.2f"
                )

                # Different default rates based on loan type
                default_rate = 5.5 if loan_type_key == "mortgage" else 7.5 if loan_type_key == "auto" else 10.5 if loan_type_key == "personal" else 6.0
                annual_rate = st.number_input(
                    "Annual Interest Rate (%)",
                    min_value=0.0,
                    value=default_rate,
                    step=0.1,
                    format="%.2f"
                )

            # Add information about the app in the sidebar
            with st.expander("About This Calculator"):
                st.markdown("""
                    <div style="font-size: 0.9rem;">
                        <p>This advanced loan calculator helps you understand the full impact of loan terms, interest rates, and extra payments.</p>
                        <p>Visualize your loan amortization schedule and make better financial decisions.</p>
                    </div>
                """, unsafe_allow_html=True)

        # Main calculation area
        main_container = st.container()

        with main_container:
            col1, col2 = st.columns([2, 1])

            with col1:
                if option == "Calculate Monthly Payment":
                    years = st.slider(
                        "Loan Term (Years)",
                        min_value=1,
                        max_value=40 if loan_type_key == "mortgage" else 10 if loan_type_key == "auto" else 7,
                        value=30 if loan_type_key == "mortgage" else 5 if loan_type_key == "auto" else 3,
                        step=1
                    )

                    extra_payment = st.number_input(
                        "Extra Monthly Payment ($)",
                        min_value=0.0,
                        value=0.0,
                        step=50.0,
                        format="%.2f",
                        help="Additional amount to pay each month towards principal."
                    )

                    num_payments = years * 12
                    monthly_rate = annual_rate / 100 / 12

                    monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments) if monthly_rate > 0 else principal / num_payments

                    calc_button = st.button("Calculate Payment Plan", type="primary", use_container_width=True)
                    if calc_button:
                        with st.spinner("Analyzing your loan..."):
                            # Add a slight delay for effect
                            import time
                            time.sleep(0.5)

                            # Calculate schedules
                            schedule, months, total_interest = calculate_amortization_schedule(
                                principal, annual_rate, monthly_payment, extra_payment, start_date
                            )
                            years_reduced = months // 12
                            normal_schedule, normal_months, normal_interest = calculate_amortization_schedule(
                                principal, annual_rate, monthly_payment, 0, start_date
                            )
                            interest_saved = normal_interest - total_interest
                            time_saved = normal_months - months

                            # Display metrics in cards
                            st.markdown("### 📈 Your Loan Overview")
                            col_metrics = st.columns(4)
                            with col_metrics[0]:
                                st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-label">Monthly Payment</div>
                                        <div class="metric-value">${monthly_payment:.2f}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col_metrics[1]:
                                st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-label">Payoff Time</div>
                                        <div class="metric-value">{years_reduced} yrs {months % 12} mths</div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col_metrics[2]:
                                st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-label">Total Interest</div>
                                        <div class="metric-value">${total_interest:,.2f}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                            with col_metrics[3]:
                                st.markdown(f"""
                                    <div class="metric-card" style="border-left: 5px solid #10b981;">
                                        <div class="metric-label">Interest Saved</div>
                                        <div class="metric-value" style="color: #10b981;">${interest_saved:,.2f}</div>
                                    </div>
                                """, unsafe_allow_html=True)

                            # Display additional metrics if extra payments are made
                            if extra_payment > 0:
                                st.markdown("### 🚀 Time & Money Saved With Extra Payments")
                                time_metric, money_metric = st.columns(2)
                                with time_metric:
                                    months_saved = normal_months - months
                                    years_saved = months_saved // 12
                                    months_remainder = months_saved % 12
                                    st.markdown(f"""
                                        <div class="metric-card" style="border-left: 5px solid #8b5cf6;">
                                            <div class="metric-label">Time Saved</div>
                                            <div class="metric-value" style="color: #8b5cf6;">
                                                {years_saved} yrs {months_remainder} mths
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                with money_metric:
                                    st.markdown(f"""
                                        <div class="metric-card" style="border-left: 5px solid #f97316;">
                                            <div class="metric-label">Money Saved</div>
                                            <div class="metric-value" style="color: #f97316;">
                                                ${normal_interest - total_interest:,.2f}
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)

                            # Create tabs for different visualizations
                            viz_tab1, viz_tab2, viz_tab3 = st.tabs([
                                "Amortization Chart",
                                "Payment Breakdown",
                                "Detailed Schedule"
                            ])

                            with viz_tab1:
                                st.plotly_chart(
                                    plot_amortization(schedule, loan_type_key),
                                    use_container_width=True
                                )

                            with viz_tab2:
                                col_pie, col_bar = st.columns(2)
                                with col_pie:
                                    st.plotly_chart(
                                        plot_payment_breakdown(principal, total_interest),
                                        use_container_width=True
                                    )
                                with col_bar:
                                    if extra_payment > 0:
                                        st.plotly_chart(
                                            plot_monthly_breakdown(monthly_payment, extra_payment),
                                            use_container_width=True
                                        )
                                    else:
                                        st.info("Add extra monthly payments to see payment breakdown.")

                            with viz_tab3:
                                st.dataframe(
                                    schedule.style.format({
                                        "Total Payment": "${:,.2f}",
                                        "Interest": "${:,.2f}",
                                        "Principal": "${:,.2f}",
                                        "Remaining Balance": "${:,.2f}"
                                    }),
                                    use_container_width=True,
                                    height=400
                                )
                elif option == "Calculate Loan Term":
                    # Calculate the minimum payment required (interest-only payment)
                    min_payment = principal * (annual_rate / 100 / 12) if annual_rate > 0 else 1.0

                    # Set a reasonable default payment that would pay off the loan in a reasonable time
                    default_payment = max(min_payment * 1.5, principal / (30 * 12))

                    st.info(f"Minimum payment required (interest only): ${min_payment:.2f}")

                    monthly_payment = st.number_input(
                        "Monthly Payment ($)",
                        min_value=float(min_payment + 0.01),  # Slightly above interest-only payment
                        value=float(default_payment),
                        step=10.0,
                        format="%.2f",
                        help="Amount you can pay monthly. Must be greater than minimum interest payment."
                    )

                    extra_payment = st.number_input(
                        "Extra Monthly Payment ($)",
                        min_value=0.0,
                        value=0.0,
                        step=50.0,
                        format="%.2f"
                    )

                    # Create a placeholder for results
                    results_placeholder = st.empty()

                    # Debug: Print input values to console
                    st.write(f"Debug - Principal: ${principal}, Rate: {annual_rate}%, Monthly Payment: ${monthly_payment}, Extra: ${extra_payment}")

                    # Make the button more prominent
                    st.markdown("### Click below to calculate your loan term")
                    calc_button = st.button("Calculate Loan Term", type="primary", use_container_width=True)

                    if calc_button:
                        try:
                            with st.spinner("Calculating your loan term..."):
                                import time
                                time.sleep(0.5)  # Simulate processing delay

                                # Calculate the amortization schedule
                                schedule, months, total_interest = calculate_amortization_schedule(
                                    principal, annual_rate, monthly_payment, extra_payment, start_date
                                )

                                # Debug: Print calculation results
                                st.write(f"Debug - Months: {months}, Total Interest: ${total_interest:.2f}, Schedule Length: {len(schedule)}")

                                if months <= 0 or len(schedule) == 0:
                                    results_placeholder.error("The payment amount is too small to pay off the loan or an error occurred. Please increase your monthly payment or check inputs.")
                                else:
                                    years = months // 12

                                    # Use the results placeholder to display results
                                    with results_placeholder.container():
                                        st.markdown("### 📊 Term Analysis Results")

                                        col_metrics = st.columns(3)
                                        with col_metrics[0]:
                                            st.markdown(f"""
                                                <div class="metric-card">
                                                    <div class="metric-label">Payoff Time</div>
                                                    <div class="metric-value">{years} yrs {months % 12} mths</div>
                                                </div>
                                            """, unsafe_allow_html=True)
                                        with col_metrics[1]:
                                            st.markdown(f"""
                                                <div class="metric-card">
                                                    <div class="metric-label">Total Interest</div>
                                                    <div class="metric-value">${total_interest:,.2f}</div>
                                                </div>
                                            """, unsafe_allow_html=True)
                                        with col_metrics[2]:
                                            st.markdown(f"""
                                                <div class="metric-card">
                                                    <div class="metric-label">Total Payments</div>
                                                    <div class="metric-value">${principal + total_interest:,.2f}</div>
                                                </div>
                                            """, unsafe_allow_html=True)

                                        # Create tabs for different visualizations
                                        viz_tab1, viz_tab2 = st.tabs(["Amortization Chart", "Detailed Schedule"])

                                        with viz_tab1:
                                            st.plotly_chart(
                                                plot_amortization(schedule, loan_type_key),
                                                use_container_width=True
                                            )

                                        with viz_tab2:
                                            st.dataframe(
                                                schedule.style.format({
                                                    "Total Payment": "${:,.2f}",
                                                    "Interest": "${:,.2f}",
                                                    "Principal": "${:,.2f}",
                                                    "Remaining Balance": "${:,.2f}"
                                                }),
                                                use_container_width=True,
                                                height=400
                                            )
                        except Exception as e:
                            st.error(f"Error during calculation: {str(e)}")
                            st.write("Debug - Exception occurred, check inputs or code logic.")
                elif option == "Calculate Interest Saved":
                        # Get baseline information
                        years = st.slider(
                            "Original Loan Term (Years)",
                            min_value=1,
                            max_value=40 if loan_type_key == "mortgage" else 10 if loan_type_key == "auto" else 7,
                            value=30 if loan_type_key == "mortgage" else 5 if loan_type_key == "auto" else 3
                        )

                        num_payments = years * 12
                        monthly_rate = annual_rate / 100 / 12

                        # Calculate original monthly payment
                        monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments) if monthly_rate > 0 else principal / num_payments

                        # Get extra payment information
                        extra_payment = st.number_input(
                            "Extra Monthly Payment ($)",
                            min_value=0.0,
                            value=100.0,
                            step=50.0,
                            format="%.2f"
                        )

                        calc_button = st.button("Calculate Interest Saved", type="primary", use_container_width=True)
                        if calc_button:
                            with st.spinner("Calculating potential savings..."):
                                # Add a slight delay for effect
                                import time
                                time.sleep(0.5)

                                # Calculate original payment schedule
                                original_schedule, original_months, original_interest = calculate_amortization_schedule(
                                    principal, annual_rate, monthly_payment, 0, start_date
                                )

                                # Calculate accelerated payment schedule
                                new_schedule, new_months, new_interest = calculate_amortization_schedule(
                                    principal, annual_rate, monthly_payment, extra_payment, start_date
                                )

                                # Calculate savings
                                interest_saved = original_interest - new_interest
                                time_saved = original_months - new_months
                                years_saved = time_saved // 12
                                months_saved = time_saved % 12

                                # Display metrics in cards
                                st.markdown("### 💰 Interest Savings Analysis")

                                col_metrics = st.columns(3)
                                with col_metrics[0]:
                                    st.markdown(f"""
                                        <div class="metric-card" style="border-left: 5px solid #10b981;">
                                            <div class="metric-label">Interest Saved</div>
                                            <div class="metric-value" style="color: #10b981;">${interest_saved:,.2f}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                with col_metrics[1]:
                                    st.markdown(f"""
                                        <div class="metric-card" style="border-left: 5px solid #8b5cf6;">
                                            <div class="metric-label">Time Saved</div>
                                            <div class="metric-value" style="color: #8b5cf6;">{years_saved} yrs {months_saved} mths</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                with col_metrics[2]:
                                    st.markdown(f"""
                                        <div class="metric-card">
                                            <div class="metric-label">Original Payoff</div>
                                            <div class="metric-value">{original_months // 12} yrs {original_months % 12} mths</div>
                                        </div>
                                    """, unsafe_allow_html=True)

                                # Create comparison data for visualization
                                comparison_data = pd.DataFrame({
                                    'Category': ['Original Interest', 'Interest with Extra Payments', 'Time Reduction'],
                                    'Amount': [original_interest, new_interest, time_saved / original_months * 100],
                                    'Label': [f"${original_interest:,.2f}", f"${new_interest:,.2f}", f"{years_saved} yrs {months_saved} mths"]
                                })

                                # Create tabs for different visualizations
                                viz_tab1, viz_tab2 = st.tabs(["Comparison Chart", "Detailed Schedule"])

                                with viz_tab1:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        # Plot interest comparison
                                        comparison_fig = go.Figure()

                                        comparison_fig.add_trace(go.Bar(
                                            x=['Original Loan', 'With Extra Payments'],
                                            y=[original_interest, new_interest],
                                            text=[f"${original_interest:,.2f}", f"${new_interest:,.2f}"],
                                            textposition='outside',
                                            marker_color=['#ef4444', '#10b981']
                                        ))

                                        comparison_fig.update_layout(
                                            title="Interest Comparison",
                                            yaxis_title="Total Interest ($)",
                                            plot_bgcolor="rgba(0,0,0,0)",
                                            paper_bgcolor="rgba(0,0,0,0)",
                                        )

                                        st.plotly_chart(comparison_fig, use_container_width=True)

                                    with col2:
                                        # Plot time comparison
                                        time_fig = go.Figure()

                                        time_fig.add_trace(go.Bar(
                                            x=['Original Loan', 'With Extra Payments'],
                                            y=[original_months, new_months],
                                            text=[f"{original_months // 12}y {original_months % 12}m",
                                                f"{new_months // 12}y {new_months % 12}m"],
                                            textposition='outside',
                                            marker_color=['#ef4444', '#10b981']
                                        ))

                                        time_fig.update_layout(
                                            title="Loan Term Comparison",
                                            yaxis_title="Months to Payoff",
                                            plot_bgcolor="rgba(0,0,0,0)",
                                            paper_bgcolor="rgba(0,0,0,0)",
                                        )

                                        st.plotly_chart(time_fig, use_container_width=True)

                                with viz_tab2:
                                    st.dataframe(
                                        new_schedule.style.format({
                                            "Total Payment": "${:,.2f}",
                                            "Interest": "${:,.2f}",
                                            "Principal": "${:,.2f}",
                                            "Remaining Balance": "${:,.2f}"
                                        }),
                                        use_container_width=True,
                                        height=400
                                    )
if __name__ == "__main__":
    main()
