import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Enterprise Warehouse Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- INITIAL DATA ----------------
if "data" not in st.session_state:
    st.session_state.data = [
        {"Product_ID": 1, "Place_Name": "Mumbai Hub", "Category": "Electronics", "Quantity": 25, "Warehouse_Section": "A1", "Capacity_Used": 70, "Last_Backup": "2026-02-28"},
        {"Product_ID": 2, "Place_Name": "Delhi Storage", "Category": "Furniture", "Quantity": 8, "Warehouse_Section": "B2", "Capacity_Used": 50, "Last_Backup": "2026-02-27"},
        {"Product_ID": 3, "Place_Name": "Bangalore Unit", "Category": "Electronics", "Quantity": 5, "Warehouse_Section": "C1", "Capacity_Used": 80, "Last_Backup": "2026-02-25"},
    ]

data = st.session_state.data

# ---------------- GLOBAL STYLING ----------------
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.card {
    padding: 20px;
    border-radius: 16px;
    color: white;
    text-align: center;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}

.blue {background: linear-gradient(135deg,#1e3a8a,#2563eb);}
.green {background: linear-gradient(135deg,#065f46,#10b981);}
.orange {background: linear-gradient(135deg,#92400e,#f97316);}

.section-card {
    padding:20px;
    border-radius:16px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    color:white;
    margin-bottom:20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
}

.status-good {color:#22c55e; font-weight:bold;}
.status-mid {color:#f59e0b; font-weight:bold;}
.status-bad {color:#ef4444; font-weight:bold;}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;color:#60a5fa;'>🏢 Enterprise Warehouse Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Executive Dashboard", "Inventory Control", "Warehouse Operations", "Admin & Security"]
)

# ---------------- EXECUTIVE DASHBOARD ----------------
if menu == "Executive Dashboard":

    st.subheader("📊 Executive Overview")

    total_places = len(data)
    total_inventory = sum(item["Quantity"] for item in data)
    warehouse_utilization = round(sum(item["Capacity_Used"] for item in data)/len(data), 2)

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card blue'>📍<br>Total Places<br>{total_places}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card green'>📦<br>Total Inventory Units<br>{total_inventory}</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card orange'>🏭<br>Avg Utilization<br>{warehouse_utilization}%</div>", unsafe_allow_html=True)

    st.markdown("### 🚨 Capacity Risk Alerts")
    for item in data:
        if item["Capacity_Used"] >= 85:
            st.error(f"🔴 {item['Place_Name']} nearing full capacity ({item['Capacity_Used']}%)")
        elif item["Capacity_Used"] >= 70:
            st.warning(f"🟠 {item['Place_Name']} above optimal range ({item['Capacity_Used']}%)")

# ---------------- INVENTORY CONTROL ----------------
elif menu == "Inventory Control":

    st.subheader("📦 Inventory Master Data")

    st.dataframe(data, use_container_width=True)

    st.markdown("### 🔄 Inventory Adjustment")

    place_list = [item["Place_Name"] for item in data]
    selected_place = st.selectbox("Select Place", place_list)
    updated_qty = st.number_input("Updated Quantity", min_value=0, step=1)

    if st.button("Update Inventory", type="primary"):
        for item in data:
            if item["Place_Name"] == selected_place:
                item["Quantity"] = updated_qty
        st.success(f"✅ Inventory for {selected_place} Updated")

# ---------------- WAREHOUSE OPERATIONS ----------------
elif menu == "Warehouse Operations":

    st.subheader("🏗️ Warehouse Command Center")

    sections = sorted(list(set(item["Warehouse_Section"] for item in data)))
    section = st.selectbox("Select Warehouse Section", sections)

    section_data = [item for item in data if item["Warehouse_Section"] == section]

    total_qty = sum(item["Quantity"] for item in section_data)
    avg_capacity = round(sum(item["Capacity_Used"] for item in section_data)/len(section_data),1)

    col1, col2 = st.columns(2)
    col1.metric("Section Inventory", total_qty)
    col2.metric("Average Capacity", f"{avg_capacity}%")

    st.markdown("---")

    if avg_capacity < 70:
        st.markdown("<p class='status-good'>🟢 Section Operating Normally</p>", unsafe_allow_html=True)
    elif avg_capacity < 85:
        st.markdown("<p class='status-mid'>🟠 Section Near Capacity</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='status-bad'>🔴 Section Critical</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### 📦 Active Places in Section {section}")

    for item in section_data:

        if item["Capacity_Used"] < 70:
            status_color = "#22c55e"
        elif item["Capacity_Used"] < 85:
            status_color = "#f59e0b"
        else:
            status_color = "#ef4444"

        st.markdown(f"""
        <div class='section-card'>
        <h4>{item['Place_Name']}</h4>
        Category: {item['Category']} <br>
        Inventory Units: {item['Quantity']} <br>
        Capacity Used: <span style='color:{status_color}; font-weight:bold;'>
        {item['Capacity_Used']}%
        </span>
        </div>
        """, unsafe_allow_html=True)

        st.progress(item["Capacity_Used"]/100)

# ---------------- ADMIN & SECURITY ----------------
elif menu == "Admin & Security":

    st.subheader("🔐 Administrative Access")

    password = st.text_input("Enter Administrator Password", type="password")

    if password == "WMS@2026":

        st.success("Access Authorized")

        st.markdown("### ➕ Register New Warehouse Place")

        with st.form("new_place_form"):
            place = st.text_input("Place Name")
            category = st.text_input("Category")
            qty = st.number_input("Initial Quantity", min_value=0, step=1)
            section = st.text_input("Warehouse Section")
            capacity = st.slider("Capacity Utilization (%)", 0, 100)
            submitted = st.form_submit_button("Register Place")

            if submitted:
                new_id = max(item["Product_ID"] for item in data)+1
                new_entry = {
                    "Product_ID": new_id,
                    "Place_Name": place,
                    "Category": category,
                    "Quantity": qty,
                    "Warehouse_Section": section,
                    "Capacity_Used": capacity,
                    "Last_Backup": datetime.today().date().isoformat()
                }
                data.append(new_entry)
                st.success(f"✅ New Place {place} Registered Successfully")

        st.markdown("### 🗂️ Data Continuity")
        st.info(f"Last System Backup: {max(item['Last_Backup'] for item in data)}")

    elif password:
        st.error("❌ Unauthorized Access")