import streamlit as st
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

st.set_page_config(page_title="Python Code Debugger AI", page_icon="🐍")
st.title("🐍 Automatic Python Code Debugger with CrewAI")

code_input = st.text_area("Paste your Python code here:", height=300, placeholder="def add(a, b):\n    return a + b")

if code_input and st.button("Analyze and Debug"):

    reviewer = Agent(
        role="Python Code Reviewer",
        goal="Detect errors and bad practices in Python code",
        backstory="You are a Python expert capable of spotting problems quickly and effectively.",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4")
    )

    analyst = Agent(
        role="Python Error Analyst",
        goal="Explain why the code has issues and how to resolve them",
        backstory="You are a senior engineer with deep knowledge of debugging and code design.",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4")
    )

    fixer = Agent(
        role="Correction Suggester",
        goal="Generate a corrected and optimized version of the code",
        backstory="You focus on refactoring, readability, and Python best practices.",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4")
    )

    # Step 1: Review the code
    task_review = Task(
        description=f"Step 1: Here is some Python code to review:\n\n{code_input}\n\nPlease identify any bugs or bad practices.",
        expected_output="A list of identified errors or bad practices.",
        agent=reviewer
    )
    crew_review = Crew(agents=[reviewer], tasks=[task_review], verbose=True)
    review_result = crew_review.kickoff()
    st.subheader("🔍 Code Review")
    st.write(review_result)

    # Step 2: Analyze the review findings
    task_analyze = Task(
        description=f"Step 2: Analyze the following review findings and explain their causes and consequences:\n\n{review_result}",
        expected_output="Detailed reasoning behind the identified issues.",
        agent=analyst
    )
    crew_analyze = Crew(agents=[analyst], tasks=[task_analyze], verbose=True)
    analyze_result = crew_analyze.kickoff()
    st.subheader("💡 Error Analysis")
    st.write(analyze_result)

    # Step 3: Generate a fix based on the analysis
    task_fix = Task(
        description=f"Step 3: Based on the following analysis, provide a corrected and optimized version of the code.\n\nAnalysis:\n{analyze_result}\n\nOriginal Code:\n{code_input}",
        expected_output="Corrected Python code with explanations of changes.",
        agent=fixer
    )
    crew_fix = Crew(agents=[fixer], tasks=[task_fix], verbose=True)
    fix_result = crew_fix.kickoff()
    st.subheader("🛠 Suggested Fix")
    st.write(fix_result)

else:
    st.info("Paste your code to start the analysis.")
