import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Shopping Trends SuperApp", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("shopping_trends.xlsx", sheet_name="shopping_trends")
    return df

df = load_data()

st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the analysis section:", ["📅 Purchase Frequency Analysis", "🛒 Item Purchased Analysis"])


if app_mode == "📅 Purchase Frequency Analysis":
    st.title("🛍️ Shopping Trends Dashboard - Frequency Analysis")

    
    frequency_filter = st.sidebar.selectbox("Select purchase frequency:", df["Frequency of Purchases"].unique(), index=0)

    filtered_df = df[df["Frequency of Purchases"] == frequency_filter]

    
    st.markdown(f"### 📌 Data for **'{frequency_filter}'** group")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Customers", filtered_df.shape[0])
    col2.metric("💵 Total Revenue", f"${filtered_df['Purchase Amount (USD)'].sum():,.2f}")
    col3.metric("📈 Avg. Previous Purchases", f"{filtered_df['Previous Purchases'].mean():.2f}")

    
    st.markdown("### 🎨 Age Distribution Chart")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_df["Age"], bins=10, kde=True, color=sns.color_palette("plasma", 10)[4], edgecolor='black')
    ax.set_xlabel("Age")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Customer Age Distribution", fontsize=14)
    st.pyplot(fig)



elif app_mode == "🛒 Item Purchased Analysis":
    st.title("🛒 Shopping Trends Dashboard - Item Purchased Analysis")

    st.sidebar.header("Filters")
    gender_filter = st.sidebar.multiselect(
        "Select Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    age_filter = st.sidebar.slider(
        "Select Age Range:",
        min_value=int(df["Age"].min()),
        max_value=int(df["Age"].max()),
        value=(int(df["Age"].min()), int(df["Age"].max()))
    )

    
    df_filtered = df[
        (df["Gender"].isin(gender_filter)) &
        (df["Age"] >= age_filter[0]) &
        (df["Age"] <= age_filter[1])
    ]

    
    st.subheader("Top 10 Most Purchased Items")
    item_counts = df_filtered["Item Purchased"].value_counts().reset_index()
    item_counts.columns = ["Item Purchased", "Count"]

    fig = px.bar(
        item_counts.head(10),
        x="Count",
        y="Item Purchased",
        orientation='h',
        color="Count",
        color_continuous_scale="Teal",
        title="Top 10 Most Purchased Items"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("Distribution of Purchased Items")
    fig2 = px.pie(
        item_counts,
        names="Item Purchased",
        values="Count",
        title="Item Purchased Distribution",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    st.plotly_chart(fig2, use_container_width=True)
