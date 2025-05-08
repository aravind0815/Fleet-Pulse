# import streamlit as st

# def set_custom_theme():
#     st.markdown("""
#         <style>
#             /* Dark sidebar styling */
#             section[data-testid="stSidebar"] {
#                 background-color: #1f1f2e;
#                 color: white;
#             }

#             /* Sidebar text and header */
#             .sidebar .sidebar-content {
#                 color: white;
#             }

#             /* General text color */
#             body {
#                 color: white;
#             }

#             /* Cards for metrics */
#             .card {
#                 padding: 1.5em;
#                 background: #28293e;
#                 border-radius: 12px;
#                 box-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
#                 text-align: center;
#             }

#             .metric {
#                 font-size: 2em;
#                 font-weight: bold;
#                 color: #f7f7f7;
#             }

#             .label {
#                 font-size: 1em;
#                 color: #b0b0b0;
#             }

#             /* Fixing input contrast in dark mode */
#             input, .stDateInput input {
#                 background-color: #2f2f3f !important;
#                 color: white !important;
#             }
#         </style>
#     """, unsafe_allow_html=True)



import streamlit as st

def set_custom_theme():
    st.markdown("""
        <style>
            /* Smooth animated gradient for sidebar */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1e1e30 0%, #29293d 100%);
                color: white;
                padding: 1rem;
                animation: gradientScroll 15s ease infinite;
                background-size: 300% 300%;
            }

            @keyframes gradientScroll {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* General body and font tweaks */
            html, body {
                font-family: 'Segoe UI', sans-serif;
                color: #f5f6fa;
                background-color: #12121c;
            }

            /* Metric card styles */
            .card {
                padding: 1.5em;
                background: #2c2f4a;
                border-radius: 14px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.6);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .card:hover {
                transform: scale(1.03);
                box-shadow: 0 6px 30px rgba(0, 255, 255, 0.3);
            }

            .metric {
                font-size: 2.3em;
                font-weight: bold;
                color: #00ffff;
            }

            .label {
                font-size: 1.1em;
                color: #aaaac4;
            }

            /* Date input + form styling */
            input, .stDateInput input, select, textarea {
                background-color: #1d1f33 !important;
                color: #ffffff !important;
                border: 1px solid #3d3f50 !important;
                border-radius: 6px;
                padding: 0.5rem;
            }

            /* Buttons */
            button {
                border-radius: 10px !important;
                transition: all 0.2s ease-in-out !important;
            }

            button:hover {
                background-color: #00ffff !important;
                color: black !important;
                transform: scale(1.05);
            }

            /* Headings */
            h1, h2, h3, h4 {
                color: #f0f0f0;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            /* Subtle animations on appearance */
            .element-container {
                animation: fadeIn 1s ease-out;
            }

            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(10px); }
                100% { opacity: 1; transform: translateY(0); }
            }
        </style>
    """, unsafe_allow_html=True)
