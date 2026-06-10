import streamlit as st
import pandas as pd

st.set_page_config(
page_title="봄·가을은 정말 짧아지고 있는가?",
layout="wide"
)

st.title("🌸🍂 봄·가을은 정말 짧아지고 있는가?")

st.write("""
서울의 장기 기온 자료를 이용하여
봄과 가을의 길이가 실제로 짧아지고 있는지 분석합니다.
""")

# -----------------------

# CSV 불러오기

# -----------------------

try:
df = pd.read_csv("ta_20260601093156(1).csv")
except Exception as e:
st.error(f"CSV 파일을 읽을 수 없습니다.\n{e}")
st.stop()

# -----------------------

# 데이터 확인

# -----------------------

st.subheader("원본 데이터")

with st.expander("데이터 미리보기"):
st.dataframe(df.head())

# -----------------------

# 날짜 정리

# -----------------------

df["날짜"] = df["날짜"].astype(str)

# 앞의 탭 제거

df["날짜"] = df["날짜"].str.replace("\t", "", regex=False)

df["날짜"] = pd.to_datetime(
df["날짜"],
errors="coerce"
)

# 날짜 변환 실패 제거

df = df.dropna(subset=["날짜"])

# -----------------------

# 파생 변수 생성

# -----------------------

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

# -----------------------

# 계절 길이 계산

# -----------------------

result = []

years = sorted(df["연도"].unique())

for year in years:

```
year_df = df[df["연도"] == year]

spring_days = len(
    year_df[
        (year_df["월"] >= 3)
        & (year_df["월"] <= 5)
        & (year_df["평균기온(℃)"] >= 5)
        & (year_df["평균기온(℃)"] < 20)
    ]
)

autumn_days = len(
    year_df[
        (year_df["월"] >= 9)
        & (year_df["월"] <= 11)
        & (year_df["평균기온(℃)"] >= 5)
        & (year_df["평균기온(℃)"] < 20)
    ]
)

result.append(
    {
        "연도": year,
        "봄 길이": spring_days,
        "가을 길이": autumn_days,
        "봄+가을": spring_days + autumn_days
    }
)
```

season_df = pd.DataFrame(result)

# -----------------------

# 그래프

# -----------------------

st.subheader("연도별 봄 길이")

st.line_chart(
season_df.set_index("연도")["봄 길이"]
)

st.subheader("연도별 가을 길이")

st.line_chart(
season_df.set_index("연도")["가을 길이"]
)

st.subheader("연도별 봄+가을 길이")

st.line_chart(
season_df.set_index("연도")["봄+가을"]
)

# -----------------------

# 초기/최근 비교

# -----------------------

early = season_df.head(20)
recent = season_df.tail(20)

early_avg = early["봄+가을"].mean()
recent_avg = recent["봄+가을"].mean()

difference = recent_avg - early_avg

st.subheader("통계 비교")

col1, col2, col3 = st.columns(3)

col1.metric(
"초기 20년 평균",
f"{early_avg:.1f}일"
)

col2.metric(
"최근 20년 평균",
f"{recent_avg:.1f}일"
)

col3.metric(
"변화량",
f"{difference:.1f}일"
)

# -----------------------

# 결론

# -----------------------

st.subheader("탐구 결과")

if difference < 0:

```
st.success(
    f"""
```

최근 20년의 봄+가을 평균 길이는
초기 20년보다 {abs(difference):.1f}일 감소했습니다.

따라서 이 자료에서는
봄과 가을이 짧아지는 경향이 확인됩니다.
"""
)

else:

```
st.warning(
    f"""
```

최근 20년의 봄+가을 평균 길이는
초기 20년보다 {difference:.1f}일 증가했습니다.

이 자료만으로는
봄·가을이 짧아진다고 결론 내리기 어렵습니다.
"""
)

# -----------------------

# 결과표

# -----------------------

st.subheader("분석 결과표")

st.dataframe(
season_df,
use_container_width=True
)
