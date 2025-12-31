import pandas as pd
import os

# 1. 파일 불러오기
file_path = 'youtube_result.csv'

if not os.path.exists(file_path):
    print("❌ CSV 파일이 없어요! main.py를 먼저 실행해주세요.")
else:
    df = pd.read_csv(file_path)

    # 2. '좋아요 확률(%)' 계산하기 (소수점 둘째자리까지)
    # 0으로 나누는 에러 방지를 위해 조회수가 0이면 그냥 0으로 처리
    df['Like_Ratio'] = df.apply(lambda x: (x['Likes'] / x['Views'] * 100) if x['Views'] > 0 else 0, axis=1)
    df['Like_Ratio'] = df['Like_Ratio'].round(2) # 보기 좋게 반올림

    # 3. 순위 매기기
    # 만족도 1등 (비율이 높은 순서)
    top_quality = df.sort_values(by='Like_Ratio', ascending=False).head(5)
    
    # 낚시 의심? (비율이 낮은 순서)
    low_reaction = df.sort_values(by='Like_Ratio', ascending=True).head(5)

    # 4. 결과 출력
    print("="*50)
    print("🏆 [만족도 TOP 5] 시청자가 '엄지척'을 많이 한 영상")
    print("="*50)
    for index, row in top_quality.iterrows():
        print(f"[{row['Like_Ratio']}%] {row['Title']} (조회수: {row['Views']})")

    print("\n" + "="*50)
    print("📉 [반응 저조 TOP 5] 조회수 대비 좋아요가 적은 영상")
    print("="*50)
    for index, row in low_reaction.iterrows():
        print(f"[{row['Like_Ratio']}%] {row['Title']} (조회수: {row['Views']})")

    # 5. 파일로 다시 저장 (분석 결과 포함)
    df.to_csv('youtube_ratio_analyzed.csv', index=False, encoding='utf-8-sig')
    print("\n✅ 분석된 내용을 'youtube_ratio_analyzed.csv'로 저장했습니다.")