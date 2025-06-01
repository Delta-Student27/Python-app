# app.py
import streamlit as st
import auth
import backend
import database
import receipt

st.set_page_config(page_title="Voting System with Login", page_icon="🗳️", layout="centered")

# --- Session States ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'voted' not in st.session_state:
    st.session_state.voted = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'page' not in st.session_state or st.session_state.page not in ["Login", "Register"]:
    st.session_state.page = "Login"

# --- Authentication Pages ---
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.is_admin(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = True
            st.success("Logged in as Admin!")
        elif auth.login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = False
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password!")

    if st.button("Register Here"):
        st.session_state.page = "Register"

def register_page():
    st.title("📝 Register")

    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif auth.register_user(username, password):
            st.success("Registration successful! Please login.")
            st.session_state.page = "Login"
        else:
            st.error("Username already exists.")

    if st.button("Back to Login"):
        st.session_state.page = "Login"

# --- Voting Page ---
def voting_page():
    st.title(f"🗳️ Welcome {st.session_state.username}")
    st.markdown("---")

    if st.session_state.voted:
        st.success("✅ You have already voted. Thank you for your participation!")
    else:
        st.header("Cast Your Vote")

        candidates = backend.get_candidates()
        candidate_names = [f"{c['party']} - {c['candidate']} ({c['symbol']})" for c in candidates]
        selected_index = st.radio("Choose your party:", range(len(candidates)),
                                  format_func=lambda x: candidate_names[x])

        if st.button("Vote Now"):
            selected_candidate = candidates[selected_index]
            success = backend.vote(selected_candidate["party"], st.session_state.username)
            if success:
                st.session_state.voted = True
                st.success("✅ Your vote has been recorded. Thank you for voting!")
                receipt.generate_receipt(st.session_state.username, selected_candidate)
            else:
                st.session_state.voted = True
                st.warning("⚠️ You have already voted.")

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.voted = False
        st.session_state.is_admin = False
        st.session_state.page = "Login"

# --- Admin Page ---
def admin_page():
    st.title("👨‍💼 Admin Panel")
    st.header("System Controls")

    if st.button("Reset Votes and Users (⚠️ CAREFUL)"):
        database.reset_all()
        st.success("✅ All votes, users, and voting records have been reset.")

    st.header("Current Results")
    results = backend.get_results()
    if results:
        for candidate, votes in results.items():
            st.write(f"**{candidate}**: {votes} votes")
    else:
        st.write("No votes yet.")

    if st.button("Logout Admin"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.voted = False
        st.session_state.is_admin = False
        st.session_state.page = "Login"

# --- Main App ---
def main():
    if not st.session_state.logged_in:
        if st.session_state.page == "Login":
            login_page()
        elif st.session_state.page == "Register":
            register_page()
    else:
        if st.session_state.is_admin:
            admin_page()
        else:
            voting_page()

if __name__ == '__main__':
    main()
