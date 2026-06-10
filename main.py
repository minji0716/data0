import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="봄·가을은 정말 짧아지고 있는가?",
    layout="wide"
)

st.title("🌸🍂 봄·가을은 정말 짧아지고 있는가?")
st.markdown("""
기상청 장기 기온 자료를 이용하여
봄과 가을의 길이가 실제로 줄어들고 있는지 분석합니다.
""")

# ---------------------------
# 데이터 불러오기
# ---------------------------
FILE_NAME = "ta_20260601093156(1).csv"

df = pd.read_csv(FILE_NAME)

df["날짜"] = df["날짜"].astype(str).str.strip()
df["날짜"] = pd.to_datetime(df["날짜"])

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

# ---------------------------
# 계절 정의
# ---------------------------
# 봄 : 평균기온 5~20도
# 가을 : 평균기온 5~20도
#
# 여름 : 20도 초과
# 겨울 : 5도 미만
#
# 기상학 연구에서 자주 활용되는 기준
# ---------------------------

spring_lengths = []
autumn_lengths = []

years = sorted(df["연도"].unique())

for year in years:

    year_data = df[df["연도"] == year]

    # 봄 후보 (3~5월)
    spring = year_data[
        (year_data["월"].between(3, 5))
        & (year_data["평균기온(℃)"] >= 5)
        & (year_data["평균기온(℃)"] < 20)
    ]

    # 가을 후보 (9~11월)
    autumn = year_data[
        (year_data["월"].between(9, 11))
        & (year_data["평균기온(℃)"] >= 5)
        & (year_data["평균기온(℃)"] < 20)
    ]

    spring_lengths.append([year, len(spring)])
    autumn_lengths.append([year, len(autumn)])

spring_df = pd.DataFrame(
    spring_lengths,
    columns=["연도", "봄 길이"]
)

autumn_df = pd.DataFrame(
    autumn_lengths,
    columns=["연도", "가을 길이"]
)

season_df = spring_df.merge(
    autumn_df,
    on="연도"
)

season_df["봄+가을"] = (
    season_df["봄 길이"] +
    season_df["가을 길이"]
)

# ---------------------------
# 기초 통계
# ---------------------------

first_20 = season_df.head(20)
last_20 = season_df.tail(20)

early_avg = first_20["봄+가을"].mean()
recent_avg = last_20["봄+가을"].mean()

change = recent_avg - early_avg

# ---------------------------
# 결과 출력
# ---------------------------

st.header("📊 연도별 봄 길이")

st.line_chart(
    season_df.set_index("연도")["봄 길이"]
)

st.header("📊 연도별 가을 길이")

st.line_chart(
    season_df.set_index("연도")["가을 길이"]
)

st.header("📊 연도별 봄+가을 총 길이")

st.line_chart(
    season_df.set_index("연도")["봄+가을"]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "초기 20년 평균",
        f"{early_avg:.1f}일"
    )

with col2:
    st.metric(
        "최근 20년 평균",
        f"{recent_avg:.1f}일"
    )

with col3:
    st.metric(
        "변화량",
        f"{change:.1f}일"
    )

# ---------------------------
# 결론 자동 생성
# ---------------------------

st.header("🔍 탐구 결론")

if change < 0:
    st.success(
        f"""
최근 20년의 봄+가을 평균 길이는
초기 20년보다 {abs(change):.1f}일 감소했습니다.

따라서 장기 기온 자료에서는
봄과 가을이 짧아지는 경향이 관찰됩니다.
"""
    )
else:
    st.warning(
        f"""
최근 20년의 봄+가을 평균 길이는
초기 20년보다 {change:.1f}일 증가했습니다.

이 자료만으로는
봄·가을이 짧아진다고 결론내리기 어렵습니다.
"""
    )

st.header("📋 분석 데이터")

st.dataframe(season_df, use_container_width=True)
