import streamlit as st
import math
import random
import re
from collections import Counter

# --- 1. DATA COLLECTION (The Scraper Hook) ---
def fetch_amazon_data(category_id):
    """
    In a live environment, replace this mock data with an API call to a service 
    like Rainforest API or ScrapingBee to avoid Cloud IP blocks.
    """
    # Simulated API response for demonstration
    titles = [
        "Coloring Book for Adults: Mindfulness and Relaxation Patterns",
        "Mindfulness Journal for Women: Daily Gratitude Practice",
        "Adult Coloring Book: Stress Relief Patterns and Mandalas",
        "The Shadow Work Journal: A Guide to Integrate and Heal",
        "Atomic Habits: An Easy & Proven Way to Build Good Habits"
    ]
    
    books = []
    # Simulating 20 books scraped from a category
    for _ in range(20):
        books.append({
            "title": random.choice(titles),
            "price": round(random.uniform(5.99, 14.99), 2),
            "bsr": random.randint(500, 60000)
        })
        
    return {
        "competition": random.randint(10000, 50000), # Total search results
        "books": books
    }

# --- 2. DATA CRUNCHING (Math & NLP) ---
def analyze_niche(category_id):
    data = fetch_amazon_data(category_id)
    books = data['books']
    
    total_bsr = 0
    total_revenue = 0
    all_titles = ""
    
    for book in books:
        total_bsr += book['bsr']
        all_titles += book['title'] + " "
        
        # Revenue Algorithm: (85000 / BSR^0.85) * Price * 70% Royalty
        daily_sales = math.floor(85000 / math.pow(book['bsr'], 0.85))
        daily_revenue = daily_sales * book['price'] * 0.70
        total_revenue += daily_revenue
        
    avg_bsr = total_bsr // len(books)
    est_monthly_revenue = math.floor(total_revenue * 30)
    
    # NLP Keyword Extraction
    # Convert to lowercase and extract words with 4 or more letters
    words = re.findall(r'\b[a-z]{4,}\b', all_titles.lower())
    
    # Filter out common stop words
    stop_words = {'this', 'that', 'with', 'from', 'your', 'book', 'guide', 'easy'}
    filtered_words = [w for w in words if w not in stop_words]
    
    # Get the top 10 most frequent keywords
    top_keywords = Counter(filtered_words).most_common(10)
    
    return {
        "avg_bsr": avg_bsr,
        "competition": data['competition'],
        "revenue": est_monthly_revenue,
        "demand": "High" if avg_bsr < 50000 else "Moderate",
        "keywords": top_keywords
    }

# --- 3. FRONTEND UI ---
st.set_page_config(page_title="KDP Niche Analyzer", layout="centered")

st.title("📚 KDP Niche Analyzer")
st.write("Enter an Amazon Category Node ID to extract Best Seller metrics and keyword demand.")

# User Input
cat_id = st.text_input("Amazon Category Node ID", placeholder="e.g., 154606011")

# Action Button
if st.button("Analyze Niche", type="primary"):
    if not cat_id:
        st.warning("Please enter a Category ID.")
    else:
        with st.spinner("Scraping Amazon and crunching the data..."):
            results = analyze_niche(cat_id)
            
            st.divider()
            
            # Display Metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Average BSR", f"{results['avg_bsr']:,}")
            col2.metric("Competition", f"{results['competition']:,}")
            col3.metric("Est. Monthly Rev", f"${results['revenue']:,}")
            col4.metric("Demand Level", results['demand'])
            
            st.subheader("🎯 Top Extracted Keywords")
            st.write("Keywords extracted directly from the titles of top-selling books.")
            
            # Display Keywords as visual tags using simple HTML/CSS
            kw_html = ""
            for kw, count in results['keywords']:
                kw_html += f"<span style='background-color: #f0f2f6; color: #31333F; padding: 6px 12px; margin: 4px; border-radius: 16px; display: inline-block; font-weight: 500;'>{kw.capitalize()} ({count})</span>"
                
            st.markdown(kw_html, unsafe_allow_html=True)
