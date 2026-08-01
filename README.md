# 洛秧桌宠

洛秧桌宠是一个基于 PyQt5 的 Windows 桌面陪伴小程序。它会常驻桌面，用 2048×2048 透明 PNG 和程序动画呈现洛秧的不同动作，支持拖动、边缘移动、打字陪写气泡、成长等级、金币扭蛋机、可拖动配饰和大模型 API 对话。

本项目是在 [Xzyery/naichashu](https://github.com/Xzyery/naichashu) 的基础上制作的角色定制版本。主要修改包括洛秧角色素材、人格和对话、黑白 UI、46 个状态映射、静态图程序动画以及高 DPI 显示支持。完整归属和许可说明见 [NOTICE.md](NOTICE.md)。

## 免编程下载运行

普通用户不需要安装 Python，也不需要打包。

前往本仓库的 [Releases](../../releases/latest) 页面下载 `Luoyang-Desktop-Pet-v1.0.0-Windows.zip`，解压后双击 `洛秧桌宠.exe` 即可运行，不需要安装 Python。

首次运行后，程序会在 exe 同目录生成本地存档；AI 配置在保存接口设置后生成：

- `luoyang_profile.json`
- `luoyang_ai_config.json`

这两个文件用于保存等级、金币、抽奖、配饰位置和 API 设置。

## 素材预览

<p>
  <img src="luoyang_assets/01_idle.png" width="120" alt="安静陪伴">
  <img src="luoyang_assets/02_sleepy.png" width="120" alt="启动起床">
  <img src="luoyang_assets/03_arrive.png" width="120" alt="挥手出现">
  <img src="luoyang_assets/04_goodbye.png" width="120" alt="挥手告别">
  <img src="luoyang_assets/05_eat.png" width="120" alt="小口吃东西">
  <img src="luoyang_assets/06_study.png" width="120" alt="认真学习">
  <img src="luoyang_assets/07_shy.png" width="120" alt="害羞">
  <img src="luoyang_assets/08_sleep.png" width="120" alt="睡着了">
</p>

<p>
  <img src="luoyang_assets/09_confused.png" width="120" alt="疑惑">
  <img src="luoyang_assets/10_angry.png" width="120" alt="生气">
  <img src="luoyang_assets/11_cry.png" width="120" alt="委屈落泪">
  <img src="luoyang_assets/12_celebrate.png" width="120" alt="开心庆祝">
  <img src="luoyang_assets/13_encourage.png" width="120" alt="给你打气">
  <img src="luoyang_assets/14_run.png" width="120" alt="小跑">
  <img src="luoyang_assets/15_give_flower.png" width="120" alt="双手送花">
  <img src="luoyang_assets/16_stretch.png" width="120" alt="伸懒腰">
</p>

配饰示例：

<p>
  <img src="accessories/crown_small.png" width="90" alt="小皇冠">
  <img src="accessories/crown_full_sugar.png" width="90" alt="月白皇冠">
  <img src="accessories/glasses_study.png" width="90" alt="学习眼镜">
  <img src="accessories/flower_clip.png" width="90" alt="小花发夹">
  <img src="accessories/milk_tea_hat.png" width="90" alt="黑白蝴蝶结礼帽">
  <img src="accessories/lucky_star_halo.png" width="90" alt="欧气星环">
</p>

## 快速开始

1. 安装 Python 3.10 或更高版本。
2. 在项目目录安装依赖：

```bat
pip install -r requirements.txt
```

3. 双击运行：

```bat
run_naicha_mouse.bat
```

也可以在命令行运行：

```bat
python main.py
```

## 主要功能

- 启动动画：先显示揉眼起床，再挥手出现。
- 退出动画：右键退出后挥手告别，约 3.5 秒后关闭。
- PNG 动效：程序会按状态添加呼吸、摇摆、点头、弹跳、发抖、奔跑起伏等轻量动画。
- 常规随机：日常、休息、吃饭、学习、工作和低概率事件表情会按权重切换。
- 打字陪写：检测键盘节奏，显示安全拟态气泡，不显示真实输入内容。
- 移动模式：支持停止移动、底部散步、边缘巡游和召唤回来。
- 大小档位：30% 至 200%，默认 175%；按显示器 DPI 生成高分辨率角色和配饰画面。
- 成长系统：记录等级、互动值、金币、陪伴时间和今日专注次数。
- 扭蛋机：消耗金币抽取配饰、称号、演出、语言奖励和白花碎片。
- 配饰系统：抽到配饰后可佩戴、隐藏、缩放，右键长按配饰可拖动调整位置。
- 气泡样式：抽到气泡边框后，可在右键菜单切换黑白蕾丝气泡等样式。
- 演出收藏：抽到演出奖励后，可在右键菜单中回放收藏演出。
- AI 聊天：可配置 OpenAI-compatible、Claude Messages 或 Gemini generateContent 接口，与洛秧对话。

## 右键菜单

- `摸摸洛秧`
- `喂点东西`
- `送你花花`
- `开始专注` / `结束专注`
- `休息一下`
- `久坐伸展`
- `鼓励我一下`
- `庆祝一下`
- `状态面板`
- `气泡样式`
- `演出收藏`
- `AI 聊天`
- `洛秧扭蛋机`
- `配饰`
- `称号`
- `关闭/开启打字跟随`
- `关闭/开启打字气泡`
- `换个常驻动作`
- `召唤回来`
- `移动模式`
- `大小`
- `透明度`
- `退出`

## 成长和金币规则

互动值用于升级，金币用于扭蛋。获得互动值时，会同步获得等量金币。

| 行为 | 奖励 |
|---|---:|
| 每日首次启动 | +10 互动值，+10 金币 |
| 陪伴 10 分钟 | +5 互动值，+5 金币 |
| 摸摸 | +2 互动值，+2 金币 |
| 喂食 | +5 互动值，+5 金币 |
| 送花 | +5 互动值，+5 金币 |
| 庆祝 | +3 互动值，+3 金币 |
| 完成一次专注 | +25 互动值，+25 金币 |

规则说明：

- 等级上限为 52。
- 互动操作每日上限为 200 互动值。
- 陪伴时长获得的互动值和金币无每日上限。
- 升级所需互动值公式：

```text
required_exp = int(55 + level * level * 0.25 + level * 18)
```

## 洛秧扭蛋机

| 抽取方式 | 消耗 |
|---|---:|
| 每日首抽 | 20 金币 |
| 单抽 | 30 金币 |
| 十连 | 270 金币 |

奖池概率：

| 档位 | 概率 | 内容 |
|---|---:|---|
| 普通 | 68% | 小互动值、金币返还、白花碎片、即时台词、普通口头禅 |
| 稀有 | 24% | 临时配饰、稀有口头禅、气泡边框、稀有演出 |
| 超稀有 | 7% | 永久配饰、特殊口头禅包、称号、特殊演出收藏 |
| 隐藏 | 1% | 隐藏配饰、隐藏称号、隐藏语言、大奖礼包 |

十连至少包含 1 个稀有及以上奖励。60 抽未出超稀有及以上时，下一个稀有及以上结果会升级为超稀有。

隐藏档里的 `月白珍藏礼包` 会一次性获得：

- 互动值 +520
- 金币 +520
- 白花碎片 +52
- 隐藏配饰：月白皇冠、欧气星环
- 隐藏称号：今日欧气小秧
- 气泡样式：永久月白蕾丝气泡边框
- 演出收藏：愉快飞天庆祝
- 隐藏口头禅：秧秧的认真话、好运低语、小小祝福

## AI 聊天配置

右键选择 `AI 聊天` -> `配置 API`，填写：

- 接口格式：OpenAI-compatible、Anthropic Claude Messages 或 Google Gemini generateContent。
- Base URL：按服务商控制台提供的地址填写。
- 模型名：按服务商控制台支持的模型名填写。
- API Key：只保存在本地 `luoyang_ai_config.json`，不会写入项目仓库。

请从所使用模型服务商的官方控制台获取 Base URL、API Key 和模型名。不要提交或分享生成的 `luoyang_ai_config.json`。

## 配饰说明

气泡边框抽到后可在右键菜单 `聊天和成长` -> `气泡样式` 中切换。黑白蕾丝气泡会带月白渐变、深灰描边和右上角花饰，状态面板也会同步使用当前气泡样式。

配饰透明 PNG 放在 `accessories/`，配饰位置和默认尺寸写在 `naicha_mouse_accessories.json`。

已包含的配饰素材包括：

- 小皇冠、月白皇冠
- 学习眼镜、耳机、工作牌
- 睡帽、云朵睡帽、黑白蝴蝶结礼帽
- 星星发夹、小花发夹、粉色蝴蝶结
- 白花挂件、小背包、围巾
- 欧气星环、守护披风、彩虹贴纸

右键菜单进入 `配饰` 可切换显示、缩放、重置位置或佩戴已有配饰。右键长按当前配饰可以拖动位置。

## 文件结构

| 路径 | 说明 |
|---|---|
| `main.py` | 桌宠主程序 |
| `run_naicha_mouse.bat` | Windows 双击启动脚本 |
| `build_exe.bat` | Windows 一键打包脚本 |
| `requirements.txt` | Python 依赖 |
| `release/` | 可直接双击运行的 exe |
| `luoyang_assets/` | 16 张 2048×2048 洛秧透明 PNG 状态素材 |
| `accessories/` | 透明 PNG 配饰素材 |
| `app_icon.ico` | exe 图标，来自 `luoyang_assets/01_idle.png` |
| `tools/process_luoyang_assets.py` | 从桌面源图重新生成透明状态素材 |
| `naicha_mouse_state_map.json` | 状态、素材、随机池和触发配置 |
| `naicha_mouse_dialogues.json` | 气泡文案池 |
| `naicha_mouse_gacha_pool.json` | 扭蛋机奖池、概率和奖励配置 |
| `naicha_mouse_accessories.json` | 配饰默认位置、尺寸和素材文件 |

运行后会自动生成本地数据文件：

| 路径 | 说明 |
|---|---|
| `luoyang_profile.json` | 等级、互动值、金币、陪伴时间和抽奖数据 |
| `luoyang_ai_config.json` | AI 聊天 API 配置 |

这两个文件属于个人本地数据，已经写入 `.gitignore`。

## 自定义

修改状态素材：

```json
{
  "id": "idle_static_cute",
  "file": "01_idle.png",
  "motion": "breathe"
}
```

`motion` 可使用 `breathe`、`sleepy`、`wave`、`sway`、`nod`、`wiggle`、`sleep`、`nibble`、`write`、`confused`、`pop`、`shake`、`dance`、`jump`、`cry`、`run`、`float`、`bounce`、`present` 或 `stretch`。

常规随机由 `naicha_mouse_state_map.json` 里的 `randomGroups` 控制总权重，由每个状态的 `random_group` 和 `random_weight` 控制分组和组内权重。

修改气泡文案：编辑 `naicha_mouse_dialogues.json`。

修改奖池：编辑 `naicha_mouse_gacha_pool.json`。

修改配饰位置和默认尺寸：编辑 `naicha_mouse_accessories.json`。

## 项目来源与许可

- 原项目：[Xzyery/naichashu](https://github.com/Xzyery/naichashu)
- 本项目属于角色定制和功能修改版本，并非原作者发布的官方版本。
- 截至本仓库整理时，原项目没有提供开源许可证。本仓库因此不擅自添加 MIT、GPL 等许可证，也不表示获得了原作者代码与原素材的再授权。
- 洛秧角色图片及配饰图片不因代码公开而自动获得可复制、商用或训练授权。
- 计划复制、分发或商用本项目之前，请分别取得原项目作者及相关素材权利人的许可。

更详细的信息见 [NOTICE.md](NOTICE.md)。
