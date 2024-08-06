@tool
extends Node3D

@export var multimeshInstance: MultiMeshInstance3D
@export var pages: int

@export_category("Debug")
@export var instance: bool:
	set(value):
		if not Engine.is_editor_hint(): return
		instance_pages()

var page_size = Vector3(1, 0.0005, 1)
var multimesh: MultiMesh


func _ready() -> void:
	multimesh = multimeshInstance.multimesh
	instance_pages()


func instance_pages() -> void:
	multimesh.instance_count = pages
	(multimesh.mesh as BoxMesh).size = page_size
	
	for i in range(pages):
		var pos = Transform3D()
		var y = i * page_size.y
		pos = pos.translated(Vector3(0, y, 0))
		multimesh.set_instance_transform(i, pos)
	
	print("Instanced " + str(pages) + " pages")
