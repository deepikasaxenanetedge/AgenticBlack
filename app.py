import streamlit as st
import mysql.connector
import pandas as pd


# Database connection function
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Default XAMPP password is empty
        database="intelligent_agent_db"  # Change this to your actual database name
    )
    return conn

# Main application
def main():
    st.title("MySQL Database Manager")
    
    # Add CSS to ensure content is visible
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
            background-color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Simple navigation with tabs
    tabs = st.tabs(["NO_TAGS", "Regulatory Stopwords", "Knowledge Source"])
    
    # NO_TAGS tab
    with tabs[0]:
        st.header("NO_TAGS Management")
        
        # Display current data
        try:
            conn = get_connection()
            df = pd.read_sql("SELECT `condition` FROM NO_TAGS", conn)
            st.subheader("Current Entries:")
            st.dataframe(df)
            conn.close()
        except Exception as e:
            st.error(f"Error loading data: {e}")
        
        # Form to add new entry
        st.subheader("Add New Entry")
        form1 = st.form(key='no_tags_form')
        condition = form1.text_input("Enter Condition:")
        submit_button = form1.form_submit_button("Add Entry")
        
        if submit_button:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO NO_TAGS (`condition`) VALUES (%s)", (condition,))
                conn.commit()
                st.success(f"Added: {condition}")
                conn.close()
                st.rerun()
            except Exception as e:
                st.error(f"Error adding entry: {e}")
        
        # Delete entries
        st.subheader("Delete Entry")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT `condition` FROM NO_TAGS")
            conditions = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            if conditions:
                selected_condition = st.selectbox("Select `condition` to delete:", conditions)
                if st.button("Delete Selected"):
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM NO_TAGS WHERE `condition` = %s", (selected_condition,))
                        conn.commit()
                        st.success(f"Deleted: {selected_condition}")
                        conn.close()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting entry: {e}")
            else:
                st.info("No entries to delete.")
        except Exception as e:
            st.error(f"Error loading data for deletion: {e}")
    
    # Regulatory Stopwords tab
    with tabs[1]:
        st.header("Regulatory Stopwords Management")
        
        # Display current data
        try:
            conn = get_connection()
            df = pd.read_sql("SELECT words FROM regulatory_stopwords", conn)
            st.subheader("Current Entries:")
            st.dataframe(df)
            conn.close()
        except Exception as e:
            st.error(f"Error loading data: {e}")
        
        # Form to add new entry
        st.subheader("Add New Stopword")
        form2 = st.form(key='stopwords_form')
        word = form2.text_input("Enter Stopword:")
        submit_button = form2.form_submit_button("Add Stopword")
        
        if submit_button:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO regulatory_stopwords (words) VALUES (%s)", (word,))
                conn.commit()
                st.success(f"Added: {word}")
                conn.close()
                st.rerun()
            except Exception as e:
                st.error(f"Error adding entry: {e}")
        
        # Delete entries
        st.subheader("Delete Stopword")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM regulatory_stopwords")
            words = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            if words:
                selected_word = st.selectbox("Select stopword to delete:", words)
                if st.button("Delete Selected", key=f"delete_{selected_word}"):
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM regulatory_stopwords WHERE words = %s", (selected_word,))
                        conn.commit()
                        st.success(f"Deleted: {selected_word}")
                        conn.close()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting entry: {e}")
            else:
                st.info("No entries to delete.")
        except Exception as e:
            st.error(f"Error loading data for deletion: {e}")
    
    # Knowledge Source tab
    with tabs[2]:
        st.header("Knowledge Source Management")
        
        # Display current data
        try:
            conn = get_connection()
            df = pd.read_sql("SELECT * FROM knowledge_source", conn)
            st.subheader("Current Entries:")
            st.dataframe(df)
            conn.close()
        except Exception as e:
            st.error(f"Error loading data: {e}")
        
        # Form to add new entry
        st.subheader("Add New Rule")
        form3 = st.form(key='knowledge_form')
        condition = form3.text_input("Enter Condition:")
        action = form3.text_input("Enter Action:")
        submit_button = form3.form_submit_button("Add Rule")
        
        if submit_button:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                "INSERT INTO knowledge_source (`condition`, action) VALUES (%s, %s)", 
                (condition, action)
                )
                conn.commit()
                st.success(f"Added: {condition} -> {action}")
                conn.close()
                st.rerun()
            except Exception as e:
                st.error(f"Error adding entry: {e}")
        
        # Delete entries
        st.subheader("Delete Rule")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT `condition`, `action` FROM knowledge_source")
            rows = cursor.fetchall()
            conn.close()

            if rows:
                rules = [f"{row[0]} -> {row[1]}" for row in rows]
                selected_rule = st.selectbox("Select rule to delete:", rules)

                # Extract condition from "condition -> action"
                selected_condition = selected_rule.split(" -> ")[0]

                # Use a stable unique key based on condition
                unique_key = f"delete_{selected_condition}"

                # Ensure the button ID is unique
                if st.button("Delete Selected", key=f"delete_ks_{selected_condition}"):
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM knowledge_source WHERE `condition` = %s", (selected_condition,))
                        conn.commit()
                        st.success(f"Deleted: {selected_rule}")
                        conn.close()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting entry: {e}")
            else:
                st.info("No entries to delete.")
        except Exception as e:
            st.error(f"Error loading data for deletion: {e}")

# Run the application
if __name__ == "__main__":
    main()