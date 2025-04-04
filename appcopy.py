import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Database Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f1f3f4;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e0e5ec;
        border-radius: 8px;
        padding: 10px 20px;
        color: #444;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e73df !important;
        color: white !important;
    }
    .stButton>button {
        background-color: #4e73df;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #3a5ccc;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .delete-btn>button {
        background-color: #e74a3b;
    }
    .delete-btn>button:hover {
        background-color: #d52a1a;
    }
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div[data-testid="stForm"] {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .css-1rs6os {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #36454f;
    }
    .success {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection function
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Default XAMPP password is empty
        database="intelligent_agent_db"  # Change this to your actual database name
    )
    return conn

# Get counts for dashboard
def get_table_counts():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get counts from each table
        cursor.execute("SELECT COUNT(*) FROM NO_TAGS")
        no_tags_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM regulatory_stopwords")
        stopwords_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM knowledge_source")
        knowledge_count = cursor.fetchone()[0]
        
        conn.close()
        return no_tags_count, stopwords_count, knowledge_count
    except Exception as e:
        st.error(f"Error getting counts: {e}")
        return 0, 0, 0

# Main application
def main():
    # Application header with logo
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("https://via.placeholder.com/100x100.png?text=DB", width=80)
    with col2:
        st.title("Intelligent Agent Database Manager")
        st.markdown("<p style='color: #666; margin-top: -15px;'>Manage your database configurations with ease</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dashboard metrics
    no_tags_count, stopwords_count, knowledge_count = get_table_counts()
    
    st.subheader("📊 Database Overview")
    
    # Create metrics cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card">
            <h3 style="color: #4e73df;">NO_TAGS</h3>
            <h2>{no_tags_count}</h2>
            <p>Total Conditions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <h3 style="color: #1cc88a;">Regulatory Stopwords</h3>
            <h2>{stopwords_count}</h2>
            <p>Total Words</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card">
            <h3 style="color: #f6c23e;">Knowledge Source</h3>
            <h2>{knowledge_count}</h2>
            <p>Total Rules</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create visual representation
    if no_tags_count > 0 or stopwords_count > 0 or knowledge_count > 0:
        data = {
            'Category': ['NO_TAGS', 'Regulatory Stopwords', 'Knowledge Source'],
            'Count': [no_tags_count, stopwords_count, knowledge_count]
        }
        df_chart = pd.DataFrame(data)
        fig = px.bar(
            df_chart, 
            x='Category', 
            y='Count', 
            color='Category',
            color_discrete_map={
                'NO_TAGS': '#4e73df',
                'Regulatory Stopwords': '#1cc88a',
                'Knowledge Source': '#f6c23e'
            },
            title="Database Entries Distribution"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Simple navigation with tabs
    tabs = st.tabs(["NO_TAGS", "Regulatory Stopwords", "Knowledge Source"])
    
    # NO_TAGS tab
    with tabs[0]:
        st.header("🏷️ NO_TAGS Management")
        
        # Display current data in a card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        try:
            conn = get_connection()
            df = pd.read_sql("SELECT `condition` FROM NO_TAGS", conn)
            st.subheader("Current Entries")
            if not df.empty:
                st.dataframe(df, use_container_width=True, height=300)
            else:
                st.info("No entries found. Add your first entry below.")
            conn.close()
        except Exception as e:
            st.error(f"Error loading data: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Two-column layout for add/delete
        col1, col2 = st.columns(2)
        
        # Form to add new entry
        with col1:
            st.subheader("Add New Entry")
            form1 = st.form(key='no_tags_form')
            condition = form1.text_input("Enter Condition:", placeholder="Enter condition text here...")
            submit_button = form1.form_submit_button("Add Entry")
            
            if submit_button and condition:
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
            elif submit_button and not condition:
                st.warning("Please enter a condition.")
        
        # Delete entries
        with col2:
            st.subheader("Delete Entry")
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT `condition` FROM NO_TAGS")
                conditions = [row[0] for row in cursor.fetchall()]
                conn.close()
                
                if conditions:
                    selected_condition = st.selectbox("Select condition to delete:", conditions)
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        delete_btn = st.empty()
                        st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                        if st.button("Delete", key="delete_no_tags"):
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
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No entries to delete.")
            except Exception as e:
                st.error(f"Error loading data for deletion: {e}")
    
    # Regulatory Stopwords tab
    with tabs[1]:
        st.header("⛔ Regulatory Stopwords Management")
        
        # Display current data in a card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        try:
            conn = get_connection()
            df = pd.read_sql("SELECT words FROM regulatory_stopwords", conn)
            st.subheader("Current Entries")
            if not df.empty:
                st.dataframe(df, use_container_width=True, height=300)
            else:
                st.info("No stopwords found. Add your first stopword below.")
            conn.close()
        except Exception as e:
            st.error(f"Error loading data: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Two-column layout for add/delete
        col1, col2 = st.columns(2)
        
        # Form to add new entry
        with col1:
            st.subheader("Add New Stopword")
            form2 = st.form(key='stopwords_form')
            word = form2.text_input("Enter Stopword:", placeholder="Enter stopword here...")
            submit_button = form2.form_submit_button("Add Stopword")
            
            if submit_button and word:
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
            elif submit_button and not word:
                st.warning("Please enter a stopword.")
        
        # Delete entries
        with col2:
            st.subheader("Delete Stopword")
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT words FROM regulatory_stopwords")
                words = [row[0] for row in cursor.fetchall()]
                conn.close()
                
                if words:
                    selected_word = st.selectbox("Select stopword to delete:", words)
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                        if st.button("Delete", key="delete_stopword"):
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
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No entries to delete.")
            except Exception as e:
                st.error(f"Error loading data for deletion: {e}")
    
    # Knowledge Source tab
    with tabs[2]:
        st.header("🧠 Knowledge Source Management")
        
        # Display current data in a card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        try:
            conn = get_connection()
            df = pd.read_sql("SELECT * FROM knowledge_source", conn)
            st.subheader("Current Entries")
            if not df.empty:
                st.dataframe(df, use_container_width=True, height=300)
            else:
                st.info("No rules found. Add your first rule below.")
            conn.close()
        except Exception as e:
            st.error(f"Error loading data: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Form to add new entry
        st.subheader("Add New Rule")
        col1, col2 = st.columns(2)
        
        with col1:
            form3 = st.form(key='knowledge_form')
            condition = form3.text_area("Enter Condition:", placeholder="Enter condition here...", height=100)
            action = form3.text_area("Enter Action:", placeholder="Enter action here...", height=100)
            submit_button = form3.form_submit_button("Add Rule")
            
            if submit_button and condition and action:
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
            elif submit_button and (not condition or not action):
                st.warning("Please enter both condition and action.")
        
        # Delete entries
        with col2:
            st.subheader("Delete Rule")
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT `condition`, `action` FROM knowledge_source")
                rows = cursor.fetchall()
                conn.close()

                if rows:
                    rules = [f"{row[0]} -> {row[1]}" for row in rows]
                    # Use a container to make the display area scrollable
                    container = st.container()
                    with container:
                        selected_rule = st.selectbox("Select rule to delete:", rules)

                    # Extract condition from "condition -> action"
                    selected_condition = selected_rule.split(" -> ")[0]

                    col1, col2 = st.columns([4, 1])
                    with col2:
                        st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                        if st.button("Delete", key="delete_rule"):
                            try:
                                conn = get_connection()
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM knowledge_source WHERE `condition` = %s", (selected_condition,))
                                conn.commit()
                                st.success(f"Deleted rule successfully")
                                conn.close()
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting entry: {e}")
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No entries to delete.")
            except Exception as e:
                st.error(f"Error loading data for deletion: {e}")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #999;'>"
        "© 2025 Intelligent Agent Database Manager | Developed with Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

# Run the application
if __name__ == "__main__":
    main()