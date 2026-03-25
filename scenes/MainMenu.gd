extends Control
# ============================================================
# 主菜单场景
# 游戏入口界面，包含新游戏、继续游戏、卡牌图鉴、设置等按钮
# ============================================================

@onready var btn_new = $CenterContainer/VBox/BtnNewGame
@onready var btn_continue = $CenterContainer/VBox/BtnContinue
@onready var btn_cards = $CenterContainer/VBox/BtnCards
@onready var btn_settings = $CenterContainer/VBox/BtnSettings
@onready var btn_check = $CenterContainer/VBox/BtnCheck
@onready var btn_full_chain = $CenterContainer/VBox/BtnFullChain
@onready var btn_settlement_preview = $CenterContainer/VBox/BtnSettlementPreview
@onready var feedback = $CenterContainer/VBox/Feedback

const SETTLEMENT_MODAL_SCENE := preload("res://scenes/MysteryBroadsheetModal.tscn")

var settlement_modal: Control

func _ready():
	Globals.log("MainMenu", "_ready() called")

	btn_new.pressed.connect(_on_goto_full_chain)
	btn_continue.pressed.connect(_on_button_pressed.bind("继续游戏"))
	btn_cards.pressed.connect(_on_goto_cards)
	btn_settings.pressed.connect(_on_button_pressed.bind("设置"))
	btn_check.pressed.connect(_on_goto_check)
	btn_full_chain.pressed.connect(_on_goto_full_chain)
	btn_settlement_preview.pressed.connect(_on_open_settlement_preview)
	_feedback("新游戏和完整周循环都会进入最新 Godot 周循环原型")

func _on_button_pressed(name: String):
	Globals.log("MainMenu", "button pressed: %s" % name)
	_feedback("你点击了「%s」" % name)

func _on_goto_cards():
	var path := str(Globals.scene_paths.get("card_collection", "res://scenes/CardCollection.tscn"))
	Globals.log("MainMenu", "_on_goto_cards() -> %s" % path)
	var err = get_tree().change_scene_to_file(path)
	if err != OK:
		Globals.log_error("MainMenu", "change_scene failed: %d" % err)

func _on_goto_check():
	var path := str(Globals.scene_paths.get("event_check", "res://scenes/EventCheck.tscn"))
	Globals.log("MainMenu", "_on_goto_check() -> %s" % path)
	var err = get_tree().change_scene_to_file(path)
	if err != OK:
		Globals.log_error("MainMenu", "change_scene failed: %d" % err)

func _on_goto_full_chain():
	var path := str(Globals.scene_paths.get("full_chain", "res://scenes/FullChainGame.tscn"))
	Globals.log("MainMenu", "_on_goto_full_chain() -> %s" % path)
	var err = get_tree().change_scene_to_file(path)
	if err != OK:
		Globals.log_error("MainMenu", "change_scene failed: %d" % err)

func _on_open_settlement_preview():
	var modal = _ensure_settlement_modal()
	if modal != null and modal.has_method("open_modal"):
		modal.call("open_modal")
		_feedback("神秘特刊正在展开")

func _ensure_settlement_modal() -> Control:
	if is_instance_valid(settlement_modal):
		return settlement_modal

	settlement_modal = SETTLEMENT_MODAL_SCENE.instantiate()
	add_child(settlement_modal)
	if settlement_modal.has_signal("closed"):
		settlement_modal.connect("closed", Callable(self, "_on_settlement_preview_closed"))
	return settlement_modal

func _on_settlement_preview_closed():
	_feedback("神秘特刊已经合上")

func _feedback(text: String):
	Globals.log("MainMenu", "feedback: %s" % text)
	feedback.text = text
	var tween = create_tween()
	feedback.modulate.a = 0.0
	tween.tween_property(feedback, "modulate:a", 1.0, 0.3)
