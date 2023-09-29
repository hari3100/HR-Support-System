HR Support System - Data Corp
Welcome to the HR Support System project developed by Harikrishnan Nair and Aniket Gajare, Priya Randive, Mohit Sharma, and Rahul Tripathi for the Ganesh Utsav Coding Competition 2023 at IT Vedant Institute.

Overview
The HR Support System is a comprehensive web application designed to assist HR professionals in making informed decisions. It incorporates machine learning models, a user-friendly interface, and a chatbot to streamline HR-related tasks. This README provides an overview of the project structure, functionality, and how to run the application.

Project Structure
final_build.py: This is the main Python script that contains the Streamlit application code. It serves as the entry point for running the application.

attritionmodel2.pkl: This file contains the trained machine learning model for attrition prediction.

attritionscaling2.pkl: This file contains the data scaling object used for preprocessing data for the attrition model.

JobSatisfactionmodel.pkl: This file contains the trained machine learning model for job satisfaction prediction.

JobSatisfactionscaling.pkl: This file contains the data scaling object used for preprocessing data for the job satisfaction model.

performancemodel.pkl: This file contains the trained machine learning model for performance rating prediction.

performancescaling.pkl: This file contains the data scaling object used for preprocessing data for the performance rating model.

Data: This folder contains images used in the Streamlit application.

lottiefiles: This folder contains Lottie animation files used in the Streamlit application.

Features
1. Attrition Prediction
Predict the likelihood of employee attrition (leaving the company) based on various factors such as age, distance from home, and more.

2. Job Satisfaction Prediction
Predict an employee's job satisfaction score based on factors like marital status, salary hike, and more.

3. Performance Rating Prediction
Predict an employee's performance rating based on factors like environment satisfaction, department, and more.

4. HR Support Chatbot
Access HR support and information using the built-in chatbot, which can answer HR-related questions and provide assistance.

5. Employee Attrition Dashboard
A visually appealing dashboard that provides various KPIs, including total employees, active employees, total attrition, attrition rate, average age, and more.

How to Run
Ensure you have Python installed on your system.

Install the required Python packages by running:

css
Copy code
pip install streamlit pandas scikit-learn streamlit-lottie streamlit-option-menu
Run the application using the following command:

arduino
Copy code
streamlit run final_build.py
The application will open in your web browser, allowing you to explore its features.

Privacy and Security
Rest assured that your data is treated with the utmost privacy and security. The application does not store any personal data or information entered by users, ensuring your interactions with the chatbot are private and secure.

Contact
If you have any questions or need assistance, please feel free to reach out to us at harrinair2000@gmail.com.

Disclaimer
Disclaimer: This application is for demonstration purposes only and should not be used for making real HR decisions. The predictions provided by the models may not always be accurate and should be used as a reference.
