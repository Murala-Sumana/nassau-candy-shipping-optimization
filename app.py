import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Nassau Candy | Decision Intelligence", page_icon="🍬", layout="wide")
BASE = Path(__file__).parent
RAW_CANDIDATES = ["Nassau Candy Distributor (3).csv", "Nassau Candy Distributor.csv"]
RAW_PATH = next((BASE / name for name in RAW_CANDIDATES if (BASE / name).exists()), None)
FILES = {
    "Factory recommendations": "factory_recommendations.csv",
    "Factory performance": "factory_performance_summary.csv",
    "Product summary": "product_summary.csv",
    "Model comparison": "model_comparison.csv",
    "Factory–destination distances": "factory_destination_distances.csv",
    "Nearest-factory assignments": "nearest_factory_assignments.csv",
    "Single-factory comparison": "single_factory_distance_comparison.csv",
}
FACTORIES = ["Lot's O' Nuts", "Wicked Choccy's", "Sugar Shack", "Secret Factory", "The Other Factory"]

@st.cache_data
def read_csv(path):
    return pd.read_csv(path, low_memory=False)

data, missing = {}, []
for label, filename in FILES.items():
    path = BASE / filename
    if path.exists():
        try:
            data[label] = read_csv(path)
        except Exception:
            missing.append(filename)
    else:
        missing.append(filename)
raw = read_csv(RAW_PATH) if RAW_PATH else None

st.markdown("""
<style>
.stApp{background:radial-gradient(ellipse at top left,#142748 0%,#091426 48%,#070e1d 100%);color:#edf3ff}
[data-testid="stHeader"]{background:rgba(5,13,28,.85)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#101d38,#0a1428);border-right:1px solid #263a5e}
[data-testid="stSidebar"] *{color:#e6edff}
.block-container{padding-top:1.3rem;max-width:1550px}
h1,h2,h3{color:#f4f7ff!important}
p,label,[data-testid="stCaptionContainer"]{color:#c2cee4}
div[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(33,51,91,.95),rgba(17,31,59,.95));border:1px solid #30476f;border-radius:16px;padding:15px;box-shadow:0 8px 22px #0003}
div[data-testid="stMetricLabel"]{color:#bdc9e2} div[data-testid="stMetricValue"]{color:#fff;font-weight:750}
div[data-testid="stPlotlyChart"]{background:rgba(13,26,49,.72);border:1px solid #263d63;border-radius:15px;padding:7px}
.stDownloadButton button,.stButton button{border-radius:10px;border:1px solid #48659a;background:#172d52;color:white}
hr{border-color:#263d63}
.hero{background:linear-gradient(110deg,rgba(29,49,92,.92),rgba(17,31,58,.85));border:1px solid #344d7b;padding:22px 25px;border-radius:18px;margin-bottom:16px}
.hero p{margin-bottom:0;color:#b9c9e5}.pill{display:inline-block;background:#183c4c;color:#8ff0ce;border:1px solid #287c76;padding:4px 10px;border-radius:999px;font-size:.8rem;margin-bottom:8px}
</style>
""", unsafe_allow_html=True)

def col(df, candidates):
    if df is None: return None
    norm = {str(c).lower().replace(" ", "_"): c for c in df.columns}
    for item in candidates:
        k = item.lower().replace(" ", "_")
        if k in norm: return norm[k]
    for c in df.columns:
        if any(item.lower().replace(" ", "_") in str(c).lower().replace(" ", "_") for item in candidates): return c
    return None

def dark(fig, height=350):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce7fb", family="Arial"), margin=dict(l=12,r=12,t=45,b=12),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_xaxes(gridcolor="#203454",zerolinecolor="#203454")
    fig.update_yaxes(gridcolor="#203454",zerolinecolor="#203454")
    return fig

def money(v):
    return f"${v:,.2f}"

st.sidebar.markdown("<div style='padding:10px 4px 22px'><div style='font-size:1.45rem;font-weight:800'>🍬 Nassau Candy</div><div style='color:#9fb5d8'>Factory & Shipping Decision Intelligence</div></div>", unsafe_allow_html=True)
pages = ["Overview", "Factory Optimization Simulator", "What-If Scenario Analysis", "Recommendation Dashboard", "Risk & Impact Panel"] + list(FILES.keys()) + ["Raw Data Explorer", "About & Limitations"]
page = st.sidebar.radio("NAVIGATION", pages)
st.sidebar.markdown("---")
st.sidebar.caption("Explore scenarios. Validate assumptions before decisions.")
if raw is None:
    st.sidebar.warning("Raw dataset not found. Upload the original CSV beside app.py to enable order filters.")
if missing:
    st.sidebar.caption("Some optional summary CSVs are missing: " + ", ".join(missing))

rec = data.get("Factory recommendations")
perf = data.get("Factory performance")
models = data.get("Model comparison")
distances = data.get("Factory–destination distances")
product = col(rec, ["Product_Name", "Product Name", "Product"]) if rec is not None else None
factory = col(rec, ["Assigned_Factory", "Assigned Factory", "Factory"]) if rec is not None else None
sales = col(rec, ["Total_Sales", "Total Sales", "Sales"]) if rec is not None else None
profit = col(rec, ["Total_Profit", "Total Profit", "Profit"]) if rec is not None else None
units = col(rec, ["Total_Units", "Total Units", "Units"]) if rec is not None else None
margin = col(rec, ["Profit_Margin_Percent", "Profit Margin Percent", "Profit Margin"]) if rec is not None else None

if page == "Overview":
    st.markdown("<div class='hero'><div class='pill'>DATA • INSIGHTS • SCENARIOS</div><h1 style='margin:0'>🍭 Factory & Shipping Decision Intelligence</h1><p>Nassau Candy Distributor · Interactive analytics and scenario exploration</p></div>", unsafe_allow_html=True)
    st.info("This is an exploratory decision-support prototype. Factory alternatives are scenario candidates, not verified feasible assignments. Distances are straight-line estimates; shipping-cost and capacity data are unavailable.")
    if rec is not None:
        def num(c): return pd.to_numeric(rec[c], errors="coerce") if c else pd.Series(dtype=float)
        k=st.columns(5)
        k[0].metric("Products reviewed", f"{rec[product].nunique():,}" if product else "—")
        k[1].metric("Total sales", money(num(sales).sum()) if sales else "—")
        k[2].metric("Total profit", money(num(profit).sum()) if profit else "—")
        k[3].metric("Units", f"{num(units).sum():,.0f}" if units else "—")
        k[4].metric("Mean product margin", f"{num(margin).mean():.1f}%" if margin else "—")
        a,b=st.columns([1.5,1])
        with a:
            st.subheader("Sales vs profit by product")
            if product and sales and profit:
                d=rec[[product,sales,profit]].copy()
                d[sales]=pd.to_numeric(d[sales],errors="coerce"); d[profit]=pd.to_numeric(d[profit],errors="coerce")
                d=d.nlargest(8,sales).sort_values(sales)
                fig=go.Figure(); fig.add_bar(name="Sales",x=d[product],y=d[sales],marker_color="#60a5fa"); fig.add_bar(name="Profit",x=d[product],y=d[profit],marker_color="#e879c5")
                fig.update_layout(barmode="group",xaxis_title="",yaxis_title="Dataset amount",xaxis_tickangle=-20)
                st.plotly_chart(dark(fig,390),use_container_width=True)
        with b:
            st.subheader("Products by current mapped factory")
            if factory:
                d=rec[factory].fillna("Unassigned").value_counts().rename_axis("Factory").reset_index(name="Products")
                st.plotly_chart(dark(px.pie(d,names="Factory",values="Products",hole=.6,color_discrete_sequence=["#a78bfa","#f472b6","#2dd4bf","#fbbf24","#60a5fa"]),390),use_container_width=True)
    if raw is not None:
        st.subheader("Order dataset snapshot")
        st.caption(f"{len(raw):,} rows · {raw.shape[1]} columns · Raw CSV loaded")
        st.dataframe(raw.head(8),use_container_width=True,hide_index=True)
    st.subheader("Start exploring")
    st.write("Use the **Factory Optimization Simulator** to compare straight-line distance by destination, or **What-If Scenario Analysis** to inspect how a candidate assignment compares with the current mapped factory.")

elif page == "Factory Optimization Simulator":
    st.markdown("<div class='hero'><h1>🧭 Factory Optimization Simulator</h1><p>Compare candidate factories for a selected product and destination.</p></div>",unsafe_allow_html=True)
    st.warning("Candidate factories are not confirmed production-compatible. Distance is straight-line distance, not road distance, actual delivery time, or shipping cost.")
    if rec is None or distances is None:
        st.error("Required recommendation or distance CSV is missing.")
    else:
        prod_list=sorted(rec[product].dropna().unique()) if product else []
        citycol=col(distances,["City"]); postalcol=col(distances,["Postal Code"]); dist_factory=col(distances,["Factory"]); kmcol=col(distances,["Distance_km","Distance km"])
        left,right=st.columns(2)
        with left: chosen_product=st.selectbox("Select product",prod_list)
        with right:
            destinations=distances[[citycol,postalcol]].drop_duplicates().copy()
            destinations["Destination label"]=destinations[citycol].astype(str)+" · ZIP "+destinations[postalcol].astype(str)
            chosen_dest=st.selectbox("Select destination",destinations["Destination label"].tolist())
        selected=destinations[destinations["Destination label"]==chosen_dest].iloc[0]
        city,postal=selected[citycol],selected[postalcol]
        row=rec[rec[product]==chosen_product].iloc[0]
        current=row[factory] if factory else "Not mapped"
        opts=distances[(distances[citycol]==city)&(distances[postalcol].astype(str)==str(postal))].copy()
        opts[kmcol]=pd.to_numeric(opts[kmcol],errors="coerce")
        opts=opts.sort_values(kmcol)
        candidate=st.selectbox("Compare with candidate factory",opts[dist_factory].tolist(),index=opts[dist_factory].tolist().index(current) if current in opts[dist_factory].tolist() else 0)
        currrow=opts[opts[dist_factory]==current]
        candrow=opts[opts[dist_factory]==candidate]
        c1,c2,c3=st.columns(3)
        c1.metric("Current mapped factory",str(current))
        c2.metric("Current straight-line distance",f"{currrow[kmcol].iloc[0]:,.0f} km" if not currrow.empty else "N/A")
        cand_km=float(candrow[kmcol].iloc[0]) if not candrow.empty else None
        current_km=float(currrow[kmcol].iloc[0]) if not currrow.empty else None
        c3.metric("Candidate distance",f"{cand_km:,.0f} km" if cand_km is not None else "N/A",delta=(f"{current_km-cand_km:,.0f} km shorter" if current_km is not None and cand_km is not None and current_km>=cand_km else (f"{cand_km-current_km:,.0f} km longer" if current_km is not None and cand_km is not None else None)))
        fig=px.bar(opts,x=dist_factory,y=kmcol,color=dist_factory,color_discrete_sequence=["#60a5fa","#e879c5","#2dd4bf","#fbbf24","#a78bfa"],labels={dist_factory:"Candidate factory",kmcol:"Straight-line distance (km)"},title=f"Candidate distances to {city} ({postal})")
        st.plotly_chart(dark(fig,380),use_container_width=True)
        st.subheader("Product business context")
        c1,c2,c3=st.columns(3)
        c1.metric("Recorded sales",money(float(row[sales])) if sales else "N/A")
        c2.metric("Recorded gross profit",money(float(row[profit])) if profit else "N/A")
        c3.metric("Profit margin",f"{float(row[margin]):.2f}%" if margin else "N/A")
        st.caption("No monetary shipping impact is calculated because transportation costs and factory capacity are not available. Validate production capability before treating any alternative as feasible.")

elif page == "What-If Scenario Analysis":
    st.markdown("<div class='hero'><h1>🔀 What-If Scenario Analysis</h1><p>Inspect the distance difference between the current mapping and a proposed factory.</p></div>",unsafe_allow_html=True)
    st.warning("This scenario estimates geographic distance only. It does not predict actual lead-time savings or profit changes.")
    if rec is not None and distances is not None:
        citycol=col(distances,["City"]); postalcol=col(distances,["Postal Code"]); faccol=col(distances,["Factory"]); kmcol=col(distances,["Distance_km"])
        products=sorted(rec[product].dropna().unique())
        p=st.selectbox("Product",products)
        rr=rec[rec[product]==p].iloc[0]; current=rr[factory]
        locs=distances[[citycol,postalcol]].drop_duplicates().copy(); locs["label"]=locs[citycol].astype(str)+" · ZIP "+locs[postalcol].astype(str)
        label=st.selectbox("Destination",locs.label.tolist()); loc=locs[locs.label==label].iloc[0]
        d=distances[(distances[citycol]==loc[citycol])&(distances[postalcol].astype(str)==str(loc[postalcol]))].copy(); d[kmcol]=pd.to_numeric(d[kmcol],errors="coerce")
        available=d[faccol].tolist(); default=available.index(current) if current in available else 0
        proposed=st.selectbox("Proposed factory",available,index=default)
        a=d[d[faccol]==current][kmcol]; b=d[d[faccol]==proposed][kmcol]
        if not a.empty and not b.empty:
            before=float(a.iloc[0]); after=float(b.iloc[0]); delta=before-after; pct=(delta/before*100) if before else 0
            x,y,z=st.columns(3); x.metric("Current distance",f"{before:,.1f} km"); y.metric("Proposed distance",f"{after:,.1f} km"); z.metric("Distance difference",f"{delta:+,.1f} km",delta=f"{pct:+.1f}% of current distance")
            st.plotly_chart(dark(px.bar(pd.DataFrame({"Scenario":["Current mapping","Proposed mapping"],"Distance (km)":[before,after]}),x="Scenario",y="Distance (km)",color="Scenario",color_discrete_sequence=["#60a5fa","#2dd4bf"],title="Current vs proposed distance"),350),use_container_width=True)
            if proposed==current: st.info("The proposed factory is the same as the current mapping; no distance change in this scenario.")
            elif after<before: st.success("This candidate is geographically closer for the selected destination. Production feasibility, route distance, shipping mode, and cost still need validation.")
            else: st.warning("This candidate is farther away for the selected destination; there may be other business reasons to consider it, but those are not modeled here.")
        st.subheader("Profit context (unchanged in this simulation)")
        c1,c2=st.columns(2); c1.metric("Historical product profit",money(float(rr[profit])) if profit else "N/A"); c2.metric("Historical product margin",f"{float(rr[margin]):.2f}%" if margin else "N/A")
        st.caption("Profit is shown for context only; no profit improvement is claimed because logistics costs are absent from the dataset.")

elif page == "Recommendation Dashboard":
    st.markdown("<div class='hero'><h1>✨ Recommendation Dashboard</h1><p>Rank candidate scenarios using distance and business-review context.</p></div>",unsafe_allow_html=True)
    st.warning("The priority slider ranks geographic candidates; it does not represent a validated cost optimizer. Product-factory compatibility and capacity are not supplied.")
    if rec is not None and distances is not None:
        speed_weight=st.slider("Optimization priority: speed / distance vs profit risk",0,100,70,5,help="Higher values give more weight to shorter straight-line distance. Lower values give more weight to preserving high-margin products; shipping cost is not modeled.")
        st.caption(f"Distance priority: {speed_weight}% · Margin-protection priority: {100-speed_weight}%")
        citycol=col(distances,["City"]); postalcol=col(distances,["Postal Code"]); faccol=col(distances,["Factory"]); kmcol=col(distances,["Distance_km"])
        citylist=sorted(distances[citycol].dropna().astype(str).unique()); chosen_city=st.selectbox("Region / destination city",["All available cities"]+citylist)
        rows=[]
        for _,r in rec.iterrows():
            base_factory=r[factory] if factory else "Unknown"
            sub=distances.copy()
            if chosen_city!="All available cities": sub=sub[sub[citycol].astype(str)==chosen_city]
            if sub.empty: continue
            # summarize each candidate's distances across the chosen destination set
            sub[kmcol]=pd.to_numeric(sub[kmcol],errors="coerce")
            mean_dist=sub.groupby(faccol)[kmcol].mean()
            if base_factory not in mean_dist.index: continue
            base_distance=float(mean_dist[base_factory])
            margin_value=float(pd.to_numeric(pd.Series([r[margin] if margin else 0]),errors="coerce").fillna(0).iloc[0])
            for f,dist in mean_dist.items():
                if pd.isna(dist): continue
                dist=float(dist); distance_gain=base_distance-dist
                # transparent normalized score, not an optimizer objective from business cost data
                maxd=max(float(mean_dist.max()),1.0)
                distance_score=100*(1-dist/maxd)
                margin_score=max(0,min(100,margin_value))
                score=(speed_weight/100)*distance_score+((100-speed_weight)/100)*margin_score
                rows.append({"Product":r[product],"Current factory":base_factory,"Candidate factory":f,"Mean straight-line distance (km)":round(dist,1),"Distance change vs current (km)":round(distance_gain,1),"Product margin (%)":round(margin_value,2),"Priority score (heuristic)":round(score,2),"Review flag":"Low margin — review" if margin_value<20 else "Check feasibility"})
        ranked=pd.DataFrame(rows)
        if not ranked.empty:
            ranked=ranked[ranked["Candidate factory"]!=ranked["Current factory"]].sort_values("Priority score (heuristic)",ascending=False)
            st.dataframe(ranked.head(30),use_container_width=True,hide_index=True)
            st.download_button("Download candidate ranking CSV",ranked.to_csv(index=False).encode(),"candidate_reassignment_ranking.csv","text/csv")
            st.caption("Score is a transparent heuristic combining normalized distance and product margin; it is not a learned prediction or proof of optimality. Candidate rows should be reviewed for production suitability and capacity.")
        else: st.info("No candidate rows available for the selected filter.")

elif page == "Risk & Impact Panel":
    st.markdown("<div class='hero'><h1>⚠️ Risk & Impact Panel</h1><p>Review data quality and business risks before acting on candidate assignments.</p></div>",unsafe_allow_html=True)
    if rec is not None and margin:
        rr=rec.copy(); rr[margin]=pd.to_numeric(rr[margin],errors="coerce")
        low=rr[rr[margin]<20]
        a,b,c=st.columns(3); a.metric("Products below 20% margin",len(low)); b.metric("Products reviewed",len(rr)); c.metric("Shipping cost data","Unavailable")
        st.subheader("Low-margin review alerts")
        if not low.empty: st.dataframe(low,use_container_width=True,hide_index=True)
        else: st.success("No products are below the 20% review threshold in the recommendation table.")
    if raw is not None:
        st.subheader("Date and lead-time data quality")
        date_order=col(raw,["Order Date"]); date_ship=col(raw,["Ship Date"])
        if date_order and date_ship:
            tmp=raw[[date_order,date_ship]].copy()
            tmp[date_order]=pd.to_datetime(tmp[date_order],dayfirst=True,errors="coerce"); tmp[date_ship]=pd.to_datetime(tmp[date_ship],dayfirst=True,errors="coerce")
            tmp["Observed lead time (days)"]=(tmp[date_ship]-tmp[date_order]).dt.days
            invalid=int((tmp["Observed lead time (days)"].isna() | (tmp["Observed lead time (days)"]<0)).sum())
            positive=tmp.loc[tmp["Observed lead time (days)"]>=0,"Observed lead time (days)"]
            long_count=int((positive>90).sum())
            x,y,z=st.columns(3); x.metric("Rows with invalid/missing dates",f"{invalid:,}"); y.metric("Rows with lead time > 90 days",f"{long_count:,}"); z.metric("Median observed lead time",f"{positive.median():,.0f} days" if not positive.empty else "N/A")
            st.warning("The source dates appear inconsistent and lead times may be unusually long. Treat historical lead-time values and model-based estimates as unvalidated until the source data is confirmed.")
    st.subheader("Impact limits")
    st.markdown("- Actual transport costs are not present, so monetary logistics savings cannot be calculated.\n- Factory capacity, inventory, production compatibility and service constraints are not provided.\n- Distances are straight-line estimates for selected destination ZIP codes, not actual road/shipping routes.\n- Any alternative factory shown is a candidate for review, not an instruction to reassign production.")

elif page in FILES:
    df=data.get(page)
    st.markdown(f"<div class='hero'><h1>📂 {page}</h1><p>Explore, filter, chart, and download prepared project data.</p></div>",unsafe_allow_html=True)
    if df is None: st.error("This CSV was not found beside app.py.")
    else:
        search=st.text_input("🔎 Search this table",placeholder="Type a product, factory, or value...")
        view=df
        if search:
            mask=df.astype(str).apply(lambda s:s.str.contains(search,case=False,na=False)).any(axis=1); view=df[mask]
        st.caption(f"Showing {len(view):,} of {len(df):,} rows · {len(df.columns)} columns")
        st.dataframe(view,use_container_width=True,hide_index=True,height=470)
        st.download_button("⬇ Download filtered data",view.to_csv(index=False).encode(),file_name=f"{page.lower().replace('–','_').replace(' ','_')}.csv",mime="text/csv")
        numeric=view.select_dtypes(include="number").columns.tolist(); textcols=view.select_dtypes(exclude="number").columns.tolist()
        if numeric and len(view)>1:
            with st.expander("📊 Build a quick chart"):
                yy=st.selectbox("Value to plot",numeric); xx=st.selectbox("Group by",textcols) if textcols else None
                if xx:
                    d=view[[xx,yy]].dropna().head(100)
                    if not d.empty: st.plotly_chart(dark(px.bar(d,x=xx,y=yy,color_discrete_sequence=["#60a5fa"]),380),use_container_width=True)

elif page == "Raw Data Explorer":
    st.markdown("<div class='hero'><h1>🧾 Raw Data Explorer</h1><p>Filter original order records by product, region and shipping mode.</p></div>",unsafe_allow_html=True)
    if raw is None: st.error("Raw dataset CSV not found beside app.py.")
    else:
        product_col=col(raw,["Product Name"]); region_col=col(raw,["Region"]); mode_col=col(raw,["Ship Mode"])
        a,b,c=st.columns(3); view=raw.copy()
        if product_col:
            values=sorted(view[product_col].dropna().astype(str).unique()); chosen=a.multiselect("Product",values,default=[])
            if chosen: view=view[view[product_col].astype(str).isin(chosen)]
        if region_col:
            values=sorted(view[region_col].dropna().astype(str).unique()); chosen=b.multiselect("Region",values,default=[])
            if chosen: view=view[view[region_col].astype(str).isin(chosen)]
        if mode_col:
            values=sorted(view[mode_col].dropna().astype(str).unique()); chosen=c.multiselect("Ship mode",values,default=[])
            if chosen: view=view[view[mode_col].astype(str).isin(chosen)]
        st.caption(f"Showing {len(view):,} filtered rows from {len(raw):,} total records")
        st.dataframe(view,use_container_width=True,hide_index=True,height=450)
        st.download_button("Download filtered orders",view.to_csv(index=False).encode(),"filtered_nassau_orders.csv","text/csv")

else:
    st.markdown("<div class='hero'><h1>ℹ️ About this project</h1><p>Scope, assumptions, and responsible interpretation.</p></div>",unsafe_allow_html=True)
    st.markdown("""
### Current capabilities
- Product and factory performance summaries and model comparison.
- Candidate factory distance comparison for selected destinations.
- What-if distance scenarios and a heuristic ranking that combines distance priority with product margin context.
- Filters for product, region and ship mode in the raw-data explorer.
- Low-margin and data-quality risk alerts.

### Important limitations
- The source contains date inconsistencies and unusually long observed lead times.
- Product-to-factory assignments are predefined; candidate alternatives are not guaranteed to be production-compatible.
- Factory coordinates are assumptions; straight-line distances are not road routes or actual delivery times.
- Transportation prices, factory capacity, inventory, production constraints and service constraints are not modeled.
- The priority score is a transparent heuristic, not a validated optimization objective.
- No monetary savings or guaranteed lead-time improvements are claimed.

### Next steps for a production-grade optimizer
Validate the source data, verify factory locations, add transport costs and route times, document product/factory compatibility, and model capacity and inventory constraints before making operational recommendations.
""")

st.markdown("---")
st.caption("Nassau Candy Distributor · Academic decision-support prototype · Validate assumptions before operational use.")
