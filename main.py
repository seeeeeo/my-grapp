import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 페이지 기본 설정
# ==================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# 제목
# ==================================================
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.caption(
    "KOBIS 일별 박스오피스 데이터를 바탕으로 "
    "시간의 흐름에 따른 영화 관객 수와 추이를 시각화합니다."
)


# ==================================================
# 데이터 불러오기
# ==================================================
@st.cache_data
def load_data():

    url = (
        "https://raw.githubusercontent.com/greatsong/"
        "modudata/main/data/kobis_daily.csv"
    )

    df = pd.read_csv(url)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 일관객을 숫자로 변환
    df["일관객"] = pd.to_numeric(
        df["일관객"],
        errors="coerce"
    ).fillna(0)

    # 필요한 데이터가 없는 행 제거
    df = df.dropna(
        subset=["날짜", "영화명"]
    )

    return df


# ==================================================
# 데이터 로드
# ==================================================
try:
    df = load_data()

except Exception as e:
    st.error(
        f"데이터를 불러오는 중 오류가 발생했습니다: {e}"
    )
    st.stop()


# ==================================================
# 1번 그래프
# 영화별 일별 관객 수 추이
# ==================================================
st.markdown("---")

st.header("1. 영화별 일별 관객 수 추이")


# 영화 선택
movie_list = sorted(
    df["영화명"].unique()
)

selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    movie_list
)


# 선택한 영화의 데이터
movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)


# 1번 그래프
if not movie_df.empty:

    fig1 = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        markers=True,
        title=f"'{selected_movie}' 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "관객 수 (명)"
        }
    )

    # 마우스를 올렸을 때 날짜와 관객수 표시
    fig1.update_traces(
        hovertemplate=(
            "<b>날짜:</b> %{x|%Y-%m-%d}"
            "<br>"
            "<b>관객수:</b> %{y:,}명"
            "<extra></extra>"
        )
    )

    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="관객 수 (명)",
        hovermode="x unified",
        height=550
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

else:

    st.warning(
        "선택한 영화의 데이터가 없습니다."
    )


# 1번 그래프 설명 자리
st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "여기에 직접 작성하세요."
)


# ==================================================
# 2번 그래프
# 관객수 상위 5개 영화의 일별 관객수 비교
# ==================================================
st.markdown("---")

st.header(
    "2. 관객수 상위 5개 영화의 일별 관객수 비교"
)

st.write(
    "기간 내 일관객 합계가 가장 큰 5편의 "
    "날짜별 일관객을 비교합니다."
)


# --------------------------------------------------
# 영화별 일관객 합계 계산
# --------------------------------------------------
movie_totals = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)


# 일관객 합계 상위 5개 영화
top5_movies = movie_totals.head(5).index.tolist()


# --------------------------------------------------
# TOP 5 데이터 추출
# --------------------------------------------------
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()


# --------------------------------------------------
# 전체 날짜 만들기
# --------------------------------------------------
all_dates = pd.date_range(
    start=df["날짜"].min(),
    end=df["날짜"].max(),
    freq="D"
)


# --------------------------------------------------
# 영화 × 날짜 조합 만들기
# --------------------------------------------------
movie_date_index = pd.MultiIndex.from_product(
    [top5_movies, all_dates],
    names=["영화명", "날짜"]
)


# --------------------------------------------------
# 영화별 날짜별 일관객 계산
# --------------------------------------------------
daily_top5 = (
    top5_df
    .groupby(
        ["영화명", "날짜"]
    )["일관객"]
    .sum()
)


# --------------------------------------------------
# 기록이 없는 날짜는 0명으로 채우기
# --------------------------------------------------
daily_top5 = (
    daily_top5
    .reindex(
        movie_date_index,
        fill_value=0
    )
    .reset_index()
)


# --------------------------------------------------
# 2번 선 그래프
# --------------------------------------------------
fig2 = px.line(
    daily_top5,
    x="날짜",
    y="일관객",
    color="영화명",
    title="기간 내 일관객 합계 상위 5개 영화",
    labels={
        "날짜": "날짜",
        "일관객": "관객 수 (명)",
        "영화명": "영화"
    }
)


# 마우스를 올렸을 때 표시
fig2.update_traces(
    hovertemplate=(
        "<b>영화:</b> %{fullData.name}"
        "<br>"
        "<b>날짜:</b> %{x|%Y-%m-%d}"
        "<br>"
        "<b>관객수:</b> %{y:,}명"
        "<extra></extra>"
    )
)


# 그래프 모양
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="관객 수 (명)",
    hovermode="x unified",
    height=600,
    legend_title="영화"
)


# 그래프 출력
st.plotly_chart(
    fig2,
    use_container_width=True
)


# --------------------------------------------------
# 2번 그래프 설명 자리
# --------------------------------------------------
st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "여기에 직접 작성하세요."
)


# ==================================================
# TOP 5 영화 확인
# ==================================================
with st.expander("🏆 기간 내 관객수 상위 5개 영화 보기"):

    top5_table = (
        movie_totals
        .head(5)
        .reset_index()
    )

    top5_table.columns = [
        "영화명",
        "기간 일관객 합계"
    ]

    top5_table["기간 일관객 합계"] = (
        top5_table["기간 일관객 합계"]
        .astype(int)
    )

    st.dataframe(
        top5_table,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 3번 그래프
# 앞으로 추가할 구역
# ==================================================
st.markdown("---")

st.header("3. 앞으로 추가할 그래프")

st.info(
    "여기에 다음 시간 관련 그래프를 추가할 예정입니다."
)
