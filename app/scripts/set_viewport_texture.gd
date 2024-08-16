@tool
extends MeshInstance3D

@export var viewport: Viewport

@export_category("Debug")
@export var set_tex: bool:
	set(value):
		if not Engine.is_editor_hint(): return
		set_texture()


func _ready() -> void:
	set_texture()


func set_texture() -> void:
	(material_override as StandardMaterial3D).albedo_texture = viewport.get_texture()
	print("viewport texture is set")
