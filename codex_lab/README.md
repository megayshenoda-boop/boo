# Codex Lab

هذا الفولدر مساحة تجارب معزولة خارج `lords_bot`.

الهدف منه:

- نجرب بدون لمس المسار الرئيسي مباشرة.
- نبني أدوات تحليل صغيرة تمنعنا من الضياع بين الوثائق والكود.
- نحول الوضع من "إحساس عام" إلى "لوحة متابعة واضحة".

## ما الموجود هنا

- `build_inventory.py`
  - سكربت static analysis يقرأ `lords_bot/commands.py` و `lords_bot/protocol.py`
  - يخرج inventory منظم للأوامر
  - يميز بين:
    - direct packet builders
    - composite helpers
    - encrypted vs plain commands
- `COMMAND_INVENTORY.md`
  - ناتج مولد من السكربت
- `command_inventory.json`
  - نسخة JSON من نفس البيانات
- `NEXT_EXPERIMENTS.md`
  - خطة الحركة التالية داخل المعمل
- `DOC_DRIFT.md`
  - أهم التعارضات الحالية بين الوثائق والكود
- `build_response_map.py`
  - يقرأ `lords_bot/test_results.json` و `lords_bot/round2_results.json`
  - يخرج خريطة normalized للردود
- `RESPONSE_MAP.md`
  - ملخص مقروء للردود وأنماطها
- `response_map.json`
  - نسخة JSON من نفس البيانات
- `EVIDENCE_RULES.md`
  - معيار موحد لمعنى "شغال"
- `PRIORITY_BOARD.md`
  - ترتيب التنفيذ حتى لا يتشتت الشغل
- `build_signal_ledger.py`
  - يبني قاموسًا صغيرًا لمعاني الردود المتكررة
- `RESPONSE_SIGNAL_LEDGER.md`
  - يميز بين heartbeat, map-view, state-update, unknown responses
- `response_signal_ledger.json`
  - نسخة JSON من نفس القاموس

## قواعد العمل داخل المعمل

- لا نعدل المسار الرئيسي إلا بعد أن تكون الفكرة اتثبتت هنا.
- أي استنتاج يجب أن يكون له مصدر: كود، نتيجة اختبار، أو artifact موجود في المشروع.
- نميز دائما بين:
  - implemented
  - server responded
  - semantically verified
  - visible in-game effect

## التشغيل

```bash
python codex_lab/build_inventory.py
python codex_lab/build_response_map.py
python codex_lab/build_signal_ledger.py
```

## ملاحظة

المعمل الحالي يركز على التحليل المحلي والتنظيم. لا يوجد فيه أي افتراض أن الاتصال الحي أو الاختبارات الشبكية تم إثباتها من داخله بعد.
