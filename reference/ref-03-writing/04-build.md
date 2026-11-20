# 제작 방법

## 1순위: Pen Ball

[원본 저장소](https://github.com/makersmakingchange/3D-Printed-Low-Tech-Assistive-Devices-Kit/tree/main/Pen-Ball)의 `Documentation/`에 있는 출력 가이드, 사이즈 가이드, 조립 가이드를 그대로 따릅니다. 이 저장소에는 파일을 복사하지 않습니다.

## 3순위: 굵은 펜 손잡이

| 매개변수 세트 | 소재 | 층 높이 | 채움 | 서포트 | 방향 |
|---|---|---|---|---|---|
| `ref03-30mm`, `ref03-38mm` | PETG 또는 TPU | 0.2 mm | 20% | 없음 | 세워서 |

```sh
for s in ref03-30mm ref03-38mm; do
  openscad -p reference/ref-03-writing/cad/params.json -P $s -o $s.stl cad/built_up_handle.scad
done
```
