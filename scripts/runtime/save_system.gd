extends Node

const SAVE_PATH := "user://save/runtime_state.dat"
const LEGACY_GROWTH_PATH := "user://save/growth.dat"

var growth: float = 0.0
var desktop_time: float = 0.0
var last_exit_time: int = 0


func _ready() -> void:
	_ensure_save_dir()
	load_facts()


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST or what == NOTIFICATION_PREDELETE:
		last_exit_time = Time.get_unix_time_from_system()
		save_facts()


func load_facts() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
		if file:
			var data = file.get_var()
			if data is Dictionary:
				growth = float(data.get("growth", 0.0))
				desktop_time = float(data.get("desktop_time", 0.0))
				last_exit_time = int(data.get("last_exit_time", 0))
				return

	_load_legacy_growth()


func save_facts() -> void:
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_var({
			"growth": growth,
			"desktop_time": desktop_time,
			"last_exit_time": last_exit_time,
		})


func set_runtime_facts(next_growth: float, next_desktop_time: float) -> void:
	growth = next_growth
	desktop_time = next_desktop_time


func _ensure_save_dir() -> void:
	var dir := DirAccess.open("user://")
	if dir and not dir.dir_exists("save"):
		dir.make_dir("save")


func _load_legacy_growth() -> void:
	if not FileAccess.file_exists(LEGACY_GROWTH_PATH):
		return

	var file := FileAccess.open(LEGACY_GROWTH_PATH, FileAccess.READ)
	if not file:
		return

	var data = file.get_var()
	if data is Dictionary:
		growth = float(data.get("growth_value", 0.0))

