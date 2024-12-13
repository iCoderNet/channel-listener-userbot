import re
import json

def parse_to_json(template):
    data = {}

    token_name_match = re.search(r'First Call\)\*\* \$(\S+)', template)
    data['token_symbol'] = f"${token_name_match.group(1)}" if token_name_match else None

    caller_match = re.search(r'got first call from:\s*\[([^\]]+)\]\((https?://[^\)]+)\)', template)
    data['caller_name'] = caller_match.group(1).strip() if caller_match else None
    data['caller_link'] = caller_match.group(2).strip() if caller_match else None

    avg_cpw_match = re.search(r'Avg CPW.*?(\d+\.\d+)', template)
    data['avg_cpw'] = avg_cpw_match.group(1) if avg_cpw_match else None

    total_calls_match = re.search(r'Total calls: (\d+)', template)
    data['total_calls'] = int(total_calls_match.group(1)) if total_calls_match else None

    address_match = re.search(r'Total calls: \d+\s+([^\r\n]+)', template)
    data['address'] = (
        ''.join(c for c in address_match.group(1).strip() if c.isprintable())
        if address_match else None
    )
    data['address'] = data['address'].replace('`', '')

    mcap_match = re.search(r'MCap\*\*: \$(\d+[\.\d]*[KMB]?)', template)
    liquid_match = re.search(r'Liquid\*\*: \$(\d+[\.\d]*[KMB]?)', template)
    volume_6h_match = re.search(r'6h\*\*: \$(\d+[\.\d]*[KMB]?)', template)
    volume_1h_match = re.search(r'1h\*\*: \$(\d+[\.\d]*[KMB]?)', template)

    data['market_data'] = {
        'mcap': mcap_match.group(1) if mcap_match else None,
        'liquid': liquid_match.group(1) if liquid_match else None,
        'volume_6h': volume_6h_match.group(1) if volume_6h_match else None,
        'volume_1h': volume_1h_match.group(1) if volume_1h_match else None,
    }

    chain_match = re.search(r'Chain:\*\* #([A-Z]+)', template)
    data['chain'] = chain_match.group(1) if chain_match else None

    name_match = re.search(r'Name:\*\* ([^\n]+)', template)
    data['name'] = name_match.group(1).strip() if name_match else None

    roi_link_match = re.search(r'% ROI\]\((https:\/\/t\.me\/CallAnalyserBot\?start=scan-caller-[^\)]+)\)', template)
    top_week_link_match = re.search(r'Top Week\]\((https:\/\/t\.me\/CallAnalyserBot\?start=latest-week-calls-[^\)]+)\)', template)
    data['caller_links'] = {
        'roi': roi_link_match.group(1) if roi_link_match else None,
        'top_week': top_week_link_match.group(1) if top_week_link_match else None,
    }

    trending_link_match = re.search(r'KOL Trending 🔥\]\((https:\/\/t\.me\/walloftrophies\/\d+)\)', template)
    data['trending_link'] = trending_link_match.group(1) if trending_link_match else None

    maestro_link_match = re.search(r'Maestro\]\((https:\/\/t\.me\/MaestroSniperBot\?start=[^\)]+)\)', template)
    maestro_pro_link_match = re.search(r'Maestro Pro\]\((https:\/\/t\.me\/MaestroProBot\?start=[^\)]+)\)', template)
    magnum_link_match = re.search(r'Magnum\]\((https:\/\/t\.me\/magnum_trade_bot\?start=[^\)]+)\)', template)
    data['buy_links'] = {
        'maestro': maestro_link_match.group(1) if maestro_link_match else None,
        'maestro_pro': maestro_pro_link_match.group(1) if maestro_pro_link_match else None,
        'magnum': magnum_link_match.group(1) if magnum_link_match else None,
    }

    dexs_link_match = re.search(r'DexS\]\((https:\/\/dexscreener\.com\/[^\)]+)\)', template)
    dext_link_match = re.search(r'DexT\]\((https:\/\/www\.dextools\.io\/[^\)]+)\)', template)
    pirb_scan_link_match = re.search(r'PIRB Scan\]\((https:\/\/t\.me\/PIRBViewBot\?start=[^\)]+)\)', template)
    data['scan_links'] = {
        'dexs': dexs_link_match.group(1) if dexs_link_match else None,
        'dext': dext_link_match.group(1) if dext_link_match else None,
        'pirb_scan': pirb_scan_link_match.group(1) if pirb_scan_link_match else None,
    }

    return json.dumps(data, indent=4)


# Example template code
'''
template = """
☘️**(First Call)** $RIZZLE got first call from:
[DEGEMS CALLS](https://t.me/DEGEMSCALLS/3571)   |**⚡️**[**Avg CPW](https://t.me/CallAnalyserPortal/130)****:** 602.28
Total calls: 1
‎`52495A5A4C450000000000000000000000000000.rE99nDT3riuM9VjMQkVstMqRGBsnUHw6vm`‎

🎯**--BUY**--: [Maestro](https://t.me/MaestroSniperBot?start=52495A5A4C450000000000000000000000000000.rE99nDT3riuM9VjMQkVstMqRGBsnUHw6vm-callanalyser) | [Maestro Pro](https://t.me/MaestroProBot?start=52495A5A4C450000000000000000000000000000.rE99nDT3riuM9VjMQkVstMqRGBsnUHw6vm-callanalyser) | [Magnum](https://t.me/magnum_trade_bot?start=KsVSApge_snipe_52495A5A4C450000000000000000000000000000.rE99nDT3riuM9VjMQkVstMqRGBsnUHw6vm)

🔎**Scan:** [DexS](https://dexscreener.com/xrpl/52495A5A4C450000000000000000000000000000.rE99nDT3riuM9VjMQkVstMqRGBsnUHw6vm_XRP) | [DexT](https://www.dextools.io/app/en/xrpl/pair-explorer/52495A5A4C450000000000000000000000000000.rE99nDT3riuM9VjMQkVstMqRGBsnUHw6vm_XRP) | [PIRB Scan](https://t.me/PIRBViewBot?start=52495A5A4C450000000000000000000000000000.rE99nDT3riuM9VjMQkVstMqRGBsnUHw6vm)
**🔒MCap**: $175.7K | **Liquid**: $12.5K
**🕚Volume: 6h**: $36.8K | **1h**: $12.1K
🔰**Chain:** #XRPL | 🔰**Name:** RIZZLE
📞**Caller:** [% ROI](https://t.me/CallAnalyserBot?start=scan-caller-1001304149592) | [Top Week](https://t.me/CallAnalyserBot?start=latest-week-calls-1001304149592)
📈**Trending:** [KOL Trending 🔥](https://t.me/walloftrophies/136)

**Listen to qualified calls in real time** [@CallAnalyser](https://t.me/CallAnalyser)
➖️➖️➖️➖️➖️➖️➖️➖
✅**XRP** **chain:** Trading bots & how to trade [here](https://t.me/CallAnalyser/111683) ✅
"""

result = parse_to_json(template)
open("result.json", "w").write(result)
'''
