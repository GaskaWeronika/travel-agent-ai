import streamlit as st
import time
from langchain_core.messages import AIMessage
from agent_ai.travel_agent import travel_agent


def process_stream(stream):
    for chunk in stream:
        chunk_data = chunk[0]
        if isinstance(chunk_data, AIMessage):
            yield chunk_data.content
            time.sleep(0.01)

graph = travel_agent.graph
config = {"configurable": {"thread_id": "0"}} 
st.title("Travel Agent")

if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

if not st.session_state['form_submitted']:

    with st.form("initial_form"):
        interests = st.multiselect(
            "Interests",
            ["culture", "relaxation", "adventure", "nature", "history", "museums", "sports", "food"]
        )
        transport = st.selectbox(
            "Preferred mode of transport",
            ["plane", "train", "car", "bus"]
        )
        budget_min = st.number_input("Minimum budget (PLN)", min_value=100, max_value=50000, value=1000, step=100)
        budget_max = st.number_input("Maximum budget (PLN)", min_value=budget_min, max_value=100000, value=3000, step=100)

        travel_days = st.slider("Number of travel days", 2, 30, 7)
        start_location_options = [
            "Warsaw (WAW)", "Krakow (KRK)", "Gdansk (GDN)", "Wroclaw (WRO)",
            "Poznan (POZ)", "Katowice (KTW)", "Rzeszow (RZE)", "Szczecin (SZZ)",
            "Łodz (LCJ)", "Lublin (LUZ)"
        ]
        start_location = st.selectbox("Starting location", start_location_options, index=1)

        submit_button = st.form_submit_button("Find Recommendations")

        if submit_button:
            st.session_state["interests"] = interests
            st.session_state["transport"] = transport
            st.session_state["budget_min"] = budget_min
            st.session_state["budget_max"] = budget_max
            st.session_state["travel_days"] = travel_days
            st.session_state["start_location"] = start_location
            st.session_state['form_submitted'] = True
            
else:
    st.write("Form successfully submitted. You can start chatting now.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User interaction
if (user_question := st.chat_input("Hi, how can I help you today?")) and st.session_state['form_submitted']:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        user_update_state = {
                "messages": [user_question],
                "interests": st.session_state.interests,
                "transport": st.session_state.transport,
                "budget_min": st.session_state.budget_min,
                "budget_max": st.session_state.budget_max,
                "travel_days": st.session_state.travel_days,
                "start_location": st.session_state.start_location,
            }
        response_generator = graph.stream(
            user_update_state, 
            config=config, # type: ignore
            stream_mode="messages"
            )
        full_response = st.write_stream(process_stream(response_generator))
        st.session_state.messages.append({"role": "assistant", "content": full_response})






