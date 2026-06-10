import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="봄·가을은 정말 짧아지고 있는가?",
    layout="wide"
)

st.title("🌸🍂 봄·가을은 정말 짧아지고 있는가?")
st.write("기상청 기온 데이터를 이용한 통계 탐구")

# =====================
# 파일 읽기
# =====================

FILE_NAME = "ta_20260601093156(2).csv"

try:
    df = pd.read_csv(FILE_NAME, encoding="utf-8")
except:
    try:
        df = pd.read_csv(FILE_NAME, encoding="cp949")
    except Exception as e:
        st.error(f"파일을 읽을 수 없습니다.\n\n{e}")
        st.stop()

# =====================
# 컬럼 확인
# =====================

st.subheader("CSV 컬럼 확인")

df.columns = df.columns.str.strip()

st.write(df.columns.tolist())

# =====================
# 날짜 컬럼 찾기
# =====================

date_col = None

for col in df.columns:
    if "날짜" in col:
        date_col = col
        break

if date_col is None:
    st.error("날짜 컬럼을 찾을 수 없습니다.")
    st.stop()

# =====================
# 평균기온 컬럼 찾기
# =====================

temp_col = None

for col in df.columns:
    if "평균기온" in col:
        temp_col = col
        break

if temp_col is None:
    st.error("평균기온 컬럼을 찾을 수 없습니다.")
    st.stop()

# =====================
# 날짜 처리
# =====================

df[date_col] = (
    df[date_col]
    .astype(str)
    .str.replace("\t", "", regex=False)
    .str.strip()
)

df[date_col] = pd.to_datetime(
    df[date_col],
    errors="coerce"
)

df = df.dropna(subset=[date_col])

# =====================
# 연도, 월 생성
# =====================

df["연도"] = df[date_col].dt.year
df["월"] = df[date_col].dt.month

# =====================
# 기온 숫자 변환
# =====================

df[temp_col] = pd.to_numeric(
    df[temp_col],
    errors="coerce"
)

df = df.dropna(subset=[temp_col])

# =====================
# 계절 길이 계산
# =====================

result = []

years = sorted(df["연도"].unique())

for year in years:

    year_df = df[df["연도"] == year]

    spring_days = len(
        year_df[
            (year_df["월"] >= 3)
            & (year_df["월"] <= 5)
            & (year_df[temp_col] >= 10)
            & (year_df[temp_col] <= 22)
        ]
    )

    autumn_days = len(
        year_df[
            (year_df["월"] >= 9)
            & (year_df["월"] <= 11)
            & (year_df[temp_col] >= 10)
            & (year_df[temp_col] <= 22)
        ]
    )

    result.append({
        "연도": year,
        "봄 일수": spring_days,
        "가을 일수": autumn_days,
        "총 일수": spring_days + autumn_days
    })

season_df = pd.DataFrame(result)

# =====================
# 데이터 표시
# =====================

st.subheader("분석 데이터")

st.dataframe(season_df)

# =====================
# 그래프
# =====================

st.subheader("📈 봄 일수 변화")

st.line_chart(
    season_df.set_index("연도")["봄 일수"]
)

st.subheader("📈 가을 일수 변화")

st.line_chart(
    season_df.set_index("연도")["가을 일수"]
)

st.subheader("📈 봄+가을 총 일수 변화")

st.line_chart(
    season_df.set_index("연도")["총 일수"]
)

# =====================
# 통계
# =====================

corr = season_df["연도"].corr(
    season_df["총 일수"]
)

st.subheader("📊 통계 분석")

st.write(f"상관계수 : {corr:.3f}")

first_years = season_df.head(20)
last_years = season_df.tail(20)

past_avg = first_years["총 일수"].mean()
recent_avg = last_years["총 일수"].mean()

st.write(f"초기 20년 평균 : {past_avg:.1f}일")
st.write(f"최근 20년 평균 : {recent_avg:.1f}일")

change = recent_avg - past_avg

st.write(f"변화량 : {change:.1f}일")

# =====================
# 결론
# =====================

st.subheader("📝 결론")

if change < 0:
    st.success(
        "최근으로 갈수록 봄·가을의 총 길이가 감소하는 경향이 나타났습니다."
    )
else:
    st.info(
        "뚜렷한 감소 경향은 확인되지 않았습니다."
    )
