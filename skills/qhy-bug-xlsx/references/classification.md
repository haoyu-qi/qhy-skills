# Bug List Classification Reference

Use this reference when the default script needs adjustment for a project-specific bug list.

## Common Columns

- `Bug编号`: identifier; trim spaces and tabs, preserve as text.
- `Bug标题`: original defect title; preserve wording, normalize whitespace only.
- `严重程度`: extract the leading number as `级别数`.
- `解决方案`: raw status or disposition; preserve in output and use for classification.
- `解决日期`: may contain a real Excel date serial or free-text notes. Split dates into `解决日期` and non-date text into `备注`.

## Recommended Output Headers

`来源`, `Bug编号`, `严重级别`, `级别数`, `状态归类`, `模块`, `处理建议`, `计划/提示`, `解决日期`, `Bug标题`, `原解决方案`, `备注`

## Module Keywords

- `指挥调度`: `指挥调度`, `调度会议`
- `融合会议`: `融合会议`
- `简易会议`: `简易会议`, `快速会议`, `多人会议`
- `共享/协作`: `共享`, `协作`, `屏幕共享`
- `地图/定位`: `地图`, `定位`, `位置上报`, `标会`, `标绘`
- `图像资源`: `图像资源`, `预置位`
- `日程/预定会议`: `日程`, `预定会议`, `最近会议`
- `IM/通话`: `IM`, `语音通话`, `微信视频电话`
- `转写/AI`: `转写`, `字幕`, `华智ai`, `华智AI`, `会议纪要`
- `设备/登录`: `登录`, `设备`, `上线`, `下线`, `内网`, `外网`
- `性能/后台`: `CPU`, `cpu`, `发烫`, `挂机`, `息屏`, `后台`, `多任务`, `卡顿`, `未响应`
- `音视频`: `视频`, `音频`, `麦克风`, `摄像头`, `蓝牙`, `耳机`, `声音`, `黑屏`, `图像`
