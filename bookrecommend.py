import streamlit as st
import pandas as pd

# ----------------------------------
# 데이터 불러오기
# ----------------------------------
df = pd.read_csv("추천도서_교양50권_태그.csv")

st.set_page_config(page_title="📚 서울고 1학년 교양 도서 추천", layout="wide")
st.title("📚 서울고 1학년을 위한 맞춤 도서 추천")

# ----------------------------------
# 태그 목록 만들기
# ----------------------------------
# 세미콜론으로 구분된 태그를 리스트로 변환
df["tags_feature"] = df["tags_feature"].fillna("").apply(lambda x: str(x).split(";"))
df["tags_career"] = df["tags_career"].fillna("").apply(lambda x: str(x).split(";"))

feature_tags = sorted({tag for tags in df["tags_feature"] for tag in tags if tag})
career_tags = sorted({tag for tags in df["tags_career"] for tag in tags if tag})

# ----------------------------------
# 사용자 입력: 태그 선택
# ----------------------------------
st.sidebar.header("🔍 필터")
sel_features = st.sidebar.multiselect("도서 특징 태그 선택", feature_tags)
sel_careers = st.sidebar.multiselect("추천 진로 태그 선택", career_tags)

# ----------------------------------
# 필터링 함수
# ----------------------------------
def match_tags(row):
    cond1 = all(tag in row["tags_feature"] for tag in sel_features)
    cond2 = all(tag in row["tags_career"] for tag in sel_careers)
    return cond1 and cond2

if sel_features or sel_careers:
    filtered = df[df.apply(match_tags, axis=1)]
else:
    filtered = df

# ----------------------------------
# 결과 출력 (카드 스타일)
# ----------------------------------
st.markdown("### 🎈 추천 도서 리스트")

cols = st.columns(4)  # 한 줄에 4권씩
for i, row in enumerate(filtered.itertuples()):
    with cols[i % 4]:
        st.markdown(f"**{row.상품명}**")
        st.caption(f"{row.인물} | {row.출판사} ({str(row._4)[:4]})")  # 발행년도 앞 4자리
        st.write("특징 태그:", " ".join(row.tags_feature))
        st.write("진로 태그:", " ".join(row.tags_career))
        kyobo_url = f"https://search.kyobobook.co.kr/search?keyword={row.상품명}"
        st.link_button("교보문고에서 보기", kyobo_url)
        st.divider()
