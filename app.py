import streamlit as st
from graphs.graph_runner import MentalHealthGraphRunner
from config.settings import load_config

# ------------------ Session Initialization ------------------
if 'initialized' not in st.session_state:
    try:
        load_config()
        st.session_state.runner = MentalHealthGraphRunner()
        st.session_state.session_id = st.session_state.runner.start_session()
        st.session_state.session_active = True
        st.session_state.messages = []
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"❌ Failed to initialize: {e}")
        st.stop()

# ------------------ Sidebar Controls ------------------
with st.sidebar:
    st.title("⚙️ Session Control")
    if st.button("🔚 End Session"):
        if st.session_state.session_active:
            try:
                result = st.session_state.runner.end_session(st.session_state.session_id)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**(System)**: {result['response']}"
                })
                st.session_state.session_active = False
                st.success("Session ended.")
            except Exception as e:
                st.error(f"Ending session failed: {e}")

# ------------------ Page Heading ------------------
st.title("🧠 Mental Health Support System")
st.markdown("You're not alone. This is a space to talk safely.")
st.info("In an emergency, call 911 or go to the nearest hospital.")

# ------------------ Display Chat Messages ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ Chat Input and Response Handling ------------------
if st.session_state.session_active:
    user_input = st.chat_input("How are you feeling today?")

    if user_input:
        # Show & save user message
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            result = st.session_state.runner.process_message(
                st.session_state.session_id, user_input
            )
            print("Runner result:", result)  # Debug print

            response_text = result.get("response", "I'm here for you.")
            agent = result.get("current_agent", "Assistant")
            crisis_level = result.get("crisis_level", 0)
            session_active = result.get("session_active", True)

            formatted_response = f"**({agent})**: {response_text}"
            st.chat_message("assistant").markdown(formatted_response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response
            })

            if crisis_level >= 6:
                st.warning(f"🚨 Crisis detected! Level: {crisis_level}/10")

            if not session_active:
                st.session_state.session_active = False
                st.info("✅ The assistant has closed the session.")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
            print("Error:", e)  # Debug print
