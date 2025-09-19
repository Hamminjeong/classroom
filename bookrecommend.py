import streamlit as st
import pandas as pd

# ----------------------------------
# 데이터 불러오기
# ----------------------------------
df = pd.read_csv("추천도서_교양50권_태그.csv")

st.set_page_config(page_title="📚 고등학생 교양 추천도서", layout="wide")
st.title("📚 고등학생 맞춤 교양 추천도서")

# ----------------------------------
# 태그 처리
# ----------------------------------
df["tags_feature"] = df["tags_feature"].fillna("").apply(lambda x: str(x).split(";"))
df["tags_career"] = df["tags_career"].fillna("").apply(lambda x: str(x).split(";"))

feature_tags = sorted({tag for tags in df["tags_feature"] for tag in tags if tag})
career_tags = sorted({tag for tags in df["tags_career"] for tag in tags if tag})

# ----------------------------------
# UI: 태그 선택 (체크박스)
# ----------------------------------
st.sidebar.header("🔍 필터")

st.sidebar.subheader("도서 특징 태그")
sel_features = []
for tag in feature_tags:
    if st.sidebar.checkbox(tag, key=f"f_{tag}"):
        sel_features.append(tag)

st.sidebar.subheader("추천 진로 태그")
sel_careers = []
for tag in career_tags:
    if st.sidebar.checkbox(tag, key=f"c_{tag}"):
        sel_careers.append(tag)

# AND/OR 선택
mode = st.sidebar.radio("태그 조건 방식", ["AND", "OR"])

# ----------------------------------
# 필터링 함수
# ----------------------------------
def match_tags(row, selected, mode, tag_type):
    tags = row[tag_type]
    if not selected:
        return True
    if mode == "AND":
        return all(tag in tags for tag in selected)
    else:  # OR
        return any(tag in tags for tag in selected)

filtered = df[
    df.apply(lambda row: match_tags(row, sel_features, mode, "tags_feature"), axis=1)
    & df.apply(lambda row: match_tags(row, sel_careers, mode, "tags_career"), axis=1)
]

# ----------------------------------
# 결과 출력 (작은 카드 + 표지)
# ----------------------------------
st.markdown("### 🎈 추천 도서 리스트")

cols = st.columns(5)  # 한 줄에 5권씩
for i, row in enumerate(filtered.itertuples()):
    with cols[i % 5]:
        cover = getattr(row, "cover_url", None)
        if not isinstance(cover, str) or not cover.startswith("http"):
            cover = "https://via.placeholder.com/120x160.png?text=No+Image"
        st.image(cover, width=120)
        st.markdown(f"**{row.상품명}**")
        st.caption(f"{row.인물} | {row.출판사} ({str(row._4)[:4]})")
        st.write(" ".join(row.tags_feature))
        st.write(" ".join(row.tags_career))
        kyobo_url = f"https://search.kyobobook.co.kr/search?keyword={row.상품명}"
        st.link_button("교보문고에서 보기", kyobo_url)
