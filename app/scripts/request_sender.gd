extends Node


@export var le_request : LineEdit
@export var btn_request : Button
@export var rtl_raw_result : RichTextLabel
@export var rtl_result : RichTextLabel


func _ready() -> void:
	btn_request.pressed.connect(request)
	btn_request.pressed.connect(func(): set_result(""))


func request() -> void:
	var url = le_request.text
	
	var http = HTTPRequest.new()
	http.use_threads = true
	add_child(http)
	
	var err = http.request(url, [], HTTPClient.METHOD_GET)
	if err != OK: set_result("Cannot create http request"); return
	
	var result = await http.request_completed
	err = result[0]
	var code = result[1]
	var body = result[3] as PackedByteArray
	if err != OK: set_result("Request failed with code: " + str(code)); return
	
	remove_child(http)
	
	set_result(body.get_string_from_utf8())


func set_result(result : String) -> void:
	rtl_raw_result.text = result
	rtl_result.text = result
