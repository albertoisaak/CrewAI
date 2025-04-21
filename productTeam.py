import streamlit as st
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

st.set_page_config(page_title="AI Product Team Simulator", page_icon="🧑‍💻")
st.title("🧑‍💻 AI Product Development Team with CrewAI")

feature_idea = st.text_area("Describe the product or feature you want to build:", height=200, placeholder="Example: A mobile app that tracks water intake and reminds users to drink water.")

if feature_idea and st.button("Run Product Team Simulation"):
    # Define agents
    ux_designer = Agent(
        role="UX Designer",
        goal="Design a user-friendly and intuitive interface",
        backstory="You're an expert in user experience and interface design, focused on accessibility and usability.",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4")
    )

    backend_dev = Agent(
        role="Backend Developer",
        goal="Define a scalable backend architecture for the application",
        backstory="You're a software engineer specializing in APIs, databases, and secure backend infrastructure.",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4")
    )

    frontend_dev = Agent(
        role="Frontend Developer",
        goal="Plan the implementation of the UI components",
        backstory="You're skilled in modern frontend frameworks and ensure smooth UX implementation.",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4")
    )

    qa_engineer = Agent(
        role="QA Engineer",
        goal="Create a test strategy and detect potential points of failure",
        backstory="You're a quality assurance expert focused on preventing bugs and ensuring feature reliability.",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4")
    )

    # Step 1: UX Task
    task_ux = Task(
        description=f"Design the user experience and interface for the following product idea:\n\n{feature_idea}\n\nInclude a flow, wireframe ideas, and UX priorities.",
        expected_output="UX flow, key screens, and design rationale.",
        agent=ux_designer
    )
    crew_ux = Crew(agents=[ux_designer], tasks=[task_ux], verbose=True)
    result_ux = crew_ux.kickoff()

    # Step 2: Backend uses UX context
    task_backend = Task(
        description=f"Based on the following UX design, define the backend architecture:\n\n{result_ux}\n\nInclude APIs, database schema, and authentication strategy.",
        expected_output="Backend architecture description, key endpoints, and data models.",
        agent=backend_dev
    )
    crew_backend = Crew(agents=[backend_dev], tasks=[task_backend], verbose=True)
    result_backend = crew_backend.kickoff()

    # Step 3: Frontend uses UX and Backend context
    task_frontend = Task(
        description=f"Based on the UX design and backend architecture below, describe how the frontend will be implemented:\n\nUX Design:\n{result_ux}\n\nBackend Architecture:\n{result_backend}",
        expected_output="Component structure, framework choice, integration points.",
        agent=frontend_dev
    )
    crew_frontend = Crew(agents=[frontend_dev], tasks=[task_frontend], verbose=True)
    result_frontend = crew_frontend.kickoff()

    # Step 4: QA uses all previous outputs
    task_qa = Task(
        description=f"Create a QA plan for the product based on the following information:\n\nUX Design:\n{result_ux}\n\nBackend Architecture:\n{result_backend}\n\nFrontend Plan:\n{result_frontend}\n\nInclude test strategies, edge cases, and automation ideas.",
        expected_output="Comprehensive QA plan including manual and automated tests.",
        agent=qa_engineer
    )
    crew_qa = Crew(agents=[qa_engineer], tasks=[task_qa], verbose=True)
    result_qa = crew_qa.kickoff()

    # Show results
    st.subheader("🎨 UX Design")
    st.write(result_ux)

    st.subheader("🧩 Backend Architecture")
    st.write(result_backend)

    st.subheader("🖥️ Frontend Plan")
    st.write(result_frontend)

    st.subheader("✅ QA Strategy")
    st.write(result_qa)

else:
    st.info("Enter a product idea to begin.")