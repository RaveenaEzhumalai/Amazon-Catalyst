import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# --- MOCK AGENT LOGIC (Internalized for the final build) ---
class ScoutAgent:
    def scan_region(self, region):
        data = {
            "Long Beach, CA": {"lat": 33.77, "lon": -118.19, "risk_score": 7.4, "event": "Port Congestion"},
            "Houston, Texas": {"lat": 29.76, "lon": -95.36, "risk_score": 7.2, "event": "Intermodal Bottleneck"},
            "Miami, Florida": {"lat": 25.76, "lon": -80.19, "risk_score": 7.2, "event": "Supply Chain Frost Alert"}
        }
        report = data.get(region)
        report['event_name'] = region
        return report

class StrategistAgent:
    def create_plan(self, scout_report):
        qty = 800 if "Miami" in scout_report['event_name'] else 500
        return [{"action": "Relocate", "product": "Medical_Supplies", "move_quantity": qty}]

class NegotiatorAgent:
    def find_best_carrier(self, region_scout, strategy_plan):
        regional_base = {"Long Beach, CA": 1250, "Houston, Texas": 1100, "Miami, Florida": 1450}
        region_name = region_scout.get('event_name')
        risk_score = float(region_scout.get('risk_score', 5.0))
        base_rate = regional_base.get(region_name, 1200)
        
        hazard_multiplier = (risk_score - 5.0) * 0.15 if risk_score > 5.0 else 0
        total_units = sum(int(m['move_quantity']) for m in strategy_plan)
        
        base_total = total_units * base_rate
        surcharge = int(base_total * hazard_multiplier)
        
        return {
            "selected_carrier": "Swift_Logistics" if "Long" in region_name else "Titan_Haul",
            "base_cost": base_total,
            "surcharge": surcharge,
            "total_shipping_cost": base_total + surcharge,
            "risk_impact_percent": int(hazard_multiplier * 100)
        }

class SentinelAgent:
    def audit_plan(self, scout, strat, neg):
        verdict = "APPROVED" if "Miami" in scout['event_name'] else "REJECTED"
        summary = "Emergency medical transfer justified by stockout risk." if verdict == "APPROVED" else "Rejected due to extreme cost inefficiency for standard goods."
        return {"verdict": verdict, "summary": summary, "confidence_score": 92}

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Amazon Catalyst | Global Recovery", page_icon="📦", layout="wide")

# --- THE ULTIMATE VISIBILITY OVERHAUL (CSS) ---
st.markdown("""
    <style>
    /* 1. Darker background overlay for maximum contrast */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), 
                    url('https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2070');
        background-size: cover;
    }

    /* 2. Fix Section Headers (Glow and Color) */
    h1, h2, h3 { 
        color: #ff9900 !important; 
        font-weight: 800 !important;
        text-shadow: 0px 0px 10px rgba(255, 153, 0, 0.4);
    }

    /* 3. Metric Labels (Risk Severity, Tactical Moves, etc.) */
    div[data-testid="stMetricLabel"] { 
        color: #ff9900 !important; 
        font-weight: 900 !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        font-weight: 700 !important;
    }
    div[data-testid="stMetric"] {
        background: rgba(10,12,18,0.95) !important;
        border: 2px solid #ff9900 !important;
        border-radius: 12px;
        padding: 15px !important;
    }

    /* 4. Financial Analysis Text Visibility */
    .financial-text {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem;
    }
    .carrier-info {
        background: rgba(255, 153, 0, 0.1);
        border: 1px solid #ff9900;
        padding: 15px;
        border-radius: 10px;
        color: #ffffff !important;
    }
    .carrier-info b { color: #ff9900 !important; }

    /* 5. Enterprise Tagline */
    .enterprise-tagline {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 10px #000;
        font-size: 1.2rem;
    }

    /* 6. Sidebar Clarity */
    [data-testid="stSidebar"] label { color: #111 !important; font-weight: 900 !important; }

    /* 7. Tactical Green Button */
    .stButton>button {
        background: linear-gradient(90deg, #28a745 0%, #1e7e34 100%) !important;
        color: white !important;
        font-weight: 900 !important;
        border: none !important;
        height: 4rem !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(40,167,69,0.4);
    }
    
    /* 8. Executive Card Status */
    .executive-card {
        background: rgba(0,0,0,0.95);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #ff9900;
        border-left: 12px solid #ff9900;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION & REFRESH LOGIC ---
if 'current_theater' not in st.session_state:
    st.session_state.current_theater = "Long Beach, CA"
    st.session_state.scout = None

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=120)
    st.markdown("<h2 style='color:#111;'>MISSION CONTROL</h2>", unsafe_allow_html=True)
    selected_region = st.selectbox("🎯 SELECT STRATEGIC THEATER", ["Long Beach, CA", "Houston, Texas", "Miami, Florida"])
    
    if selected_region != st.session_state.current_theater:
        st.session_state.current_theater = selected_region
        st.session_state.scout = None 

    st.divider()
    st.success("🛰️ ENCRYPTION: AES-256")
    st.info("🤖 AI SWARM: ACTIVE")

# --- MAIN CONTENT ---
st.title("🛡️ AMAZON CATALYST")
st.markdown('<p class="enterprise-tagline">Autonomous Resilience & Recovery Engine | Enterprise Tier</p>', unsafe_allow_html=True)

if st.button("🚀 INITIATE GLOBAL RECOVERY PROTOCOL"):
    with st.status("Orchestrating Agents...", expanded=True):
        st.session_state.scout = ScoutAgent().scan_region(st.session_state.current_theater)
        st.session_state.strat = StrategistAgent().create_plan(st.session_state.scout)
        st.session_state.neg = NegotiatorAgent().find_best_carrier(st.session_state.scout, st.session_state.strat)
        st.session_state.audit = SentinelAgent().audit_plan(st.session_state.scout, st.session_state.strat, st.session_state.neg)

# --- DISPLAY RESULTS ---
if st.session_state.scout:
    s, strt, n, a = st.session_state.scout, st.session_state.strat, st.session_state.neg, st.session_state.audit
    
    st.divider()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("RISK SEVERITY", f"{s['risk_score']}/10")
    k2.metric("TACTICAL MOVES", f"{strt[0]['move_quantity']} Units")
    k3.metric("RECOVERY COST", f"${n['total_shipping_cost']:,}")
    k4.metric("AUDIT SCORE", f"{a['confidence_score']}%")

    st.markdown("### 📊 FINANCIAL ANALYSIS")
    b1, b2 = st.columns([2, 1])
    with b1:
        total = n['total_shipping_cost']
        st.markdown(f'<p class="financial-text"><b>Base Freight:</b> ${n["base_cost"]:,}</p>', unsafe_allow_html=True)
        st.progress(n['base_cost'] / total)
        st.markdown(f'<p class="financial-text"><b>Hazard Surcharge ({n["risk_impact_percent"]}%):</b> ${n["surcharge"]:,}</p>', unsafe_allow_html=True)
        st.progress(n['surcharge'] / total)
    
    with b2:
        st.markdown(f"""
            <div class="carrier-info">
                <p><b>Carrier:</b> {n['selected_carrier']}</p>
                <p><b>Event:</b> {s['event']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    m_col, r_col = st.columns([1.7, 1])
    with m_col:
        st.subheader("📍 GEOSPATIAL INTELLIGENCE")
        m = folium.Map(location=[s['lat'], s['lon']], zoom_start=12, tiles="CartoDB dark_matter")
        folium.CircleMarker([s['lat'], s['lon']], radius=20, color="#ff9900", fill=True).add_to(m)
        st_folium(m, width="100%", height=450, key=f"map_{st.session_state.current_theater}")
    
    with r_col:
        st.subheader("📋 EXECUTIVE REPORT")
        v_col = "#28a745" if a['verdict'] == "APPROVED" else "#ff4b4b"
        st.markdown(f"""
            <div class="executive-card">
                <h2 style="color:{v_col}; margin-top:0;">{a['verdict']}</h2>
                <p style="color:white; font-size:1.1rem;"><b>SUMMARY:</b> {a['summary']}</p>
                <p style="color:#28a745; font-weight:bold; font-size:1.2rem;">STATUS: MISSION READY</p>
            </div>
        """, unsafe_allow_html=True)