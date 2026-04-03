extends Control

@onready var btn_new = $CenterContainer/VBox/BtnNewGame
@onready var btn_continue = $CenterContainer/VBox/BtnContinue
@onready var btn_cards = $CenterContainer/VBox/BtnCards
@onready var btn_settings = $CenterContainer/VBox/BtnSettings
@onready var btn_check = $CenterContainer/VBox/BtnCheck
@onready var btn_full_chain = $CenterContainer/VBox/BtnFullChain
@onready var btn_settlement_preview = $CenterContainer/VBox/BtnSettlementPreview
@onready var feedback = $CenterContainer/VBox/Feedback
@onready var btn_psd_ui_toggle = $SideDock/Margin/VBox/BtnPsdUiToggle
@onready var psd_preview_panel = $PsdPreviewPanel
@onready var psd_preview_viewport = $PsdPreviewPanel/Margin/VBox/PsdPreviewViewport
@onready var psd_preview_mount = $PsdPreviewPanel/Margin/VBox/PsdPreviewViewport/PsdPreviewMount

const SETTLEMENT_MODAL_SCENE_PATH := "res://scenes/MysteryBroadsheetModal.tscn"
const PSD_UI_PREVIEW_SCENE_PATH := "res://scenes/ui/imported/GoldenUiUi.tscn"
const PSD_UI_PREVIEW_SIZE := Vector2(606.0, 744.0)

var settlement_modal: Control
var psd_ui_preview: Control

func _ready():
	Globals.log("MainMenu", "_ready() called")

	btn_new.pressed.connect(_on_goto_full_chain)
	btn_continue.pressed.connect(_on_button_pressed.bind("Continue"))
	btn_cards.pressed.connect(_on_goto_cards)
	btn_settings.pressed.connect(_on_button_pressed.bind("Settings"))
	btn_check.pressed.connect(_on_goto_check)
	btn_full_chain.pressed.connect(_on_goto_full_chain)
	btn_settlement_preview.pressed.connect(_on_open_settlement_preview)
	btn_psd_ui_toggle.pressed.connect(_on_toggle_psd_ui_preview)
	psd_preview_viewport.resized.connect(_layout_psd_ui_preview)

	psd_preview_panel.visible = false
	btn_psd_ui_toggle.text = "Show PSD UI"
	_feedback("Use UI LAB to preview the imported PSD scene inside the main menu.")

func _on_button_pressed(name: String):
	Globals.log("MainMenu", "button pressed: %s" % name)
	_feedback("%s is not wired yet." % name)

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
		_feedback("Settlement broadsheet preview opened.")

func _ensure_settlement_modal() -> Control:
	if is_instance_valid(settlement_modal):
		return settlement_modal

	var packed_scene: PackedScene = load(SETTLEMENT_MODAL_SCENE_PATH) as PackedScene
	if packed_scene == null:
		Globals.log_error("MainMenu", "failed to load settlement modal scene")
		_feedback("Settlement preview failed to load.")
		return null

	settlement_modal = packed_scene.instantiate()
	add_child(settlement_modal)
	if settlement_modal.has_signal("closed"):
		settlement_modal.connect("closed", Callable(self, "_on_settlement_preview_closed"))
	return settlement_modal

func _on_settlement_preview_closed():
	_feedback("Settlement broadsheet preview closed.")

func _on_toggle_psd_ui_preview():
	var next_visible: bool = not psd_preview_panel.visible
	psd_preview_panel.visible = next_visible
	btn_psd_ui_toggle.text = "Hide PSD UI" if next_visible else "Show PSD UI"

	if next_visible:
		_ensure_psd_ui_preview()
		call_deferred("_layout_psd_ui_preview")
		_feedback("PSD UI preview is now visible on the right.")
	else:
		_feedback("PSD UI preview hidden.")

func _ensure_psd_ui_preview() -> Control:
	if is_instance_valid(psd_ui_preview):
		return psd_ui_preview

	var packed_scene: PackedScene = load(PSD_UI_PREVIEW_SCENE_PATH) as PackedScene
	if packed_scene == null:
		Globals.log_error("MainMenu", "failed to load PSD UI preview scene")
		_feedback("PSD UI preview failed to load. Open the imported scene in Godot to inspect imports.")
		psd_preview_panel.visible = false
		btn_psd_ui_toggle.text = "Show PSD UI"
		return null

	psd_ui_preview = packed_scene.instantiate()
	psd_ui_preview.mouse_filter = Control.MOUSE_FILTER_IGNORE
	psd_preview_mount.add_child(psd_ui_preview)
	return psd_ui_preview

func _layout_psd_ui_preview():
	if not psd_preview_panel.visible:
		return
	if not is_instance_valid(psd_ui_preview):
		return

	var available: Vector2 = psd_preview_viewport.size
	if available.x <= 0.0 or available.y <= 0.0:
		return

	var scale_factor: float = min(available.x / PSD_UI_PREVIEW_SIZE.x, available.y / PSD_UI_PREVIEW_SIZE.y)
	scale_factor = clamp(scale_factor, 0.01, 1.0)
	psd_ui_preview.scale = Vector2.ONE * scale_factor

	var scaled_size: Vector2 = PSD_UI_PREVIEW_SIZE * scale_factor
	psd_ui_preview.position = (available - scaled_size) * 0.5

func _feedback(text: String):
	Globals.log("MainMenu", "feedback: %s" % text)
	feedback.text = text
	var tween = create_tween()
	feedback.modulate.a = 0.0
	tween.tween_property(feedback, "modulate:a", 1.0, 0.3)
