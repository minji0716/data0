import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="봄·가을은 정말 짧아지고 있는가?",
    layout="wide"
)

st.title("🌸🍂 봄·가을은 정말 짧아지고 있는가?")
st.subheader("기온 데이터를 이용한 통계적 탐구")

# =========================
# 데이터 불러오기
# =========================

FILE_NAME = "ta_20260601093156(2).csv"

try:
    df = pd.read_csv(FILE_NAME)

except Exception as e:
    st.error(f"파일을 읽을 수 없습니다.\n{e}")
    st.stop()

# =========================
# 전처리
# =========================

df["날짜"] = df["날짜"].astype(str).str.strip()
df["날짜"] = pd.to_datetime(df["날짜"])

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

temp_col = "평균기온(℃)"

# =========================
# 계절 정의
# =========================
# 봄 : 10~22℃
# 여름 : 22℃ 초과
# 가을 : 10~22℃
# 겨울 : 10℃ 미만
#
# 봄 : 3~5월
# 가을 : 9~11월
# 범위 내에 드는 날 수 계산
# =========================

result = []

years = sorted(df["연도"].unique())

for year in years:

    year_df = df[df["연도"] == year]

    spring = year_df[
        (year_df["월"].between(3, 5))
        & (year_df[temp_col] >= 10)
        & (year_df[temp_col] <= 22)
    ]

    autumn = year_df[
        (year_df["월"].between(9, 11))
        & (year_df[temp_col] >= 10)
        & (year_df[temp_col] <= 22)
    ]

    result.append({
        "연도": year,
        "봄 일수": len(spring),
        "가을 일수": len(autumn),
        "봄+가을": len(spring) + len(autumn)
    })

season_df = pd.DataFrame(result)

# =========================
# 데이터 확인
# =========================

st.header("📋 분석 데이터")

st.dataframe(season_df.tail(20))

# =========================
# 그래프
# =========================

st.header("📈 연도별 봄 일수")

spring_chart = season_df.set_index("연도")[["봄 일수"]]
st.line_chart(spring_chart)

st.header("📈 연도별 가을 일수")

autumn_chart = season_df.set_index("연도")[["가을 일수"]]
st.line_chart(autumn_chart)

st.header("📈 연도별 봄+가을 총 일수")

total_chart = season_df.set_index("연도")[["봄+가을"]]
st.line_chart(total_chart)

# =========================
# 통계 분석
# =========================

st.header("📊 통계 분석")

corr_spring = season_df["연도"].corr(season_df["봄 일수"])
corr_autumn = season_df["연도"].corr(season_df["가을 일수"])
corr_total = season_df["연도"].corr(season_df["봄+가을"])

st.metric(
    "연도와 봄 일수 상관계수",
    round(corr_spring, 3)
)

st.metric(
    "연도와 가을 일수 상관계수",
    round(corr_autumn, 3)
)

st.metric(
    "연도와 봄+가을 일수 상관계수",
    round(corr_total, 3)
)

# =========================
# 초기/최근 비교
# =========================

st.header("🔍 과거와 현재 비교")

first20 = season_df.head(20)
last20 = season_df.tail(20)

past_avg = first20["봄+가을"].mean()
recent_avg = last20["봄+가을"].mean()

change = recent_avg - past_avg

st.write(f"초기 20년 평균 : **{past_avg:.1f}일**")
st.write(f"최근 20년 평균 : **{recent_avg:.1f}일**")
st.write(f"변화량 : **{change:.1f}일**")

# =========================
# 결론
# =========================

st.header("📝 자동 결론")

if corr_total < -0.2 and recent_avg < past_avg:
    st.success(
        "분석 결과, 연도가 증가할수록 봄·가을 일수가 감소하는 경향이 나타났습니다. "
        "따라서 '봄과 가을이 짧아지고 있다'는 가설을 지지하는 결과가 확인됩니다."
    )

elif corr_total > 0.2:
    st.info(
        "봄·가을 일수가 증가하는 경향이 관측됩니다."
    )

else:
    st.warning(
        "뚜렷한 감소 추세는 확인되지 않았습니다."
    )

# =========================
# 원본 데이터
# =========================

with st.expander("원본 기온 데이터 보기"):
    st.dataframe(df)
