# 사례 (cases)

참여자 한 명 = 사례 폴더 하나. 새 사례는 템플릿을 복사해 시작합니다.

```sh
cp -r cases/_template cases/case-01
```

폴더 이름은 `case-01`, `case-02`… 순번만 씁니다([개인정보 원칙](../docs/privacy.md)). `_`로 시작하는 폴더는 평가 도구가 건너뜁니다.

| 파일 | 단계 | 내용 |
|---|---|---|
| `README.md` | 전체 | 사례 요약: 목표 동작, 기기, 현재 상태 |
| `01-interview.md` | 1 | 면담 기록 (익명화) |
| `02-requirements.md` | 1 | 측정값과 설계 요구사항 |
| `03-design-rationale.md` | 2 | 기존 설계 검토, 설계 결정과 이유 |
| `04-build.md` + `bom.csv` | 2 | 출력 조건, 부품 목록, 조립 방법 |
| `05-pre-delivery-check.md` | 3 | 전달 전 점검 (버전마다) |
| `evaluation.csv` | 1, 4 | baseline / v1 / v2 평가 ([기준](../docs/evaluation.md)) |
| `CHANGELOG.md` | 4 | 버전별 변경 내용과 이유 |
| `cad/`, `stl/`, `photos/` | 2, 5 | CAD 원본, 출력 파일, 사진(EXIF 삭제) |

진행 상황 확인: `python3 tools/at_eval.py`
