# 제작 방법

## 출력 조건 (시작값)

| 부품 | 매개변수 세트 | 소재 | 층 높이 | 채움 | 벽 | 서포트 | 방향 |
|---|---|---|---|---|---|---|---|
| 레버 캡 | `ref02-worstcase` | PETG | 0.2 mm | 40% 이상 | 4 | 나사 보스 아래만 | 앞면이 바닥 (캡 입구가 위) |

강도 계산(R7)은 꽉 찬 단면을 전제로 합니다. 채움이 낮으면 실제 강도가 낮아지므로 벽 4개, 채움 40% 이상으로 시작하고, 전달 전 점검의 하중 시험으로 확인합니다.

```sh
openscad -p reference/ref-02-door-knob/cad/params.json -P ref02-worstcase -o ref02.stl cad/knob_lever.scad
python3 tools/design_params.py lever --torque <실측 N·m>   # 실측 후 다시 계산
```

## 부품

| 품목 | 수량 | 비고 |
|---|---|---|
| 출력한 레버 캡 | 1 | |
| M4 × 12 mm 나사 (플라스틱용 탭핑) | 3 | 지름 3.4 mm 구멍에 바로 체결 |
| TPU 또는 고무 패드 (지름 약 8 mm) | 3 | 나사 끝에 붙여 문고리 보호 |
