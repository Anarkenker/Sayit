from sayit.domain.models import Candidate, RewritePlan, RewriteRequest, ToneType
from sayit.engines.local.templates import TemplateRepository


class LocalGenerator:
    def __init__(self, templates: TemplateRepository) -> None:
        self._templates = templates

    def generate(
        self,
        request: RewriteRequest,
        plan: RewritePlan,
    ) -> list[Candidate]:
        language = request.language or "zh"
        bundle = self._templates.load_intent_templates(language, plan.intent.value)
        audience_key = plan.audience if plan.audience in bundle["audiences"] else "default"
        audience_bundle = bundle["audiences"].get(audience_key) or bundle["audiences"]["default"]

        candidates: list[Candidate] = []
        for tone in plan.variant_tones:
            texts = audience_bundle.get(tone.value) or bundle["audiences"]["default"].get(tone.value, [])
            if not texts:
                continue
            template = texts[0]
            candidates.append(
                Candidate(
                    label=tone.value,
                    text=self._fill_template(template, request.text, tone),
                )
            )
        return candidates

    def _fill_template(self, template: str, original_text: str, tone: ToneType) -> str:
        topic = self._infer_topic(original_text)
        deadline = self._infer_deadline(original_text)
        filled = template.format(topic=topic, deadline=deadline)
        if tone == ToneType.FIRM and "尽快" not in filled and deadline:
            return filled.replace("明确的时间点", f"{deadline}前的明确时间点")
        return filled

    def _infer_topic(self, text: str) -> str:
        stripped = text.strip()
        if len(stripped) <= 14:
            return stripped
        return "这件事"

    def _infer_deadline(self, text: str) -> str:
        for token in ("今天内", "今天", "明天", "本周", "这周", "尽快"):
            if token in text:
                return token
        return "方便时"
