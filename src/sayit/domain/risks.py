from sayit.domain.models import RiskFlag

RISK_DESCRIPTIONS: dict[RiskFlag, str] = {
    RiskFlag.ACCUSATORY: "句子带责备感，容易激起防御。",
    RiskFlag.TOO_BLUNT: "表达过直，缺少缓冲。",
    RiskFlag.TOO_WEAK: "立场太弱，可能导致对方忽略重点。",
    RiskFlag.TOO_VAGUE: "信息不足，难以稳定判断意图。",
    RiskFlag.COMMANDING: "像命令，不像请求或协商。",
    RiskFlag.LACKS_BUFFER: "缺少过渡语，读起来偏硬。",
    RiskFlag.LACKS_TIMEPOINT: "推进类表达没有明确下一步时间感。",
    RiskFlag.LACKS_COLLABORATION: "缺少配合姿态，容易形成对立。",
    RiskFlag.FACT_DRIFT: "候选引入了原文没有的事实。",
    RiskFlag.FABRICATED_REASON: "候选补充了原文没有的理由或借口。",
}
