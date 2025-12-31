import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 아까 저장한 CSV 파일 읽어오기
file_path = 'youtube_result.csv'

if not os.path.exists(file_path):
    print("❌ CSV 파일이 없어요! main.py를 먼저 실행해서 데이터를 모아주세요.")
else:
    df = pd.read_csv(file_path)

    # 2. 그래프 스타일 설정
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

    # 3. 산점도(Scatter Plot) 그리기
    # X축: 좋아요 수, Y축: 조회수
    sns.scatterplot(data=df, x='Likes', y='Views', s=100, color='red', alpha=0.7)

    # 4. 그래프 제목과 라벨 달기 (한글 깨짐 방지를 위해 영어로 표기)
    plt.title('Youtube Algorithm: Likes vs Views', fontsize=15)
    plt.xlabel('Likes (좋아요)', fontsize=12)
    plt.ylabel('Views (조회수)', fontsize=12)

    # 5. 그래프 보여주기
    print("📈 그래프 창이 뜰 겁니다. 잠시만 기다리세요...")
    plt.show()