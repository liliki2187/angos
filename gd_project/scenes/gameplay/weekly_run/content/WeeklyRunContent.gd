extends RefCounted

const WEEK_DAYS := 7

const DIFFICULTY_P := {
	"easy": 0.60,
	"normal": 0.50,
	"hard": 1.0 / 3.0,
}

const MACRO_LABELS := [
	{"key": "credibility", "label": "公信"},
	{"key": "weirdness", "label": "诡名"},
	{"key": "reputation", "label": "声望"},
	{"key": "order", "label": "守序"},
	{"key": "mania", "label": "狂性"},
]

const SLOT_DATA := [
	{"id": "front-main", "name": "头版头条", "weight": 1.00, "desc": "最高曝光，承担本期调性。"},
	{"id": "front-side", "name": "头版次条", "weight": 0.70, "desc": "高曝光，适合补足主话题。"},
	{"id": "feature-1", "name": "重点专题 A", "weight": 0.45, "desc": "适合高价值调查稿。"},
	{"id": "feature-2", "name": "重点专题 B", "weight": 0.40, "desc": "适合做题材连携。"},
	{"id": "inner-1", "name": "内页 A", "weight": 0.20, "desc": "标准曝光，适合补多样性。"},
	{"id": "inner-2", "name": "内页 B", "weight": 0.20, "desc": "标准曝光，适合边缘稿件。"},
]

const STAFF_POOL := [
	{"id": "ivy", "name": "艾薇·冷烛", "role": "外采调查", "attrs": {"explore": 5, "insight": 4, "occult": 2, "survival": 3, "reason": 3, "social": 2}},
	{"id": "qiao", "name": "乔然", "role": "城市跑口", "attrs": {"explore": 3, "insight": 4, "occult": 1, "survival": 2, "reason": 5, "social": 4}},
	{"id": "mora", "name": "莫拉", "role": "灵视记者", "attrs": {"explore": 2, "insight": 3, "occult": 5, "survival": 2, "reason": 2, "social": 3}},
	{"id": "reed", "name": "里德", "role": "战地摄影", "attrs": {"explore": 4, "insight": 2, "occult": 1, "survival": 5, "reason": 3, "social": 2}},
]

const REGION_DATA := [
	{
		"id": "us",
		"name": "北美禁区带",
		"hint": "初始解锁。都市传说与军事封锁交叠。",
		"unlock_rule": "always",
		"nodes": [
			{"id": "n51", "name": "51 区外围公路", "kind": "permanent", "days": 2, "type": "sci", "difficulty": "normal", "enemy": 2, "k_a": 3, "k_b": 2, "need": {"explore": 4, "survival": 2}, "description": "围绕夜间封锁和可疑货运展开跟拍，寻找能上头版的实证。", "risk_text": "军方与保安巡逻频繁。"},
			{"id": "skin", "name": "罗斯威尔档案残页", "kind": "permanent", "days": 1, "type": "sci", "difficulty": "normal", "enemy": 1, "k_a": 2, "k_b": 2, "need": {"insight": 3, "reason": 3}, "description": "在档案馆和旧报社之间追索失踪页。", "risk_text": "成功质量决定后续区域解锁速度。"},
			{"id": "temp_ufo", "name": "突发：雷达异常光点", "kind": "temp", "days": 2, "type": "pop", "difficulty": "hard", "enemy": 3, "k_a": 4, "k_b": 3, "deadline_day": 4, "need": {"explore": 5, "survival": 3}, "description": "城市雷达站刚刚记录到异常光点，热度高但窗口极短。", "risk_text": "过期即消失。"},
			{"id": "hidden_gate", "name": "灵视：黑色方尖碑的回声", "kind": "hidden", "days": 3, "type": "occult", "difficulty": "normal", "enemy": 4, "k_a": 4, "k_b": 2, "unlock_rule": "hidden_monolith", "need": {"occult": 4, "survival": 2}, "description": "当诡名与狂性同时越界，灵视记者会听见来自沙海的回声。", "risk_text": "失败会推高狂性。"},
		],
	},
	{
		"id": "east_asia",
		"name": "东亚神秘地带",
		"hint": "需要：声望≥55 或拿到罗斯威尔残页证据。",
		"unlock_rule": "east_asia",
		"nodes": [
			{"id": "harbor_echo", "name": "港口回声仓栈", "kind": "permanent", "days": 2, "type": "pop", "difficulty": "normal", "enemy": 2, "k_a": 3, "k_b": 2, "need": {"social": 3, "reason": 3}, "description": "跟随码头流言和失踪航运记录，拼出被压下来的新闻源。", "risk_text": "适合补足大众关注。"},
			{"id": "mountain_signal", "name": "山中电台失踪案", "kind": "permanent", "days": 3, "type": "occult", "difficulty": "hard", "enemy": 3, "k_a": 4, "k_b": 3, "need": {"explore": 4, "occult": 3, "survival": 3}, "description": "沿着废弃电台的短波干扰深入山谷。", "risk_text": "高风险高回报。"},
		],
	},
]

const STORY_TAG_MAP := {
	"sci": ["Politics", "Military", "Economy"],
	"occult": ["Gossip", "Pets", "Humor"],
	"pop": ["Sport", "Shopping", "Gossip"],
}

const QUALITY_MAP := {
	1: {"quality": "Bronze", "base_value": 150},
	2: {"quality": "Silver", "base_value": 300},
	3: {"quality": "Gold", "base_value": 450},
}

const ATTR_LABELS := {
	"explore": "探索",
	"insight": "洞察",
	"occult": "诡思",
	"survival": "生存",
	"reason": "理性",
	"social": "社交",
}

const TAG_LABELS := {
	"sci": "科学纪实",
	"occult": "神秘玄学",
	"pop": "大众热度",
}

const FILLER_SUBJECTS := {
	"Politics": ["预算案风波", "地方选举震荡", "安全听证泄密", "市政采购黑幕"],
	"Military": ["边境演训记录", "驻防调整谣言", "军备采购追踪", "哨所口供残卷"],
	"Economy": ["码头物流停摆", "黑市金价异动", "厂区裁员余震", "消费指数回落"],
	"Sport": ["主场重建争议", "联赛爆冷", "俱乐部内幕", "冠军游行失控"],
	"Gossip": ["名流秘会", "夜宴侧录", "家族婚约风波", "演员罢演内幕"],
	"Pets": ["宠物诊所失踪案", "街区猫狗热潮", "罕见生物传闻", "流浪犬收容争议"],
	"Humor": ["荒诞榜单", "街头怪谈栏目", "讽刺小剧场", "报社笑料合订本"],
	"Shopping": ["促销季暗箱", "百货断货潮", "抢购失控", "新品试卖记录"],
}

const BRIEFING_EVENT_IDS := [
	"paper-price-spike",
	"crowd-sightings",
	"faction-clearance",
	"advertiser-pressure",
]

const BRIEFING_EVENTS := {
	"paper-price-spike": "纸价又涨了一轮；但读者对超自然栏目的来信也明显变多。",
	"crowd-sightings": "本周城里出现两起“官方否认但群众坚信”的目击报告。",
	"faction-clearance": "势力联系人放来消息：如果这周发刊足够稳，下一张区域通行许可就会松动。",
	"advertiser-pressure": "广告主变得谨慎了，意味着组版时不能只顾刺激，还得照顾整体可信度和版面平衡。",
}

const BRIEFING_TASK_TEMPLATES := [
	{"id": "hold_credibility", "summary": "本周至少拿下一条能稳住可信度的调查稿。"},
	{"id": "protect_margin", "summary": "发刊时尽量减少空版，避免广告主进一步收缩。"},
	{"id": "push_unlock", "summary": "优先跟进能推动下一片区域解锁的素材。"},
	{"id": "watch_mania", "summary": "本周注意压住狂性，避免隐藏节点副作用外溢。"},
]

static func get_briefing_text(event_id: String) -> String:
	return str(BRIEFING_EVENTS.get(event_id, "本周没有额外简报。"))
