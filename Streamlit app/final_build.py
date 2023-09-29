import streamlit as st
import streamlit.components.v1 as components
import pickle
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import json


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Load the models for attrition, job satisfaction, and performance rating
att_ra_reg = pickle.load(open('attritionmodel2.pkl', 'rb'))
att_se = pickle.load(open('attritionscaling2.pkl', 'rb'))

job_sat_ra_reg = pickle.load(open('JobSatisfactionmodel.pkl', 'rb'))
job_sat_se = pickle.load(open('JobSatisfactionscaling.pkl', 'rb'))

per_ra_reg = pickle.load(open('performancemodel.pkl', 'rb'))
per_se = pickle.load(open('performancescaling.pkl', 'rb'))

# Encoding maps
emp_department_map = {'Data Science': 5, 'Development': 3, 'Finance': 1, 'Human Resources': 0, 'Research & Development': 4, 'Sales': 2}
emp_job_role_map = {'Business Analyst': 13, 'Data Scientist': 8, 'Delivery Manager': 3, 'Developer': 14, 'Finance Manager': 6, 'Healthcare Representative': 15, 'Human Resources': 1, 'Laboratory Technician': 16, 'Manager': 7, 'Manager R&D': 10, 'Manufacturing Director': 12, 'Research Director': 5, 'Research Scientist': 11, 'Sales Executive': 9, 'Sales Representative': 4, 'Senior Developer': 17, 'Senior Manager R&D': 0, 'Technical Architect': 18, 'Technical Lead': 2}

# Function to make performance rating predictions
def predict_performance_rating(user_input):
    # Scale the user input
    scaled_data = per_se.transform(user_input)

    # Make predictions for performance rating
    performance_prediction = per_ra_reg.predict(scaled_data)
    return performance_prediction

# Function to create the performance rating page
def performance_rating_page():
    st.title("Performance Rating Prediction")

    # Split the features into two columns
    col1, col2 = st.columns(2)

    # Create a form to enter employee information for performance prediction in the first column
    with col1:
        EmpEnvironmentSatisfaction = st.slider("Employee Environment Satisfaction", 1, 4, 2)
        EmpLastSalaryHikePercent = st.slider("Employee Last Salary Hike Percent", 1, 25, 10)
        YearsSinceLastPromotion = st.slider("Years Since Last Promotion", 0, 15, 3)
        EmpDepartment = st.selectbox("Employee Department", ['Data Science', 'Development', 'Finance', 'Human Resources', 'Research & Development', 'Sales'])
        EmpDepartment_encoded = emp_department_map[EmpDepartment]

    # Create a form to enter employee information for performance prediction in the second column
    with col2:
        ExperienceYearsInCurrentRole = st.slider("Experience Years in Current Role", 0, 20, 2)
        EmpHourlyRate = st.slider("Employee Hourly Rate", 20, 100, 50)
        EmpJobRole = st.selectbox("Employee Job Role", ['Business Analyst', 'Data Scientist', 'Delivery Manager', 'Developer', 'Finance Manager', 'Healthcare Representative', 'Human Resources', 'Laboratory Technician', 'Manager', 'Manager R&D', 'Manufacturing Director', 'Research Director', 'Research Scientist', 'Sales Executive', 'Sales Representative', 'Senior Developer', 'Senior Manager R&D', 'Technical Architect', 'Technical Lead'])
        EmpJobRole_encoded = emp_job_role_map[EmpJobRole]
        TotalWorkExperienceInYears = st.slider("Total Work Experience (years)", 0, 40, 5)

    # Create a button to make performance predictions at the center
    with col1:
        if st.button("Predict Performance Rating"):
            # Create a DataFrame with user input
            user_df = pd.DataFrame(data=[[EmpEnvironmentSatisfaction, EmpLastSalaryHikePercent, YearsSinceLastPromotion, EmpDepartment_encoded,
                                          ExperienceYearsInCurrentRole, EmpHourlyRate, EmpJobRole_encoded, TotalWorkExperienceInYears]],
                                   columns=['EmpEnvironmentSatisfaction', 'EmpLastSalaryHikePercent', 'YearsSinceLastPromotion',
                                            'EmpDepartment', 'ExperienceYearsInCurrentRole', 'EmpHourlyRate', 'EmpJobRole',
                                            'TotalWorkExperienceInYears'])

            # Make predictions for performance rating
            performance_prediction = predict_performance_rating(user_df)

            st.subheader("Performance Rating Prediction")

            # Display messages and images based on the prediction
            if performance_prediction[0] == 2:
                st.error("POOR PERFORMANCE")
                st.image("Poor-Performance.jpg", width=300, caption="Poor Performance",use_column_width=True)
            elif performance_prediction[0] == 3:
                st.success("GOOD PERFORMANCE")
                st.image("good.jpg", width=300, caption="Good Performance",use_column_width=True)
            elif performance_prediction[0] == 4:
                st.info("EXCELLENT PERFORMANCE")
                st.image("excellent.jpg", width=300, caption="Excellent Performance",use_column_width=True)
    st.write(
            f"""
            <style>
            img {{
                display: block;
                margin: 0 auto;
                max-width: 50%; /* Adjust the maximum width as needed */
                height: auto;   /* Maintain aspect ratio */
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


# Function to make attrition predictions
def predict_attrition(user_input):
    # Scale the user input
    scaled_data = att_se.transform(user_input)

    # Make predictions for attrition
    attrition_prediction = att_ra_reg.predict(scaled_data)
    return attrition_prediction

# Function to create the main page for attrition prediction
def attrition_page():
    st.title("Attrition Prediction Web App")

    # Create two columns for features
    col1, col2 = st.columns(2)

    # Create a form to enter employee information for attrition prediction in the first column
    with col1:
        Age = st.slider("Age", 18, 65, 30)
        DistanceFromHome = st.slider("Distance From Home (miles)", 1, 29, 10)
        TotalWorkExperienceInYears = st.slider("Total Work Experience (years)", 0, 40, 5)
        ExperienceYearsInCurrentRole = st.slider("Experience Years in Current Role", 0, 20, 2)
        YearsWithCurrManager = st.slider("Years with Current Manager", 0, 20, 2)
        

    # Create a form to enter employee information for attrition prediction in the second column
    with col2:
        # Encode categorical features
        OverTime = st.selectbox("OverTime", ['No', 'Yes'])
        OverTime_encoded = 1 if OverTime == 'Yes' else 0

        MaritalStatus = st.selectbox("Marital Status", ['Divorced', 'Married', 'Single'])
        MaritalStatus_encoded = {'Divorced': 2, 'Married': 1, 'Single': 0}[MaritalStatus]

        EmpJobRole = st.selectbox("Employee Job Role", ['Business Analyst', 'Data Scientist', 'Delivery Manager', 'Developer', 'Finance Manager', 'Healthcare Representative', 'Human Resources', 'Laboratory Technician', 'Manager', 'Manager R&D', 'Manufacturing Director', 'Research Director', 'Research Scientist', 'Sales Executive', 'Sales Representative', 'Senior Developer', 'Senior Manager R&D', 'Technical Architect', 'Technical Lead'])
        EmpJobRole_encoded = emp_job_role_map[EmpJobRole]

        EmpJobInvolvement = st.slider("Employee Job Involvement", 1, 4, 2)
        ExperienceYearsAtThisCompany = st.slider("Experience Years at This Company", 0, 40, 5)
        EmpEnvironmentSatisfaction = st.slider("Employee Environment Satisfaction", 1, 4, 2)

    # Create a container to center the "Predict Attrition" button
    button_container = st.empty()

    if st.button("Predict Attrition"):
            # Create a DataFrame with user input
            user_df = pd.DataFrame(data=[[Age, DistanceFromHome, TotalWorkExperienceInYears, ExperienceYearsInCurrentRole, 
                                          YearsWithCurrManager, EmpJobInvolvement, ExperienceYearsAtThisCompany, 
                                          EmpEnvironmentSatisfaction, OverTime_encoded, MaritalStatus_encoded, 
                                          EmpJobRole_encoded]],
                                   columns =['Age', 'DistanceFromHome', 'TotalWorkExperienceInYears', 
                                            'ExperienceYearsInCurrentRole', 'YearsWithCurrManager', 'EmpJobInvolvement',
                                            'ExperienceYearsAtThisCompany', 'EmpEnvironmentSatisfaction', 'OverTime',
                                            'MaritalStatus', 'EmpJobRole'])

            # Make predictions for attrition
            attrition_prediction = predict_attrition(user_df)

            st.subheader("Attrition Prediction")
            if attrition_prediction[0] == 0:
                st.success("No attrition predicted. Employee is likely to stay.")
                st.image("noatt.jpg", width=100, caption="NO!", use_column_width=True)
            else:
                st.warning("Attrition predicted. Employee may leave the company.")
                st.image("yesatt.jpg", width=100, caption="YES!", use_column_width=True)
    st.write(
            f"""
            <style>
            img {{
                display: block;
                margin: 0 auto;
                max-width: 20%; /* Adjust the maximum width as needed */
                height: auto;   /* Maintain aspect ratio */
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )



    
        
    
        


# Function to make job satisfaction predictions
def predict_job_satisfaction(user_input):
    # Scale the user input
    scaled_data = job_sat_se.transform(user_input)

    # Make predictions for job satisfaction
    job_satisfaction_prediction = job_sat_ra_reg.predict(scaled_data)
    return job_satisfaction_prediction

# Function to create the job satisfaction prediction page
def job_satisfaction_page():
    st.title("Job Satisfaction Prediction")

    marital_status_map = {'Divorced': 1, 'Married': 2, 'Single': 0}
    over_time_map = {'No': 0, 'Yes': 1}
    gender_map = {'Female': 1, 'Male': 0}
    job_role_map = {'Healthcare Representative': 6, 'Human Resources': 4, 'Laboratory Technician': 2, 'Manager': 8, 'Manufacturing Director': 7, 'Research Director': 3, 'Research Scientist': 1, 'Sales Executive': 0, 'Sales Representative': 5}

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        MaritalStatus = st.selectbox("Marital Status", ['Divorced', 'Married', 'Single'])
        MaritalStatus_encoded = marital_status_map[MaritalStatus]

        PercentSalaryHike = st.slider("Percent Salary Hike", 1, 25, 10)

        OverTime = st.selectbox("OverTime", ['No', 'Yes'])
        OverTime_encoded = over_time_map[OverTime]

        Gender = st.selectbox("Gender", ['Female', 'Male'])
        Gender_encoded = gender_map[Gender]

        JobRole = st.selectbox("Job Role", ['Healthcare Representative', 'Human Resources', 'Laboratory Technician',
                                                 'Manager', 'Manufacturing Director', 'Research Director',
                                                 'Research Scientist', 'Sales Executive', 'Sales Representative'])
        JobRole_encoded = job_role_map[JobRole]

    with col2:
        EnvironmentSatisfaction = st.slider("Environment Satisfaction", 1, 4, 2)
        TotalWorkingYears = st.slider("Total Working Years", 1, 40, 10)
        HourlyRate = st.slider("Hourly Rate", 20, 100, 50)
        Age = st.slider("Age", 18, 65, 30)

        BusinessTravel = st.selectbox("Business Travel", ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'])
        BusinessTravel_encoded = {'Non-Travel': 0, 'Travel_Frequently': 1, 'Travel_Rarely': 2}[BusinessTravel]

        MonthlyIncome = st.slider("Monthly Income", 1000, 20000, 5000)

    # Center the prediction result between the two columns
    prediction_container = st.empty()
    if st.button("Predict Job Satisfaction"):
        # Create a DataFrame with user input
        user_df = pd.DataFrame(data=[[MaritalStatus_encoded, PercentSalaryHike, OverTime_encoded, Gender_encoded,
                                      JobRole_encoded, EnvironmentSatisfaction, TotalWorkingYears, HourlyRate, Age,
                                      BusinessTravel_encoded, MonthlyIncome]],
                               columns=['MaritalStatus', 'PercentSalaryHike', 'OverTime', 'Gender', 'JobRole',
                                        'EnvironmentSatisfaction', 'TotalWorkingYears', 'HourlyRate', 'Age',
                                        'BusinessTravel', 'MonthlyIncome'])

        # Make predictions for job satisfaction
        job_satisfaction_prediction = predict_job_satisfaction(user_df)

        prediction_container.subheader("Job Satisfaction Prediction")

        # Display messages and images based on the prediction
        if job_satisfaction_prediction[0] == 1:
            prediction_container.error("LOW SATISFACTION")
            st.image("low satisfaction.jpg", width=300, caption="Low Satisfaction",use_column_width=True)
        elif job_satisfaction_prediction[0] == 2:
            prediction_container.warning("MEDIUM SATISFACTION")
            st.image("medium satisfaction.jpeg", width=300, caption="Medium Satisfaction",use_column_width=True)
        elif job_satisfaction_prediction[0] == 3:
            prediction_container.success("HIGH SATISFACTION")
            st.image("high satisfaction.jpeg", width=300, caption="High Satisfaction",use_column_width=True)
        elif job_satisfaction_prediction[0] == 4:
            prediction_container.info("VERY HIGH SATISFACTION")
            st.image("very high satisfaction.jpeg", width=300, caption="Very High Satisfaction",use_column_width=True)
    st.write(
            f"""
            <style>
            img {{
                display: block;
                margin: 0 auto;
                max-width: 30%; /* Adjust the maximum width as needed */
                height: auto;   /* Maintain aspect ratio */
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

# Function to create the Dialogflow chatbot section
def dialogflow_chatbot():
    st.title("HR Support Chatbot")

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Load the Lottie animation file
    lottie_coding = load_lottiefile("hiii.json")

    # Display the Lottie animation in the first column
    with col1:
        st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=700,
            width=700,
            key=None,
        )

    # Embed the Dialogflow chatbot in the second column using components.html
    with col2:
        components.html(
            """
            <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
                <df-messenger
                    intent="WELCOME"
                    chat-title="HR_Support_chatbot"
                    agent-id="34099a43-1bb7-4938-94c2-4e94a7325ab1"
                    language-code="en">
                </df-messenger>
            """,
            width=650,  # Adjust the width as needed
            height=600,
        )

    

# Function to embed the Power BI dashboard in full-screen mode
def embed_power_bi_dashboard():
    st.title("Power BI Dashboard")
    # Embed the Power BI dashboard using an iframe in full-screen mode
    power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiZDllYzBjNzUtMTRlZi00MWU3LTg2M2QtYmQyOTBiYmQ3NzlkIiwidCI6ImRiYmUwNjZlLWI2NTAtNGJjZS1iOGE1LTQ0MWNkOWNiZjdlYyJ9"
    st.components.v1.iframe(power_bi_url, width=1300, height=700)  # Adjust width and height as needed

# Contact information for five individuals
# Function to create the contact page with separate columns for each contact
# Function to create the contact page with separate columns for each contact
def contact_page():
    st.title("Contact Information")

    # Create columns for layout
    cols = st.columns(5)  # Create 5 columns

    contacts = [
        ("Harikrishnan Nair", "harrinair2000@gmail.com", "8652449890", "linkedin.com/in/hari-nair3"),
        ("Aniket Gajare", "aniketgajare999@gmail.com", "7738486949", "linkedin.com/in/aniket-gajare"),
        ("Priya Randive", "priya900randive@gmail.com", "9769976402", "linkedin.com/in/priya-randive"),
        ("Rahul Tripathi", "rahulmadavi458@gmail.com", "7666185592", "linkedin.com/in/rahul-tripathi-19163021b"),
        ("Mohit Sharma", "mohiticai123@gmail.com", "8369777536", "linkedin.com/in/mohit-sharma-53a985233"),
    ]

    for i, (name, email, phone, linkedin) in enumerate(contacts):
        with cols[i]:  # Use the layout column directly
            st.subheader(name)
            st.write(f"📧 Email: {email}")  
            st.write(f"📞 Phone: {phone}")  
            st.write(f"🌐 LinkedIn: {linkedin}")  


# Home Page
def home_page():
    # Set the background color and text color
    st.markdown(
        """
        <style>
        .reportview-container {
            background: linear-gradient(to bottom, #f1f6f9, #c5d6e9);
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create two columns
    col1, col2 = st.columns([1, 2])

    # Display the Lottie animation in the first column
    with col1:
        lottie_coding = load_lottiefile("hello.json")
        st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=400,
            width=400,
            key=None,
        )

    # Display your data in the second column
    with col2:
        st.title("HR Support System - Data Corp")

        st.markdown("Welcome to the HR Support System. This web application provides various HR-related predictions and features.")

        st.header("Functionalities:")

        st.subheader("1. Attrition Prediction")
        st.write("Predict the likelihood of employee attrition (leaving the company) based on various factors such as age, distance from home, and more.")

        st.subheader("2. Job Satisfaction Prediction")
        st.write("Predict an employee's job satisfaction score based on factors like marital status, salary hike, and more.")

        st.subheader("3. Performance Rating Prediction")
        st.write("Predict an employee's performance rating based on factors like environment satisfaction, department, and more.")

        st.subheader("4. Employee Attrition Dashboard")
        st.write("A very intuitive dashboard that consists of various KPIs showing Total employees, Active employee, Total Attrition, Attrition Rate, Average Age, and many more things")

        st.subheader("5. HR Support Chatbot")
        st.write("Access HR support and information using the built-in chatbot, which can answer HR-related questions and provide assistance.")

        st.header("How to Use:")

        st.write("1. Use the navigation bar at the top to select the functionality you want to use.")
        st.write("2. Fill in the required information and click the 'Predict' button to get predictions.")
        st.write("3. Enjoy the HR support chatbot for assistance and information.")

        st.header("About the Models:")

        st.write("The application uses machine learning models to make predictions. These models are trained to provide accurate results based on the input data.")
        st.write("The models include:")
        st.write("- Attrition Prediction Model")
        st.write("- Job Satisfaction Prediction Model")
        st.write("- Performance Rating Prediction Model")

        st.header("Privacy and Security:")

        st.write("Your data is treated with the utmost privacy and security. The application does not store any personal data or information entered by users.")
        st.write("Your interactions with the chatbot are private and secure.")

        st.header("Contact:")

        st.write("If you have any questions or need assistance, please feel free to reach out to us at support@hrsystem.com.")

        st.header("Disclaimer:")

        st.markdown("*Disclaimer:* This application is for demonstration purposes only and should not be used for making real HR decisions. The predictions provided by the models may not always be accurate and should be used as a reference.")


# Main function for the Streamlit app
def main():
    st.set_page_config(
        page_title="HR Support System",
        page_icon="📊",
        layout="wide",
    )

    st.title("HR Support System")

    # Navigation bar
    selected = option_menu(
    menu_title="Main Menu",
    options= ['Home','Attrition','Performance','Job Satisfaction','Dashboard','Chatbot','Contact'],
    icons= ['house','graph-up-arrow','speedometer2','emoji-laughing','chat-square-dots','laptop-fill','person-lines-fill'],
    orientation= 'horizontal',

)

    if selected == "Home":
        home_page()
    elif selected == "Attrition":
        attrition_page()
    elif selected == "Performance":
        performance_rating_page()
    elif selected == "Job Satisfaction":
        job_satisfaction_page()
    elif selected == "Chatbot":
        dialogflow_chatbot()
    elif selected == "Dashboard":
        embed_power_bi_dashboard()
    elif selected == "Contact":
        contact_page()

if __name__ == "__main__":
    main()
