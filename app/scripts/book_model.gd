@tool
extends Node3D

@export var root: Node3D
@export var meshInstance: MeshInstance3D
@export var pages: int

@export_category("Debug")
@export var instance: bool:
	set(value):
		if not Engine.is_editor_hint(): return
		instance_pages()

@export var clear: bool:
	set(value):
		if not Engine.is_editor_hint(): return
		clear_pages()

var page_size = Vector3(1, 0.0005, 1)


func _ready() -> void:
	instance_pages()


func instance_pages() -> void:
	(meshInstance.mesh as BoxMesh).size = page_size
	
	# Clear prev
	clear_pages()
	
	# Create new
	for i in range(pages):
		var page = MeshInstance3D.new()
		page.mesh = meshInstance.mesh
		page.material_override = meshInstance.material_override
		
		var page_transform = Transform3D()
		var y = i * page_size.y
		page_transform = page_transform.translated(Vector3(0, y, 0))
		
		page.transform = page_transform
		
		root.add_child(page)
	
	print("Instanced " + str(pages) + " pages")


func clear_pages() -> void:
	for page in root.get_children():
		page.queue_free()
