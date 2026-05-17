"""
配置管理 / Configuration management
"""
import random

# Google 域名池 — 实测可对 Opera Mini UA 稳定返回 200 + Gx5Zad 结构
# 的大区域域名。单个域名连续请求会被限流(403),轮询多个域名能把
# 压力分摊到不同 (region, IP) 槽位。小国 TLD(.jm/.sl/.nf 等)对
# 非住宅 IP 不友好,已排除。
#
# Verified-stable Google domains: each returns 200 + Gx5Zad for Opera Mini
# UA. Rotating spreads load across (region, IP) buckets so a single domain
# being rate-limited doesn't kill the whole pipeline. Small-TLD domains
# (.jm/.sl/.nf, etc.) are excluded because they 403 on non-residential IPs.
_STABLE_DOMAINS = (
    "www.google.com",
    "www.google.com.au",
    "www.google.com.br",
    "www.google.ca",
    "www.google.es",
    "www.google.it",
    "www.google.pl",
    "www.google.ru",
    "www.google.com.tr",
    "www.google.co.in",
    "www.google.com.mx",
)


# 默认不注入 cookies — 2026-05 实测:Opera Mini UA + CONSENT cookies
# 反而触发 403(Google 校验 UA 与流量画像一致性)。如果在欧盟出口下
# 需要绕过 consent 墙,可手动通过 headers 注入 Cookie 头。
#
# Empirically (2026-05): Opera Mini UA + CONSENT cookies triggers a 403
# (Google checks UA-vs-traffic consistency). If you exit through an EU
# IP and hit the consent wall, inject Cookie via headers manually.
GOOGLE_COOKIES: dict = {}


def get_opera_mini_user_agent() -> str:
    """
    生成随机 Opera Mini User-Agent (触发 div.Gx5Zad 容器的轻量 SERP)
    Generate random Opera Mini UA (triggers div.Gx5Zad lightweight SERP)

    2026-05 实测:这是当前 httpx + 纯 HTTP 路径下唯一稳定可用的 UA。
    Lynx UA 已被 Google 拦下("Update your browser"),
    现代 Chrome UA 会被重定向到需要 JS 的页面。

    Empirically (2026-05): this is the only UA still working under a
    pure httpx pipeline. Lynx UA gets a "Update your browser" page;
    modern Chrome UA gets a JS-required page.
    """
    patterns = [
        "Opera/9.80 (J2ME/MIDP; Opera Mini/{v}/{b}; U; {l}) Presto/{p} Version/{f}",
        "Opera/9.80 (Android; Linux; Opera Mobi/{mb}; U; {l}) Presto/{p} Version/{f}",
        "Opera/9.80 (iPhone; Opera Mini/{v}/{b}; U; {l}) Presto/{p} Version/{f}",
        "Opera/9.80 (iPad; Opera Mini/{v}/{b}; U; {l}) Presto/{p} Version/{f}",
    ]
    repl = {
        "{l}": random.choice(["en-US", "en-GB", "de-DE", "fr-FR", "es-ES", "ru-RU", "zh-CN"]),
        "{p}": random.choice(["2.6.35", "2.7.60", "2.8.119"]),
        "{f}": random.choice(["10.00", "11.10", "12.16"]),
        "{v}": random.choice(["4.0", "5.0.17381", "7.1.32444", "9.80"]),
        "{b}": random.choice(["18.678", "24.743", "503"]),
        "{mb}": random.choice(["27", "447", "ADR-1011151731"]),
    }
    result = random.choice(patterns)
    for k, v in repl.items():
        result = result.replace(k, v)
    return result


def get_random_user_agent() -> str:
    """
    获取随机 User-Agent (默认 Opera Mini,匹配主解析路径 div.Gx5Zad)
    Get random User-Agent (default Opera Mini, matches div.Gx5Zad parser)
    """
    return get_opera_mini_user_agent()


def get_random_domain() -> str:
    """
    从稳定域名池中随机取一个 Google 搜索 URL
    Pick a random Google search URL from the stable-domain pool.
    """
    return f"https://{random.choice(_STABLE_DOMAINS)}/search"


def iter_stable_domains():
    """
    返回稳定域名池(每个 URL),供重试逻辑切换域名使用
    Yield search URLs from the stable-domain pool, used by retry logic
    to swap domain on rate-limit.
    """
    return [f"https://{d}/search" for d in _STABLE_DOMAINS]
