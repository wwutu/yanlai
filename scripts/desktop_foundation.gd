extends Node2D

const WINDOW_SIZE := Vector2i(220, 220)
const SCREEN_MARGIN := Vector2i(32, 48)
const SINGLE_INSTANCE_PORT := 47147

var _single_instance_server := TCPServer.new()
var _dragging := false
var _drag_offset := Vector2i.ZERO


func _ready() -> void:
	if not _claim_single_instance():
		_notify_existing_instance()
		get_tree().quit()
		return

	_setup_window()
	_place_window_bottom_right()
	set_process(true)


func _process(_delta: float) -> void:
	_poll_single_instance_activation()
	_update_drag()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			_start_drag()
		else:
			_dragging = false


func _claim_single_instance() -> bool:
	return _single_instance_server.listen(SINGLE_INSTANCE_PORT, "127.0.0.1") == OK


func _notify_existing_instance() -> void:
	var client := StreamPeerTCP.new()
	if client.connect_to_host("127.0.0.1", SINGLE_INSTANCE_PORT) != OK:
		return

	var started_at := Time.get_ticks_msec()
	while client.get_status() == StreamPeerTCP.STATUS_CONNECTING and Time.get_ticks_msec() - started_at < 500:
		client.poll()
		OS.delay_msec(10)

	if client.get_status() == StreamPeerTCP.STATUS_CONNECTED:
		client.put_utf8_string("activate")
		client.disconnect_from_host()


func _poll_single_instance_activation() -> void:
	if not _single_instance_server.is_connection_available():
		return

	var peer := _single_instance_server.take_connection()
	if peer:
		DisplayServer.window_move_to_foreground()
		peer.disconnect_from_host()


func _setup_window() -> void:
	get_window().size = WINDOW_SIZE
	get_window().transparent = true
	get_window().transparent_bg = true
	get_tree().root.transparent = true
	get_viewport().transparent_bg = true
	get_tree().root.transparent_bg = true
	RenderingServer.set_default_clear_color(Color(0.0, 0.0, 0.0, 0.0))

	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_TRANSPARENT, true)
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_BORDERLESS, true)
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_RESIZE_DISABLED, true)


func _place_window_bottom_right() -> void:
	var usable_rect := DisplayServer.screen_get_usable_rect()
	var target_position := usable_rect.position + usable_rect.size - WINDOW_SIZE - SCREEN_MARGIN
	DisplayServer.window_set_position(target_position)


func _start_drag() -> void:
	_dragging = true
	_drag_offset = DisplayServer.mouse_get_position() - DisplayServer.window_get_position()


func _update_drag() -> void:
	if not _dragging:
		return

	if not Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		_dragging = false
		return

	DisplayServer.window_set_position(DisplayServer.mouse_get_position() - _drag_offset)
