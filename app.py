import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Nassau Candy | Optimization Dashboard", page_icon="🍬", layout="wide")
DATA_DIR = Path(__file__).parent

FILES = {
    "Factory recommendations": "factory_recommendations.csv",
    "Factory performance": "factory_performance_summary.csv",
    "Product summary": "product_summary.csv",
    "Model comparison": "model_comparison.csv",
    "Factory–destination distances": "factory_destination_distances.csv",
    "Nearest-factory assignments": "nearest_factory_assignments.csv",
    "Single-factory comparison": "single_factory_distance_comparison.csv",
}

@st.cache_data
def read_csv(path):
    return pd.read_csv(path)

data, missing = {}, []
for label, filename in FILES.items():
    path = DATA_DIR / filename
    if path.exists():
        try:
            data[label] = read_csv(path)
        except Exception:
            missing.append(filename)
    else:
        missing.append(filename)

st.markdown("""
<style>
.stApp {background:radial-gradient(ellipse at top left,#142748 0%,#091426 48%,#070e1d 100%);color:#edf3ff}
[data-testid="stHeader"]{background:rgba(5,13,28,.85)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#101d38,#0a1428);border-right:1px solid #263a5e}
[data-testid="stSidebar"] *{color:#e6edff}
.block-container{padding-top:1.5rem;max-width:1500px}
h1,h2,h3{color:#f4f7ff!important}
p,label,[data-testid="stCaptionContainer"]{color:#c2cee4}
div[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(33,51,91,.95),rgba(17,31,59,.95));border:1px solid #30476f;border-radius:16px;padding:16px;box-shadow:0 8px 22px #0003}
div[data-testid="stMetricLabel"]{color:#bdc9e2}
div[data-testid="stMetricValue"]{color:#fff;font-weight:750}
div[data-testid="stPlotlyChart"]{background:rgba(13,26,49,.72);border:1px solid #263d63;border-radius:15px;padding:8px}
.stDownloadButton button,.stButton button{border-radius:10px;border:1px solid #48659a;background:#172d52;color:white}
hr{border-color:#263d63}
.hero{background:linear-gradient(110deg,rgba(29,49,92,.92),rgba(17,31,58,.85));border:1px solid #344d7b;padding:22px 25px;border-radius:18px;margin-bottom:16px}
.hero p{margin-bottom:0;color:#b9c9e5}
.pill{display:inline-block;background:#183c4c;color:#8ff0ce;border:1px solid #287c76;padding:4px 10px;border-radius:999px;font-size:.8rem;margin-bottom:8px}
</style>
""", unsafe_allow_html=True)

def col(df, candidates):
    norm = {str(c).lower().replace(" ", "_"): c for c in df.columns}
    for item in candidates:
        k = item.lower().replace(" ", "_")
        if k in norm:
            return norm[k]
    for c in df.columns:
        if any(item.lower().replace(" ", "_") in str(c).lower().replace(" ", "_") for item in candidates):
            return c
    return None

def dark(fig, height=350):
    fig.update_layout(height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce7fb",family="Arial"),margin=dict(l=12,r=12,t=45,b=12),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_xaxes(gridcolor="#203454",zerolinecolor="#203454")
    fig.update_yaxes(gridcolor="#203454",zerolinecolor="#203454")
    return fig

st.sidebar.markdown("<div style='padding:10px 4px 22px'><div style='font-size:1.45rem;font-weight:800'>🍬 Nassau Candy</div><div style='color:#9fb5d8'>Factory & Shipping Optimization</div></div>",unsafe_allow_html=True)
pages = ["Overview"] + list(FILES.keys()) + ["About & Limitations"]
page = st.sidebar.radio("NAVIGATION", pages)
st.sidebar.markdown("---")
st.sidebar.caption("Better insights. More informed decisions.")
if missing:
    st.sidebar.warning("Missing files: " + ", ".join(missing))

if page == "Overview":
    st.markdown("<div class='hero'><div class='pill'>DATA • INSIGHTS • DECISIONS</div><h1 style='margin:0'>🍭 Factory & Shipping Optimization</h1><p>Nassau Candy Distributor · Interactive decision-support dashboard</p></div>",unsafe_allow_html=True)
    st.info("Exploratory analysis and proposed recommendations only. This is not an automated factory-allocation optimizer; review the README for data-quality concerns and assumptions.")
    rec = data.get("Factory recommendations")
    perf = data.get("Factory performance")
    models = data.get("Model comparison")
    product = col(rec,["Product_Name","Product"]) if rec is not None else None
    factory = col(rec,["Assigned_Factory","Factory"]) if rec is not None else None
    sales = col(rec,["Total_Sales","Sales"]) if rec is not None else None
    profit = col(rec,["Total_Profit","Profit"]) if rec is not None else None
    units = col(rec,["Total_Units","Units"]) if rec is not None else None
    margin = col(rec,["Profit_Margin_Percent","Profit Margin"]) if rec is not None else None
    def num(c):
        return pd.to_numeric(rec[c],errors="coerce") if rec is not None and c else pd.Series(dtype=float)
    k = st.columns(5)
    k[0].metric("Products reviewed", f"{rec[product].nunique():,}" if rec is not None and product else "—")
    k[1].metric("Total sales", f"₹{num(sales).sum():,.2f}" if sales else "—")
    k[2].metric("Total profit", f"₹{num(profit).sum():,.2f}" if profit else "—")
    k[3].metric("Total units", f"{num(units).sum():,.0f}" if units else "—")
    k[4].metric("Avg. profit margin", f"{num(margin).mean():.2f}%" if margin else "—")

    left,right=st.columns([1.6,1])
    with left:
        st.subheader("📊 Sales vs. profit")
        if rec is not None and product and sales and profit:
            d=rec[[product,sales,profit]].copy()
            d[sales]=pd.to_numeric(d[sales],errors="coerce"); d[profit]=pd.to_numeric(d[profit],errors="coerce")
            d=d.nlargest(5,sales).sort_values(sales)
            fig=go.Figure()
            fig.add_bar(name="Total sales",x=d[product],y=d[sales],marker_color="#60a5fa")
            fig.add_bar(name="Total profit",x=d[product],y=d[profit],marker_color="#e879c5")
            fig.update_layout(barmode="group",xaxis_title="",yaxis_title="Amount",xaxis_tickangle=-18)
            st.plotly_chart(dark(fig,390),use_container_width=True)
        else: st.warning("Sales/profit chart unavailable: expected columns were not found.")
    with right:
        st.subheader("🏭 Products by factory")
        if rec is not None and factory:
            d=rec[factory].fillna("Unassigned").value_counts().rename_axis("Factory").reset_index(name="Products")
            fig=px.pie(d,names="Factory",values="Products",hole=.62,color_discrete_sequence=["#a78bfa","#f472b6","#2dd4bf","#fbbf24","#60a5fa"])
            fig.update_traces(textposition="inside",textinfo="percent")
            fig.update_layout(annotations=[dict(text=f"{d['Products'].sum()}<br>Products",x=.5,y=.5,font_size=18,showarrow=False)])
            st.plotly_chart(dark(fig,390),use_container_width=True)
        else: st.warning("Factory chart unavailable: factory column was not found.")

    st.subheader("✨ Product recommendations")
    if rec is not None:
        st.dataframe(rec,use_container_width=True,hide_index=True,height=350)
        st.download_button("⬇ Download recommendations CSV",rec.to_csv(index=False).encode(),file_name="factory_recommendations.csv",mime="text/csv")
    else: st.warning("factory_recommendations.csv was not found beside app.py.")
    c1,c2=st.columns(2)
    with c1:
        st.subheader("📈 Factory performance")
        if perf is not None: st.dataframe(perf,use_container_width=True,hide_index=True)
    with c2:
        st.subheader("🧠 Model comparison")
        if models is not None: st.dataframe(models,use_container_width=True,hide_index=True)

elif page == "About & Limitations":
    st.markdown("<div class='hero'><h1>ℹ️ About this project</h1><p>Scope, assumptions, and responsible interpretation.</p></div>",unsafe_allow_html=True)
    st.markdown("""
### Project scope
- Summarizes product and factory performance.
- Compares machine-learning lead-time prediction models.
- Explores straight-line geographic distances to selected destinations.
- Presents proposed product/factory assignments for review.

### Important limitations
- The source data contains date inconsistencies and unusually long calculated shipping lead times.
- Product-to-factory assignments are proposed/predefined mappings, not outputs from a constrained optimizer.
- Factory coordinates are assumptions and have not been independently verified.
- Geographic distances are straight-line estimates, not road distances or actual shipping routes.
- Geographic analysis covers selected destinations rather than every destination.
- Factory capacity, inventory, transportation prices, and operational constraints are not modeled.
- Model scores describe performance on the available dataset and do not guarantee future accuracy.

Treat results as exploratory decision support. Validate the data, locations, production capability, inventory, and logistics costs before operational use.
""")
else:
    df=data.get(page)
    st.markdown(f"<div class='hero'><h1>📂 {page}</h1><p>Explore, filter, chart, and download the prepared project data.</p></div>",unsafe_allow_html=True)
    if df is None:
        st.error("This CSV was not found. Make sure it is in the same repository folder as app.py.")
    else:
        search=st.text_input("🔎 Search this table",placeholder="Type a product, factory, or value...")
        view=df
        if search:
            mask=df.astype(str).apply(lambda s:s.str.contains(search,case=False,na=False)).any(axis=1)
            view=df[mask]
        st.caption(f"Showing {len(view):,} of {len(df):,} rows · {len(df.columns)} columns")
        st.dataframe(view,use_container_width=True,hide_index=True,height=470)
        st.download_button("⬇ Download filtered data",view.to_csv(index=False).encode(),file_name=f"{page.lower().replace('–','_').replace(' ','_')}.csv",mime="text/csv")
        numeric=view.select_dtypes(include="number").columns.tolist()
        textcols=view.select_dtypes(exclude="number").columns.tolist()
        if numeric and len(view)>1:
            with st.expander("📊 Build a quick chart"):
                y=st.selectbox("Value to plot",numeric)
                if textcols:
                    x=st.selectbox("Group by",textcols)
                    d=view[[x,y]].dropna().head(100)
                    if not d.empty: st.plotly_chart(dark(px.bar(d,x=x,y=y,color_discrete_sequence=["#60a5fa"]),380),use_container_width=True)
                else: st.plotly_chart(dark(px.histogram(view,x=y,color_discrete_sequence=["#60a5fa"]),380),use_container_width=True)

st.markdown("---")
st.caption("Nassau Candy Distributor · Academic project dashboard · Verify assumptions before operational use.")
