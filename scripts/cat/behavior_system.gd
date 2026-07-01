extends Node

const CatBrainScript := preload("res://scripts/cat/cat_brain.gd")
const CatBehaviorScript := preload("res://scripts/cat/cat_behavior.gd")
const CONFIG_PATH := "res://config/cat_behaviors.cfg"

var current_behavior_id := "idle"
var current_behavior_title := "Idle"
var behavior_elapsed := 0.0
var behavior_duration := 1.0

var _brain := CatBrainScript.new()
var _behaviors: Array = []
var _rng := RandomNumberGenerator.new()
var _previous_behavior_id := ""

var _is_settling := false
var _settle_elapsed := 0.0
var _settle_duration := 0.8
var _settle_min := 0.5
var _settle_max := 1.5

var _interaction_system: Node = null
var _pet_acknowledged := false
var _pet_acknowledge_timer := 0.0
const PET_ACKNOWLEDGE_DURATION := 0.4


func _ready() -> void:
	_rng.randomize()
	_behaviors = [
		CatBehaviorScript.new("idle", "Idle"),
		CatBehaviorScript.new("walk", "Walk"),
		CatBehaviorScript.new("sit", "Sit"),
		CatBehaviorScript.new("sleep", "Sleep"),
	]
	_configure_behaviors()
	_start_behavior(_find_behavior("idle"))
	_connect_interaction()


func _process(delta: float) -> void:
	_update_pet_acknowledge(delta)
	if _is_settling:
		_settle_elapsed += maxf(0.0, delta)
		if _settle_elapsed >= _settle_duration:
			_is_settling = false
			_settle_elapsed = 0.0
			_choose_next_behavior()
	else:
		behavior_elapsed += maxf(0.0, delta)
		if behavior_elapsed >= behavior_duration:
			_begin_settle()


func get_current_behavior_id() -> String:
	return current_behavior_id


func get_behavior_elapsed() -> float:
	return behavior_elapsed


func get_behavior_duration() -> float:
	return behavior_duration


func is_settling() -> bool:
	return _is_settling


func is_pet_acknowledged() -> bool:
	return _pet_acknowledged


func _update_pet_acknowledge(delta: float) -> void:
	if _pet_acknowledged:
		_pet_acknowledge_timer -= delta
		if _pet_acknowledge_timer <= 0.0:
			_pet_acknowledged = false


func _begin_settle() -> void:
	_is_settling = true
	_settle_elapsed = 0.0
	_settle_duration = _rng.randf_range(_settle_min, _settle_max)


func _choose_next_behavior() -> void:
	var context := {
		"previous_behavior_id": _previous_behavior_id,
	}
	var next_behavior := _brain.choose_next_behavior(_behaviors, context, _rng)
	_start_behavior(next_behavior)


func _start_behavior(behavior: RefCounted) -> void:
	if behavior == null:
		return
	_previous_behavior_id = current_behavior_id
	current_behavior_id = behavior.id
	current_behavior_title = behavior.title
	behavior_elapsed = 0.0
	behavior_duration = behavior.sample_duration(_rng)


func _find_behavior(behavior_id: String) -> RefCounted:
	for behavior in _behaviors:
		if behavior.id == behavior_id:
			return behavior
	return null


func _configure_behaviors() -> void:
	var config := ConfigFile.new()
	var error := config.load(CONFIG_PATH)
	if error != OK:
		push_warning("Could not load cat behavior config: %s" % CONFIG_PATH)
		return

	for behavior in _behaviors:
		behavior.configure(config)

	_settle_min = float(config.get_value("settle", "min_duration", _settle_min))
	_settle_max = float(config.get_value("settle", "max_duration", _settle_max))


func _connect_interaction() -> void:
	_interaction_system = get_node_or_null("../InteractionSystem")
	if _interaction_system and _interaction_system.has_signal("interaction_requested"):
		_interaction_system.interaction_requested.connect(_on_interaction_requested)


func _on_interaction_requested(type: String, position: Vector2, target: String) -> void:
	if type == "pet":
		_handle_pet()


func _handle_pet() -> void:
	match current_behavior_id:
		"idle", "sit":
			_pet_acknowledged = true
			_pet_acknowledge_timer = PET_ACKNOWLEDGE_DURATION
		"sleep":
			pass
		"walk":
			pass
