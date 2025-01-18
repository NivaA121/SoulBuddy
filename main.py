import streamlit as st
import requests

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "8ea73213-7aea-4e70-a59a-035e18c1e7b9"
APPLICATION_TOKEN = "AstraCS:pinDiknMSzhSWNtEzJjzdpMi:5ebdd7d258e44c654262ca24c1235dc35f29491def6f03e5f2001ce0577de9e2"
ENDPOINT = "327861e0-c476-4426-ac05-86c1e4cdffbf"


def run_flow(message: str) -> dict:
    """
    Call the LangFlow API to process the message.
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


# Streamlit Interface
st.set_page_config(page_title="Hackonauts Chatbot", layout="centered")

st.title("Chat with SoulBuddies")
st.markdown("Data-Driven Social Insights with Langflow and DataStax Astra DB.")

# Input container
with st.container():
    st.write("### Enter your message:")
    user_message = st.text_input("", placeholder="Type your message here...")

# Button and response container
if st.button("Send"):
    if not user_message.strip():
        st.error("⚠️ Please enter a valid message.")
    else:
        with st.spinner("Waiting for response..."):
            try:
                response = run_flow(user_message)
                # Extract the result
                result = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get(
                    "results", {}).get("message", {}).get("text", "No response.")
                
                # Response container
                st.success("Response Received:")
                st.markdown(f"""
                    <div style="background-color:#f9f9f9; padding:10px; border-radius:5px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                        <p style="color:#333; font-size:16px; font-family:Arial, sans-serif;">{result}</p>
                    </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ An error occurred: {e}")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
