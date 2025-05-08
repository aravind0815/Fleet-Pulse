# dashboard/utils/db.py
import psycopg2
import pandas as pd
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_connection():
    return psycopg2.connect(
        host="localhost",  # change if deployed
        dbname="fleetpulse_db",
        user="postgres",
        password="Aravind@123",
        port=5432
    )

def fetch_recent_breakdowns(threshold=0.7):
    conn = get_connection()
    query = f"""
        SELECT * FROM truck_breaksown_logs
        WHERE breakdown_risk >= {threshold}
        ORDER BY timestamp DESC
        LIMIT 100
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_summary_stats():
    conn = get_connection()
    stats = {}
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT truck_id) FROM truck_breaksown_logs")
    stats['total_trucks'] = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM truck_breaksown_logs WHERE breakdown_risk > 0.9")
    stats['high_risk'] = cur.fetchone()[0]
    cur.execute("SELECT MAX(breakdown_risk) FROM truck_breaksown_logs WHERE timestamp >= CURRENT_DATE")
    stats['max_risk_today'] = cur.fetchone()[0] or 0
    conn.close()
    return stats
