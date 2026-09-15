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
python3 scripts/build.py   # 生成 docs/
python3 scripts/check.py   # 发布前检查
```

## 目录结构

- `content/data.py`：站点配置、GA4、导流入口、全档位价格数据
- `content/articles.py`：对比文章正文、常见追问、站点 FAQ
- `scripts/build.py`：静态生成，输出到 `docs/`
- `scripts/check.py`：链接、canonical、schema、GA4、UTM、sitemap 与跨站互链检查
- `static/`：搜索引擎验证文件，构建时原样复制

## 价格维护

价格以各家官方定价页为准，每月 1 号核对一次，核对日期写在 `content/data.py` 的 `CHECKED`，
全站页面统一读取该值。
