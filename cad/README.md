# 매개변수 설계 시작점

사례마다 처음부터 그리지 않도록, 자주 나오는 두 동작(쥐기, 문 열기)의 매개변수 OpenSCAD 모델을 둡니다. 사례에 쓸 때는 파일을 `cases/case-XX/cad/`로 복사하고, 맨 위 매개변수를 `02-requirements.md`의 측정값으로 바꿉니다.

| 파일 | 목표 동작 | 핵심 매개변수 |
|---|---|---|
| [`built_up_handle.scad`](built_up_handle.scad) | 숟가락·포크·칫솔·펜을 약한 악력으로 쥐기 | `grip_d`(쥘 수 있는 지름), `slot_w`/`slot_t`(끼울 손잡이 치수), `grooves` |
| [`knob_lever.scad`](knob_lever.scad) | 손목 회전 없이 원형 문고리 열기 | `knob_d`, `knob_depth`, `lever_len` |

## 렌더링

[OpenSCAD](https://openscad.org/)에서 열어 Customizer 패널로 값을 바꾸거나, 명령줄에서:

```sh
openscad -o grip.stl -D grip_d=34 -D slot_w=11 cad/built_up_handle.scad
openscad -o lever.stl -D knob_d=52 cad/knob_lever.scad
```

GitHub Actions가 매 push마다 두 모델을 기본값으로 렌더링해 문법·형상 오류를 확인합니다.

## 상태

**검증 전 초안입니다.** 기본값으로 렌더링되는지만 CI로 확인하며, 아직 출력해서 사람 손으로 써 본 적이 없습니다. 첫 사례에 쓰면서 고친 내용을 여기에 반영합니다.

- 굵은 손잡이: 식기의 입에 닿는 부분은 덮지 않습니다. 손잡이가 끝으로 갈수록 가늘어지는 식기는 TPU로 출력해 마찰로 고정하거나 `slot_through = false`로 막힌 홈을 씁니다.
- 문고리 레버: 고정 나사 끝에 TPU나 고무 패드를 대어 문고리를 긁지 않게 합니다. 잠금장치는 건드리지 않고, 레버가 문틀·벽에 닿지 않는지 설치 전에 확인합니다. 임대 주택이면 설치 전에 허락을 받습니다.
