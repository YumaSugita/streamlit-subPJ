import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
import datetime

st.title('日本企業株価可視化アプリ')
st.write(datetime.date.today())

st.sidebar.write("""
# 日本企業株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間**の株価
""")


@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df


try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin = st.sidebar.number_input('最小値：', 0.0, 14999.9, 0.0)
    ymax = st.sidebar.number_input('最大値：', 0.0, 15000.0, 15000.0)

    tickers = {
        'トヨタ': '7203.T',
        'ZOZO': '3092.T',
        'sony': '6758.T',
        '東日本旅客鉄道': '9020.T',
        '三越伊勢丹ホールディングス': '3099.T',
        'パナソニック　ホールディングス': '6752.T',
        '日清食品ホールディングス': '2897.T',
        'ミクシィ': '2121.T',
        'KADOKAWA': '9468.T',
        '任天堂': '7974.T',
        'サントリー食品インターナショナル': '2587.T',
        'キャノン': '7751.T',
        '楽天': '4755.T'
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['トヨタ']
    )

    if not companies:
        st.error('少なくとも1社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (JPY)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )

        chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！なにかエラーが起きているようです！"
    )

