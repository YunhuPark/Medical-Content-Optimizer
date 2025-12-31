# 🏥 YouTube Medical Content Optimizer (의료 정보 접근성 강화 프로젝트)

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat-square&logo=pandas&logoColor=white)
![YouTube API](https://img.shields.io/badge/YouTube_API-Data_Collection-FF0000?style=flat-square&logo=youtube&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=flat-square&logo=python&logoColor=white)

> **데이터 분석을 통해 의료 정보의 확산 패턴을 규명하고, 조회수를 극대화하는 AI 제목 최적화 솔루션**

## 📌 1. 프로젝트 개요 (Overview)
* **주제:** YouTube 내 의료 건강 정보(당뇨 등) 콘텐츠의 알고리즘 확산 패턴 분석 및 제목 생성 알고리즘 개발
* **목표:** 전문성은 높지만 접근성이 낮은 의료인(Medical Pro)의 콘텐츠가 대중에게 더 잘 도달할 수 있도록, 일반인 인플루언서의 성공 문법(Keyword Pattern)을 분석하여 적용함.
* **개발 기간:** 2025.12.31 (1-Day Intensive Project)
* **역할:** 데이터 수집(ETL), 전처리, 시각화(EDA), 모델링 전 과정 1인 개발

## 💡 2. 문제 정의 및 가설 (Hypothesis)
* **문제점:** 의학적으로 정확한 정보를 제공하는 '의료인' 채널보다, 자극적인 썸네일을 사용하는 '일반인' 채널의 조회수가 월등히 높은 현상 발견.
* **가설:** "일반인 유튜버들은 시청자의 클릭을 유도하는 특정 **'트리거 키워드(Trigger Keyword)'**를 패턴화하여 사용하고 있을 것이다."
* **검증 방법:** '당뇨(Diabetes)' 키워드 상위 50개 영상 데이터를 수집하여 **[전문가 그룹 vs 일반인 그룹]** 간의 성과 지표를 비교 분석.

## 📊 3. 데이터 분석 과정 (Process & Insight)

### 3-1. 데이터 수집 (Data Collection)
* **Google YouTube Data API v3**를 활용하여 키워드 관련 상위 노출 영상의 메타데이터(제목, 조회수, 좋아요, 채널명 등) 수집.
* `viewCount` 기준 정렬을 통해 시장에서 이미 검증된 고성과 영상(Best Practice) 표본 추출.

### 3-2. 탐색적 데이터 분석 (EDA)
* **정량적 비교:** 분석 결과, 일반인 그룹의 평균 조회수가 전문가 그룹 대비 **약 1.4배 높음**을 확인. 반면, 신뢰도 지표인 '좋아요 비율(Like Ratio)'은 전문가 그룹이 우세함.
* **인사이트:** 의료 콘텐츠의 확산을 위해서는 **'전문가의 신뢰성'에 '일반인의 마케팅적 키워드'를 결합**하는 전략이 필요함.

<p align="center">
  <img src="image_695c68.jpg" alt="전문가 vs 일반인 비교 분석 그래프" width="80%">
  <br>
  <em>[Figure 1] 전문가 그룹(Medical Pro) vs 일반인 그룹(General) 성과 비교</em>
</p>

### 3-3. 텍스트 마이닝 (Text Mining)
* 일반인 그룹의 영상 제목을 형태소 단위로 분석(Tokenizing).
* **핵심 키워드 추출:** `음식`, `3가지`, `충격`, `과일`, `교수` 등의 단어가 유의미하게 높은 빈도(TF)로 등장함을 발견.
* **패턴 도출:** "공포심 자극(충격, 현실)" + "쉬운 해결책(음식, 3가지)" + "권위 차용(교수, 박사)"의 3박자 패턴 확인.

<p align="center">
  <img src="image_696fa6.jpg" alt="일반인 유튜버 키워드 랭킹" width="80%">
  <br>
  <em>[Figure 2] 일반인 유튜버들의 조회수 Trigger Keyword TOP 15</em>
</p>

## 🤖 4. 솔루션 개발: AI 제목 판독기 (AI Title Scorer)
* **기능:** 사용자가 입력한 제목의 '잠재 조회수 효율'을 예측하여 **0~100점의 점수**로 환산해주는 알고리즘 개발.
* **로직:** 텍스트 마이닝으로 추출한 고효율 키워드에 가중치(Weighting)를 부여하여, 단순 매칭이 아닌 **데이터 기반의 평가 모델** 구축.
* **성과:** `youtube_analyzer.py` 구현 완료. 실제 테스트 결과, 최적화된 키워드 조합 시 예측 점수 100점 달성 및 조회수 상승 요인 시각화 성공.

<p align="center">
  <img src="image_69dfcd.jpg" alt="AI 판독기 실행 화면" width="80%">
  <br>
  <em>[Figure 3] AI Title Scorer 실제 구동 화면 (100점 달성 예시)</em>
</p>

## 🛠 5. 기술 스택 (Tech Stack)
* **Language:** Python 3.x
* **Data Collection:** Google API Client (YouTube Data API v3)
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Text Processing:** Re (Regular Expression), Collections

## 📂 6. 프로젝트 구조 (File Structure)
```bash
youtube_study/
├── archive/                # 📜 학습 과정 아카이브 (초기 모델링 기록)
│   ├── main.py             # IT 기술(API) 기초 학습 코드
│   ├── analyze.py          # 데이터 시각화 연습 코드
│   └── medical_study.py    # 의료 데이터 비교 분석 초기 코드
├── youtube_analyzer.py     # ⭐ [Main] 최종 완성된 AI 분석기
├── medical_final.csv       # 💾 분석용 샘플 데이터 (당뇨)
├── requirements.txt        # 📦 의존성 패키지 목록
├── .gitignore              # 🚫 Git 업로드 제외 설정
├── image_695c68.jpg        # 🖼️ README용 이미지 (그래프)
├── image_696fa6.jpg        # 🖼️ README용 이미지 (키워드)
├── image_69dfcd.jpg        # 🖼️ README용 이미지 (실행화면)
└── README.md               # 📄 프로젝트 명세서
