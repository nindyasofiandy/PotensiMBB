import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

st.set_page_config(page_title="Data Site", layout="wide")

st.title("")
data = pd.read_csv("Data_Potensi_MBBRiskLevel.csv")
dataRiskScore = pd.read_csv("riskScoreSite.csv")

with st.sidebar:
    selected = option_menu("Menu", ["Dataset Overview", "Data Distribution", "Analysis"], icons=['graph-up', 'gear-wide-connected', 'graph-up'])

if selected == "Dataset Overview":
    st.markdown("<h1 style='text-align: center; color: #D32F2F; margin-bottom: 0px;'>Dataset Overview</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <hr style="border:0; border-top:1px solid #444944; margin-top:8px; margin-bottom:30px;">
        """, 
        unsafe_allow_html=True
    )

    totalData = len(data)
    totalColumn = len(data.columns)
    totalSite = data["Site Name"].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.html(
            f"""
            <div style="
                background-color:#EDBFBF;
                padding:18px;
                border-radius:12px;
                text-align:center;
            ">
                <div style="
                    font-size: 28px;
                    font-weight: 700;
                    color:#000000;
                ">
                    {totalData:,} 
                </div>

                <div style="
                    font-size:14px;
                    color:#000000;
                    margin-top:5px;
                ">
                    Total Data
                </div>
            
            </div>
            """
        )

    with col2:
        st.html(
            f"""
            <div style="
                background-color:#EDBFBF;
                padding:18px;
                border-radius:12px;
                text-align:center;
            ">
                <div style="
                    font-size: 28px;
                    font-weight: 700;
                    color:#000000;
                ">
                    {totalColumn:,} 
                </div>
                
                <div style="
                    font-size:14px;
                    color:#000000;
                    margin-top:5px;
                ">
                    Total Kolom
                </div>
            
            </div>
            """
        )

    with col3:
        st.html(
            f"""
            <div style="
                background-color:#EDBFBF;
                padding:18px;
                border-radius:12px;
                text-align:center;
            ">
                <div style="
                    font-size: 28px;
                    font-weight: 700;
                    color:#000000;
                ">
                    {totalSite:,} 
                </div>
            
                <div style="
                    font-size:14px;
                    color:#000000;
                    margin-top:5px;
                ">
                    Total Site
                </div>

            </div>
            """
        )

    st.dataframe(data.head(20))

if selected == "Data Distribution":
    st.markdown("<h1 style='text-align: center; color: #D32F2F; margin-bottom: 0px;'>Data Distribution</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <hr style="border:0; border-top:1px solid #444944; margin-top:8px; margin-bottom:30px;">
        """, 
        unsafe_allow_html=True
    )

    st.markdown("<div style='text-align: center; font-weight:bold'>Device Distribution by Site</div>", unsafe_allow_html=True)
    deviceSite = (
        data.groupby("Site Name")["Hostname"].nunique().reset_index(name="Total Device").sort_values("Total Device", ascending=False)
    )

    figDevice = px.bar(
        deviceSite,
        x="Site Name",
        y="Total Device",
        text="Total Device",
        color_discrete_sequence=["#5673C2"]
    )

    figDevice.update_layout(
        xaxis_title="Site",
        yaxis_title="Total Device"
    )

    figDevice.update_traces(textposition="outside")
    st.plotly_chart(figDevice, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='text-align: center; font-weight:bold'>XDR Status Distribution</div>", unsafe_allow_html=True)
        xdrDistribution = data[["Xdr Status"]].value_counts().reset_index()
        xdrDistribution.columns = ["XDR Status", "Total Device"]

        figXDR = px.pie(
            xdrDistribution,
            names="XDR Status",
            values="Total Device",
            hole=0.4,
            color="XDR Status",
            color_discrete_map={
                "DONE": "#55A059",
                "Exclude": "#DE9F3F",
                "Not Feasible": "#9E9E9E"
            }
        )

        figXDR.update_traces(textposition="inside", textfont=dict(color="black"))
        st.plotly_chart(figXDR, use_container_width=True)

    with col2:
        st.markdown("<div style='text-align: center; font-weight:bold'>UIM Status Distribution</div>", unsafe_allow_html=True)
        uimDistribution = data[["Uim Status"]].value_counts().reset_index()
        uimDistribution.columns = ["UIM Status", "Total Device"]

        figUIM = px.pie(
            uimDistribution,
            names="UIM Status",
            values="Total Device",
            hole=0.4,
            color="UIM Status",
            color_discrete_map={
                "Monitored UIM": "#55A059",
                "Not Installed Agent UIM": "#E14949",
                "Not Available": "#9E9E9E",
                "Agent UIM Inactive": "#DE9F3F"
            }          
        )

        figUIM.update_traces(textposition="inside", textfont=dict(color="black"))
        st.plotly_chart(figUIM, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div style='text-align: center; font-weight:bold'>SIEM Status Distribution</div>", unsafe_allow_html=True)
        siemDistribution = data[["Siem Status"]].value_counts().reset_index()
        siemDistribution.columns = ["SIEM Status", "Total Device"]

        figSIEM = px.pie(
            siemDistribution,
            names="SIEM Status",
            values="Total Device",
            hole=0.4,
            color="SIEM Status",
            color_discrete_map={
                "DONE": "#55A059",
                "Not Feasible": "#9E9E9E"
            }
        )

        figSIEM.update_traces(textposition="inside", textfont=dict(color="black"))
        st.plotly_chart(figSIEM, use_container_width=True)

    with col4:
        st.markdown("<div style='text-align: center; font-weight:bold'>EoS Distribution</div>", unsafe_allow_html=True)
        eosDistribution = (
            data["Eos Date"].value_counts().reset_index()
        )
        eosDistribution.columns= ["Eos Date", "Total Device"]

        figEOS = px.pie(
            eosDistribution,
            names="Eos Date",
            values="Total Device",
            hole=0.4,
            color="Eos Date",
            color_discrete_map={
                2025: "#E14949",
                2026: "#DE9F3F",
                2027: "#C5D655",
                2028: "#55A059"
            }  
        )

        figEOS.update_traces(textposition="inside", textfont=dict(color="black"))
        st.plotly_chart(figEOS, use_container_width=True)

    col5, col6, col7 = st.columns([1, 2, 1])
    with col6:
        st.markdown("<div style='text-align: center; font-weight:bold'>Risk Level Distribution</div>", unsafe_allow_html=True)
        riskDistribution = (
            data["Risk Level"].value_counts().reset_index()
        )
        riskDistribution.columns = ["Risk Level", "Total Device"]

        figRisk = px.bar(
            riskDistribution,
            x="Risk Level",
            y="Total Device",
            text="Total Device",
            color="Risk Level",
            color_discrete_map={
                "High":"#E14949",
                "Medium":"#DE9F3F",
                "Low":"#55A059"
            }
        )

        figRisk.update_traces(textposition="outside")
        st.plotly_chart(figRisk, use_container_width=True)

if selected == "Analysis":
    st.markdown("<h1 style='text-align: center; color: #D32F2F; margin-bottom:0px'>Analysis</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <hr style="border:0; border-top:1px solid #444944; margin-top:8px; margin-bottom:30px;">
        """, 
        unsafe_allow_html=True
    )

    st.markdown("<div style='text-align: center; font-weight:bold;'>Top 5 Priority Sites</div>", unsafe_allow_html=True)
    topSite = (
        dataRiskScore.sort_values("Risk Score", ascending=False).head(5)
    )

    figTopSite = px.bar(
        topSite,
        x="Risk Score",
        y="Site Name",
        orientation="h",
        text="Risk Score",
        color_discrete_sequence=["#5673C2"]
    )

    figTopSite.update_traces(textposition="inside", textfont=dict(color="white"))
    figTopSite.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(figTopSite, use_container_width=True)

    st.markdown("<h2 style='text-align: center; font-size: 30px;'><b>Device Risk</b></h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='text-align: center; font-weight:bold;'>Risk Level by Site</div>", unsafe_allow_html=True)
        siteRisk = (
            data.groupby(["Site Name", "Risk Level"])["Hostname"].nunique().unstack(fill_value=0).reset_index()
        )

        siteRisk = siteRisk.sort_values(by="High", ascending=False)

        figSiteRisk = px.bar(
            siteRisk,
            x="Site Name",
            y=["High", "Medium", "Low"],
            barmode="stack",
            labels={
                "variable": "Risk Level"
            },
            color_discrete_map={
                "High": "#E14949",
                "Medium": "#DE9F3F",
                "Low": "#55A059"
            }
        )

        st.plotly_chart(figSiteRisk, use_container_width=True)

    with col2:
        st.markdown("<div style='text-align: center; font-weight:bold;'>Top 10 Device with High Risk</div>", unsafe_allow_html=True)
        deviceRisk = (
            data[["Hostname", "Site Name", "Klasifikasi Risk Score", "Risk Level", "Eos Date"]].sort_values("Klasifikasi Risk Score", ascending=False).head(10).sort_values("Klasifikasi Risk Score", ascending=True)
        )

        deviceRisk["Device"] = (
            deviceRisk["Hostname"] + " - " + deviceRisk["Site Name"]
        )

        figDeviceRisk = px.bar(
            deviceRisk,
            x="Klasifikasi Risk Score",
            y="Device",
            orientation="h",
            text="Klasifikasi Risk Score",
            color_discrete_sequence=["#5673C2"]
        )

        figDeviceRisk.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        figDeviceRisk.update_traces(textposition="inside", textfont=dict(color="white"))
        st.plotly_chart(figDeviceRisk, use_container_width=True)

    st.markdown("<h2 style='text-align: center; font-size: 30px;'><b>Device Replacement</b></h2>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div style='text-align: center; font-weight:bold;'>Device Replacement by Year (2026 - 2030)</div>", unsafe_allow_html=True)
        yearReplacement = (
            data[data["Eos Date"].between(2026, 2030)].groupby("Eos Date")["Hostname"].nunique().reset_index(name="Total Device")
        )
        
        yearReplacement = yearReplacement.sort_values(by="Total Device", ascending=False)

        figyearReplacement = px.pie(
            yearReplacement,
            names="Eos Date",
            values="Total Device",
            hole=0.4,
            color="Eos Date",
            color_discrete_map={
                2026: "#E14949",
                2027: "#DE9F3F",
                2028: "#55A059"
            }
        )
        figyearReplacement.update_traces(textposition="inside", textfont=dict(color="black"))
        st.plotly_chart(figyearReplacement, use_container_width=True)

    with col4:
        st.markdown("<div style='text-align: center; font-weight:bold;'>Device Replacement by Site</div>", unsafe_allow_html=True)
        siteReplacement = (
            data[data["Eos Date"].between(2026, 2030)].groupby(["Site Name", "Eos Date"])["Hostname"].nunique().reset_index(name="Total Device")
        )
        siteReplacement["Eos Date"] = siteReplacement["Eos Date"].astype(str)

        totalSite = (
            siteReplacement.groupby("Site Name")["Total Device"].sum().sort_values(ascending=False)
        )

        siteReplacement["Site Name"] = pd.Categorical(
            siteReplacement["Site Name"],
            categories=totalSite.index,
            ordered=True
        )

        figSiteReplacement = px.bar(
            siteReplacement,
            x="Site Name",
            y="Total Device",
            color="Eos Date",
            color_discrete_map={
                "2026": "#E14949",
                "2027": "#DE9F3F",
                "2028": "#55A059"
            }
        )

        figSiteReplacement.update_layout(
            xaxis_title="Site Name",
            yaxis_title="Total Device",
            legend_title = "Eos Year"
        )

        st.plotly_chart(figSiteReplacement, use_container_width=True)