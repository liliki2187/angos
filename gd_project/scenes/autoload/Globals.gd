extends Node
# ============================================================
# 全局变量与配置（AutoLoad 单例）
# 所有跨场景共享的常量、配置、状态集中在此管理
# ============================================================

# === 调试开关：release 时设为 false ===
var debug := true

# === 界面颜色主题 ===
var theme_colors := {
	"bg_dark": Color(0.08, 0.06, 0.1, 1),
	"bg_card": Color(0.15, 0.13, 0.2, 1),
	"bg_panel": Color(0.12, 0.1, 0.16, 1),
	"bg_image": Color(0.1, 0.08, 0.14, 1),
	"text_primary": Color(0.9, 0.85, 0.95),
	"text_secondary": Color(0.6, 0.55, 0.65),
	"text_dim": Color(0.75, 0.7, 0.8),
	"border": Color(0.3, 0.25, 0.4, 0.5),
	"border_detail": Color(0.4, 0.35, 0.5, 0.8),
	"dimmer": Color(0, 0, 0, 0.5),
}

# === 卡牌配置 ===
var card := {
	"width": 100,
	"height": 200,
	"count": 100,
	"columns": 5,
}

# === 场景路径 ===
var scene_paths := {
	"main_menu": "res://scenes/ui/main_menu/MainMenu.tscn",
	"card_collection": "res://scenes/gameplay/card_collection/CardCollection.tscn",
	"event_check": "res://scenes/gameplay/event_check/EventCheck.tscn",
	"weekly_run": "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn",
	"full_chain": "res://scenes/gameplay/weekly_run/WeeklyRunGame.tscn",
}

# === 日志工具函数 ===

func log(scene: String, msg: String):
	"""统一日志输出，格式：[场景名] 描述"""
	if debug:
		print("[%s] %s" % [scene, msg])

func log_error(scene: String, msg: String):
	"""统一错误输出"""
	push_error("[%s] ERROR: %s" % [scene, msg])
