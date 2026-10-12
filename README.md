# AI 订阅比价指南

ChatGPT、Claude、Gemini、Grok 以及主流 AI 编程工具的订阅价格、额度口径与选购对比。

[访问网站](https://ai66man.github.io/chatgpt-plus-sub/)

## 站点定位

- 只做**跨品牌比价与横评**：价格总表、能力对比、编程订阅比价、购买渠道对比
- 页面上只列**各家官方美元标价**并标注核对日期；人民币开通报价不在本站维护
- 不做单品充值页，不提供跨区订阅或绕过地区限制的方法

## 商业关系

本站为 GoPlus 提供商业导流，页面中的「国内开通」入口会跳转到该第三方服务商并带来源标识参数。
本站与 OpenAI、Anthropic、Google、xAI 均无隶属关系。完整披露见站内「关于本站」页面。

## 本地构建

需要 Python 3.10+。

```sh
python3 scripts/build.py     # 生成 docs/
python3 scripts/check.py     # 发布前检查
python3 scripts/indexnow.py  # 推送后：把新增或 lastmod 变化的 URL 提交到 IndexNow（必应）
```

## 目录结构

- `content/data.py`：站点配置、GA4、导流入口、全档位价格数据、各页面更新日期、首页按用途推荐
- `content/articles.py`：对比文章正文（含 `published` / `updated` / `audience`）、常见追问、站点 FAQ
- `scripts/build.py`：静态生成，输出到 `docs/`；sitemap lastmod 与 schema dateModified 按页读取
- `scripts/check.py`：链接、canonical、schema、GA4、UTM、sitemap、外链密度（首页 ≤3、文章小店 ≤2）与跨站互链检查
- `scripts/indexnow.py`：IndexNow 提交，状态记在 `scripts/.indexnow-state.json`
- `static/`：搜索引擎验证文件与 IndexNow key 文件，构建时原样复制到站点根目录

## 价格维护

价格以各家官方定价页为准，每月 1 号核对一次，核对日期写在 `content/data.py` 的 `CHECKED`，
全站页面统一读取该值。文章有实质修改时同步改该篇的 `updated`；首页、FAQ、索引、关于页的日期在 `PAGE_DATES`。

## 外链规则

- 每篇文章最多两处小店入口（文首结论旁、文末「怎么开通」），来源区固定一条 GoPlus 链接
- 首页外链合计不超过 3 个；所有外链带 `utm_campaign=ai66man_compare` 与 `rel="sponsored"`
- 与 imi0801 的 ChatGPT 百科站不互链
