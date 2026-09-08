"""Astra UI 工作流的离线回归；不调用模型 API、不改游戏资产。"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


images = module("astra_test_image_helper", "skills/openrouter-image-gen/scripts/openrouter_image_gen.py")
manifest = module("astra_test_manifest", "scripts/check_delivery_manifest.py")


class PromptPlanning(unittest.TestCase):
    def test_ui_defaults_do_not_ban_visual_language(self):
        terms = images.build_negative_constraints("ui-screen", "opaque", [])
        for banned in ("frame border", "presentation mockup", "ui chrome", "drop shadow", "extra fingers", "oversaturated colors"):
            self.assertNotIn(banned, terms)

    def test_anatomy_is_not_added_to_map(self):
        terms = " ".join(images.build_negative_constraints("background", "opaque", []))
        self.assertNotIn("anatomy", terms)
        self.assertNotIn("limbs", terms)

    def test_transparency_is_scoped_and_shadow_is_allowed(self):
        terms = images.build_negative_constraints("prop", "transparent", [])
        self.assertIn("unintended opaque background", terms)
        self.assertNotIn("drop shadow", terms)

    def test_explicit_negatives_can_replace_defaults(self):
        terms = images.build_negative_constraints("ui-screen", "opaque", ["Dust", "dust", " "], use_defaults=False)
        self.assertEqual(terms, ["Dust"])

    def test_empty_negative_clause_not_emitted(self):
        result = images.build_prompt("palette study", "ui-screen", "opaque", [], [])
        self.assertNotIn("Avoid:", result)
        self.assertNotIn("production-ready", result)

    def test_cli_switch_reaches_planner(self):
        args = images.build_parser().parse_args(["generate", "--prompt", "painted clip", "--asset-type", "prop",
                                                 "--background", "transparent", "--no-default-negatives",
                                                 "--negative", "dust"])
        plan = images.plan_request(args)
        self.assertEqual(plan.negative_constraints, ["dust"])
        self.assertEqual(plan.model, "openai/gpt-5-image")
        self.assertEqual(plan.background, "transparent")

    def test_opaque_requests_still_do_not_call_external_helper(self):
        with self.assertRaises(images.ValidationError):
            images.choose_model("opaque", "auto")

    def test_transparent_jpeg_rejected(self):
        with self.assertRaises(images.ValidationError):
            images.validate_gpt_image_request("1024x1024", None, "transparent", "jpeg", "medium")

    def test_invalid_count_rejected(self):
        with self.assertRaises(images.ValidationError):
            images.validate_count(0)


class RecordLint(unittest.TestCase):
    def lint(self, body):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.md"
            path.write_text(body, encoding="utf-8")
            return manifest.check_file(path, manifest.load_artifact_types())

    def test_concept_does_not_require_status_or_named_reviewer(self):
        _, failed = self.lint("- 产物类型：visual_style_reference\n- 变更范围：配色\n- 验证证据：原图与结果目视对比\n- 未验证边界：未接入运行时\n")
        self.assertFalse(failed)

    def test_missing_scope_is_reported(self):
        _, failed = self.lint("- 产物类型：visual_style_reference\n- 验证证据：待补\n- 未验证边界：运行时\n")
        self.assertTrue(failed)

    def test_runtime_cannot_claim_no_evidence(self):
        _, failed = self.lint("- 产物类型：runtime_state_preview\n- 变更范围：状态\n- 验证证据：未验证\n- 未验证边界：全量回归\n")
        self.assertTrue(failed)

    def test_unknown_artifact_is_reported(self):
        _, failed = self.lint("- 产物类型：invented\n- 变更范围：配色\n- 验证证据：无\n- 未验证边界：全部\n")
        self.assertTrue(failed)


class SkillConfiguration(unittest.TestCase):
    def test_ui_roles_inherit_model_without_widening_permissions(self):
        mapping = {"ui-designer": "ui-designer", "ux-laoge": "ux-diagnosis",
                   "angus-art-director": "angus-art-director",
                   "angus-character-pixel-director": "angus-character-pixel-director",
                   "steam-indie-appraiser": "steam-indie-appraiser"}
        for shell, skill in mapping.items():
            with self.subTest(role=shell):
                config = tomllib.loads((ROOT / ".codex/agents" / (shell + ".toml")).read_text(encoding="utf-8-sig"))
                self.assertEqual(config["sandbox_mode"], "read-only")
                self.assertNotIn("model", config)
                self.assertNotIn("model_reasoning_effort", config)
                self.assertIn(f"skills/{skill}/SKILL.md", config["developer_instructions"])

    def test_kb_metadata_matches_existing_skill(self):
        for suffix in ("risks", "cross-page", "symptoms", "principles", "templates"):
            folder = ROOT / "skills" / ("ux-kb-" + suffix)
            metadata = json.loads((folder / "skill_meta.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["name"], folder.name)
            self.assertEqual(metadata["source"], "SKILL.md")
            self.assertTrue((folder / metadata["source"]).is_file())

    def test_known_artifact_ids_remain_compatible(self):
        ids = manifest.load_artifact_types()
        self.assertEqual(len(ids), len(set(ids)))
        for required in ("visual_style_reference", "filled_state_text_mock", "runtime_state_preview",
                         "production_candidate", "component_class_contract", "isolated_technical_probe"):
            self.assertIn(required, ids)


if __name__ == "__main__":
    unittest.main()
