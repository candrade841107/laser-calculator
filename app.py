import streamlit as st
import json

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="CADSUBLIMAX Pricing", page_icon="⚡")

# --- LOAD MATERIALS ---
def load_data():
    try:
        with open('materials.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "3mm_mdf": {"name": "3mm MDF", "cost_per_sq_mm": 0.00003, "cut_speed_mmin": 2.0, "power_draw_kw": 3.0, "pierce_time_sec": 0.5},
            "3mm_acrylic": {"name": "3mm Acrylic", "cost_per_sq_mm": 0.00006, "cut_speed_mmin": 1.5, "power_draw_kw": 3.5, "pierce_time_sec": 0.8}
        }

materials = load_data()

# --- APP LAYOUT ---
st.title("✂️ Laser Cut Pricing Calculator")
st.markdown("### CADSUBLIMAX - Professional Quoting Tool")

with st.sidebar:
    st.header("Project Settings")
    mat_key = st.selectbox("Select Material", options=list(materials.keys()), format_func=lambda x: materials[x]['name'])
    
    use_gen = st.toggle("⚡ Blackout Mode (Generator)", help="Uses $0.25/kWh instead of $0.1061/kWh")
    
    st.divider()
    st.info("Ecuador IVA: 15% (Applied automatically)")

# --- INPUTS ---
col1, col2 = st.columns(2)

with col1:
    width = st.number_input("Part Width (mm)", min_value=1.0, value=100.0)
    height = st.number_input("Part Height (mm)", min_value=1.0, value=100.0)
    
with col2:
    length = st.number_input("Total Cut Length (mm)", min_value=1.0, value=500.0)
    pierces = st.number_input("Number of Pierces", min_value=0, value=1)

# --- LOGIC ENGINE ---
if st.button("Calculate Final Quote", type="primary"):
    mat = materials[mat_key]
    energy_rate = 0.2500 if use_gen else 0.1061
    
    # 1. Base Costs
    mat_cost = (width * height) * mat['cost_per_sq_mm'] * 1.10
    time_min = ((length / 1000) / mat['cut_speed_mmin']) + ((pierces * mat['pierce_time_sec']) / 60)
    energy_cost = (time_min / 60) * mat['power_draw_kw'] * energy_rate
    
    # 2. Business Logic
    subtotal = (mat_cost + energy_cost + 20.0) * 1.35  # Cost + Setup + 35% Margin
    iva = subtotal * 0.15
    total = subtotal + iva

    # --- RESULTS DISPLAY ---
    st.success(f"## Total to Pay: ${total:.2f}")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Subtotal", f"${subtotal:.2f}")
    res_col2.metric("IVA (15%)", f"${iva:.2f}")
    res_col3.metric("Time", f"{time_min:.2f} min")
    
    # Professional Message for WhatsApp
    ws_msg = f"*CADSUBLIMAX Quote*\nMat: {mat['name']}\nDim: {width}x{height}mm\nPrice: ${total:.2f} (IVA included)"
    st.text_area("Copy for WhatsApp:", value=ws_msg)
