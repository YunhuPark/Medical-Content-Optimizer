import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os
import platform

# ==========================================
# ▼ 한글 폰트 자동 설정 (그래프 글자 깨짐 해결)
# ==========================================
system_name = platform.system()
if system_name == 'Windows':
    plt.rc('font', family='Malgun Gothic') # 윈도우
elif system_name == 'Darwin':
    plt.rc('font', family='AppleGothic') # 맥
    plt.rcParams['axes.unicode_minus'] = False
else:
    print("⚠️ 한글 폰트 설정이 어려운 운영체제입니다.")

# ==========================================
# 1. 데이터 불러오기
# ==========================================
file_path = 'medical_study_result.csv'

if not os.path.exists(file_path):
    print("❌ 데이터 파일이 없어요! medical_study.py를 먼저 실행해주세요.")
else:
    df = pd.read_csv(file_path)

    # 2. '일반인(General)' 영상만 골라내기
    # (의사들이 쓴 점잖은 단어 말고, 조회수 터진 일반인 단어를 찾기 위함)
    target_df = df[df['Type'] == 'General']
    
    print(f"📊 분석 대상: 일반인 영상 {len(target_df)}개의 제목을 분석합니다...")

    # 3. 제목 텍스트 전처리 (청소)
    titles = target_df['Title'].tolist()
    all_text = " ".join(titles) # 제목들을 긴 문장 하나로 합치기
    
    # 특수문자 제거 ([...], !, ? 등 제거하고 한글/영어/숫자만 남김)
    clean_text = re.sub(r'[^\w\s]', '', all_text)
    
    # 단어 쪼개기 (띄어쓰기 기준)
    words = clean_text.split()

    # 4. 불용어(Stopwords) 제거 - 분석에 필요 없는 흔한 단어 빼기
    # '당뇨'는 검색어니까 당연히 많겠죠? 제외합니다.
    stop_words = ['당뇨', '당뇨병', '에', '이', '가', '은', '는', '을', '를', '의', '하는', '있는'] 
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 1] # 1글자 단어도 제외

    # 5. 빈도수 계산 (가장 많이 나온 단어 15개)
    word_counts = Counter(meaningful_words)
    top_words = word_counts.most_common(15)
    
    # 데이터프레임으로 변환 (그래프 그리기 위해)
    word_df = pd.DataFrame(top_words, columns=['Word', 'Count'])

    # 6. 시각화 (가로 막대 그래프)
    plt.figure(figsize=(10, 8))
    sns.barplot(data=word_df, y='Word', x='Count', palette='viridis')
    plt.title(f"일반인 유튜버들의 '조회수 치트키' 단어 TOP 15", fontsize=15)
    plt.xlabel('등장 횟수', fontsize=12)
    plt.ylabel('단어', fontsize=12)
    plt.grid(axis='x', alpha=0.5)
    
    print("\n✅ 분석 완료! 어떤 단어가 1등인지 확인해보세요.")
    plt.show()