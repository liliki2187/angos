extends RefCounted
## 地区来稿是气氛内容，任务、权限和时间仍来自正式游戏 payload。
## 每地区只登记一张图片；左卡、大图和地图证据共享同一个 Texture2D。

const ASSET_DIR := "res://Assets/ui/angus_packaging/world_map/soft_columns_v1/"
const NEWS := {
	"us": {
		"photo": "us.png", "headline": "洗衣店里出现了一片海",
		"deck": "断电两小时后，潮线仍在三扇滚筒窗之间保持水平。\n店外道路干燥，最近海岸线在一千公里外。",
		"note": "先别\n按脱水。", "map_label": "北美", "anchor": Vector2(632, 366),
	},
	"east_asia": {
		"photo": "east_asia.png", "headline": "天文台在凌晨向北移动",
		"deck": "凌晨三点，整座天文台向北平移了五十米。\n值班员坚持所有仪器仍在原位。",
		"note": "请给天文台\n装里程表。", "map_label": "东亚", "anchor": Vector2(1012, 430),
	},
	"pacific": {
		"photo": "pacific.png", "headline": "深海电波正在重复呼号",
		"deck": "失联渔船的最后讯号来自海面千米以下。\n海面浮标却记录到同一组短波。",
		"note": "这次真的\n不是杂音。", "map_label": "太平洋", "anchor": Vector2(1028, 650),
	},
}
static var _textures: Dictionary = {}

static func get_news(region: Dictionary) -> Dictionary:
	var id := str(region.get("id", ""))
	var result: Dictionary = region.get("world_map_news", NEWS.get(id, {})).duplicate(true)
	if result.is_empty():
		result = {"photo": "", "headline": "等待这片地区的来稿", "deck": str(region.get("hint", "尚未收到地区新闻。")), "note": "给未知\n留一页。", "map_label": str(region.get("name", "地区"))}
	var file := str(result.get("photo", ""))
	result["source_path"] = ASSET_DIR + file if not file.is_empty() else ""
	result["texture"] = texture(str(result.source_path))
	return result

static func texture(path: String) -> Texture2D:
	if path.is_empty():
		return null
	if not _textures.has(path):
		_textures[path] = load(path) as Texture2D if ResourceLoader.exists(path) else null
	return _textures[path] as Texture2D
