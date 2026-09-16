import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)


# ============================================================
# 데이터 불러오기
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜(datetime)로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 열 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


df = load_data()


# ============================================================
# 제목
# ============================================================

st.title("영화 데이터 그래프 도감 1 - 시간")

st.write(
    "영화별 날짜에 따른 일관객 변화를 살펴보는 그래프입니다."
)


# ============================================================
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# ============================================================

st.header("1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie} - 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
)

fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis=dict(
        title="날짜",
    ),
    yaxis=dict(
        title="일관객 수",
        tickformat=",",
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown("**이 그래프로 알 수 있는 것**")

st.empty()


# ============================================================
# 앞으로 추가할 그래프
# ============================================================

st.divider()

st.header("2. 다음 그래프")

st.info("앞으로 추가할 그래프 영역입니다.")


# ============================================================
# 그래프 3
# ============================================================

# st.divider()
# st.header("3. 그래프 제목")
#
# 여기에 새로운 그래프를 추가하세요.


# ============================================================
# 그래프 4
# ============================================================

# st.divider()
# st.header("4. 그래프 제목")
#
# 여기에 새로운 그래프를 추가하세요.
