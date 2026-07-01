extends Node2D

const WINDOW_SIZE := Vector2(220.0, 220.0)
const CONFIG_PATH := "res://config/cat_behaviors.cfg"
const DEBUG_CONFIG_PATH := "res://config/debug.cfg"
const ART_PREVIEW_CONFIG_PATH := "res://config/art_preview.cfg"
const DEBUG_BACKGROUND_COLOR := Color(0.0, 0.0, 0.0, 0.35)
const INFO_BG_COLOR := Color(0.0, 0.0, 0.0, 0.65)
const INFO_TEXT_COLOR := Color(0.95, 0.95, 0.95, 1.0)
const SPRITE_TARGET_SIZE := Vector2(160.0, 130.0)
const SPRITE_BASE_POSITION := Vector2(30.0, 62.0)

const VALIDATION_SPRITE_PATHS := {
	"idle": "res://assets/validation/sprites/cat/idle.png",
	"walk": "res://assets/validation/sprites/cat/walk.png",
	"sit": "res://assets/validation/sprites/cat/sit.png",
	"sleep": "res://assets/validation/sprites/cat/sleep.png",
}

const PRODUCTION_FRAME_PATHS := {
	"idle": [
		"res://assets/characters/cat/sprites/idle/frame_01.png",
		"res://assets/characters/cat/sprites/idle/frame_02.png",
	],
	"walk": [
		"res://assets/characters/cat/sprites/walk/frame_01.png",
	],
	"sit": [
		"res://assets/characters/cat/sprites/sit/frame_01.png",
	],
	"sleep": [
		"res://assets/characters/cat/sprites/sleep/frame_01.png",
	],
}

const ASSET_CONFIG_PATH := "res://config/gameplay.cfg"

var _look_direction := 0.0
var _transition_duration := 0.55
var _breath_period := 4.8
var _sit_breath_amount := 1.4
var _sleep_breath_amount := 0.8
var _walk_body_sway := 1.2
var _pause_settle_amount := 0.35
var _show_debug_background := false

var _behavior_system: Node = null
var _growth_system: Node = null
var _reveal_system: Node = null
var _sprite_frames := {}
var _show_growth_info := false
var _pet_glow_alpha := 0.0
var _asset_source := "validation"
var _idle_fps := 1.0
var _art_preview_enabled := false
var _art_preview_frame_dir := ""
var _art_preview_fps := 8.0
var _art_preview_frames := []


func _ready() -> void:
	_configure_motion()
	_configure_debug_visuals()
	_configure_asset_source()
	_load_cat_sprites()
	_configure_art_preview()
	_load_art_preview_frames()
	_behavior_system = get_node_or_null("../BehaviorSystem")
	_growth_system = get_node_or_null("../GrowthSystem")
	_reveal_system = get_node_or_null("../RevealSystem")


func _process(delta: float) -> void:
	_update_behavior_expression(delta)
	_update_pet_glow(delta)
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
		_show_growth_info = !_show_growth_info
		queue_redraw()


func _draw() -> void:
	if _show_debug_background:
		draw_rect(Rect2(Vector2.ZERO, WINDOW_SIZE), DEBUG_BACKGROUND_COLOR, true)

	_draw_validation_cat()

	if _show_growth_info:
		_draw_growth_info()


func _draw_validation_cat() -> void:
	var texture := _get_current_texture()
	if texture == null:
		return

	var draw_rect := _get_sprite_rect(texture)
	var reveal_amount := _get_reveal_amount()
	var full_color_alpha := lerpf(0.18, 1.0, reveal_amount)
	var soft_shape_alpha := lerpf(0.38, 0.08, reveal_amount)
	var warm_reveal_alpha := smoothstep(0.0, 1.0, reveal_amount) * 0.16

	draw_texture_rect(texture, draw_rect, false, Color(0.68, 0.66, 0.62, soft_shape_alpha))
	draw_texture_rect(texture, draw_rect, false, Color(1.0, 0.96, 0.88, full_color_alpha))
	draw_texture_rect(texture, draw_rect, false, Color(1.0, 0.78, 0.45, warm_reveal_alpha))

	if _pet_glow_alpha > 0.01:
		draw_texture_rect(texture, draw_rect, false, Color(1.0, 0.85, 0.6, _pet_glow_alpha))


func _get_reveal_amount() -> float:
	if _reveal_system == null or not _reveal_system.has_method("get_reveal_percentage"):
		return 1.0
	return clampf(_reveal_system.get_reveal_percentage() / 100.0, 0.0, 1.0)


func _draw_growth_info() -> void:
	var growth_pct := 0
	if _growth_system:
		growth_pct = int(_growth_system.get_final_growth())
	var text := "%d%%" % growth_pct
	var font := ThemeDB.fallback_font
	var font_size := 11
	var text_size := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size)
	var padding := Vector2(6.0, 3.0)
	var bg_size := text_size + padding * 2.0
	var bg_pos := Vector2((WINDOW_SIZE.x - bg_size.x) * 0.5, WINDOW_SIZE.y - bg_size.y - 6.0)
	draw_rect(Rect2(bg_pos, bg_size), INFO_BG_COLOR, true)
	draw_string(font, bg_pos + padding, text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, INFO_TEXT_COLOR)


func _configure_motion() -> void:
	var config := ConfigFile.new()
	var error := config.load(CONFIG_PATH)
	if error != OK:
		push_warning("Could not load cat behavior config: %s" % CONFIG_PATH)
		return

	_transition_duration = float(config.get_value("motion", "transition_duration", _transition_duration))
	_breath_period = float(config.get_value("motion", "breath_period", _breath_period))
	_sit_breath_amount = float(config.get_value("motion", "sit_breath_amount", _sit_breath_amount))
	_sleep_breath_amount = float(config.get_value("motion", "sleep_breath_amount", _sleep_breath_amount))
	_walk_body_sway = float(config.get_value("motion", "walk_body_sway", _walk_body_sway))
	_pause_settle_amount = float(config.get_value("motion", "pause_settle_amount", _pause_settle_amount))


func _configure_debug_visuals() -> void:
	var config := ConfigFile.new()
	var error := config.load(DEBUG_CONFIG_PATH)
	if error != OK:
		return

	_show_debug_background = bool(config.get_value("visual", "show_debug_background", _show_debug_background))


func _configure_asset_source() -> void:
	var config := ConfigFile.new()
	var error := config.load(ASSET_CONFIG_PATH)
	if error != OK:
		return

	_asset_source = str(config.get_value("assets", "source", _asset_source))
	_idle_fps = float(config.get_value("animation", "idle_fps", _idle_fps))


func _configure_art_preview() -> void:
	var config := ConfigFile.new()
	var error := config.load(ART_PREVIEW_CONFIG_PATH)
	if error != OK:
		return

	_art_preview_enabled = bool(config.get_value("preview", "enabled", _art_preview_enabled))
	_art_preview_frame_dir = str(config.get_value("preview", "frame_dir", _art_preview_frame_dir))
	_art_preview_fps = float(config.get_value("preview", "fps", _art_preview_fps))


func _get_current_behavior_id() -> String:
	if _art_preview_enabled and not _art_preview_frames.is_empty():
		return "idle"
	if _behavior_system and _behavior_system.has_method("get_current_behavior_id"):
		if _behavior_system.has_method("is_settling") and _behavior_system.is_settling():
			return "idle"
		return _behavior_system.get_current_behavior_id()
	return "idle"


func _get_behavior_elapsed() -> float:
	if _behavior_system and _behavior_system.has_method("get_behavior_elapsed"):
		return _behavior_system.get_behavior_elapsed()
	return 0.0


func _get_behavior_duration() -> float:
	if _behavior_system and _behavior_system.has_method("get_behavior_duration"):
		return _behavior_system.get_behavior_duration()
	return 1.0


func _update_behavior_expression(delta: float) -> void:
	var behavior_id := _get_current_behavior_id()

	match behavior_id:
		"walk":
			_look_direction = sin(_get_behavior_elapsed() * 1.8) * 0.35
		"sleep":
			_look_direction = lerpf(_look_direction, 0.0, minf(1.0, delta * 2.0))
		_:
			_look_direction = lerpf(_look_direction, 0.0, minf(1.0, delta * 1.5))


func _get_breath_offset() -> Vector2:
	var wave := sin(Time.get_ticks_msec() / 1000.0 / maxf(_breath_period, 0.1) * TAU)
	return Vector2(wave * _sit_breath_amount, -wave * _sit_breath_amount * 0.35)


func _get_sleep_breath_offset() -> Vector2:
	var wave := sin(Time.get_ticks_msec() / 1000.0 / maxf(_breath_period, 0.1) * TAU)
	return Vector2(wave * _sleep_breath_amount, -wave * _sleep_breath_amount * 0.25)


func _load_cat_sprites() -> void:
	for behavior_id in VALIDATION_SPRITE_PATHS.keys():
		var frames := []
		if _asset_source == "production":
			frames = _load_texture_frames(PRODUCTION_FRAME_PATHS.get(behavior_id, []))
		if frames.is_empty():
			frames = _load_texture_frames([VALIDATION_SPRITE_PATHS[behavior_id]])
		if frames.is_empty():
			push_warning("Could not load any cat sprite frames for behavior: %s" % behavior_id)
			continue
		_sprite_frames[behavior_id] = frames


func _load_art_preview_frames() -> void:
	_art_preview_frames.clear()
	if not _art_preview_enabled or _art_preview_frame_dir.is_empty():
		return

	var dir := DirAccess.open(_art_preview_frame_dir)
	if dir == null:
		push_warning("Could not open art preview frame directory: %s" % _art_preview_frame_dir)
		return

	var frame_paths := []
	dir.list_dir_begin()
	var file_name := dir.get_next()
	while file_name != "":
		if not dir.current_is_dir() and file_name.get_extension().to_lower() == "png":
			frame_paths.append(_art_preview_frame_dir.path_join(file_name))
		file_name = dir.get_next()
	dir.list_dir_end()

	frame_paths.sort()
	_art_preview_frames = _load_texture_frames(frame_paths)
	if _art_preview_frames.is_empty():
		push_warning("No art preview frames loaded from: %s" % _art_preview_frame_dir)


func _load_texture_frames(paths: Array) -> Array:
	var frames := []
	for path in paths:
		if not FileAccess.file_exists(str(path)):
			continue
		var image := Image.new()
		var error := image.load(str(path))
		if error != OK:
			continue
		frames.append(ImageTexture.create_from_image(image))
	return frames


func _get_current_texture() -> Texture2D:
	if _art_preview_enabled and not _art_preview_frames.is_empty():
		return _art_preview_frames[_get_preview_frame_index()]

	var behavior_id := _get_current_behavior_id()
	var frames: Array = _sprite_frames.get(behavior_id, [])
	if frames.is_empty():
		frames = _sprite_frames.get("idle", [])
	if frames.is_empty():
		return null
	return frames[_get_frame_index(behavior_id, frames.size())]


func _get_preview_frame_index() -> int:
	if _art_preview_frames.size() <= 1:
		return 0
	var frame := int(floor(Time.get_ticks_msec() / 1000.0 * maxf(_art_preview_fps, 0.01)))
	return frame % _art_preview_frames.size()


func _get_frame_index(behavior_id: String, frame_count: int) -> int:
	if frame_count <= 1:
		return 0
	var fps := _get_animation_fps(behavior_id)
	var frame := int(floor(Time.get_ticks_msec() / 1000.0 * maxf(fps, 0.01)))
	return frame % frame_count


func _get_animation_fps(behavior_id: String) -> float:
	match behavior_id:
		"idle":
			return _idle_fps
		_:
			return _idle_fps


func get_current_sprite_rect() -> Rect2:
	var texture := _get_current_texture()
	if texture == null:
		return Rect2()
	return _get_sprite_rect(texture)


func _get_sprite_rect(texture: Texture2D) -> Rect2:
	var source_size := texture.get_size()
	var scale := minf(SPRITE_TARGET_SIZE.x / source_size.x, SPRITE_TARGET_SIZE.y / source_size.y)
	var draw_size := source_size * scale
	var draw_position := SPRITE_BASE_POSITION + (SPRITE_TARGET_SIZE - draw_size) * 0.5
	draw_position += _get_behavior_draw_offset()
	return Rect2(draw_position, draw_size)


func _get_behavior_draw_offset() -> Vector2:
	var breath := _get_breath_offset()
	match _get_current_behavior_id():
		"walk":
			return Vector2(sin(_get_behavior_elapsed() * 4.0) * _walk_body_sway, breath.y)
		"sleep":
			return _get_sleep_breath_offset()
		"idle":
			return Vector2(0.0, _pause_settle_amount + breath.y)
		_:
			return breath


func _update_pet_glow(delta: float) -> void:
	var target_alpha := 0.0
	if _behavior_system and _behavior_system.has_method("is_pet_acknowledged"):
		if _behavior_system.is_pet_acknowledged():
			target_alpha = 0.12
	_pet_glow_alpha = lerpf(_pet_glow_alpha, target_alpha, minf(1.0, delta * 8.0))
