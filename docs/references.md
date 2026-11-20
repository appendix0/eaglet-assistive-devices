# 참고문헌

이 저장소의 숫자, 설계 규칙, 구조가 어디서 왔는지 한곳에 모았습니다. 문서와 코드는 `[R번호]`로 이 목록을 가리킵니다.

**확인 수준**: 근거를 어디까지 직접 확인했는지 적습니다. 숫자를 인용하기 전에 확인 수준을 보세요.

- **원문**: 본문이나 표를 직접 읽음
- **초록**: 공식 기록의 초록·요약만 읽음 (본문 미확인)
- **2차**: 다른 문서가 인용한 내용으로만 확인 (원문 미확인)

조사일: 2026-11-20.

## 설계 수치의 근거

| ID | 문헌 | 쓰는 곳 | 확인 수준 |
|---|---|---|---|
| R1 | Jordon M, Levine D, Richards J, Poole C, Padalino C, Babbitt K, Brit M. Biomechanical assessment of grasping postures in individuals with rheumatoid arthritis when holding adaptive silverware. *Frontiers in Rehabilitation Sciences* 7 (2026). [doi:10.3389/fresc.2026.1770139](https://doi.org/10.3389/fresc.2026.1770139) | 굵은 손잡이 지름, ref-01 | 원문 (결과·표 1–2). 고찰·한계 절은 요약만 |
| R2 | McDonald SS, Levine D, Richards J, Aguilar L. Effectiveness of adaptive silverware on range of motion of the hand. *PeerJ* 4:e1667 (2016). [doi:10.7717/peerj.1667](https://doi.org/10.7717/peerj.1667) | 굵은 손잡이 지름, ref-01, ref-03 | 원문 (PMC4756747) |
| R3 | Kong Y-K, Lowe BD. Optimal cylindrical handle diameter for grip force tasks. *International Journal of Industrial Ergonomics* 35(6):495–507 (2005). [CDC Stacks](https://stacks.cdc.gov/view/cdc/197408) | `design_params.py grip` (손 길이의 19.7%, 30–40 mm 쾌적) | 초록 |
| R4 | Yoo J-I, Choi H, Ha Y-C. Mean hand grip strength and cut-off value for sarcopenia in Korean adults using KNHANES VI. *J Korean Med Sci* 32(5):868–872 (2017). [doi:10.3346/jkms.2017.32.5.868](https://doi.org/10.3346/jkms.2017.32.5.868) | 참조 사례의 악력 조건 | 원문 (표 2). 여성 80세 이상 행의 인원수에 원문 오기로 보이는 값 있음 |
| R5 | U.S. Access Board. *2010 ADA Standards for Accessible Design*, §309.4 Operation. [access-board.gov](https://www.access-board.gov/ada/#ada-309) | 조작력 22.2 N 상한, 비틀기·꽉 쥐기 금지 | 2차 (R6의 인용문과 Access Board 페이지 요약이 일치) |
| R6 | Greene L. Decoded: Operable force for door hardware. *iDigHardware* (2014, 2017 갱신). [link](https://idighardware.com/2014/03/decoded-operational-force-for-door-hardware/) | R5 인용, ICC A117.1-2017 회전 조작 28 lbf·in(3.16 N·m) 상한, BHMA A156.2 레버 28 lbf·in | 원문 (해설 기사). 표준 원문은 유료라 미확인 |
| R7 | Prusa Polymers. *Prusament PETG Technical Data Sheet*. [PDF](https://cdn.shopify.com/s/files/1/1745/6181/files/PETG_TechSheet_ENG.pdf) | 출력물 인장 항복 47 MPa(수평), 층간 접착 18 MPa | 2차 (검색 발췌. PDF는 글꼴 인코딩 문제로 숫자를 읽지 못함). **쓰기 전에 최신 TDS로 확인** |

## 실패 요인과 평가

| ID | 문헌 | 쓰는 곳 | 확인 수준 |
|---|---|---|---|
| R8 | Phillips B, Zhao H. Predictors of assistive technology abandonment. *Assistive Technology* 5(1):36–45 (1993). [doi:10.1080/10400435.1993.10132205](https://doi.org/10.1080/10400435.1993.10132205) | 포기율(약 29%)과 "사용자 필요 변화"가 가장 강한 예측 요인이라는 점 | 2차 |
| R9 | Savage S, Flores-Saviaga C, Rodney R, Savage L, Schull J, Mankoff J. The global care ecosystems of 3D printed assistive devices. *ACM Transactions on Accessible Computing* 15(4), Art. 31 (2022). [doi:10.1145/3537676](https://doi.org/10.1145/3537676) · [arXiv:2210.14984](https://arxiv.org/abs/2210.14984) | 후속 확인·다자 협력이 있을 때 성과가 높음 → 14일 실사용 후 개선 단계 | 초록 (arXiv) |
| R10 | AJOT 2023 Research Platform, 77(S2) RP26: ALS 클리닉의 맞춤 3D 프린팅 보조기기 타당성 연구. [doi:10.5014/ajot.2023.77S2-RP26](https://doi.org/10.5014/ajot.2023.77S2-RP26) | 기성품 포기율이 높은 집단, 7명 중 4명만 후속 면담 | 2차 (저자 미확인) |
| R11 | Benham S, Milstrey B, Stemple J, Davis J, Scatena D, Bush J, Amy K. Customized 3D printed devices for individuals with physical disabilities: Satisfaction and performance of mobile device access. *RESNA Annual Conference* (2023). [PDF](https://www.resna.org/sites/default/files/conference/2023/NewEmergingTechnology/84_Benham/84_Benham.pdf) | QUEST 2.0과 COPM을 사전·사후로 함께 쓴 사례 | 원문 (서론·방법) |
| R12 | Moya Ferrari AL, Baleotti LR, Sandnes FE, Medola FO. Strategic design framework for personalized assistive products: Design tools for systemic orthosis co-creation. *Strategic Design Research Journal* (Unisinos). [PDF](https://revistas.unisinos.br/index.php/sdrj/article/download/27223/60750634/60811093) | 상지 보조기 포기가 외관·제작 한계와 연결됨 | 원문 (초록) |
| R13 | Queensland Health. *Outcome measures for assistive technology*. [PDF](https://www.health.qld.gov.au/__data/assets/pdf_file/0034/1477186/Outcome-Measures-for-AT.pdf) | COPM, QUEST 2.0, PIADS 개요 | 2차 |

## 구조와 설계를 빌려온 오픈소스

| ID | 출처 | 빌려온 것 | 라이선스 |
|---|---|---|---|
| R14 | Makers Making Change (Neil Squire). [toothpaste-squeezer](https://github.com/makersmakingchange/toothpaste-squeezer) 등 기기별 저장소 | 사례 폴더의 문서 구성: 설계 근거, 제작 체크리스트, 부품 목록, 출력 가이드, 사용자 가이드, 변경 이력 | 구조만 참고(파일 복사 없음). 해당 기기는 CC BY-SA 4.0 |
| R15 | Makers Making Change. [3D-Printed-Low-Tech-Assistive-Devices-Kit](https://github.com/makersmakingchange/3D-Printed-Low-Tech-Assistive-Devices-Kit) — Palm Pen Holder, Pen Ball, Key Turner 등 7종 | ref-03에서 기존 설계 후보로 검토 | **저장소에 라이선스 명시 없음** (2026-11-20 확인). 링크만 하고 파일은 복사하지 않음 |
| R16 | Best-README-Template (othneildrew). [GitHub](https://github.com/othneildrew/Best-README-Template) | README 구조 | MIT |

## 국내 플랫폼

| ID | 출처 | 내용 | 확인 수준 |
|---|---|---|---|
| R17 | 국립재활원 보조기기 열린플랫폼 (열린사람들·열린제작실·열린페이지). [의약일보 기사](https://medicaldaily.co.kr/news/11125) | 당사자 참여 개발, 설계도·가이드 오픈소스 공유 | 2차 (언론) |
| R18 | 국립재활원 AT Open Platform. *IEEE Access* (2024). [DOAJ](https://doaj.org/article/0cb83f4bcbd447a4a49fb509b487e71f) | R17과 같은 플랫폼인지 미확인 | 2차 (저자·제목 미확인) |
| R19 | 경기도재활공학서비스연구지원센터 3D보조기기 공공 플랫폼 (사업계획서의 ITDA). [벤처스퀘어 기사](https://www.venturesquare.net/905169/) | 맞춤 보조기기 사례·설계 공개, 공모전 수상작 공개 | 2차 (언론). **주소·등록 절차 미확인** |

## 그 밖에 검토한 자료

- Printables, [Door handle (parameterized OpenSCAD model)](https://printables.com/model/107647-door-handle-parameterized-openscad-model): 매개변수 문고리 손잡이. ref-02에서 검토.
- UNH Institute on Disability, [MakerAbility Catalog](https://iod.unh.edu/ATinNH/access-assistive-technology/welcome-makerability-hub/makerability-catalog): 3D 프린팅 보조도구 목록.
- Georgia Tech 학위논문, [손 기능 장애인을 위한 매개변수 보조기기 설계 도구](https://repository.gatech.edu/server/api/core/bitstreams/26d0891f-a56e-45c7-a929-3aded5f1280b/content): 접근이 차단되어 저자·연도 미확인.

## 빠진 근거

이 조사에서 **찾지 못한** 것도 남깁니다. 다음 팀이 같은 검색을 반복하지 않도록 하기 위해서입니다.

- 한국 고령자의 손 길이 분포 (Size Korea 고령자 조사에 있을 수 있으나 표를 찾지 못함). 지금은 사용자 실측이 필요합니다.
- 가정용 원형 문고리를 돌리는 데 실제로 드는 토크, 고령자의 손목 회전 토크(문고리 기준). 지금은 표준의 상한(R6)으로 설계합니다.
- 펜 굵기와 필기 시 집기 힘을 고령자·관절염 환자에게서 측정한 동료 심사 연구.
- 맞춤 3D 프린팅 기기와 기성품의 포기율을 비교한 대조 연구.
