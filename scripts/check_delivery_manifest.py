# -*- coding: utf-8 -*-
"""交付 manifest / 评审文档轻量检查脚本（trial，2026-07-08 起）。

来源：错题本复盘（A165）。针对错误家族 F1「验证等级冒充」和 F2「几何声明无证据」，
把"AI 忘了做"变成"机器会问"。只做文本存在性检查，不替代真实几何 QA、复审或截图验收。

用法：
    python scripts/check_delivery_manifest.py <文件1.md> [文件2.md ...]

检查项：
    1. 产物类型声明：文档必须包含「产物类型」字段或 workflow-gates.yml 中任一 artifact_type id。
    2. 几何声明配证据：声称"正交通过 / 几何通过"时，必须同时出现图像证据引用和裁切 / 参考线说明。
    3. 交付完成配 STATUS：声称"本轮交付完成"时，必须提及 STATUS 更新。
    4. 生产候选配复审：声称升级为"生产候选 / 生产标杆 / 资源标杆 / 真源候选"时，必须提及复审。

退出码：0 = 全部通过；1 = 存在 FAIL；2 = 参数或文件错误。
无第三方依赖。
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATES_YML = REPO_ROOT / "docs" / "workflows" / "workflow-gates.yml"

# 否定语境：命中声明词但前方紧邻否定词时，不视为放行声明
NEGATION = r"(不得|不能|禁止|不应|不算|不等于|未|没有|不可)[^。\n]{0,10}$"


def load_artifact_types():
    """从 workflow-gates.yml 的 artifact_types 块提取类型 id（无 PyYAML 依赖）。"""
    types = []
    if not GATES_YML.exists():
        return types
    in_block = False
    for line in GATES_YML.read_text(encoding="utf-8").splitlines():
        if re.match(r"^artifact_types:\s*$", line):
            in_block = True
            continue
        if in_block:
            if re.match(r"^\S", line):  # 回到顶层 key，块结束
                break
            m = re.match(r"^  (\w+):\s*$", line)
            if m:
                types.append(m.group(1))
    return types


def negated(text, match_start):
    """检查命中位置前方是否有否定语境。"""
    prefix = text[max(0, match_start - 24):match_start]
    return re.search(NEGATION, prefix) is not None


def find_claims(text, pattern):
    """返回未被否定语境包裹的声明命中列表。"""
    hits = []
    for m in re.finditer(pattern, text):
        if not negated(text, m.start()):
            hits.append(m.group(0))
    return hits


def check_file(path, artifact_types):
    """返回 (results, has_fail)。results 为 (级别, 检查名, 说明) 列表。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    results = []
    has_fail = False

    # 检查 1：产物类型声明
    type_hits = [t for t in artifact_types if t in text]
    if "产物类型" in text or type_hits:
        detail = "产物类型字段存在" if "产物类型" in text else f"含类型 id：{', '.join(type_hits[:3])}"
        results.append(("PASS", "产物类型声明", detail))
    else:
        results.append(("FAIL", "产物类型声明",
                        "未找到「产物类型」字段，也未找到任何 workflow-gates.yml artifact_type id"))
        has_fail = True

    # 检查 2：几何声明配证据
    geo_claims = find_claims(
        text, r"正交通过|几何通过|几何 ?QA ?通过|geometry[ _]?pass|orthogonal[ _]?pass|text_geometry_pass|art_shell_geometry_pass")
    if geo_claims:
        has_image = re.search(r"\.(png|jpg|jpeg|webp)\b|docs/screenshots/", text) is not None
        has_qa_words = re.search(r"参考线|guides?|裁切|crop|角度|deg", text) is not None
        if has_image and has_qa_words:
            results.append(("PASS", "几何声明配证据",
                            f"命中声明（{geo_claims[0]} 等 {len(geo_claims)} 处），已见图像引用与裁切/参考线说明"))
        else:
            missing = []
            if not has_image:
                missing.append("图像证据引用（.png 路径或 docs/screenshots/）")
            if not has_qa_words:
                missing.append("裁切 / 参考线 / 角度说明")
            results.append(("FAIL", "几何声明配证据",
                            f"声称几何/正交通过（{geo_claims[0]} 等），但缺少：{'；'.join(missing)}"))
            has_fail = True
    else:
        results.append(("SKIP", "几何声明配证据", "本文档未声称几何/正交通过"))

    # 检查 3：交付完成配 STATUS
    done_claims = find_claims(text, r"本轮交付完成|交付已完成|本轮已交付完成")
    if done_claims:
        if re.search(r"STATUS", text, re.IGNORECASE):
            results.append(("PASS", "交付完成配 STATUS", "已提及 STATUS 更新"))
        else:
            results.append(("FAIL", "交付完成配 STATUS",
                            "声称本轮交付完成，但未提及资产线 STATUS.md 更新"))
            has_fail = True
    else:
        results.append(("SKIP", "交付完成配 STATUS", "本文档未声称本轮交付完成"))

    # 检查 4：生产候选配复审
    prod_claims = find_claims(
        text, r"(?:是|作为|升级为|判定为|已成为|锁定为)[^。\n]{0,12}(?:生产候选|生产标杆|资源标杆|真源候选)|production_candidate[^。\n]{0,8}(?:通过|pass)")
    if prod_claims:
        if re.search(r"复审|像素艺术|art[ _]?director|review", text, re.IGNORECASE):
            results.append(("PASS", "生产候选配复审", "已提及复审"))
        else:
            results.append(("FAIL", "生产候选配复审",
                            f"声称生产候选/标杆（{prod_claims[0]}），但未提及像素艺术复审或等价复审"))
            has_fail = True
    else:
        results.append(("SKIP", "生产候选配复审", "本文档未声称生产候选/标杆/真源候选"))

    return results, has_fail


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    if len(argv) < 2:
        print("用法：python scripts/check_delivery_manifest.py <文件1.md> [文件2.md ...]")
        return 2
    artifact_types = load_artifact_types()
    if not artifact_types:
        print(f"[警告] 未能从 {GATES_YML} 提取 artifact_types；产物类型检查只认「产物类型」字段")
    overall_fail = False
    for arg in argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"[错误] 文件不存在：{arg}")
            return 2
        results, has_fail = check_file(path, artifact_types)
        overall_fail = overall_fail or has_fail
        print(f"\n=== {path} ===")
        for level, name, detail in results:
            print(f"[{level}] {name}：{detail}")
        print(f"结果：{'FAIL（交付前先补齐）' if has_fail else 'PASS'}")
    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
