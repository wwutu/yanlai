extends RefCounted

const SAVE_PATH := "user://save/life_seed.dat"

const TOTAL_REGIONS := 8
const FIRST_THRESHOLD := 3.0
const LAST_THRESHOLD := 95.0

const ADJACENCY := {
	0: [2],
	1: [2],
	2: [0, 1, 3, 7],
	3: [2, 4, 5, 6, 7],
	4: [3],
	5: [3],
	6: [3],
	7: [2, 3],
}

var seed_value: int = 0
var region_order: Array = []
var region_thresholds: Array = []
var region_colors: Array = []


func _init() -> void:
	if not _load():
		_generate()
		_save()


func get_reveal_alpha(region_idx: int, growth: float) -> float:
	var order_pos := region_order.find(region_idx)
	if order_pos == -1:
		return 0.0
	var threshold: float = region_thresholds[order_pos]
	if growth < threshold:
		return 0.0
	var span := LAST_THRESHOLD - threshold
	if span <= 0.0:
		return 1.0
	return clampf((growth - threshold) / span, 0.0, 1.0)


func get_region_color(region_idx: int) -> Color:
	if region_idx < 0 or region_idx >= region_colors.size():
		return Color.WHITE
	return region_colors[region_idx]


func _generate() -> void:
	seed_value = randi()
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_value

	var origin := rng.randi_range(0, TOTAL_REGIONS - 1)
	region_order = _bfs_order(origin, rng)

	region_thresholds = []
	for i in range(TOTAL_REGIONS):
		var t := FIRST_THRESHOLD + (float(i) / float(TOTAL_REGIONS - 1)) * (LAST_THRESHOLD - FIRST_THRESHOLD)
		region_thresholds.append(t)

	var palette := [
		Color(0.85, 0.60, 0.35),
		Color(0.78, 0.62, 0.44),
		Color(0.90, 0.75, 0.48),
		Color(0.68, 0.48, 0.32),
		Color(0.92, 0.82, 0.62),
		Color(0.72, 0.54, 0.38),
		Color(0.80, 0.55, 0.30),
		Color(0.88, 0.70, 0.50),
	]

	region_colors = []
	for i in range(TOTAL_REGIONS):
		var idx := rng.randi_range(0, palette.size() - 1)
		region_colors.append(palette[idx])


func _bfs_order(origin: int, rng: RandomNumberGenerator) -> Array:
	var visited := {}
	var queue := [origin]
	visited[origin] = true
	var order: Array = []

	while queue.size() > 0:
		var current: int = queue.pop_front()
		order.append(current)

		var neighbors: Array = ADJACENCY.get(current, []).duplicate()
		_shuffle(neighbors, rng)

		for neighbor in neighbors:
			if not visited.has(neighbor):
				visited[neighbor] = true
				queue.append(neighbor)

	return order


func _shuffle(arr: Array, rng: RandomNumberGenerator) -> void:
	for i in range(arr.size() - 1, 0, -1):
		var j := rng.randi_range(0, i)
		var tmp = arr[i]
		arr[i] = arr[j]
		arr[j] = tmp


func _save() -> void:
	var dir := DirAccess.open("user://")
	if dir:
		if not dir.dir_exists("save"):
			dir.make_dir("save")
		var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
		if file:
			file.store_var({
				"seed_value": seed_value,
				"region_order": region_order,
				"region_thresholds": region_thresholds,
				"region_colors": region_colors,
			})


func _load() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not file:
		return false
	var data = file.get_var()
	if data == null:
		return false
	seed_value = data.get("seed_value", 0)
	region_order = data.get("region_order", [])
	region_thresholds = data.get("region_thresholds", [])
	region_colors = data.get("region_colors", [])
	return region_order.size() == TOTAL_REGIONS
