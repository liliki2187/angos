(function () {
  "use strict";

  const DIFFICULTY_P = { easy: 0.6, normal: 0.5, hard: 1 / 3 };
  const macro = { 公信: 42, 诡名: 38, 声望: 45, 守序: 48, 狂性: 22 };

  const state = {
    week: 1,
    day: 7,
    view: "weekStart",
    regionId: null,
    mission: null,
    selectedStaffIds: [],
    clues: [],
    pendingClues: [],
    pendingReports: [],
    log: [],
    filters: { sci: true, occult: true, pop: true },
    weekEvent: null,
    displayMode: "dice",
    lastCheck: null,
    phase: "briefing",
    stories: [],
    placed: {},
    subscribers: 1200,
    editorialProfile: 0,
    nextStoryId: 1,
    draggingStoryId: null,
    lastReplaceAction: null,
    undoTimer: null,
    baseDemand: 3200,
    coverPrice: 0.3,
    adSlots: 2,
    adMatchBase: 0.6,
    paperPackCost: 210,
    salaryCost: 980,
    opsCost: 260,
    printCapacity: 4200,
    subUnitValue: 0.18,
    synthTab: "phenomenon",
    synthRecipe: "r1",
    synthCraftSlots: {},
    synthPollution: 0,
    phenomenonCards: [],
    intelCards: [],
    cognitionCards: [],
    toolCards: [],
    tipOffCards: [],
    craftedReports: [],
    nextCardId: 1,
    /** 每条线索唯一题材键，自增 */
    nextTopicSeq: 1,
    /** 本周公开合成成功次数，按 primaryTopicKey 计数（合成阶段重置） */
    topicSynthOrder: {},
    /** 每次进入合成阶段自增，用于主笔内审疲劳（失败锁定至下一合成阶段） */
    synthSessionId: 0,
    /** 各主笔：内审相关状态（SAN、下次可内审的 session） */
    staffInternal: {},
    /** 合成台用人物卡（引用 STAFF，不消耗） */
    synthStaffCards: [],
    therapyCards: [],
    /** 题材 → 上次公开深度/专栏/爆料取向（sci/occult/pop）；快讯不计入 */
    lastPublicStanceByTopic: {},
    weekEventResolved: false,
    staffEffects: [],
    dynamicNodes: [],
    retiredMissionIds: {},
    completedMissionIds: {},
    chainStageResults: {},
    whiteInvestigationLog: {},
    calamityMeter: 0,
    pushBudgetWeekly: 1,
    selectedToolDiceIds: [],
    pendingDiceSelection: null,
    toolDiceInventory: [
      { id: "tool_cam_1", name: "夜视相机组", faces: [{ attr: "洞察", value: 1 }, { attr: "洞察", value: 2 }, { attr: "探索", value: 1 }, { attr: "探索", value: 1 }, { blank: true }, { blank: true }] },
      { id: "tool_tip_1", name: "匿名热线录音", faces: [{ attr: "人脉", value: 2 }, { attr: "人脉", value: 1 }, { attr: "洞察", value: 1 }, { attr: "造势", value: 1 }, { blank: true }, { blank: true }] },
    ],
    tempStaffIds: [],
    tempHireUsed: false,
    staffDiceOverrides: {},
    staffLevels: {},
    staffDebuffs: {},
    debugShowEventEffects: false,
    weekEventResult: "",
    weekEventResultLines: [],
    weekEventChoiceIndex: null,
    regionLeadEvents: {},
    globalSelectedRegionId: "us",
    missionResolving: false,
    regionLinkedTarget: null,
    openDeepChainId: null,
    activeMissions: [],
    todayResolutionQueue: [],
    processingDayTick: false,
    dayResolutionInfo: null,
    paperLayoutMode: "fixed",
    paperLabMode: false,
    paperVisualMode: "normal",
    publicationArchive: [],
    lastPublicationEcho: null,
    dispatchDecisionExperimentMode: false,
    dispatchOldSetupMode: false,
    /** 第 1 周软引导：已关闭过的 key，本局内不再弹出；新周目从第 1 周开始时随页面或 nextWeek 清空 */
    tutorialSoftW1: {},
  };

  /** localStorage：勾选「不再任何新手引导」后，本机不再弹出引导弹窗（清除站点数据可恢复） */
  const TUTORIAL_LS_DISABLE_ALL = "wm_angos_no_tutorials_v1";
  const TUTORIAL_LS_FIRST_PANEL_DONE = "wm_angos_tutorial_intro_offer_done_v1";

  function tutorialsGloballyDisabled() {
    if (state.debugSkipTutorials) return true;
    try {
      return localStorage.getItem(TUTORIAL_LS_DISABLE_ALL) === "1";
    } catch (_) {
      return false;
    }
  }

  function tutorialIntroOfferStillPending() {
    try {
      return localStorage.getItem(TUTORIAL_LS_FIRST_PANEL_DONE) !== "1";
    } catch (_) {
      return true;
    }
  }

  function markTutorialIntroOfferFinished() {
    try {
      localStorage.setItem(TUTORIAL_LS_FIRST_PANEL_DONE, "1");
    } catch (_) {}
  }

  function setTutorialsGloballyDisabled() {
    try {
      localStorage.setItem(TUTORIAL_LS_DISABLE_ALL, "1");
    } catch (_) {}
  }

  /** 引导内嵌示意图：与 Assets/tutorial-*-guide.svg 线框风格一致 */
  function tutorialSoftFigure(src, altAttr, captionHtml) {
    const a = String(altAttr).replace(/"/g, "&quot;");
    return `<div class="tutorial-soft-figure" style="margin:0 0 0.65rem;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#0b1220;"><img src="${src}" alt="${a}" style="display:block;width:100%;max-height:min(30vh,220px);height:auto;object-fit:contain;" /><p style="margin:0;padding:8px 10px;font-size:0.72rem;color:var(--muted);line-height:1.45;border-top:1px solid var(--line);">${captionHtml}</p></div>`;
  }

  /** 报刊组版实验 · 多页（中等密度：小标题 + 列表） */
  const LAB_FULL_GUIDE_PAGES = [
    `${tutorialSoftFigure(
      "Assets/tutorial-editorial-guide.svg",
      "组版示意：故事库拖入报纸版位",
      "与正式组版同一套版心习惯；本实验跳过取材与合成。",
    )}<div class="tutorial-soft-sheet">
      <h4 class="tutorial-soft-h4">组版练习场是做什么的？</h4>
      <p class="tutorial-soft-lead">主编您好。这里是《世界未解之谜周刊》的<strong>组版练习场</strong>：暂时跳过出门采访和成稿台，先熟悉报纸版心与「稿子怎么上桌」。</p>
      <ul class="tutorial-soft-ul">
        <li>完整流程里，组版排在<strong>取材 → 合成</strong>之后。</li>
        <li>本页只练<strong>最后一步</strong>，和正式第一周用的是同一套版式习惯。</li>
      </ul>
    </div>`,
    `<div class="tutorial-soft-sheet">
      <h4 class="tutorial-soft-h4">和正式周刊的关系</h4>
      <ul class="tutorial-soft-ul">
        <li><strong>回合札记</strong>：每周开场事件。</li>
        <li><strong>取材地图</strong>：选区域、跑探索。</li>
        <li><strong>合成台</strong>：把线索收成报道。</li>
        <li><strong>编辑部组版</strong>：把报道摆进版面（您现在练的就是这步）。</li>
      </ul>
    </div>`,
    `<div class="tutorial-soft-sheet">
      <h4 class="tutorial-soft-h4">关窗后会发生什么？</h4>
      <ul class="tutorial-soft-ul">
        <li>会自动播放一则<strong>填入动画示例</strong>（稿件飞入头版，可循环）。</li>
        <li>演示弹窗内可点<strong>重播</strong>立即重看；关闭后继续手动摆版。</li>
      </ul>
      <p class="tutorial-soft-note">本提示在刷新页面前只出现一次。</p>
    </div>`,
  ];

  const PAPER_DEMO_SOURCE_INNER_HTML = `<div class="nm-story-title">示例报道：港区异常回波</div>
<div class="nm-chips"><span class="nm-chip ex">探索稿</span><span class="nm-chip">标签:时政 / 经济</span><span class="nm-chip">质量:Gold</span></div>
<div class="nm-tip" style="margin-top:6px;font-size:11px;padding:6px;">拖到中间头版版位</div>`;

  const TAGS = ["Politics", "Military", "Economy", "Sport", "Gossip", "Pets", "Humor", "Shopping"];
  const QUALITY = [
    { key: "Bronze", value: 150 },
    { key: "Silver", value: 300 },
    { key: "Gold", value: 450 },
  ];
  const NEGATIVE_TYPES = ["sloppy_writing", "thin_source", "late_edit", "bias_overreach", "fabrication"];
  const LOCATIONS = ["曼哈顿", "布鲁克林", "皇后区", "布朗克斯", "华尔街", "港口区", "市政厅", "唐人街"];
  const ORGS = ["市议会", "警署", "港务局", "联邦调查局", "工商总会", "市政厅", "消防总队", "联邦法院"];
  const SUBJECTS = {
    Politics: ["预算案", "选举资金", "政务听证", "议会表决", "市政采购"],
    Military: ["边境演训", "军备采购", "驻防调整", "联合作战", "国防听证"],
    Economy: ["失业数据", "工厂裁员", "商贸指数", "税收政策", "物价走势"],
    Sport: ["职业联赛", "主场改造", "球员转会", "拳击挑战赛", "青训计划"],
    Gossip: ["名流绯闻", "晚宴风波", "婚约传闻", "社交圈密谈", "明星合约"],
    Pets: ["流浪犬收容", "宠物医疗", "猫狗领养潮", "宠物用品短缺", "社区遛犬纠纷"],
    Humor: ["讽刺专栏", "街头趣闻", "本周笑料", "漫画连载", "荒诞榜单"],
    Shopping: ["百货促销", "新品抢购", "消费榜单", "折扣季", "商场扩建"],
  };
  const ACTIONS = ["引发争议", "进入调查", "通过审议", "宣布升级", "出现反转", "再起波澜", "确认落地", "紧急叫停"];
  const PUBLIC_AFFAIRS = new Set(["Politics", "Military", "Economy"]);
  const MASS_APPEAL = new Set(["Sport", "Shopping"]);
  const LIFESTYLE_LIGHT = new Set(["Gossip", "Pets", "Humor"]);

  const slots = [
    { id: "front-main", name: "头版头条", weight: 1.0, desc: "最高曝光，约 3.0x" },
    { id: "front-side", name: "头版次条", weight: 0.7, desc: "高曝光，约 2.4x" },
    { id: "feature-1", name: "重点专题 A", weight: 0.45, desc: "中高曝光，约 1.9x" },
    { id: "feature-2", name: "重点专题 B", weight: 0.4, desc: "中高曝光，约 1.8x" },
    { id: "inner-1", name: "内页 A", weight: 0.2, desc: "标准曝光，约 1.4x" },
    { id: "inner-2", name: "内页 B", weight: 0.2, desc: "标准曝光，约 1.4x" },
  ];

  state.placed = Object.fromEntries(slots.map((s) => [s.id, null]));

  function newTopicKey() {
    return `topic_${state.nextTopicSeq++}`;
  }

  const ATTR_KEYS = ["探索", "生存", "洞察", "想象", "理性", "笔力", "胆识", "诡思", "人脉", "造势"];
  const ATTR_DOMAIN = {
    探索: "外勤",
    生存: "外勤",
    胆识: "外勤",
    洞察: "认知",
    理性: "认知",
    诡思: "认知",
    笔力: "内容",
    想象: "内容",
    造势: "内容",
    人脉: "关系",
  };
  const DOMAIN_CLASS = { 外勤: "field", 认知: "cog", 内容: "content", 关系: "social" };

  const face = (attr, value, extra) => ({ attr, value, ...(extra || {}) });
  const blankFace = (label) => ({ blank: true, label: label || "空" });

  const REGIONS = [
    {
      id: "us",
      name: "纽约市",
      unlocked: true,
      pulse: false,
      hint: "初始解锁。债主逼近，本周必须从五区里挖出能救周刊的题材。",
      nodes: [
        {
          id: "ball_light_kitchen",
          kind: "permanent",
          name: "布鲁克林厨房火球",
          days: 1,
          need: { 理性: 2, 洞察: 1 },
          tags: ["sci", "occult"],
          difficulty: "normal",
          enemyAttr: 1,
          checkType: "white",
          chainType: "deep",
          chainStage: 1,
          chainStageTotal: 4,
          chainId: "ball_lightning",
          taskTypeTitle: "深度调查 · 厨房火球第一环",
          taskTypeDesc: "调查布鲁克林公寓里的火球、磁化餐具与环形焦痕。成功后推进到市立气象站删改记录。",
          nextNode: {
            id: "ball_light_weather",
            kind: "temp",
            name: "市立气象站删改记录",
            days: 1,
            need: { 理性: 3, 人脉: 1 },
            tags: ["sci"],
            difficulty: "normal",
            enemyAttr: 2,
            checkType: "white",
            chainType: "deep",
            chainStage: 2,
            chainStageTotal: 4,
            chainId: "ball_lightning",
            previousStageId: "ball_light_kitchen",
            taskTypeTitle: "深度调查 · 厨房火球第二环",
            taskTypeDesc: "核对电场曲线、热线记录与被删改的夜间观测表，开始接触机构口径。",
            nextNode: {
              id: "ball_light_substation",
              kind: "temp",
              name: "康爱迪生地下变电室",
              days: 2,
              need: { 理性: 3, 生存: 2, 洞察: 2 },
              tags: ["sci", "occult"],
              difficulty: "hard",
              enemyAttr: 3,
              checkType: "white",
              riskTier: "high",
              chainType: "deep",
              chainStage: 3,
              chainStageTotal: 4,
              chainId: "ball_lightning",
              previousStageId: "ball_light_weather",
              taskTypeTitle: "高危深度调查 · 厨房火球第三环",
              taskTypeDesc: "地下变电室里留着不在市政采购清单上的设备编号。危险任务，失败可能造成队员状态损伤。",
              nextNode: {
                id: "ball_light_experiment",
                kind: "temp",
                name: "复现实验前夜",
                days: 2,
                need: { 理性: 4, 胆识: 2, 诡思: 2 },
                tags: ["sci", "occult"],
                difficulty: "hard",
                enemyAttr: 4,
                checkType: "white",
                riskTier: "high",
                isBlackDiceTask: true,
                blackDiceTheme: "ball_lightning",
                chainType: "deep",
                chainStage: 4,
                chainStageTotal: 4,
                chainId: "ball_lightning",
                previousStageId: "ball_light_substation",
                chainFinal: true,
                taskTypeTitle: "黑骰任务 · 厨房火球终局",
                taskTypeDesc: "火球像在回应观测者。黑骰会感应、接地或同步你的骰子，把实验推向失控边缘。",
                chain: null,
              },
              chain: null,
            },
            chain: null,
          },
          chain: null,
        },
        {
          id: "n51",
          kind: "permanent",
          name: "皇后区旧机库围栏",
          days: 2,
          need: { 探索: 2, 生存: 1 },
          tags: ["sci", "pop"],
          difficulty: "normal",
          enemyAttr: 2,
          checkType: "white",
          taskTypeTitle: "白色调查",
          taskTypeDesc: "常驻白色调查。跟拍无牌货车、夜间保安换岗与围栏内短时断电；即使失败，也会继续累积同一条调查线。",
          chain: null,
        },
        {
          id: "skin",
          kind: "permanent",
          name: "纽约飞碟剪报残页",
          days: 1,
          need: { 探索: 2, 洞察: 1 },
          tags: ["sci", "occult"],
          difficulty: "normal",
          enemyAttr: 1,
          checkType: "white",
          chainType: "deep",
          chainStage: 1,
          chainStageTotal: 4,
          chainId: "roswell_demo",
          taskTypeTitle: "深度调查 · 飞碟剪报第一环",
          taskTypeDesc: "从旧报社剪报、读者来信和港务局流言里拼出一条连续线。完成后会推进到下一阶段。",
          nextNode: {
            id: "roswell_weather_copy",
            kind: "temp",
            name: "港务局夜间雷达抄本",
            days: 1,
            need: { 洞察: 3, 理性: 2 },
            tags: ["sci", "occult"],
            difficulty: "normal",
            enemyAttr: 2,
            checkType: "white",
            chainType: "deep",
            chainStage: 2,
            chainStageTotal: 4,
            chainId: "roswell_demo",
            previousStageId: "skin",
            taskTypeTitle: "深度调查 · 飞碟剪报第二环",
            taskTypeDesc: "比对港务局夜班抄本与哈德逊航道记录。继续推进可能提高公信，也可能引来机构口径。",
            nextNode: {
              id: "roswell_radar_night",
              kind: "temp",
              name: "废弃屋顶观测点",
              days: 2,
              need: { 探索: 3, 洞察: 3, 生存: 2 },
              tags: ["sci", "occult"],
              difficulty: "hard",
              enemyAttr: 3,
              checkType: "white",
              riskTier: "high",
              chainType: "deep",
              chainStage: 3,
              chainStageTotal: 4,
              chainId: "roswell_demo",
              previousStageId: "roswell_weather_copy",
              taskTypeTitle: "高危深度调查 · 飞碟剪报第三环",
              taskTypeDesc: "夜访曼哈顿废弃屋顶观测点。需求更高，失败可能带来 debuff，但本环没有黑骰。",
              nextNode: {
                id: "roswell_tape_blank",
                kind: "temp",
                name: "三秒空白录音",
                days: 2,
                need: { 洞察: 5, 诡思: 3, 理性: 3 },
                tags: ["sci", "occult"],
                difficulty: "hard",
                enemyAttr: 4,
                checkType: "white",
                riskTier: "high",
                isBlackDiceTask: true,
                chainType: "deep",
                chainStage: 4,
                chainStageTotal: 4,
                chainId: "roswell_demo",
                previousStageId: "roswell_radar_night",
                chainFinal: true,
                allowPushBonus: true,
                taskTypeTitle: "黑骰深度调查 · 飞碟剪报终局",
                taskTypeDesc: "连续任务终局。录音里最关键的三秒被某种东西擦掉，进入后使用关卡专属黑骰机制与四档结果。",
                chain: null,
              },
              chain: null,
            },
            chain: null,
          },
          chain: null,
        },
        {
          id: "temp_ufo",
          kind: "temp",
          name: "突发：哈德逊河上空异常光点",
          days: 2,
          need: { 探索: 2, 生存: 1, 胆识: 1 },
          tags: ["sci", "pop"],
          deadlineDay: 4,
          difficulty: "hard",
          enemyAttr: 3,
          checkType: "red",
          riskTier: "high",
          taskTypeTitle: "红色截稿 · 临时情报",
          taskTypeDesc: "一次性情报窗口。市民电台和港务局都在删帖；成功、失败或超过截止日期后都会关闭。这是危险任务，但没有黑骰。",
          chain: null,
        },
        {
          id: "bus330_witness",
          kind: "permanent",
          name: "M330 末班车 · 乘客口述",
          days: 1,
          need: { 人脉: 2, 洞察: 1 },
          tags: ["occult", "pop"],
          difficulty: "normal",
          enemyAttr: 1,
          checkType: "white",
          chainType: "deep",
          chainStage: 1,
          chainStageTotal: 4,
          chainId: "bus330",
          taskTypeTitle: "深度调查 · M330 末班车第一环",
          taskTypeDesc: "从乘客、旧报和读者来信里核实末班车传闻。成功后会推进到布朗克斯废弃调度室。",
          nextNode: {
            id: "bus330_depot",
            kind: "temp",
            name: "M330 末班车 · 布朗克斯废弃调度室",
            days: 1,
            need: { 探索: 1, 洞察: 2 },
            tags: ["occult", "pop"],
            difficulty: "normal",
            enemyAttr: 2,
            checkType: "white",
            chainType: "deep",
            chainStage: 2,
            chainStageTotal: 4,
            chainId: "bus330",
            previousStageId: "bus330_witness",
            taskTypeTitle: "深度调查 · M330 末班车第二环",
            taskTypeDesc: "调查废弃调度室里的车次表、泥迹座椅和被涂黑的线路图，关系线索开始转入现场。",
            nextNode: {
              id: "bus330_station",
              kind: "temp",
              name: "M330 末班车 · 无名站牌",
              days: 2,
              need: { 探索: 3, 胆识: 2, 诡思: 1 },
              tags: ["occult"],
              difficulty: "hard",
              enemyAttr: 3,
              checkType: "white",
              riskTier: "high",
              chainType: "deep",
              chainStage: 3,
              chainStageTotal: 4,
              chainId: "bus330",
              previousStageId: "bus330_depot",
              taskTypeTitle: "高危深度调查 · M330 末班车第三环",
              taskTypeDesc: "地图上不存在的站牌出现在凌晨路线图里。危险任务，失败后果较重，但本环没有黑骰。",
              nextNode: {
                id: "bus330_tape",
                kind: "temp",
                name: "M330 末班车 · 车载录像最后三秒",
                days: 2,
                need: { 胆识: 3, 诡思: 3, 洞察: 2 },
                tags: ["occult"],
                difficulty: "hard",
                enemyAttr: 4,
                checkType: "white",
                riskTier: "high",
                isBlackDiceTask: true,
                blackDiceTheme: "bus330",
                chainType: "deep",
                chainStage: 4,
                chainStageTotal: 4,
                chainId: "bus330",
                previousStageId: "bus330_station",
                chainFinal: true,
                taskTypeTitle: "黑骰任务 · M330 末班车终局",
                taskTypeDesc: "多出来的乘客坐在监控死角里。黑骰会混入或替换你的骰子，具体机制在黑骰任务中展示。",
                chain: null,
              },
              chain: null,
            },
            chain: null,
          },
          chain: null,
        },
        {
          id: "hidden_gate",
          kind: "hidden",
          name: "华尔街废站的黑色方尖碑",
          days: 3,
          need: { 探索: 4, 诡思: 4, 生存: 2 },
          tags: ["occult"],
          difficulty: "normal",
          enemyAttr: 4,
          checkType: "white",
          riskTier: "high",
          taskTypeTitle: "隐藏调查",
          taskTypeDesc: "只有当周刊已经足够危险，废站里的方尖碑回声才会浮出地图。它能带来高价值素材，也会推高现实失控感。",
          unlock: (m) => m.狂性 >= 35 && m.诡名 >= 40,
          chain: null,
        },
      ],
    },
    {
      id: "new_england",
      name: "新英格兰走廊",
      unlocked: false,
      pulse: false,
      hint: "需要：声望≥55 或 完成「纽约飞碟剪报残页」。",
      nodes: [
        { id: "shen", kind: "permanent", name: "缅因州海岸灯塔回声", days: 3, need: { 探索: 2, 生存: 1 }, tags: ["sci", "pop"], difficulty: "normal", enemyAttr: 2, chain: null },
        { id: "chainA", kind: "permanent", name: "模糊：新英格兰未解锁线索", days: 2, need: { 探索: 3, 洞察: 2 }, tags: ["sci"], difficulty: "normal", enemyAttr: 2, chain: "locked", chainTitle: "链式调查 · 第二阶段" },
      ],
    },
    {
      id: "western_archives",
      name: "西部禁区档案",
      unlocked: false,
      pulse: false,
      hint: "需要：公信≥60（档案合作）或 守序≥60（调查许可）。",
      nodes: [{ id: "easter", kind: "permanent", name: "内华达干湖热异常", days: 3, need: { 探索: 2, 理性: 1 }, tags: ["sci"], difficulty: "normal", enemyAttr: 2, chain: null }],
    },
  ];
  const REGION_MAP_POS = {
    us: { x: 30, y: 38, label: "纽约市" },
    new_england: { x: 39, y: 30, label: "新英格兰走廊" },
    western_archives: { x: 18, y: 50, label: "西部禁区档案" },
  };
  const NODE_MAP_POS = {
    us: {
      n51: { x: 62, y: 35 },
      skin: { x: 49, y: 43 },
      temp_ufo: { x: 35, y: 28 },
      hidden_gate: { x: 48, y: 68 },
      roswell_weather_copy: { x: 48, y: 58 },
      roswell_radar_night: { x: 60, y: 64 },
      roswell_tape_blank: { x: 69, y: 56 },
      bus330_witness: { x: 18, y: 60 },
      bus330_depot: { x: 30, y: 67 },
      bus330_station: { x: 42, y: 73 },
      bus330_tape: { x: 54, y: 78 },
      ball_light_kitchen: { x: 28, y: 18 },
      ball_light_weather: { x: 40, y: 20 },
      ball_light_substation: { x: 52, y: 22 },
      ball_light_experiment: { x: 64, y: 20 },
    },
    new_england: { shen: { x: 42, y: 38 }, chainA: { x: 62, y: 56 } },
    western_archives: { easter: { x: 48, y: 46 } },
  };

  const MISSION_STORIES = {
    n51: {
      brief: "匿名读者把一张货车照片塞进编辑部信箱，照片背面只写着：皇后区旧机库还在运作。",
      objective: "跟拍无牌货车，摸清围栏内断电与保安换岗时间。",
      stakes: "常驻白色调查。失败不会封死题材，但每次外勤都会消耗周刊最后的现金和耐心。",
      fieldIntro: "凌晨两点，铁丝网被风吹得发响。线人把相机藏进外套，示意你们别再开手电。",
      dice: {
        rolling: "线人低声说：要是我十分钟没回电话，就把照片直接送去排版。",
        select: "主编：先挑能证明货车进出的骰面，别被围栏外的噪声带走。",
      },
      outcomes: {
        大成功: { line: "大成功：保安换岗、断电日志和货车路线三件事对上了。", clueTitle: "货车路线与断电表", clueDesc: "你拿到一组可互相印证的照片、车牌残号和断电时间。" },
        小成功: { line: "成功：照片能用，车牌还差两位，但足够撑起一篇追踪稿。", clueTitle: "旧机库外拍素材", clueDesc: "素材有噪点，但能证明围栏内确实有夜间运输。" },
        成功: { line: "成功：照片能用，车牌还差两位，但足够撑起一篇追踪稿。", clueTitle: "旧机库外拍素材", clueDesc: "素材有噪点，但能证明围栏内确实有夜间运输。" },
        失败: { line: "失败：线人被保安赶走，但他记下了车门上的维修编号。", clueTitle: "车门维修编号", clueDesc: "弱线索。它不能单独成稿，但能指向下一次跟拍对象。" },
        大失败: { line: "大失败：相机卡被没收，债主的电话在编辑部响了一整夜。" },
      },
    },
    temp_ufo: {
      brief: "深夜电台播出哈德逊河上空的光点录音，十五分钟后节目回放被整段替换。",
      objective: "抢在删帖前找到目击者、港务局记录和可上版的现场照片。",
      stakes: "红色截稿。这个窗口只开一次，错过后故事会被别家或沉默吃掉。",
      fieldIntro: "码头风很冷。对岸灯光一闪一灭，电台主持人的录音机一直发出倒带声。",
      dice: {
        rolling: "摄影记者：这东西不是飞机。至少，飞机不会在水面上留下第二个影子。",
        select: "主编：先保住能上封面的证据，剩下的恐惧以后再写。",
      },
      outcomes: {
        crit_success: { line: "大成功：录音、目击者和港务局雷达抄本同时指向同一段夜空。", clueTitle: "哈德逊三重证词", clueDesc: "红色截稿强素材。照片、录音和抄本能互相支撑。" },
        success_cost: { line: "成功但反噬：独家到手，港务局发言人也记住了周刊的名字。", clueTitle: "被盯上的独家", clueDesc: "素材很强，但会带来机构口径压力。" },
        partial: { line: "部分成功：照片能用，最关键的三秒却像被水汽擦掉。", clueTitle: "模糊光点底片", clueDesc: "可成稿素材，但需要后续报道补强。" },
        fail_clue: { line: "失败但有线索：现场散了，只剩一名船员反复提到河面上的第二个倒影。", clueTitle: "第二倒影证词", clueDesc: "弱线索。它更像下一篇报道的钩子。" },
        crit_fail: { line: "大失败：录音带被消磁，目击者改口，编辑部收到一封律师函草稿。" },
      },
    },
    ball_light_kitchen: {
      brief: "布鲁克林一间公寓厨房被火球穿过，冰箱门上留下了整齐的环形焦痕。",
      objective: "确认火球目击、磁化餐具和室内电路记录是否能互相印证。",
      stakes: "深度调查第一环。成功后会把故事推进到市立气象站记录。",
      fieldIntro: "房东不让你们拍墙面，只准站在门口。灶台上的金属勺仍然吸着一枚纽扣。",
      dice: {
        rolling: "科学顾问：如果这是假新闻，它也假得太懂电磁学了。",
        select: "主编：别急着写奇迹，先选能解释焦痕和磁化的骰面。",
      },
      outcomes: {
        大成功: { line: "大成功：目击时间、电路跳闸和磁化餐具形成一条清楚时间线。", clueTitle: "厨房火球时间线", clueDesc: "第一环强素材，足以追问气象站记录。" },
        小成功: { line: "成功：焦痕照片拍到了，电路记录还要找市政渠道补证。", clueTitle: "环形焦痕照片", clueDesc: "可用素材。它把厨房异常从传闻推向调查。" },
        成功: { line: "成功：焦痕照片拍到了，电路记录还要找市政渠道补证。", clueTitle: "环形焦痕照片", clueDesc: "可用素材。它把厨房异常从传闻推向调查。" },
        失败: { line: "失败：房东提前赶人，但你们带走了一支被异常磁化的叉子。", clueTitle: "磁化叉子", clueDesc: "弱线索。它无法解释火球，却证明现场不正常。" },
        大失败: { line: "大失败：房东报警，整层住户都开始拒绝采访。" },
      },
    },
    ball_light_weather: {
      brief: "市立气象站的夜间观测表出现涂改，涂改时间正好卡在厨房火球之后。",
      objective: "比对热线记录、气象站原表和电场曲线。",
      stakes: "深度调查第二环。证据开始碰到机构口径。",
      fieldIntro: "档案室的荧光灯忽明忽暗，值班员说那晚的表格早就被上级收走。",
      outcomes: {
        大成功: { line: "大成功：原始表、热线录音和电场曲线都指向同一次异常峰值。", clueTitle: "被删改的电场峰值", clueDesc: "第二环强素材，能把故事推向地下设备。" },
        小成功: { line: "成功：你们拍到涂改痕迹，也拿到一段不完整热线录音。", clueTitle: "涂改观测表", clueDesc: "可用素材。它证明有人动过记录。" },
        失败: { line: "失败：气象站拒绝配合，但值班员留下了一个康爱迪生设备编号。", clueTitle: "设备编号便签", clueDesc: "弱线索。编号指向地下变电室。" },
      },
    },
    ball_light_substation: {
      brief: "设备编号指向康爱迪生地下变电室，那里有一台不在采购清单上的旧仪器。",
      objective: "进入变电室，确认仪器编号、接地痕迹和火球事件的关系。",
      stakes: "危险深度调查。失败可能损伤队伍状态，但能靠近核心证据。",
      fieldIntro: "地下室的空气像被烧过。墙上电箱没有编号，只有一圈被擦掉的粉笔线。",
      outcomes: {
        crit_success: { line: "大成功：仪器编号、接地痕迹和火球时间线完整闭合。", clueTitle: "地下仪器完整记录", clueDesc: "高价值证据。它能支撑终局复现实验。" },
        success_cost: { line: "成功但反噬：你们拍到了仪器，也触发了电流回涌和安保追查。", clueTitle: "带反噬的仪器照片", clueDesc: "强素材，但队伍带着明显压力撤出。" },
        partial: { line: "部分成功：仪器照片只有一半清晰，编号却足够刺眼。", clueTitle: "半张仪器编号", clueDesc: "不完整素材。足以推进，难以直接定论。" },
        fail_clue: { line: "失败但有线索：电闸跳了，你们只带走一段接地线烧焦样本。", clueTitle: "烧焦接地线", clueDesc: "弱线索。样本说明异常和接地装置有关。" },
        crit_fail: { line: "大失败：变电室短路，市政巡查把周刊列入拒访名单。" },
      },
    },
    ball_light_experiment: {
      brief: "复现实验前夜，火球像在回应观测者。越像科学实验，越像有人在另一侧配合。",
      objective: "决定哪些观测数据可信，哪些异常必须隔离。",
      stakes: "黑骰终局。骰池会被异常感应、接地或同步。",
      fieldIntro: "实验室里所有金属物都朝同一个方向轻轻颤动。灯灭之前，你看见火球在玻璃上倒退。",
      dice: {
        rolling: "科学顾问：如果它真的在看我们，记录员就不要同时眨眼。",
        black: "主编：黑骰不是坏运气，是现场有东西开始回看骰子。",
        select: "主编：只计入你愿意写进封面标题的证据。",
      },
      outcomes: {
        大成功: { line: "黑骰任务大成功：实验复现成功，异常没有抓住主要记录员。", clueTitle: "可复现火球记录", clueDesc: "终局强素材。足以写成封面主稿。" },
        成功: { line: "黑骰任务成功：关键数据到手，但实验室墙面留下了新的环形焦痕。", clueTitle: "带回声的复现实验", clueDesc: "强素材，伴随轻微反噬。" },
        失败: { line: "黑骰任务失败：实验中断，录音里却多出一句不在场的人声。", clueTitle: "不在场人声", clueDesc: "弱线索。失败现场仍留下异常证据。" },
        大失败: { line: "黑骰任务大失败：火球没有出现，所有照片却拍到了同一张陌生脸。" },
      },
    },
    skin: {
      brief: "一叠纽约飞碟剪报残页被寄到编辑部，页边夹着港务局和读者来信的旧编号。",
      objective: "把剪报、读者来信和港务局流言拼成一条可追踪线。",
      stakes: "深度调查第一环。成功后转入港务局夜间雷达抄本。",
      fieldIntro: "剪报边缘被烟熏过，几张纸的日期彼此冲突，但同一个夜班编号反复出现。",
      dice: {
        rolling: "档案员：这些剪报像被人故意撕散，只留下足够让我们上钩的部分。",
        select: "主编：先把能互相指认的编号挑出来。",
      },
      outcomes: {
        大成功: { line: "大成功：剪报、来信和港务局编号拼出同一晚的完整轮廓。", clueTitle: "飞碟剪报编号链", clueDesc: "第一环强素材，指向港务局雷达抄本。" },
        小成功: { line: "成功：你们拼出关键编号，但缺一份夜班抄本。", clueTitle: "残缺编号链", clueDesc: "可用素材。它能推动下一阶段核对。" },
        成功: { line: "成功：你们拼出关键编号，但缺一份夜班抄本。", clueTitle: "残缺编号链", clueDesc: "可用素材。它能推动下一阶段核对。" },
        失败: { line: "失败：剪报年份对不上，只剩一封读者来信像在指路。", clueTitle: "读者来信编号", clueDesc: "弱线索。它保留了继续调查的入口。" },
      },
    },
    roswell_weather_copy: {
      brief: "港务局夜班抄本被人复印过多次，最关键的雷达回波只剩浅浅一圈。",
      objective: "核对雷达抄本与哈德逊航道记录。",
      stakes: "深度调查第二环。越接近机构记录，口径越容易被改写。",
      fieldIntro: "复印纸薄得透光。你们把它压在窗前，浅灰色回波终于浮出来。",
      outcomes: {
        大成功: { line: "大成功：雷达回波和航道记录在同一分钟重合。", clueTitle: "夜间雷达重合点", clueDesc: "第二环强素材，足以锁定屋顶观测点。" },
        小成功: { line: "成功：回波时间能对上，方位角还需要现场观测补证。", clueTitle: "雷达回波抄本", clueDesc: "可用素材。它把剪报变成可追踪路线。" },
        失败: { line: "失败：复印件被质疑造假，但页角留下了屋顶维护章。", clueTitle: "屋顶维护章", clueDesc: "弱线索。维护章指向曼哈顿废弃屋顶。" },
      },
    },
    roswell_radar_night: {
      brief: "废弃屋顶观测点面对哈德逊河，栏杆上还有旧相机架留下的划痕。",
      objective: "夜访屋顶，复核方位角、照片残影和目击口供。",
      stakes: "危险深度调查。失败会留下压力，但这里可能拍到独家画面。",
      fieldIntro: "屋顶门锁被新近撬过。风把城市噪声压低，像有人把纽约调成静音。",
      outcomes: {
        crit_success: { line: "大成功：方位角、残影和目击口供全部对准同一片夜空。", clueTitle: "屋顶观测三证", clueDesc: "危险强素材，直接指向三秒空白录音。" },
        success_cost: { line: "成功但反噬：照片拍到了，楼下巡逻也拍到了你们。", clueTitle: "被追查的屋顶照片", clueDesc: "强素材，但会带来现实压力。" },
        partial: { line: "部分成功：残影出现了，底片边缘却像被烧穿。", clueTitle: "烧穿底片残影", clueDesc: "不完整素材。能推进，但不够干净。" },
        fail_clue: { line: "失败但有线索：屋顶什么也没拍到，只录到一段整齐消失的三秒空白。", clueTitle: "三秒空白前奏", clueDesc: "弱线索。空白本身成了调查对象。" },
      },
    },
    roswell_tape_blank: {
      brief: "所有证据都指向一段录音：三秒钟里，城市背景声被挖走了。",
      objective: "分析空白录音，判断它是剪辑、干扰，还是某种主动擦除。",
      stakes: "黑骰深度调查。成功能拿到封面级素材，失败会污染队伍判断。",
      fieldIntro: "录音机开始播放。前三秒是纽约，后三秒还是纽约，中间却像整座城市停止呼吸。",
      dice: {
        rolling: "录音师：不是静音。静音不会把人的记忆也削掉一块。",
        black: "主编：黑骰出现时，先别急着解释，先确认哪些证据还属于我们。",
        select: "主编：只计入你敢署名的那几颗。",
      },
      outcomes: {
        大成功: { line: "黑骰任务大成功：空白被还原成一串可公开的低频脉冲。", clueTitle: "三秒低频脉冲", clueDesc: "终局强素材，可直接进入封面故事。" },
        成功: { line: "黑骰任务成功：你们听见了空白里的脉冲，也带回了轻微耳鸣。", clueTitle: "带耳鸣的空白录音", clueDesc: "强素材，伴随轻微反噬。" },
        失败: { line: "黑骰任务失败：录音没有还原，但所有人都记住了同一个不存在的标题。", clueTitle: "不存在的标题", clueDesc: "弱线索。它会影响后续写稿口径。" },
        大失败: { line: "黑骰任务大失败：录音机倒放出编辑部当天还没说出口的话。" },
      },
    },
    bus330_witness: {
      brief: "M330 末班车的乘客口述彼此矛盾，唯一相同的是：车上多了一站。",
      objective: "核实乘客名单、旧报线索和读者来信。",
      stakes: "深度调查第一环。成功后转入布朗克斯废弃调度室。",
      fieldIntro: "受访者把车票夹在圣经里。她说自己下车后，车厢里还坐着一个没人看清的人。",
      dice: {
        rolling: "线人：她不怕我们不信，她怕我们把那站名念出来。",
        select: "主编：先挑能证明乘客真的上过车的骰面。",
      },
      outcomes: {
        大成功: { line: "大成功：乘客名单、旧报和来信共同指向同一班末班车。", clueTitle: "M330 乘客交叉证词", clueDesc: "第一环强素材，指向废弃调度室。" },
        小成功: { line: "成功：口述能互相支撑，只差一张完整车次表。", clueTitle: "末班车口述稿", clueDesc: "可用素材。它把传闻变成可追踪路线。" },
        成功: { line: "成功：口述能互相支撑，只差一张完整车次表。", clueTitle: "末班车口述稿", clueDesc: "可用素材。它把传闻变成可追踪路线。" },
        失败: { line: "失败：受访者中途反悔，却留下半张旧车票。", clueTitle: "半张旧车票", clueDesc: "弱线索。票根上的线路号还看得清。" },
      },
    },
    bus330_depot: {
      brief: "废弃调度室墙上贴着旧线路图，M330 的终点站被黑色胶带盖住。",
      objective: "调查车次表、泥迹座椅和被涂黑的线路图。",
      stakes: "深度调查第二环。关系线索开始转入现场证据。",
      fieldIntro: "门一推开，调度室里的电话响了一声。听筒里只有远处刹车的尖叫。",
      outcomes: {
        大成功: { line: "大成功：车次表、泥迹和线路图缺口全部指向布朗克斯一处无名站牌。", clueTitle: "被涂黑的终点站", clueDesc: "第二环强素材，解锁无名站牌。" },
        小成功: { line: "成功：你们拍到线路图缺口，但车次表少了一页。", clueTitle: "线路图缺口照片", clueDesc: "可用素材。它足够把调查推向现场。" },
        失败: { line: "失败：调度室被提前清过场，只剩座椅下的一块湿泥。", clueTitle: "座椅下湿泥", clueDesc: "弱线索。泥里有不属于调度室的站台灰。" },
      },
    },
    bus330_station: {
      brief: "地图上不存在的站牌出现在凌晨路线图里，站名被油漆刷成一条黑线。",
      objective: "确认无名站牌、路面痕迹和凌晨车灯记录。",
      stakes: "危险深度调查。这里能接近终局录像，也最容易把人带偏。",
      fieldIntro: "站牌旁没有候车亭，只有一排新鲜脚印。它们都朝马路中央走去。",
      outcomes: {
        crit_success: { line: "大成功：站牌、脚印和车灯记录共同证明 M330 真的停过。", clueTitle: "无名站停靠证据", clueDesc: "危险强素材，指向车载录像最后三秒。" },
        success_cost: { line: "成功但反噬：证据拍到了，一名队员却坚称自己刚从车上下来。", clueTitle: "反噬停靠照片", clueDesc: "强素材，但队伍状态受到异常牵引。" },
        partial: { line: "部分成功：车灯记录能用，站牌照片却每次冲洗都多出一道黑线。", clueTitle: "多黑线的站牌照", clueDesc: "不完整素材。它能推进，但会污染叙事。" },
        fail_clue: { line: "失败但有线索：站牌消失前，你们在地上捡到一枚还温热的换乘币。", clueTitle: "温热换乘币", clueDesc: "弱线索。它把调查推向车载录像。" },
      },
    },
    bus330_tape: {
      brief: "车载录像最后三秒里，车厢灯光全灭。黑暗里多出了一排不该存在的座位。",
      objective: "判断哪些画面能计入报道，哪些画面会把读者也拖进车厢。",
      stakes: "黑骰终局。黑骰会混入、替座，或让成功变脏。",
      fieldIntro: "录像每播放一次，屏幕反光里就多一个站着的人。剪辑台旁没人愿意坐下。",
      dice: {
        rolling: "剪辑师：我数过座位，播放前和播放后不一样。",
        black: "主编：黑骰出现时，别问谁上了车，先问谁还在编辑部。",
        select: "主编：锁住能证明事实的证据，别把车上的东西一起交稿。",
      },
      outcomes: {
        大成功: { line: "黑骰任务大成功：最后三秒被定格，异常乘客没有进入成片。", clueTitle: "干净的车载定格", clueDesc: "终局强素材，可作为主封面核心证据。" },
        成功: { line: "黑骰任务成功：录像能用了，但成片里有一帧座位数对不上。", clueTitle: "有瑕疵的末班车录像", clueDesc: "强素材，伴随异常回声。" },
        失败: { line: "黑骰任务失败：录像糊成黑块，只留下车门刷卡声。", clueTitle: "车门刷卡声", clueDesc: "弱线索。失败仍能形成诡异旁证。" },
        大失败: { line: "黑骰任务大失败：剪辑台回放出你们明天才会录下的采访。" },
      },
    },
    hidden_gate: {
      brief: "华尔街废站深处有一座黑色方尖碑，只有在周刊足够接近失控时才会出现在地图上。",
      objective: "确认方尖碑材质、站台回声和它对现实秩序的影响。",
      stakes: "隐藏危险调查。素材价值极高，但会明显推高现实失控感。",
      fieldIntro: "废站里没有风，报纸边角却一直朝方尖碑方向翻动。",
      dice: {
        rolling: "主角：这不是新闻点，这是新闻点背后的门。",
        select: "主编：能写的才带走。不能写的，先别让它进编辑部。",
      },
      outcomes: {
        crit_success: { line: "大成功：方尖碑材质、回声频率和站台旧档案形成完整闭环。", clueTitle: "方尖碑完整档案", clueDesc: "隐藏强素材。它足够改写本期杂志的核心立场。" },
        success_cost: { line: "成功但反噬：你们带回样本，也带回每个人都听得见的站台广播。", clueTitle: "带广播的黑石样本", clueDesc: "强素材，但现实压力显著上升。" },
        partial: { line: "部分成功：样本拍到了，照片边缘却出现陌生站名。", clueTitle: "陌生站名照片", clueDesc: "不完整素材。它危险，却很有吸引力。" },
        fail_clue: { line: "失败但有线索：你们没有靠近方尖碑，只抄下了广播里重复的三个数字。", clueTitle: "废站三位数字", clueDesc: "弱线索。数字可能是站台、日期，也可能是债务编号。" },
        crit_fail: { line: "大失败：废站出口变成编辑部门口，没人知道你们离开了多久。" },
      },
    },
  };
  function makeAvatar(label, c1, c2) {
    const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 180'>
      <defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop stop-color='${c1}'/><stop offset='1' stop-color='${c2}'/></linearGradient></defs>
      <rect width='240' height='180' fill='url(#g)'/>
      <circle cx='120' cy='72' r='28' fill='rgba(255,255,255,0.82)'/>
      <rect x='68' y='106' width='104' height='44' rx='18' fill='rgba(255,255,255,0.72)'/>
      <text x='120' y='166' text-anchor='middle' font-size='18' fill='#0b1220' font-family='Segoe UI,Arial'>${label}</text>
    </svg>`;
    return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
  }

  const STAFF = [
    {
      id: "s1",
      name: "印第安纳穷死",
      avatar: "Assets/avatars/s1_indiana.png",
      specialty: ["探索", "胆识"],
      探索: 3, 生存: 2, 洞察: 2, 想象: 2, 理性: 2, 笔力: 1, 胆识: 4, 诡思: 1, 人脉: 2, 造势: 1,
      diceFaces: [face("探索", 2), face("探索", 1), face("胆识", 2), face("生存", 1), face("洞察", 1), blankFace()],
      growthBranches: [
        { id: "field", name: "荒野采访", desc: "探索1 -> 探索2", replaceIndex: 1, face: face("探索", 2) },
        { id: "bold", name: "不要命追踪", desc: "胆识2 -> 胆识3", replaceIndex: 2, face: face("胆识", 3) },
      ],
    },
    {
      id: "s2",
      name: "末日时钟",
      avatar: "Assets/avatars/s2_doomclock.png",
      specialty: ["洞察", "理性"],
      探索: 2, 生存: 3, 洞察: 3, 想象: 1, 理性: 3, 笔力: 2, 胆识: 2, 诡思: 0, 人脉: 3, 造势: 1,
      diceFaces: [face("洞察", 2), face("理性", 2), face("洞察", 1), face("人脉", 1), face("生存", 1), blankFace()],
      growthBranches: [
        { id: "warning", name: "提前预警", desc: "空面 -> 洞察1", replaceIndex: 5, face: face("洞察", 1) },
        { id: "rational", name: "冷静校验", desc: "理性2 -> 理性3", replaceIndex: 1, face: face("理性", 3) },
      ],
    },
    {
      id: "s3",
      name: "火鸡科学家",
      avatar: "Assets/avatars/s3_turkey_scientist.png",
      specialty: ["理性", "诡思"],
      探索: 1, 生存: 1, 洞察: 2, 想象: 3, 理性: 4, 笔力: 1, 胆识: 1, 诡思: 4, 人脉: 1, 造势: 2,
      diceFaces: [face("理性", 3), face("理性", 2), face("诡思", 2), face("洞察", 1), face("造势", 1), blankFace()],
      growthBranches: [
        { id: "lab", name: "复现实验", desc: "理性2 -> 理性3", replaceIndex: 1, face: face("理性", 3) },
        { id: "weird", name: "异常理论", desc: "造势1 -> 诡思2", replaceIndex: 4, face: face("诡思", 2) },
      ],
    },
    {
      id: "s4",
      name: "薛定谔",
      avatar: "Assets/avatars/s4_schrodinger.png",
      specialty: ["想象", "诡思"],
      探索: 2, 生存: 1, 洞察: 1, 想象: 4, 理性: 2, 笔力: 2, 胆识: 2, 诡思: 2, 人脉: 1, 造势: 2,
      diceFaces: [face("想象", 2), face("诡思", 2), face("笔力", 1), face("洞察", 1), face("造势", 1), blankFace()],
      growthBranches: [
        { id: "column", name: "怪谈专栏", desc: "笔力1 -> 笔力2", replaceIndex: 2, face: face("笔力", 2) },
        { id: "vision", name: "半醒灵感", desc: "空面 -> 诡思1", replaceIndex: 5, face: face("诡思", 1) },
      ],
    },
    {
      id: "s5",
      name: "主角",
      avatar: "Assets/avatars/s5_protagonist.png",
      specialty: ["洞察", "笔力"],
      探索: 2, 生存: 1, 洞察: 4, 想象: 3, 理性: 3, 笔力: 4, 胆识: 2, 诡思: 1, 人脉: 2, 造势: 3,
      diceFaces: [face("洞察", 2), face("笔力", 2), face("造势", 2), face("理性", 1), face("人脉", 1), blankFace()],
      growthBranches: [
        { id: "editor", name: "主编判断", desc: "人脉1 -> 洞察2", replaceIndex: 4, face: face("洞察", 2) },
        { id: "headline", name: "封面标题", desc: "造势2 -> 造势3", replaceIndex: 2, face: face("造势", 3) },
      ],
    },
    {
      id: "s6",
      name: "伪人",
      avatar: "Assets/avatars/s6_impostor.png",
      specialty: ["人脉", "探索"],
      探索: 3, 生存: 2, 洞察: 2, 想象: 1, 理性: 1, 笔力: 1, 胆识: 2, 诡思: 2, 人脉: 4, 造势: 1,
      diceFaces: [face("人脉", 2), face("探索", 2), face("洞察", 1), face("诡思", 1), face("生存", 1), blankFace()],
      growthBranches: [
        { id: "contact", name: "像谁都认识", desc: "人脉2 -> 人脉3", replaceIndex: 0, face: face("人脉", 3) },
        { id: "mask", name: "身份错位", desc: "空面 -> 人脉1", replaceIndex: 5, face: face("人脉", 1) },
      ],
    },
    {
      id: "s7",
      name: "娜娜",
      avatar: "Assets/avatars/s7_nana.png",
      specialty: ["人脉", "洞察"],
      探索: 2, 生存: 2, 洞察: 3, 想象: 2, 理性: 3, 笔力: 2, 胆识: 2, 诡思: 0, 人脉: 4, 造势: 2,
      diceFaces: [face("人脉", 2), face("洞察", 2), face("理性", 1), face("笔力", 1), face("造势", 1), blankFace()],
      growthBranches: [
        { id: "interview", name: "温和套话", desc: "笔力1 -> 人脉2", replaceIndex: 3, face: face("人脉", 2) },
        { id: "clue", name: "细节记忆", desc: "理性1 -> 洞察2", replaceIndex: 2, face: face("洞察", 2) },
      ],
    },
    {
      id: "s8",
      name: "艾灵",
      avatar: "Assets/avatars/s8_ailing.png",
      specialty: ["理性", "诡思"],
      探索: 1, 生存: 2, 洞察: 3, 想象: 3, 理性: 4, 笔力: 2, 胆识: 2, 诡思: 3, 人脉: 1, 造势: 1,
      diceFaces: [face("理性", 2), face("诡思", 2), face("洞察", 2), face("生存", 1), face("笔力", 1), blankFace()],
      growthBranches: [
        { id: "sanity", name: "理性锚定", desc: "生存1 -> 理性2", replaceIndex: 3, face: face("理性", 2) },
        { id: "echo", name: "异常共鸣", desc: "笔力1 -> 诡思2", replaceIndex: 4, face: face("诡思", 2) },
      ],
    },
  ];

  const TEMP_STAFF_POOL = [
    {
      id: "temp_stringer",
      name: "临时线人",
      avatar: makeAvatar("线", "#16a34a", "#86efac"),
      temporary: true,
      specialty: ["人脉", "洞察"],
      探索: 1, 生存: 1, 洞察: 2, 想象: 1, 理性: 1, 笔力: 1, 胆识: 1, 诡思: 1, 人脉: 3, 造势: 1,
      diceFaces: [face("人脉", 2), face("人脉", 1), face("洞察", 1), face("探索", 1), blankFace(), blankFace()],
      growthBranches: [],
    },
  ];

  const TAG_LABEL = { sci: "科学纪实", occult: "神秘玄学", pop: "世俗流量" };
  const TYPE_TO_TAG = { sci: "Politics", occult: "Gossip", pop: "Shopping" };
  const COGNITION_NAME_POOL = ["局部重力异常假说", "群体记忆偏移假说", "生态能量流理论", "低频共振干预理论", "时空弯曲第一法则", "超个体意识假说"];
  const TOOL_NAME_POOL = ["DNA测序工具组", "光谱分析仪", "口述档案检索器", "夜视相机组"];
  const ROLL_FACES = ["✓", "×", "?", "", "", ""];
  const STAFF_BY_ID = new Map([...STAFF, ...TEMP_STAFF_POOL].map((s) => [s.id, s]));
  const STAFF_BASE_ORDER = new Map([...STAFF, ...TEMP_STAFF_POOL].map((s, index) => [s.id, index]));

  const el = {
    synInventory: null,
    synWorkbench: null,
    synSynthPreview: null,
    synReports: null,
    synthesisHint: null,
    storyList: null,
    slotList: null,
    liveStats: null,
    resultBox: null,
    toast: null,
  };

  function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
  }
  function rand(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }
  function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  function fmtMoney(v) {
    return `${v >= 0 ? "+" : ""}$${Math.round(v).toLocaleString("zh-CN")}`;
  }

  function addMacro(delta) {
    Object.keys(delta || {}).forEach((k) => {
      if (typeof macro[k] !== "number") return;
      macro[k] = clamp(macro[k] + delta[k], 0, 100);
    });
  }

  function addStaffEffect(staffId, stat, delta, duration, isPermanent) {
    state.staffEffects.push({
      id: `se_${Date.now()}_${Math.floor(Math.random() * 1e6)}`,
      staffId,
      stat,
      delta,
      duration: isPermanent ? "permanent" : duration || "week",
      startWeek: state.week,
    });
  }

  function getAllStaff() {
    return [...STAFF, ...TEMP_STAFF_POOL.filter((s) => state.tempStaffIds.includes(s.id))];
  }

  function findStaff(id) {
    if (!id) return null;
    return getAllStaff().find((s) => s.id === id) || STAFF_BY_ID.get(id) || null;
  }

  function faceText(f) {
    if (!f) return "空";
    if (f.black) return f.label || "黑骰";
    if (f.blank) return f.label || "空";
    const risk = f.risk ? " + 风险" : "";
    const special = f.special ? ` + ${f.special}` : "";
    return `${f.attr}${f.value || 0}${special}${risk}`;
  }

  function faceClass(f) {
    if (f && f.black) return "face-black";
    if (!f || f.blank) return "face-blank";
    const domain = ATTR_DOMAIN[f.attr] || "";
    return `face-${DOMAIN_CLASS[domain] || "misc"} ${f.risk ? "face-risk" : ""}`.trim();
  }

  function diceFacesForStaff(staff) {
    if (!staff) return [];
    const override = state.staffDiceOverrides[staff.id];
    if (override && Array.isArray(override.faces)) return override.faces;
    return staff.diceFaces || [];
  }

  function diceFacesHtml(faces, relevantNeed, rowClass) {
    const cls = rowClass ? ` ${rowClass}` : "";
    return `<div class="dice-face-row${cls}">${(faces || []).map((f) => {
      const relevant = f && f.attr && relevantNeed && relevantNeed[f.attr] != null ? " is-relevant" : "";
      return `<span class="dice-face ${faceClass(f)}${relevant}" title="${escapeHtml(faceText(f))}">${escapeHtml(faceText(f))}</span>`;
    }).join("")}</div>`;
  }

  function diceNetHtml(faces, relevantNeed, extraClass) {
    const list = (faces || []).slice(0, 6);
    while (list.length < 6) list.push(blankFace());
    const cls = extraClass ? ` ${extraClass}` : "";
    return `<div class="dice-net${cls}">${list.map((f, idx) => {
      const relevant = f && f.attr && relevantNeed && relevantNeed[f.attr] != null;
      const muted = !relevant && !(f && f.blank) ? " is-muted" : "";
      const rel = relevant ? " is-relevant" : "";
      return `<div class="dice-net-face pos-${idx} ${faceClass(f)}${rel}${muted}" title="${escapeHtml(faceText(f))}">
        <small>${idx + 1}</small>${escapeHtml(faceText(f))}
      </div>`;
    }).join("")}</div>`;
  }

  function faceStatsForNeed(faces, need) {
    const stats = { total: 0, relevant: 0, blank: 0, values: {}, relevantValues: 0 };
    (faces || []).forEach((f) => {
      stats.total += 1;
      if (!f || f.blank) {
        stats.blank += 1;
        return;
      }
      if (f.attr && need && need[f.attr] != null) {
        stats.relevant += 1;
        stats.relevantValues += f.value || 0;
        stats.values[f.attr] = (stats.values[f.attr] || 0) + (f.value || 0);
      }
    });
    return stats;
  }

  function fitLevelForStats(stats) {
    if (!stats || !stats.total) return "低";
    const ratio = stats.relevant / stats.total;
    if (ratio >= 0.5 && stats.blank <= 1) return "高";
    if (ratio >= 0.32) return "中";
    return "低";
  }

  function staffFitSummary(staff, need) {
    const stats = faceStatsForNeed(diceFacesForStaff(staff), need || {});
    const fit = fitLevelForStats(stats);
    const needKeys = Object.keys(need || {});
    const gaps = needKeys
      .map((k) => ({ k, gap: Math.max(0, (need[k] || 0) - (stats.values[k] || 0)) }))
      .filter((x) => x.gap > 0);
    const covers = needKeys
      .filter((k) => (stats.values[k] || 0) > 0)
      .map((k) => `${k}+${stats.values[k]}`);
    return {
      fit,
      stats,
      covers,
      gaps,
      line: `适配：${fit} · 相关面 ${stats.relevant}/${stats.total || 6} · 空面 ${stats.blank}`,
      contribution: covers.length ? covers.join(" / ") : "无相关面",
      feel: fit === "高"
        ? "稳定命中本任务需求"
        : fit === "中"
          ? "可补关键项，但有空转风险"
          : "偏科或空转，建议换人补面",
    };
  }

  function specialtyHtml(staff) {
    return (staff.specialty || [])
      .map((a) => `<span class="attr-chip attr-${DOMAIN_CLASS[ATTR_DOMAIN[a]] || "misc"}">${escapeHtml(a)}</span>`)
      .join("");
  }

  function staffDetailHtml(staff, relevantNeed) {
    if (!staff) return "";
    const fit = staffFitSummary(staff, relevantNeed || {});
    const branches = (staff.growthBranches || []).map((b) => `
      <div class="growth-branch">
        <strong>${escapeHtml(b.name)}</strong>
        <span>${escapeHtml(b.desc || "")}</span>
      </div>`).join("");
    return `<div class="staff-detail-card">
      <div class="staff-detail-head">
        <img src="${staff.avatar}" alt="${escapeHtml(staff.name)}"/>
        <div>
          <div class="staff-detail-name">${escapeHtml(staff.name)}${staff.temporary ? "（临时）" : ""}</div>
          <div class="staff-detail-spec">${specialtyHtml(staff)}</div>
        </div>
      </div>
      <div class="staff-fit-verdict">
        <strong>${escapeHtml(fit.line)}</strong>
        <div style="margin-top:4px;">当前任务可补：${escapeHtml(fit.contribution)}；${escapeHtml(fit.feel)}。</div>
      </div>
      <div class="staff-detail-section">
        <div class="staff-detail-label">当前任务：${escapeHtml(Object.keys(relevantNeed || {}).map((k) => `${k}${relevantNeed[k]}`).join(" / ") || "无指定需求")}</div>
        ${diceNetHtml(diceFacesForStaff(staff), relevantNeed)}
        <div class="staff-fit-badges">
          <span class="staff-fit-badge">相关面 ${fit.stats.relevant}/6</span>
          <span class="staff-fit-badge">空面 ${fit.stats.blank}</span>
          <span class="staff-fit-badge">${escapeHtml(fit.feel)}</span>
        </div>
      </div>
      <div class="staff-detail-section">
        <div class="staff-detail-label">属性总览</div>
        <div class="staff-detail-attrs">${ATTR_KEYS.map((k) => `<span>${k} ${getStaffValue(staff, k)}</span>`).join("")}</div>
      </div>
      <details class="staff-upgrade-fold">
        <summary>下次升级分支（预览）</summary>
        ${branches || `<span class="tip-inline">暂无升级分支。</span>`}
      </details>
    </div>`;
  }

  function previewUpgradeFaces(staff, branch) {
    const faces = diceFacesForStaff(staff).map((f) => ({ ...f }));
    if (!branch) return faces;
    if (branch.replaceIndex != null && branch.face) faces[branch.replaceIndex] = branch.face;
    else if (branch.face && faces.length < 6) faces.push(branch.face);
    return faces.slice(0, 6);
  }

  function showUpgradeModal(staff) {
    if (!staff || staff.temporary) return;
    const branches = staff.growthBranches || [];
    const body = branches.length
      ? branches.map((b, idx) => `<div class="upgrade-option">
          <h4>${escapeHtml(b.name)}</h4>
          <p>${escapeHtml(b.desc || "")}</p>
          <div class="upgrade-compare">
            <div><strong>当前</strong>${diceFacesHtml(diceFacesForStaff(staff), {})}</div>
            <div><strong>升级后</strong>${diceFacesHtml(previewUpgradeFaces(staff, b), {})}</div>
          </div>
          <button type="button" data-upgrade-branch="${idx}" class="primary">选择此分支</button>
        </div>`).join("")
      : `<p>暂无可用升级分支。</p>`;
    showConfirmPopup(`${staff.name} · 升级预览`, `<div class="upgrade-modal">${body}</div>`, "每次升级都会改变骰面").then(() => {});
    setTimeout(() => {
      document.querySelectorAll("[data-upgrade-branch]").forEach((btn) => {
        btn.onclick = () => {
          const branch = branches[Number(btn.getAttribute("data-upgrade-branch"))];
          if (!branch) return;
          state.staffDiceOverrides[staff.id] = { faces: previewUpgradeFaces(staff, branch) };
          state.staffLevels[staff.id] = (state.staffLevels[staff.id] || 1) + 1;
          const ok = document.getElementById("confirmPopupOk");
          if (ok) ok.click();
          log(`${staff.name} 升级：${branch.name}`);
          if (state.view === "setup") renderSetup();
        };
      });
    }, 0);
  }

  function cleanupWeekScopedEffects() {
    state.staffEffects = state.staffEffects.filter((e) => e.duration === "permanent" || e.startWeek >= state.week);
    state.dynamicNodes = state.dynamicNodes.filter((x) => x.expireWeek >= state.week);
  }

  function getStaffValue(person, stat) {
    let v = person[stat] || 0;
    for (const eff of state.staffEffects) {
      if (eff.staffId === person.id && eff.stat === stat) v += eff.delta;
    }
    return Math.max(0, v);
  }

  function missionMaxStaff(m) {
    if (m && Number.isFinite(m.maxStaffOverride)) return m.maxStaffOverride;
    return m && m.isBlackDiceTask ? 5 : 3;
  }

  function rollOneDie(faces) {
    const list = faces && faces.length ? faces : [blankFace()];
    return { face: list[Math.floor(Math.random() * list.length)] || blankFace(), faceIndex: 0 };
  }

  function rollCharacterDice(mission, staffIds, toolDiceIds) {
    const rolls = [];
    (staffIds || []).forEach((id) => {
      const staff = findStaff(id);
      if (!staff) return;
      const faces = diceFacesForStaff(staff);
      const idx = Math.floor(Math.random() * Math.max(1, faces.length));
      rolls.push({
        id: `roll_${id}_${rolls.length}`,
        kind: staff.temporary ? "tempStaff" : "staff",
        staffId: id,
        staffName: staff.name,
        avatar: staff.avatar,
        faceIndex: idx,
        face: faces[idx] || blankFace(),
        locked: !!((faces[idx] || {}).noReroll || (mission && mission.noReroll)),
      });
    });
    const toolIds = Array.isArray(toolDiceIds) ? toolDiceIds : (state.selectedToolDiceIds || []);
    toolIds.forEach((id) => {
      const tool = state.toolDiceInventory.find((x) => x.id === id);
      if (!tool) return;
      const idx = Math.floor(Math.random() * Math.max(1, tool.faces.length));
      rolls.push({
        id: `roll_${id}_${rolls.length}`,
        kind: "tool",
        toolId: id,
        staffName: tool.name,
        avatar: "",
        faceIndex: idx,
        face: tool.faces[idx] || blankFace(),
        locked: true,
      });
    });
    return rolls;
  }

  function makeBlackFace(label, effect) {
    return { black: true, label, effect };
  }

  function blackDiceForMission(mission, baseRolls) {
    if (!mission || !mission.isBlackDiceTask) return [];
    if (mission.blackDiceTheme === "bus330") {
      const list = [
        { id: "black_bus_mix", theme: "bus330", face: makeBlackFace("混入", "mix"), desc: "一颗负面乘客骰混入己方骰池。" },
        { id: "black_bus_replace", theme: "bus330", face: makeBlackFace("替座", "replace"), desc: "一颗角色骰被可疑乘客替换。" },
      ];
      return list;
    }
    if (mission.blackDiceTheme === "ball_lightning") {
      return [
        { id: "black_light_sense", theme: "ball_lightning", face: makeBlackFace("感应", "sense"), desc: "复制一个己方成功属性为黑骰压力。" },
        { id: "black_light_ground", theme: "ball_lightning", face: makeBlackFace("接地", "ground"), desc: "最高点骰成为导体，成功也会带来反噬。" },
      ];
    }
    return [{ id: "black_generic", theme: "generic", face: makeBlackFace("干扰", "pressure"), desc: "黑骰增加本次任务压力。" }];
  }

  function applyBlackDiceToRolls(mission, rolls, blackDice) {
    const next = rolls.slice();
    const notes = [];
    const pressure = {};
    (blackDice || []).forEach((b, idx) => {
      const effect = b.face && b.face.effect;
      if (mission.blackDiceTheme === "bus330" && effect === "mix") {
        next.push({
          id: `black_mix_${idx}`,
          kind: "black",
          staffName: "可疑乘客",
          avatar: "",
          face: { attr: "诡思", value: -1, black: true, label: "鬼乘客" },
          locked: true,
          black: true,
        });
        notes.push("黑骰·混入：可疑乘客骰混进了你的骰池。");
      } else if (mission.blackDiceTheme === "bus330" && effect === "replace") {
        const targetIndex = next.findIndex((r) => r.kind === "staff" || r.kind === "tempStaff");
        if (targetIndex >= 0) {
          const target = next[targetIndex];
          next[targetIndex] = {
            id: `black_replace_${idx}`,
            kind: "black",
            staffName: `${target.staffName}？`,
            avatar: target.avatar,
            face: { attr: "胆识", value: -2, black: true, label: "替座" },
            locked: true,
            black: true,
          };
          notes.push(`黑骰·替座：${target.staffName} 的骰子被替换成了可疑乘客。`);
        }
      } else if (mission.blackDiceTheme === "ball_lightning" && effect === "sense") {
        const best = next.filter((r) => r.face && r.face.attr && !r.face.blank).sort((a, b) => (b.face.value || 0) - (a.face.value || 0))[0];
        if (best) {
          pressure[best.face.attr] = (pressure[best.face.attr] || 0) + Math.max(1, best.face.value || 1);
          notes.push(`黑骰·感应：异常复制了 ${best.staffName} 的 ${faceText(best.face)}。`);
        }
      } else if (mission.blackDiceTheme === "ball_lightning" && effect === "ground") {
        const best = next.filter((r) => r.face && r.face.attr && !r.face.blank).sort((a, b) => (b.face.value || 0) - (a.face.value || 0))[0];
        if (best) {
          best.grounded = true;
          notes.push(`黑骰·接地：${best.staffName} 的骰子成为导体，成功会带来狂性回流。`);
        }
      } else {
        pressure.探索 = (pressure.探索 || 0) + 1;
        notes.push("黑骰·干扰：本次任务压力上升。");
      }
    });
    return { rolls: next, pressure, notes };
  }

  function rollContribution(rolls, selectedIds) {
    const selected = new Set(selectedIds || []);
    const sum = {};
    (rolls || []).forEach((r) => {
      if (!selected.has(r.id)) return;
      const f = r.face || {};
      if (!f.attr || f.blank) return;
      sum[f.attr] = (sum[f.attr] || 0) + (f.value || 0);
    });
    Object.keys(sum).forEach((k) => {
      if (sum[k] < 0) sum[k] = 0;
    });
    return sum;
  }

  function blackPressureTotal(pressure) {
    return Object.values(pressure || {}).reduce((a, b) => a + (b || 0), 0);
  }

  function blackDiceTier(mission, success, contribution, pressure, selectedRolls) {
    const target = needTargetValue(mission.need || {});
    const gotTotal = Object.values(contribution || {}).reduce((a, b) => a + (b || 0), 0);
    const pressureTotal = blackPressureTotal(pressure);
    const blackSelected = (selectedRolls || []).some((r) => r.black);
    if (success && gotTotal >= target + 2 && pressureTotal <= 1 && !blackSelected) return "大成功";
    if (success) return "成功";
    if (!success && (blackSelected || pressureTotal >= 3)) return "大失败";
    return "失败";
  }

  function needTargetValue(need) {
    const keys = Object.keys(need || {});
    if (!keys.length) return 0;
    const total = keys.reduce((acc, key) => acc + Math.max(0, need[key] || 0), 0);
    const floor = total >= 4 ? 2 : 1;
    return Math.max(floor, Math.ceil(total / 3));
  }

  function contributionTotalForNeed(need, sum) {
    return Object.keys(need || {}).reduce((acc, key) => acc + Math.max(0, (sum && sum[key]) || 0), 0);
  }

  function needMetByContribution(need, sum) {
    const target = needTargetValue(need);
    if (!target) return true;
    return contributionTotalForNeed(need, sum) >= target;
  }

  function successChanceForNeed(need, faceLists) {
    const target = needTargetValue(need);
    if (!target) return 1;
    const keys = new Set(Object.keys(need || {}));
    const sources = (faceLists || []).filter((faces) => faces && faces.length);
    if (!sources.length) return 0;
    let dp = Array(target + 1).fill(0);
    dp[0] = 1;
    let total = 1;
    sources.forEach((faces) => {
      const next = Array(target + 1).fill(0);
      const list = faces && faces.length ? faces : [blankFace()];
      total *= list.length;
      list.forEach((face) => {
        const value = face && !face.blank && !face.black && face.attr && keys.has(face.attr)
          ? Math.max(0, face.value || 0)
          : 0;
        dp.forEach((count, cur) => {
          if (!count) return;
          next[Math.min(target, cur + value)] += count;
        });
      });
      dp = next;
    });
    return total ? dp[target] / total : 0;
  }

  function formatChance(chance) {
    if (!Number.isFinite(chance)) return "未知";
    return `${Math.round(Math.max(0, Math.min(1, chance)) * 100)}%`;
  }

  function formatDisplayedChanceLift(chance, baseline) {
    if (!Number.isFinite(chance) || !Number.isFinite(baseline)) return "";
    const delta = Math.round(chance * 100) - Math.round(baseline * 100);
    return delta > 0 ? `+${delta}%` : "";
  }

  function autoSelectRollsForNeed(rolls, need) {
    const ids = [];
    const target = needTargetValue(need);
    let total = 0;
    const relevant = (rolls || []).filter((r) => r.face && !r.black && !r.face.black && r.face.attr && need && need[r.face.attr] != null && (r.face.value || 0) > 0);
    relevant
      .sort((a, b) => (b.face.value || 0) - (a.face.value || 0))
      .forEach((r) => {
        if (target && total >= target) return;
        ids.push(r.id);
        total += Math.max(0, r.face.value || 0);
      });
    return ids;
  }

  function teamDiceNeedStats(mission, staffIds) {
    const need = (mission && mission.need) || {};
    const needKeys = Object.keys(need);
    const relevant = {};
    const values = {};
    let totalFaces = 0;
    let relevantFaces = 0;
    let blankFaces = 0;
    let contributingStaff = 0;
    let nonContributingStaff = 0;
    const faceLists = [];
    (staffIds || []).forEach((id) => {
      const staff = findStaff(id);
      if (!staff) return;
      const faces = diceFacesForStaff(staff);
      faceLists.push(faces);
      let staffRelevantFaces = 0;
      faces.forEach((face) => {
        totalFaces += 1;
        if (!face || face.blank) {
          blankFaces += 1;
          return;
        }
        if (face.attr && need[face.attr] != null) {
          relevant[face.attr] = (relevant[face.attr] || 0) + 1;
          relevantFaces += 1;
          staffRelevantFaces += 1;
          values[face.attr] = (values[face.attr] || 0) + (face.value || 0);
        }
      });
      if (staffRelevantFaces > 0) contributingStaff += 1;
      else nonContributingStaff += 1;
    });
    const gaps = needKeys
      .map((k) => ({ k, gap: Math.max(0, (need[k] || 0) - (values[k] || 0)) }))
      .filter((x) => x.gap > 0);
    const needValue = needKeys.reduce((sum, k) => sum + (need[k] || 0), 0);
    const coveredValue = needKeys.reduce((sum, k) => sum + Math.min(values[k] || 0, need[k] || 0), 0);
    const coverage = needValue > 0 ? coveredValue / needValue : 0;
    return {
      relevant,
      values,
      totalFaces,
      relevantFaces,
      blankFaces,
      contributingStaff,
      nonContributingStaff,
      gaps,
      needValue,
      coveredValue,
      coverage,
      targetValue: needTargetValue(need),
      successChance: successChanceForNeed(need, faceLists),
    };
  }

  function riskLabelForMission(mission, staffIds) {
    const selectedCount = (staffIds || []).length;
    if (!selectedCount) return "高";
    const stats = teamDiceNeedStats(mission, staffIds);
    if (!stats.relevantFaces) return "高";
    if (stats.successChance >= 0.55) return "低";
    if (stats.successChance >= 0.3) return "中";
    return "高";
  }

  function addDynamicNode(regionId, node, durationWeeks) {
    state.dynamicNodes.push({
      regionId,
      expireWeek: state.week + Math.max(0, (durationWeeks || 1) - 1),
      node: { ...node },
    });
  }

  function getRegionNodes(region) {
    const dyn = state.dynamicNodes.filter((x) => x.regionId === region.id).map((x) => x.node);
    return [...region.nodes, ...dyn];
  }

  function initRegionLeadEvents() {
    state.regionLeadEvents = {};
    for (const r of REGIONS) {
      const pool = [
        {
          id: `lead_${r.id}_${state.week}_1`,
          title: `${r.name} 民间传言：异常目击`,
          reliability: 0.52,
          investigated: false,
          assigned: false,
          result: "",
          spawn: () => ({
            id: `leadnode_${r.id}_${state.week}_1`,
            kind: "temp",
            name: `线索追查：${r.name}临时异动`,
            days: 2,
            need: { 人脉: 2, 洞察: 2 },
            tags: ["pop", "occult"],
            difficulty: "normal",
            enemyAttr: 2,
            deadlineDay: 4,
            chain: null,
          }),
          durationWeeks: 1,
        },
        {
          id: `lead_${r.id}_${state.week}_2`,
          title: `${r.name} 非正式研究记录`,
          reliability: 0.65,
          investigated: false,
          assigned: false,
          result: "",
          spawn: () => ({
            id: `leadnode_${r.id}_${state.week}_2`,
            kind: "permanent",
            name: `新常驻：${r.name}研究遗址`,
            days: 3,
            need: { 探索: 5, 理性: 3 },
            tags: ["sci"],
            difficulty: "hard",
            enemyAttr: 3,
            chain: null,
          }),
          durationWeeks: 6,
        },
      ];
      state.regionLeadEvents[r.id] = [rand(pool)];
    }
  }

  function investigateRegionLead(regionId, leadId) {
    const leads = state.regionLeadEvents[regionId] || [];
    const lead = leads.find((x) => x.id === leadId);
    if (!lead || lead.investigated || state.missionResolving || state.processingDayTick) return;
    if (lead.assigned) {
      const queued = findActiveMissionByLead(regionId, leadId);
      if (queued) openQueuedMission(queued);
      return;
    }
    state.mission = {
      id: `lead_mission_${lead.id}`,
      kind: "lead",
      missionType: "leadInvestigation",
      regionId,
      leadId: lead.id,
      name: `线索调查：${lead.title}`,
      days: lead.days || 2,
      need: lead.need || { 人脉: 2, 洞察: 2 },
      tags: lead.tags || ["sci", "occult"],
      difficulty: lead.difficulty || (lead.reliability >= 0.65 ? "normal" : "hard"),
      enemyAttr: lead.enemyAttr != null ? lead.enemyAttr : (lead.reliability >= 0.65 ? 2 : 3),
      useCharacterDice: true,
      chain: null,
    };
    lead.assigned = true;
    state.selectedStaffIds = [];
    renderSetup();
    setView("setup");
  }

  function log(msg) {
    state.log.unshift(`[第${state.week}周 余${state.day}日] ${msg}`);
    if (state.log.length > 40) state.log.pop();
    const logEl = document.getElementById("log");
    if (logEl) logEl.innerHTML = state.log.map((t) => `<p>${escapeHtml(t)}</p>`).join("");
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function week1TutorialActive() {
    return state.week === 1 && !state.paperLabMode;
  }

  /** bodyHtmlOrPages：单页 HTML 字符串，或最多 5 页字符串数组 */
  function showSoftTutorialModal(key, title, bodyHtmlOrPages, gateFn) {
    return new Promise((resolve) => {
      if (tutorialsGloballyDisabled()) {
        state.tutorialSoftW1[key] = true;
        resolve();
        return;
      }
      if (!gateFn() || state.tutorialSoftW1[key]) {
        resolve();
        return;
      }
      const wrap = document.getElementById("tutorialSoftModal");
      const ttl = document.getElementById("tutorialSoftTitle");
      const body = document.getElementById("tutorialSoftBody");
      const btnPrev = document.getElementById("tutorialSoftPrev");
      const btnNext = document.getElementById("tutorialSoftNext");
      const pageInd = document.getElementById("tutorialSoftPageInd");
      const firstRow = document.getElementById("tutorialSoftFirstRow");
      const neverCb = document.getElementById("tutorialSoftNever");
      if (!wrap || !ttl || !body || !btnNext) {
        resolve();
        return;
      }
      let pages = Array.isArray(bodyHtmlOrPages)
        ? bodyHtmlOrPages.slice(0, 5).filter((p) => p && String(p).trim())
        : [bodyHtmlOrPages || ""].filter((p) => p && String(p).trim());
      if (!pages.length) pages = ["<p style=\"margin:0;\">（暂无说明）</p>"];
      let pageIndex = 0;

      const showFirstTimeRow = tutorialIntroOfferStillPending();
      if (firstRow) {
        firstRow.classList.toggle("hidden", !showFirstTimeRow);
        if (neverCb) neverCb.checked = false;
      }

      const detachAll = () => {
        btnNext.removeEventListener("click", onNext);
        if (btnPrev) btnPrev.removeEventListener("click", onPrev);
        wrap.removeEventListener("click", onMask);
      };

      const finishIntroMeta = () => {
        markTutorialIntroOfferFinished();
        if (neverCb && neverCb.checked) setTutorialsGloballyDisabled();
      };

      const done = () => {
        detachAll();
        wrap.classList.add("hidden");
        state.tutorialSoftW1[key] = true;
        finishIntroMeta();
        resolve();
      };

      const renderPage = () => {
        ttl.textContent = title || "提示";
        body.innerHTML = pages[pageIndex] || "";
        const n = pages.length;
        if (pageInd) {
          pageInd.textContent = n > 1 ? `第 ${pageIndex + 1} / ${n} 页` : "";
          pageInd.classList.toggle("hidden", n <= 1);
        }
        if (btnPrev) {
          btnPrev.classList.toggle("hidden", n <= 1 || pageIndex <= 0);
          btnPrev.disabled = pageIndex <= 0;
        }
        const last = pageIndex >= n - 1;
        btnNext.textContent = last ? "知道了" : "下一页";
      };

      const onNext = () => {
        if (pageIndex < pages.length - 1) {
          pageIndex += 1;
          renderPage();
        } else {
          done();
        }
      };

      const onPrev = () => {
        if (pageIndex > 0) {
          pageIndex -= 1;
          renderPage();
        }
      };

      const onMask = (ev) => {
        if (ev.target === wrap) done();
      };

      renderPage();
      wrap.classList.remove("hidden");
      btnNext.addEventListener("click", onNext);
      if (btnPrev) btnPrev.addEventListener("click", onPrev);
      wrap.addEventListener("click", onMask);
    });
  }

  function showWeek1SoftTutorialModal(key, title, bodyHtmlOrPages) {
    return showSoftTutorialModal(key, title, bodyHtmlOrPages, week1TutorialActive);
  }

  async function runPaperLabOnboarding() {
    if (!state.paperLabMode) return;
    if (tutorialsGloballyDisabled()) return;
    await showSoftTutorialModal("lab_fullGuide", "新手引导 · 报刊组版实验", LAB_FULL_GUIDE_PAGES, () => state.paperLabMode);
    openPaperDemoLab();
  }

  async function runWeek1EditorialOnboarding() {
    if (!week1TutorialActive() || state.phase !== "editorial" || state.paperLabMode) return;
    if (tutorialsGloballyDisabled()) return;
    await showWeek1SoftTutorialModal(
      "w1_editorial",
      "第一周 · 编辑部组版",
      [
        `${tutorialSoftFigure(
          "Assets/tutorial-editorial-guide.svg",
          "组版示意：故事库拖入报纸版位",
          "示意：左为故事库；中为报纸版位（头版 / 内页等）。",
        )}<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">怎么摆版？</h4>
          <p class="tutorial-soft-lead">成稿已备好：把左侧<strong>故事库</strong>里的卡片<strong>拖进</strong>中间报纸版位。</p>
          <ul class="tutorial-soft-ul">
            <li><strong>头版</strong>最吸睛；<strong>内页</strong>略逊，但都算进本期曝光。</li>
          </ul>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">收尾</h4>
          <ul class="tutorial-soft-ul">
            <li>版式满意后点<strong>结算本期</strong>，查看销量与利润。</li>
            <li>确认后直接开始摆版；需要重来时可用<strong>清空版面</strong>。</li>
          </ul>
          <p class="tutorial-soft-note">本周内本提示只出现一次。</p>
        </div>`,
      ],
    );
  }

  async function runWeek1SynthesisOnboarding() {
    if (!week1TutorialActive() || state.phase !== "synthesis" || state.paperLabMode) return;
    if (tutorialsGloballyDisabled()) return;
    await showWeek1SoftTutorialModal(
      "w1_synthesis",
      "第一周 · 故事合成台",
      [
        `${tutorialSoftFigure(
          "Assets/tutorial-synth-guide.svg",
          "合成台示意：左侧素材拖入右侧红金蓝槽位",
          "示意：左为素材区；右为公开报道（红/金）与内审定调（蓝）槽位。",
        )}<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">合成台在做什么？</h4>
          <p class="tutorial-soft-lead">左侧是您带回的<strong>现象、认知、情报、工具</strong>（认知需先经<strong>内审</strong>生成）；右侧卡槽决定本周要出哪类稿件。</p>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">槽位颜色</h4>
          <ul class="tutorial-soft-ul">
            <li><strong>公开报道</strong>：按<strong>红色</strong>槽放入必需素材；<strong>金色虚线</strong>槽可放工具，略抬成功率。<strong>抢先快讯</strong>不需认知。</li>
            <li><strong>内审定调</strong>（蓝色）：现象→认知，可选<strong>主笔</strong>提高高等级概率（承担 SAN）；不直接上版。</li>
          </ul>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">爆炸性新闻</h4>
          <p class="tutorial-soft-lead">需要专用<strong>爆料卡</strong>（左侧「爆料卡」分类；来自探索，无法靠合成「做出来」）。</p>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">演示</h4>
          <p class="tutorial-soft-lead">关窗后会自动播<strong>拖拽示意</strong>；需要时点「合成拖拽演示」。</p>
          <p class="tutorial-soft-note">本周内本提示只出现一次。</p>
        </div>`,
      ],
    );
    if (!week1TutorialActive() || state.phase !== "synthesis" || state.paperLabMode) return;
    openSynthDemoLab();
  }

  function scheduleWeek1SoftTutorial(key, title, bodyHtmlOrPages) {
    if (tutorialsGloballyDisabled() || !week1TutorialActive() || state.tutorialSoftW1[key]) return;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (tutorialsGloballyDisabled() || !week1TutorialActive() || state.tutorialSoftW1[key]) return;
        showWeek1SoftTutorialModal(key, title, bodyHtmlOrPages);
      });
    });
  }

  let paperDemoRaf = null;
  let paperDemoGen = 0;
  let paperDemoAutoTimer = null;
  const PAPER_DEMO_AUTO_INTERVAL_MS = 1000;

  function cancelPaperDemoAnim() {
    if (paperDemoRaf != null) {
      cancelAnimationFrame(paperDemoRaf);
      paperDemoRaf = null;
    }
  }

  function clearPaperDemoAutoTimer() {
    if (paperDemoAutoTimer != null) {
      clearTimeout(paperDemoAutoTimer);
      paperDemoAutoTimer = null;
    }
  }

  function schedulePaperDemoAutoReplay() {
    clearPaperDemoAutoTimer();
    const wrap = document.getElementById("paperDemoLabModal");
    if (!wrap || wrap.classList.contains("hidden")) return;
    paperDemoAutoTimer = window.setTimeout(() => {
      paperDemoAutoTimer = null;
      const w = document.getElementById("paperDemoLabModal");
      if (!w || w.classList.contains("hidden")) return;
      playPaperDemoLab();
    }, PAPER_DEMO_AUTO_INTERVAL_MS);
  }

  function playPaperDemoLab() {
    const stage = document.getElementById("paperDemoStage");
    const flyer = document.getElementById("paperDemoFlyer");
    const slot = document.getElementById("paperDemoTargetSlot");
    const chip = document.getElementById("paperDemoSourceChip");
    const emptyHint = document.getElementById("paperDemoEmptyHint");
    const landed = document.getElementById("paperDemoLandedBlock");
    if (!stage || !flyer || !slot || !chip) return;
    clearPaperDemoAutoTimer();
    chip.innerHTML = PAPER_DEMO_SOURCE_INNER_HTML;
    if (emptyHint) emptyHint.classList.remove("hidden");
    if (landed) landed.classList.add("hidden");
    cancelPaperDemoAnim();
    stage.classList.remove("paper-demo-fx-b", "paper-demo-running");
    flyer.classList.remove("paper-demo-flyer-visible", "paper-demo-flyer-b");
    slot.classList.remove("paper-demo-slot-flash", "paper-demo-slot-filled");
    chip.classList.remove("paper-demo-source-pulse");
    flyer.innerHTML = `<div class="nm-story-title" style="font-size:12px;line-height:1.3;">示例报道：港区异常回波</div>`;
    flyer.style.transform = "";
    flyer.style.opacity = "";
    void stage.offsetWidth;

    const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      slot.classList.add("paper-demo-slot-filled");
      if (emptyHint) emptyHint.classList.add("hidden");
      if (landed) landed.classList.remove("hidden");
      schedulePaperDemoAutoReplay();
      return;
    }

    const myGen = ++paperDemoGen;
    stage.classList.add("paper-demo-fx-b");
    const sr = stage.getBoundingClientRect();
    const cr = chip.getBoundingClientRect();
    const targetEl = emptyHint && emptyHint.isConnected ? emptyHint : slot;
    const tr = targetEl.getBoundingClientRect();
    const x0 = cr.left - sr.left + cr.width / 2;
    const y0 = cr.top - sr.top + cr.height / 2;
    const x1 = tr.left - sr.left + tr.width / 2;
    const y1 = tr.top - sr.top + tr.height / 2;
    flyer.classList.add("paper-demo-flyer-visible", "paper-demo-flyer-b");
    chip.classList.add("paper-demo-source-pulse");
    const t0 = performance.now();
    const dur = 880;
    const ease = (t) => 1 - Math.pow(1 - t, 3);

    const finishLand = () => {
      chip.classList.remove("paper-demo-source-pulse");
      slot.classList.add("paper-demo-slot-flash", "paper-demo-slot-filled");
      if (emptyHint) emptyHint.classList.add("hidden");
      if (landed) landed.classList.remove("hidden");
    };

    const step = (now) => {
      if (myGen !== paperDemoGen) return;
      const t = Math.min(1, (now - t0) / dur);
      const e = ease(t);
      const x = x0 + (x1 - x0) * e;
      const y = y0 + (y1 - y0) * e;
      const sc = 1 - 0.14 * e;
      flyer.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%) scale(${sc})`;
      flyer.style.opacity = String(0.38 + 0.62 * e);
      if (t < 1) {
        paperDemoRaf = requestAnimationFrame(step);
      } else {
        paperDemoRaf = null;
        finishLand();
        schedulePaperDemoAutoReplay();
      }
    };
    flyer.style.transform = `translate(${x0}px, ${y0}px) translate(-50%, -50%) scale(1)`;
    flyer.style.opacity = "1";
    paperDemoRaf = requestAnimationFrame(step);
  }

  function openPaperDemoLab() {
    const wrap = document.getElementById("paperDemoLabModal");
    if (!wrap) return;
    clearPaperDemoAutoTimer();
    cancelPaperDemoAnim();
    wrap.classList.remove("hidden");
    requestAnimationFrame(() => playPaperDemoLab());
  }

  function closePaperDemoLab() {
    const wrap = document.getElementById("paperDemoLabModal");
    if (wrap) wrap.classList.add("hidden");
    clearPaperDemoAutoTimer();
    cancelPaperDemoAnim();
    paperDemoGen += 1;
  }

  let paperDemoLabBound = false;
  function bindPaperDemoLabUi() {
    if (paperDemoLabBound) return;
    const wrap = document.getElementById("paperDemoLabModal");
    const replay = document.getElementById("paperDemoReplay");
    const closeBtn = document.getElementById("paperDemoClose");
    if (!wrap || !replay || !closeBtn) return;
    paperDemoLabBound = true;
    replay.onclick = () => playPaperDemoLab();
    closeBtn.onclick = () => closePaperDemoLab();
    wrap.addEventListener("click", (ev) => {
      if (ev.target === wrap) closePaperDemoLab();
    });
  }

  let synthDemoRaf = null;
  let synthDemoGen = 0;
  let synthDemoAutoTimer = null;
  const SYNTH_DEMO_AUTO_INTERVAL_MS = 2200;

  function cancelSynthDemoAnim() {
    if (synthDemoRaf != null) {
      cancelAnimationFrame(synthDemoRaf);
      synthDemoRaf = null;
    }
  }

  function clearSynthDemoAutoTimer() {
    if (synthDemoAutoTimer != null) {
      clearTimeout(synthDemoAutoTimer);
      synthDemoAutoTimer = null;
    }
  }

  function scheduleSynthDemoAutoReplay() {
    clearSynthDemoAutoTimer();
    const wrap = document.getElementById("synthDemoLabModal");
    if (!wrap || wrap.classList.contains("hidden")) return;
    synthDemoAutoTimer = window.setTimeout(() => {
      synthDemoAutoTimer = null;
      const w = document.getElementById("synthDemoLabModal");
      if (!w || w.classList.contains("hidden")) return;
      playSynthDemoLab();
    }, SYNTH_DEMO_AUTO_INTERVAL_MS);
  }

  function playSynthDemoLab() {
    const stage = document.getElementById("synthDemoStage");
    const flyer = document.getElementById("synthDemoFlyer");
    const phenCard = document.getElementById("synthDemoCardPhen");
    const intelCard = document.getElementById("synthDemoCardIntel");
    const slotPhen = document.getElementById("synthDemoDropPhen");
    const slotIntel = document.getElementById("synthDemoDropIntel");
    const slotTool = document.getElementById("synthDemoDropTool");
    const resultEl = document.getElementById("synthDemoResult");
    if (!stage || !flyer || !phenCard || !intelCard || !slotPhen || !slotIntel) return;
    clearSynthDemoAutoTimer();
    cancelSynthDemoAnim();
    slotPhen.innerHTML = `<span class="syn-demo-placeholder">拖入现象</span>`;
    slotIntel.innerHTML = `<span class="syn-demo-placeholder">拖入情报</span>`;
    if (slotTool) slotTool.innerHTML = `<span class="syn-demo-placeholder">工具（可选）</span>`;
    if (resultEl) {
      resultEl.textContent = "";
      resultEl.classList.remove("synth-demo-result-flash");
    }
    flyer.classList.remove("synth-demo-flyer-visible");
    flyer.style.transform = "";
    flyer.style.opacity = "";
    phenCard.classList.remove("synth-demo-source-pulse");
    intelCard.classList.remove("synth-demo-source-pulse");
    stage.classList.remove("synth-demo-running");
    void stage.offsetWidth;

    const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      slotPhen.innerHTML = `<div class="syn-demo-chip">现象样本</div>`;
      slotIntel.innerHTML = `<div class="syn-demo-chip">情报摘要</div>`;
      if (resultEl) {
        resultEl.textContent = "执行合成 · 示意（演示不消耗真实素材）";
        resultEl.classList.add("synth-demo-result-flash");
      }
      scheduleSynthDemoAutoReplay();
      return;
    }

    const myGen = ++synthDemoGen;
    stage.classList.add("synth-demo-running");
    const sr = stage.getBoundingClientRect();
    const ease = (t) => 1 - Math.pow(1 - t, 3);
    const dur = 700;

    const runFly = (sourceEl, slotEl, chipHtml, onDone) => {
      const cr = sourceEl.getBoundingClientRect();
      const tr = slotEl.getBoundingClientRect();
      const x0 = cr.left - sr.left + cr.width / 2;
      const y0 = cr.top - sr.top + cr.height / 2;
      const x1 = tr.left - sr.left + tr.width / 2;
      const y1 = tr.top - sr.top + tr.height / 2;
      flyer.innerHTML = chipHtml;
      flyer.classList.add("synth-demo-flyer-visible");
      sourceEl.classList.add("synth-demo-source-pulse");
      const t0 = performance.now();
      const step = (now) => {
        if (myGen !== synthDemoGen) return;
        const t = Math.min(1, (now - t0) / dur);
        const e = ease(t);
        const x = x0 + (x1 - x0) * e;
        const y = y0 + (y1 - y0) * e;
        const sc = 1 - 0.12 * e;
        flyer.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%) scale(${sc})`;
        flyer.style.opacity = String(0.38 + 0.62 * e);
        if (t < 1) synthDemoRaf = requestAnimationFrame(step);
        else {
          synthDemoRaf = null;
          sourceEl.classList.remove("synth-demo-source-pulse");
          flyer.classList.remove("synth-demo-flyer-visible");
          slotEl.innerHTML = `<div class="syn-demo-chip">${chipHtml}</div>`;
          onDone();
        }
      };
      flyer.style.transform = `translate(${x0}px, ${y0}px) translate(-50%, -50%) scale(1)`;
      flyer.style.opacity = "1";
      synthDemoRaf = requestAnimationFrame(step);
    };

    runFly(phenCard, slotPhen, "现象样本", () => {
      runFly(intelCard, slotIntel, "情报摘要", () => {
        if (resultEl) {
          resultEl.textContent = "执行合成 · 示意（演示不消耗素材）";
          resultEl.classList.add("synth-demo-result-flash");
        }
        scheduleSynthDemoAutoReplay();
      });
    });
  }

  function openSynthDemoLab() {
    const wrap = document.getElementById("synthDemoLabModal");
    if (!wrap) return;
    clearSynthDemoAutoTimer();
    cancelSynthDemoAnim();
    wrap.classList.remove("hidden");
    requestAnimationFrame(() => playSynthDemoLab());
  }

  function closeSynthDemoLab() {
    const wrap = document.getElementById("synthDemoLabModal");
    if (wrap) wrap.classList.add("hidden");
    clearSynthDemoAutoTimer();
    cancelSynthDemoAnim();
    synthDemoGen += 1;
  }

  let synthDemoLabBound = false;
  function bindSynthDemoLabUi() {
    if (synthDemoLabBound) return;
    const wrap = document.getElementById("synthDemoLabModal");
    const replay = document.getElementById("synthDemoReplay");
    const closeBtn = document.getElementById("synthDemoClose");
    if (!wrap || !replay || !closeBtn) return;
    synthDemoLabBound = true;
    replay.onclick = () => playSynthDemoLab();
    closeBtn.onclick = () => closeSynthDemoLab();
    wrap.addEventListener("click", (ev) => {
      if (ev.target === wrap) closeSynthDemoLab();
    });
  }

  function renderMacro() {
    const elM = document.getElementById("macro");
    if (!elM) return;
    const keys = ["公信", "诡名", "声望", "守序", "狂性"];
    elM.innerHTML = keys.map((k) => `<div class="stat"><b>${k}</b><span>${macro[k]}</span></div>`).join("");
  }

  function setView(name) {
    state.view = name;
    if (document.body) document.body.dataset.view = name;
    ["weekStart", "global", "region", "setup", "result"].forEach((v) => {
      const node = document.getElementById("view-" + v);
      if (node) node.classList.toggle("hidden", v !== name);
    });
    updateNextDayButton();
  }

  function binomialPAtLeast(n, p, k) {
    if (k <= 0) return 1;
    if (k > n) return 0;
    let sum = 0;
    for (let x = k; x <= n; x++) sum += binomialPMF(n, p, x);
    return clamp(sum, 0, 1);
  }
  function binomialPMF(n, p, x) {
    if (x < 0 || x > n) return 0;
    return binom(n, x) * Math.pow(p, x) * Math.pow(1 - p, n - x);
  }
  function binom(n, k) {
    if (k < 0 || k > n) return 0;
    k = Math.min(k, n - k);
    let r = 1;
    for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i;
    return r;
  }

  function meetsNeed(need, staffList) {
    const sum = staffSum(staffList);
    return Object.keys(need).every((k) => (sum[k] || 0) >= need[k]);
  }
  function staffSum(staffList) {
    const sum = {};
    staffList.forEach((id) => {
      const p = findStaff(id);
      if (!p) return;
      ATTR_KEYS.forEach((k) => {
        sum[k] = (sum[k] || 0) + getStaffValue(p, k);
      });
    });
    return sum;
  }
  function poolSizes(staffList) {
    const s = staffSum(staffList);
    return { nA: (s.探索 || 0) + (s.洞察 || 0) + (s.诡思 || 0), nB: (s.生存 || 0) + (s.理性 || 0) };
  }
  function needThresholds(need) {
    return { kA: (need.探索 || 0) + (need.洞察 || 0) + (need.诡思 || 0), kB: (need.生存 || 0) + (need.理性 || 0) };
  }

  function computeExplorationP(mission, staffList) {
    const pBase = DIFFICULTY_P[mission.difficulty || "normal"] ?? 0.5;
    let deltaP = 0;
    if (!meetsNeed(mission.need, staffList)) deltaP -= 0.15;
    if (mission.kind === "temp" && state.day < (mission.deadlineDay || 0)) deltaP += 0.05;
    if (mission.kind === "hidden") deltaP -= 0.05;
    const p = clamp(pBase + deltaP, 0, 1);
    const { nA, nB } = poolSizes(staffList);
    const { kA, kB } = needThresholds(mission.need);
    const enemyAttr = mission.enemyAttr | 0;
    const nTot = nA + nB;
    const enemyA = nTot > 0 ? Math.floor((enemyAttr * nA) / nTot) : 0;
    const enemyB = enemyAttr - enemyA;
    const nAe = Math.max(0, nA - enemyA);
    const nBe = Math.max(0, nB - enemyB);
    function passProb(n, k) {
      if (k <= 0) return 1;
      if (n <= 0) return 0;
      return binomialPAtLeast(n, p, k);
    }
    const pA = passProb(nAe, kA);
    const pB = passProb(nBe, kB);
    return {
      p,
      pBase,
      deltaP,
      nA,
      nB,
      kA,
      kB,
      enemyAttr,
      enemyA,
      enemyB,
      nAe,
      nBe,
      pA,
      pB,
      pBig: pA * pB,
      pSmall: pA * (1 - pB) + (1 - pA) * pB,
      pBothFail: (1 - pA) * (1 - pB),
    };
  }

  function computeCharacterDicePreview(mission, staffList) {
    const risk = riskLabelForMission(mission, staffList);
    const stats = teamDiceNeedStats(mission, staffList);
    const gapText = stats.gaps.length ? `缺口 ${stats.gaps.map((x) => `${x.k}${x.gap}`).join(" / ")}` : "需求面值已覆盖";
    const idleText = stats.nonContributingStaff ? `，${stats.nonContributingStaff} 人无相关面` : "";
    const coverageText = stats.needValue ? `覆盖 ${stats.coveredValue}/${stats.needValue}` : "无明确需求";
    const reason = stats.totalFaces
      ? `有效相关面 ${stats.relevantFaces}，${coverageText}，空面 ${stats.blankFaces}，${gapText}${idleText}`
      : "尚未选择角色骰";
    return {
      risk,
      relevant: stats.relevant,
      totalFaces: stats.totalFaces,
      relevantFaces: stats.relevantFaces,
      blankFaces: stats.blankFaces,
      values: stats.values,
      gaps: stats.gaps,
      reason,
    };
  }

  function pickRandomIndices(len, count) {
    const arr = Array.from({ length: len }, (_, i) => i);
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return new Set(arr.slice(0, Math.min(count, len)));
  }

  function runSplitCheck(mission, staffList) {
    const meta = computeExplorationP(mission, staffList);
    const p = meta.p;
    const { nA, nB } = poolSizes(staffList);
    const { kA, kB } = needThresholds(mission.need);
    const enemyAttr = mission.enemyAttr | 0;
    const nTot = nA + nB;
    const enemyA = nTot > 0 ? Math.floor((enemyAttr * nA) / nTot) : 0;
    const enemyB = enemyAttr - enemyA;
    const rollHit = () => Math.random() < p;
    const rollsA = Array.from({ length: nA }, rollHit);
    const rollsB = Array.from({ length: nB }, rollHit);
    const voidA = pickRandomIndices(nA, enemyA);
    const voidB = pickRandomIndices(nB, enemyB);
    let hitsA = 0;
    for (let i = 0; i < nA; i++) if (!voidA.has(i) && rollsA[i]) hitsA++;
    let hitsB = 0;
    for (let i = 0; i < nB; i++) if (!voidB.has(i) && rollsB[i]) hitsB++;
    const passA = kA <= 0 ? true : hitsA >= kA;
    const passB = kB <= 0 ? true : hitsB >= kB;
    let tier;
    if (passA && passB) tier = "大成功";
    else if (passA || passB) tier = "小成功";
    else {
      const totalHits = hitsA + hitsB;
      const needSum = kA + kB;
      tier = nA + nB >= 4 && totalHits <= 1 && needSum >= 4 ? "大失败" : "失败";
    }
    return { ...meta, hitsA, hitsB, passA, passB, tier, rollsA, rollsB, voidA, voidB, enemyA, enemyB };
  }

  function pickWeekEvent() {
    const pool = [
      {
        id: "evt_passive_tipoff",
        type: "passive",
        title: "线人爆料",
        body: "匿名线人送来一份禁区坐标碎片，你的编辑部获得了额外线索。",
        sourceType: "匿名爆料",
        sourceLabel: "线人热线",
        sourceMark: "线",
        preview: ["地图/素材：获得一条临时线索", "周刊气质：诡名小幅上升"],
        resultLines: ["获得临时线索「匿名坐标碎片」", "诡名 +1"],
        confirmText: "收下坐标碎片",
        condition: () => true,
        apply: () => {
          state.clues.push({ title: "匿名坐标碎片 · 临时线索", type: "occult", tier: 1, topicKey: newTopicKey() });
          addMacro({ 诡名: 1 });
          log("本周来件：收下临时线索「匿名坐标碎片」。");
        },
      },
      {
        id: "evt_passive_grant",
        type: "passive",
        title: "学术资助",
        body: "公信较高引来研究基金，本周调查组状态提升。",
        sourceType: "财务压力",
        sourceLabel: "研究基金会",
        sourceMark: "资",
        preview: ["宏观：公信与声望趋稳", "员工：老魏本周洞察提升"],
        resultLines: ["公信 +2，声望 +1", "老魏本周 洞察 +1（临时）"],
        confirmText: "确认资助安排",
        condition: () => macro.公信 >= 55,
        apply: () => {
          addMacro({ 公信: 2, 声望: 1 });
          addStaffEffect("s2", "洞察", 1, "week", false);
          log("本周来件：研究基金通过，老魏本周洞察提升。");
        },
      },
      {
        id: "evt_choice_occult",
        type: "choice",
        title: "深夜电台异响",
        body: "诡名与狂性持续走高，深夜频道出现疑似“呼唤信号”。你要怎么处理？",
        sourceType: "异常回响",
        sourceLabel: "深夜电台",
        sourceMark: "频",
        preview: ["编辑方向：是否公开追踪异常信号", "可能影响：宏观倾向、员工状态或临时事件点"],
        condition: () => macro.诡名 >= 45 && macro.狂性 >= 25,
        options: [
          {
            text: "公开追踪信号（激进）",
            preview: "倾向：话题度与诡名显著升温；风险：公信承压，并追加临时事件点。",
            desc: "诡名 +4，公信 -2，追加一条临时 occult 事件点",
            resultLines: ["诡名 +4，公信 -2", "美国取材地图追加「深夜电台信号源」临时事件点"],
            apply: () => {
              addMacro({ 诡名: 4, 公信: -2 });
              addDynamicNode("us", {
                id: `dyn_radio_${state.week}`,
                kind: "temp",
                name: "临时：深夜电台信号源",
                days: 2,
                need: { 探索: 4, 诡思: 3 },
                tags: ["occult", "pop"],
                difficulty: "hard",
                enemyAttr: 3,
                deadlineDay: 3,
                chain: null,
              }, 1);
            },
          },
          {
            text: "秘密监听（稳妥）",
            preview: "倾向：保留神秘度，同时稳住公信；老魏本周更适合做理性研判。",
            desc: "公信 +1，诡名 +1，调查·老魏本周 理性 +1",
            resultLines: ["公信 +1，诡名 +1", "老魏本周 理性 +1（临时）"],
            apply: () => {
              addMacro({ 公信: 1, 诡名: 1 });
              addStaffEffect("s2", "理性", 1, "week", false);
            },
          },
          {
            text: "切断频道（保守）",
            preview: "倾向：守序回升、狂性下降；代价：放弃一次潜在线索机会。",
            desc: "守序 +2，狂性 -1，失去一次潜在线索机会",
            resultLines: ["守序 +2，狂性 -1", "放弃本次潜在线索机会"],
            apply: () => {
              addMacro({ 守序: 2, 狂性: -1 });
            },
          },
        ],
      },
      {
        id: "evt_choice_order",
        type: "choice",
        title: "市政协作提案",
        body: "你收到一份跨部门调查提案，可借此扩展行动能力。",
        sourceType: "势力函件",
        sourceLabel: "市政厅函件",
        sourceMark: "函",
        preview: ["编辑方向：是否与官方机构绑定", "可能影响：公信、声望、临时科学线索或地图节点"],
        condition: () => macro.守序 >= 55 || macro.公信 >= 60,
        options: [
          {
            text: "签署官方协作",
            preview: "倾向：公信与声望明显上升；地图会出现官方协作带来的科学节点。",
            desc: "公信 +3，声望 +2，新增西部档案临时科学节点",
            resultLines: ["公信 +3，声望 +2", "西部档案追加「内华达监听站异常」临时科学节点"],
            apply: () => {
              addMacro({ 公信: 3, 声望: 2 });
              addDynamicNode("western_archives", {
                id: `dyn_west_${state.week}`,
                kind: "temp",
                name: "临时：内华达监听站异常",
                days: 2,
                need: { 探索: 4, 理性: 4 },
                tags: ["sci"],
                difficulty: "normal",
                enemyAttr: 2,
                deadlineDay: 4,
                chain: null,
              }, 1);
            },
          },
          {
            text: "只拿设备不公开站队",
            preview: "倾向：获得科技线临时线索，不公开站队；诡名略有上升。",
            desc: "获得临时科技线索，诡名 +1",
            resultLines: ["获得临时线索「协作设备清单」", "诡名 +1"],
            apply: () => {
              state.clues.push({ title: "协作设备清单 · 临时线索", type: "sci", tier: 1, topicKey: newTopicKey() });
              addMacro({ 诡名: 1 });
            },
          },
          {
            text: "拒绝提案",
            preview: "倾向：维持编辑部独立性与守序；风险：声望小幅下降。",
            desc: "守序 +1，声望 -1",
            resultLines: ["守序 +1", "声望 -1"],
            apply: () => addMacro({ 守序: 1, 声望: -1 }),
          },
        ],
      },
      {
        id: "evt_choice_public",
        type: "choice",
        title: "读者来信潮",
        body: "一批读者要求“更刺激”或“更严谨”的内容，你需要选择编辑方向。",
        sourceType: "读者来信",
        sourceLabel: "读者邮袋",
        sourceMark: "信",
        preview: ["编辑方向：在猎奇热度与纪实可信之间取舍", "可能影响：五维属性、员工成长或临时投稿线索"],
        condition: () => true,
        options: [
          {
            text: "迎合热点",
            preview: "倾向：诡名与声望更容易出圈；实习生会获得长期探索成长。",
            desc: "诡名 +2，声望 +1，实习生·小赵 探索 +1（永久）",
            resultLines: ["诡名 +2，声望 +1", "小赵 探索 +1（永久）"],
            apply: () => {
              addMacro({ 诡名: 2, 声望: 1 });
              addStaffEffect("s4", "探索", 1, "permanent", true);
            },
          },
          {
            text: "坚持纪实",
            preview: "倾向：公信和守序更稳；神秘线编辑本周会受到一点压制。",
            desc: "公信 +2，守序 +1，神秘版·伊芙 诡思 -1（本周）",
            resultLines: ["公信 +2，守序 +1", "伊芙本周 诡思 -1（临时）"],
            apply: () => {
              addMacro({ 公信: 2, 守序: 1 });
              addStaffEffect("s3", "诡思", -1, "week", false);
            },
          },
          {
            text: "平衡两端",
            preview: "倾向：公信与诡名同步小幅上升，并获得一条可转化的投稿线索。",
            desc: "公信 +1，诡名 +1，获得临时情报线索",
            resultLines: ["公信 +1，诡名 +1", "获得临时线索「读者投稿拼图」"],
            apply: () => {
              addMacro({ 公信: 1, 诡名: 1 });
              state.clues.push({ title: "读者投稿拼图 · 临时线索", type: "pop", tier: 1, topicKey: newTopicKey() });
            },
          },
        ],
      },
    ];
    const available = pool.filter((e) => {
      try {
        return e.condition();
      } catch (_) {
        return false;
      }
    });
    return rand(available.length ? available : pool);
  }

  function isWeekEventDebugMode() {
    try {
      const p = new URLSearchParams(window.location.search || "");
      return p.get("debug") === "1" || p.get("debugWeekEvent") === "1";
    } catch (_) {
      return false;
    }
  }

  function weekEventLines(lines, fallback) {
    const list = Array.isArray(lines) ? lines.filter(Boolean) : [];
    if (list.length) return list;
    return fallback ? [fallback] : [];
  }

  function renderWeekEventImpact(event) {
    const resolved = state.weekEventResolved;
    const title = resolved ? "已生效" : "可能影响";
    const lines = resolved
      ? weekEventLines(state.weekEventResultLines, state.weekEventResult || "本周来件已处理。")
      : weekEventLines(event.preview, "处理后会显示精确变化。");
    return `
      <aside class="briefing-impact ${resolved ? "is-resolved" : ""}">
        <div class="briefing-impact-title">${title}</div>
        <ul class="briefing-impact-list">
          ${lines.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}
        </ul>
      </aside>`;
  }

  function renderWeekEventChoices(event, showExactEffects) {
    const options = event.options || [];
    return `
      <div class="briefing-choice-list" aria-label="本周来件处理方案">
        ${options.map((op, idx) => {
          const selected = state.weekEventChoiceIndex === idx;
          const exactText = weekEventLines(op.resultLines, op.desc || "该选择已生效。").join("；");
          const previewText = showExactEffects ? exactText : (op.preview || "会改变本周资源与编辑倾向。");
          const detailText = state.weekEventResolved && selected ? exactText : previewText;
          const stateText = state.weekEventResolved ? (selected ? "已选择" : "未采用") : `方案 ${idx + 1}`;
          return `
            <div class="briefing-choice ${selected ? "is-selected" : ""} ${state.weekEventResolved && !selected ? "is-muted" : ""}">
              <button type="button" data-evt-op="${idx}" ${state.weekEventResolved ? "disabled" : ""}>${escapeHtml(op.text)}</button>
              <div class="briefing-choice-copy">
                <strong>${escapeHtml(stateText)}</strong>
                <span>${escapeHtml(detailText)}</span>
              </div>
            </div>`;
        }).join("")}
      </div>`;
  }

  function applyWeekEventDefault() {
    if (!state.weekEvent || state.weekEventResolved) return;
    if (state.weekEvent.type === "passive" && typeof state.weekEvent.apply === "function") {
      state.weekEvent.apply();
      state.weekEventResultLines = weekEventLines(state.weekEvent.resultLines, "本周来件已生效。");
      state.weekEventResult = state.weekEventResultLines.join("；");
      state.weekEventChoiceIndex = null;
      state.weekEventResolved = true;
      renderMacro();
    }
  }

  function applyWeekEventChoice(index) {
    if (!state.weekEvent || state.weekEventResolved || state.weekEvent.type !== "choice") return;
    const op = state.weekEvent.options?.[index];
    if (!op) return;
    if (typeof op.apply === "function") op.apply();
    state.weekEventResultLines = weekEventLines(op.resultLines, op.desc || "该选择已生效。");
    state.weekEventResult = state.weekEventResultLines.join("；");
    state.weekEventChoiceIndex = index;
    state.weekEventResolved = true;
    log(`编辑部决定：${state.weekEvent.title} -> ${op.text}`);
    renderMacro();
  }

  function unlockRegions() {
    REGIONS.forEach((r) => {
      if (r.id === "us") {
        r.unlocked = true;
        return;
      }
      if (r.id === "new_england") {
        const done = state.clues.some((c) => c.title.includes("飞碟剪报")) || macro.声望 >= 55 || !!state.completedMissionIds.skin;
        r.unlocked = done;
        r.pulse = done && state.week <= 2;
        return;
      }
      if (r.id === "western_archives") {
        r.unlocked = macro.公信 >= 60 || macro.守序 >= 60;
        r.pulse = r.unlocked;
      }
    });
  }

  function nodeVisible(node) {
    if (!node || state.retiredMissionIds[node.id]) return false;
    if (node.checkType === "red" && node.deadlineDay != null && dayIndexInWeek() > node.deadlineDay) return false;
    if (node.kind !== "hidden") return true;
    if (typeof node.unlock === "function") return node.unlock(macro);
    return true;
  }

  function filterNodeTags(node) {
    const t = node.tags || [];
    if (state.filters.sci && t.includes("sci")) return true;
    if (state.filters.occult && t.includes("occult")) return true;
    if (state.filters.pop && t.includes("pop")) return true;
    return false;
  }

  function missionTypeBadges(m) {
    const badges = [];
    if ((m.checkType || "white") === "red") badges.push({ text: "红色截稿", cls: "red" });
    else badges.push({ text: "白色调查", cls: "white" });
    if (m.chainType === "deep") badges.push({ text: `深度调查${m.chainStage ? `·第${m.chainStage}阶段` : ""}`, cls: "deep" });
    if (m.isBlackDiceTask) badges.push({ text: "黑骰任务", cls: "bonus" });
    if (!m.isBlackDiceTask && (m.riskTier === "high" || m.isHighRisk)) badges.push({ text: "危险", cls: "danger" });
    if (m.allowPushBonus) badges.push({ text: "可再追", cls: "bonus" });
    return badges;
  }

  function missionTypeBadgesHtml(m) {
    return missionTypeBadges(m)
      .map((b) => `<span class="task-type-chip task-${b.cls}">${escapeHtml(b.text)}</span>`)
      .join("");
  }

  function dispatchTaskBadgesHtml(m) {
    return missionTypeBadges(m)
      .filter((b) => b.cls !== "red" && b.cls !== "white")
      .map((b) => `<span class="task-type-chip task-${b.cls}">${escapeHtml(b.text)}</span>`)
      .join("");
  }

  function missionTypeTitle(m) {
    if (m.taskTypeTitle) {
      if (!m.isBlackDiceTask && (m.riskTier === "high" || m.isHighRisk)) {
        const cleaned = m.taskTypeTitle.replace(/^高危/, "").replace(/^危险/, "").trim();
        if (cleaned) return cleaned;
      }
      return m.taskTypeTitle;
    }
    if ((m.checkType || "white") === "red") return "红色截稿";
    if (m.isBlackDiceTask) return "黑骰任务";
    if (m.chainType === "deep") return "深度调查";
    return "白色调查";
  }

  function missionTypeDesc(m) {
    if (m.taskTypeDesc) {
      if (!m.isBlackDiceTask && (m.riskTier === "high" || m.isHighRisk)) {
        return m.taskTypeDesc.replace(/高危任务/g, "危险标记").replace(/高危/g, "危险");
      }
      return m.taskTypeDesc;
    }
    if ((m.checkType || "white") === "red") return "一次性情报窗口。成功、失败或超过截止日期后关闭。";
    if (m.isBlackDiceTask) return "使用关卡专属黑骰机制，结果分大成功 / 成功 / 失败 / 大失败。";
    if (m.chainType === "deep") return "连续任务。完成后会推进为下一阶段，越接近真相，风险越高。";
    if (m.riskTier === "high") return "危险标识。难度更高、失败后果更重，但没有黑骰特殊机制。";
    return "可反复追踪的调查任务。失败不会封死题材，后续可继续累积信息。";
  }

  function missionStory(m) {
    if (!m || !m.id) return null;
    return MISSION_STORIES[m.id] || m.story || null;
  }

  function missionStoryBriefHtml(m) {
    const story = missionStory(m);
    if (!story) return "";
    const objective = story.objective ? `<div class="dispatch-story-row"><span>目标</span><strong>${escapeHtml(story.objective)}</strong></div>` : "";
    const stakes = story.stakes ? `<div class="dispatch-story-row"><span>压力</span><strong>${escapeHtml(story.stakes)}</strong></div>` : "";
    return `<div class="dispatch-story-brief">
      <div class="dispatch-story-kicker">调查简报</div>
      <p>${escapeHtml(story.brief || "这条线索需要外勤确认，才能进入本期选题。")}</p>
      ${objective || stakes ? `<div class="dispatch-story-grid">${objective}${stakes}</div>` : ""}
    </div>`;
  }

  function missionFieldIntroHtml(m) {
    const story = missionStory(m);
    if (!story || !story.fieldIntro) return "";
    return `<div class="result-field-note"><strong>现场记录</strong><span>${escapeHtml(story.fieldIntro)}</span></div>`;
  }

  function missionDiceDialogue(m, stage) {
    const story = missionStory(m);
    const dice = story && story.dice ? story.dice : {};
    if (stage === "black") return dice.black || "现场信号突然变冷，骰池里有东西开始改变本轮判断。";
    if (stage === "select") return dice.select || "主编：先挑能支撑报道的证据，别把噪声也写进稿子。";
    return dice.rolling || "外勤组抵达现场，所有人都在等第一颗骰子停下来。";
  }

  function missionDiceDialogueHtml(m, stage) {
    const text = missionDiceDialogue(m, stage);
    return text ? `<div class="dice-story-line">${escapeHtml(text)}</div>` : "";
  }

  function missionOutcomeCopy(m, key) {
    const story = missionStory(m);
    if (!story || !story.outcomes) return null;
    return story.outcomes[key] || null;
  }

  function missionOutcomeLine(m, key, fallback, prefix) {
    const copy = missionOutcomeCopy(m, key);
    const text = copy && copy.line ? copy.line : fallback;
    return `${prefix || ""}${text}`;
  }

  function missionClueRewardCopy(m, titleSuffix, tier, fallbackDesc, outcomeKey) {
    const copy = missionOutcomeCopy(m, outcomeKey) || missionOutcomeCopy(m, titleSuffix);
    return {
      title: copy && copy.clueTitle ? copy.clueTitle : titleSuffix,
      desc: copy && copy.clueDesc ? copy.clueDesc : (fallbackDesc || `线索品质：Tier ${tier}`),
    };
  }

  function missionTypePanelHtml(m, compact) {
    const progress = m.checkType === "white" && state.whiteInvestigationLog[m.id]
      ? `<div style="margin-top:0.25rem;">已追踪 ${state.whiteInvestigationLog[m.id]} 次，本题材会继续累积信息。</div>`
      : "";
    const chain = m.chainType === "deep"
      ? `<div style="margin-top:0.25rem;">连续任务：本阶段完成后会在地图上推进为下一阶段，直到最终完结。</div>`
      : "";
    const red = m.checkType === "red"
      ? `<div style="margin-top:0.25rem;color:#fecaca;">红色截稿：成功、失败或过期后都会关闭并从地图消失。</div>`
      : "";
    const high = m.riskTier === "high"
      ? `<div style="margin-top:0.25rem;color:#fde68a;">危险标识：需求更高，失败可能带来 debuff；不等于黑骰任务类型。</div>`
      : "";
    const inner = `<div><strong>${escapeHtml(missionTypeTitle(m))}</strong> ${missionTypeBadgesHtml(m)}</div>
      <div style="margin-top:0.25rem;">${escapeHtml(missionTypeDesc(m))}</div>
      ${progress}${chain}${red}${high}`;
    if (compact) return `<div class="task-type-summary">${inner}</div>`;
    return `<div class="prob-box task-type-panel">${inner}</div>`;
  }

  function missionPointMark(n) {
    if (n.checkType === "red") return "截";
    if (n.isBlackDiceTask) return "▣";
    if (n.chainType === "deep") return n.chainStage ? String(n.chainStage) : "链";
    if (n.riskTier === "high") return "!";
    if (n.kind === "hidden") return "隐";
    if (n.kind === "temp" || /突发/.test(n.name)) return "!";
    return "常";
  }

  function missionVisualClass(n) {
    const cls = [];
    if (n.checkType === "red") cls.push("node-red");
    else if (n.isBlackDiceTask) cls.push("node-black");
    else if (n.chainType === "deep") cls.push("node-deep");
    else cls.push("node-white");
    if (!n.isBlackDiceTask && (n.riskTier === "high" || n.isHighRisk)) cls.push("node-danger");
    return cls.join(" ");
  }

  const MISSION_GROUPS = [
    { key: "white", title: "白色调查 · 常驻追踪", rule: "可反复派遣，失败也会留下碎片线索。" },
    { key: "red", title: "红色截稿 · 限时关闭", rule: "成功、失败或过期后从地图关闭。" },
    { key: "deep", title: "深度链 · 阶段推进", rule: "完成当前环后，在地图上推进下一阶段。" },
    { key: "black", title: "黑骰入口 · 特殊判定", rule: "进入关卡专属黑骰机制，不等于普通危险任务。" },
  ];

  function missionGroupKey(m) {
    if (m.isBlackDiceTask) return "black";
    if ((m.checkType || "white") === "red") return "red";
    if (m.chainType === "deep") return "deep";
    return "white";
  }

  function mapHighRiskTier(m, baseTier) {
    if (m.riskTier !== "high") return { id: baseTier, label: baseTier, clueTier: baseTier === "大成功" ? 3 : baseTier === "小成功" ? 2 : baseTier === "失败" ? 1 : 0 };
    if (baseTier === "大成功") return { id: "crit_success", label: "大成功", clueTier: 3 };
    if (baseTier === "小成功") {
      const costly = m.chainStage >= 3 || (m.tags || []).includes("occult") || macro.诡名 >= 45;
      return costly
        ? { id: "success_cost", label: "成功但反噬", clueTier: 3 }
        : { id: "partial", label: "部分成功", clueTier: 2 };
    }
    if (baseTier === "失败") return { id: "fail_clue", label: "失败但有线索", clueTier: 1 };
    return { id: "crit_fail", label: "大失败", clueTier: 0 };
  }

  function clueTypeFromMission(m) {
    return (m.tags || [])[0] || "pop";
  }

  function addMissionClue(m, titleSuffix, tier, rewards, desc, outcomeKey) {
    if (tier <= 0) return null;
    const copy = missionClueRewardCopy(m, titleSuffix, tier, desc, outcomeKey);
    const clue = { title: `${m.name} · ${copy.title}`, type: clueTypeFromMission(m), tier, topicKey: newTopicKey() };
    state.clues.push(clue);
    rewards.push({ icon: rewardIconByType(clue.type), title: clue.title, desc: copy.desc });
    return clue;
  }

  function applyHighRiskOutcome(m, high, lines, rewards, prefix) {
    const p = prefix || "";
    if (high.id === "crit_success") {
      addMacro({ 声望: 6, 公信: (m.tags || []).includes("sci") ? 3 : 0, 诡名: (m.tags || []).includes("occult") ? 4 : 1 });
      lines.push(missionOutcomeLine(m, "crit_success", "大成功：录音、目击者与雷达记录三方对上。", p));
      addMissionClue(m, "高危强线索", 3, rewards, "高危五档：大成功（Tier 3）", "crit_success");
    } else if (high.id === "success_cost") {
      addMacro({ 声望: 4, 公信: -2, 狂性: 2, 诡名: 2 });
      lines.push(missionOutcomeLine(m, "success_cost", "成功但反噬：拿到独家，但市政发言人也记住了你的名字。", p));
      addMissionClue(m, "反噬独家素材", 3, rewards, "高危五档：成功但反噬（Tier 3，附带宏观代价）", "success_cost");
    } else if (high.id === "partial") {
      addMacro({ 声望: 2, 诡名: 1 });
      lines.push(missionOutcomeLine(m, "partial", "部分成功：照片能用，只有最关键的三秒糊成了灰。", p));
      addMissionClue(m, "不完整素材", 2, rewards, "高危五档：部分成功（Tier 2）", "partial");
    } else if (high.id === "fail_clue") {
      addMacro({ 声望: -1, 狂性: 1 });
      lines.push(missionOutcomeLine(m, "fail_clue", "失败但有线索：任务失败，但对方反复提到一个旧地名。", p));
      addMissionClue(m, "失败残留线索", 1, rewards, "高危五档：失败但有线索（Tier 1）", "fail_clue");
    } else {
      addMacro({ 守序: -3, 狂性: 4, 公信: -2 });
      lines.push(missionOutcomeLine(m, "crit_fail", "大失败：设备烧毁，受访者失联，只剩一段空白磁带。", p));
    }
  }

  function applyStandardOutcome(m, tier, lines, rewards) {
    if (tier === "大成功") {
      macro.声望 = Math.min(100, macro.声望 + 6);
      macro.公信 += (m.tags || []).includes("sci") ? 4 : 0;
      macro.诡名 += (m.tags || []).includes("occult") ? 5 : 2;
      if (m.kind === "hidden") macro.狂性 = Math.min(100, macro.狂性 + 4);
      lines.push(missionOutcomeLine(m, "大成功", "大成功：高质量线索。"));
      addMissionClue(m, "深度特稿素材", 3, rewards, "线索品质：高（Tier 3）", "大成功");
    } else if (tier === "小成功" || tier === "成功") {
      macro.声望 = Math.min(100, macro.声望 + 4);
      macro.诡名 += 1;
      lines.push(missionOutcomeLine(m, tier, `${m.riskTier === "high" ? "危险任务成功" : "成功"}：获得可用素材。`));
      addMissionClue(m, m.riskTier === "high" ? "危险任务素材" : "常规稿件素材", m.riskTier === "high" ? 3 : 2, rewards, m.riskTier === "high" ? "危险标识：成功（Tier 3）" : "线索品质：中（Tier 2）", tier);
    } else if (tier === "失败") {
      macro.声望 = Math.max(0, macro.声望 - 2);
      if (m.riskTier === "high") {
        addMacro({ 狂性: 2, 守序: -1 });
        lines.push(missionOutcomeLine(m, "失败", "危险任务失败：获得弱线索，但队伍状态受损。"));
        addMissionClue(m, "危险弱线索", 1, rewards, "危险标识：失败仍保留弱线索（Tier 1）", "失败");
        rewards.push({ icon: "!", title: "危险后果", desc: "狂性 +2，守序 -1。本任务没有黑骰，但失败代价更重。" });
      } else {
        lines.push(missionOutcomeLine(m, "失败", "失败：碎片线索。"));
        addMissionClue(m, "碎片线索", 1, rewards, "线索品质：低（Tier 1）", "失败");
      }
    } else {
      macro.守序 = Math.max(0, macro.守序 - 3);
      macro.狂性 = Math.min(100, macro.狂性 + 3);
      lines.push(missionOutcomeLine(m, "大失败", "大失败。"));
    }
  }

  function recordWhiteInvestigation(m, lines) {
    if ((m.checkType || "white") !== "white") return;
    state.whiteInvestigationLog[m.id] = (state.whiteInvestigationLog[m.id] || 0) + 1;
    if (m.id === "n51") {
      const count = state.whiteInvestigationLog[m.id];
      lines.push(`白色调查：本题材已追踪 ${count} 次，后续派遣会继续累积旧机库围栏证词。`);
    }
  }

  function retireRedMission(m, lines) {
    if (m.checkType !== "red") return;
    state.retiredMissionIds[m.id] = true;
    lines.push("红色截稿：情报窗口已关闭，该任务会从地图上消失。");
  }

  function advanceDeepChain(m, lines, rewards) {
    if (m.chainType !== "deep") return;
    state.completedMissionIds[m.id] = true;
    state.chainStageResults[m.id] = `${m.name} 已完成，获得阶段素材。`;
    if (!m.nextNode) {
      lines.push("深度调查：连续任务已完结，真相风险暂时收束。");
      return;
    }
    if (state.completedMissionIds[m.nextNode.id]) return;
    const alreadyVisible = getRegionNodes({ id: m.regionId, nodes: [] }).some((node) => node.id === m.nextNode.id);
    if (!alreadyVisible) addDynamicNode(m.regionId, m.nextNode, 6);
    lines.push(`深度调查：当前阶段完成，地图上出现下一阶段「${m.nextNode.name}」。`);
    rewards.push({ icon: "→", title: `连续任务推进：${m.nextNode.name}`, desc: (missionStory(m.nextNode) || {}).brief || missionTypeDesc(m.nextNode) });
  }

  function shouldOfferPushBonus(m, high) {
    if (!m.allowPushBonus || m.pushBonusUsed || state.pushBudgetWeekly <= 0) return false;
    return high && ["success_cost", "partial", "fail_clue"].includes(high.id);
  }

  async function resolvePushBonus(m, showDice) {
    const ok = await showConfirmPopup(
      "临时事件：录音里还有三秒",
      `<p style="margin:0 0 0.5rem;">你已经准备收工，但技术员说空白段里也许藏着东西。</p>
       <p style="margin:0;color:#fbbf24;">再追一次会消耗 1 行动点，并加入更糟黑骰：对手作废 +1，灾厄链 +2。</p>`,
      dayDateLabel(),
    );
    if (!ok) return false;
    state.pushBudgetWeekly -= 1;
    state.calamityMeter += 2;
    const bonusMission = { ...m, enemyAttr: (m.enemyAttr | 0) + 1, pushBonusUsed: true };
    const bonusCheck = runSplitCheck(bonusMission, state.selectedStaffIds);
    const bonusHigh = mapHighRiskTier(bonusMission, bonusCheck.tier);
    const tb = document.getElementById("tierBanner");
    if (tb) tb.textContent = `再追一次：${bonusHigh.label}`;
    const outcome = document.getElementById("bonusOutcome");
    if (outcome) outcome.innerHTML = `<div class="prob-box" style="border-color:#b45309;">
      <strong>更糟黑骰已加入</strong><br/>
      对手作废 +1 · 灾厄链 ${state.calamityMeter}/10 · 剩余追查行动点 ${state.pushBudgetWeekly}
    </div>`;
    if (showDice) {
      const h = document.getElementById("diceAnim");
      if (h) h.innerHTML = `<div class="dice-rolling-hint"><span class="dice-spinner"></span><span>再追一次：更糟黑骰加入...</span></div>`;
      await animateDiceReveal(document.getElementById("view-result"), bonusCheck);
    } else {
      await sleep(450);
      const h = document.getElementById("diceAnim");
      if (h) h.innerHTML = `<div class="prob-box">再追一次 · 调查 ${bonusCheck.hitsA}/${bonusCheck.nAe}（≥${bonusCheck.kA}）· 现场 ${bonusCheck.hitsB}/${bonusCheck.nBe}（≥${bonusCheck.kB}）· 对手作废 +1</div>`;
    }
    const bonusLines = [];
    const bonusRewards = [];
    applyHighRiskOutcome(bonusMission, bonusHigh, bonusLines, bonusRewards, "再追一次：");
    if (bonusHigh.id === "crit_fail") {
      addMacro({ 公信: -2, 狂性: 3 });
      bonusLines.push("灾厄链：官方辟谣和员工失眠将在下周事件权重中留下回声。");
    }
    const finalOutcome = document.getElementById("bonusOutcome");
    if (finalOutcome) finalOutcome.innerHTML += `<div class="prob-box" style="margin-top:0.5rem;border-color:#7c3aed;">${bonusLines.map(escapeHtml).join("<br/>")}</div>`;
    await showRewardsPopup(bonusRewards);
    return true;
  }

  function renderWeekStart() {
    if (!state.weekEvent) state.weekEvent = pickWeekEvent();
    state.phase = "briefing";
    const elW = document.getElementById("view-weekStart");
    const debugMode = isWeekEventDebugMode();
    const showExactEffects = debugMode && state.debugShowEventEffects;
    const introBrief = state.week === 1
      ? `<div class="briefing-intro">
          <strong>新任主编上任</strong><br/>
          你通过面试，直接成为《世界未解之谜周刊》的主编。杂志社快垮了，债主每天催债；本周再找不出有吸引力的故事报道，编辑部就要散伙。
        </div>`
      : "";
    const eventBlock = state.weekEvent.type === "choice"
      ? renderWeekEventChoices(state.weekEvent, showExactEffects)
      : `<div class="briefing-passive-note">${state.weekEventResolved ? "本周来件已经处理，结果已写入右侧影响栏。" : "这是一条自动生效类来件，确认后会写入本周状态。"}</div>`;
    const debugBlock = debugMode
      ? `<label class="evt-debug briefing-debug"><input type="checkbox" id="evtDebugToggle" ${state.debugShowEventEffects ? "checked" : ""}/> 调试：显示精确选项后果</label>`
      : "";
    const actionBlock = state.weekEventResolved
      ? `<button type="button" class="primary briefing-primary" id="btnEnterGlobal">进入本周取材地图</button>`
      : state.weekEvent.type === "passive"
        ? `<button type="button" class="briefing-primary" id="btnResolveEvent">${escapeHtml(state.weekEvent.confirmText || "确认本周来件")}</button>`
        : `<div class="briefing-action-note">先选择一个编辑方向，处理后进入取材地图。</div>`;
    elW.innerHTML = `
      <div class="briefing-head">
        <span>WEEK BRIEFING</span>
        <h2>第 ${state.week} 周 · 本周编辑部简报</h2>
        <p>先处理本周来件，再进入取材地图安排调查。</p>
      </div>
      <div class="briefing-grid">
        <aside class="briefing-source">
          <div class="briefing-source-mark" aria-hidden="true">${escapeHtml(state.weekEvent.sourceMark || "件")}</div>
          <div class="briefing-source-type">${escapeHtml(state.weekEvent.sourceType || "本周来件")}</div>
          <div class="briefing-source-label">${escapeHtml(state.weekEvent.sourceLabel || "编辑部")}</div>
        </aside>
        <section class="briefing-main">
          ${introBrief}
          <div class="briefing-event-title">${escapeHtml(state.weekEvent.title)}</div>
          <p class="briefing-event-body">${escapeHtml(state.weekEvent.body)}</p>
          ${eventBlock}
          <div class="briefing-actions">${actionBlock}</div>
        </section>
        ${renderWeekEventImpact(state.weekEvent)}
      </div>
      ${debugBlock}`;
    const dbg = document.getElementById("evtDebugToggle");
    if (dbg) {
      dbg.onchange = () => {
        state.debugShowEventEffects = !!dbg.checked;
        renderWeekStart();
      };
    }
    if (state.weekEvent.type === "passive") {
      const btn = document.getElementById("btnResolveEvent");
      if (btn) btn.onclick = () => {
        applyWeekEventDefault();
        renderWeekStart();
      };
    } else {
      elW.querySelectorAll("[data-evt-op]").forEach((btn) => {
        btn.onclick = () => {
          applyWeekEventChoice(Number(btn.getAttribute("data-evt-op")));
          renderWeekStart();
        };
      });
    }
    const enterGlobal = document.getElementById("btnEnterGlobal");
    if (enterGlobal) enterGlobal.onclick = () => {
      state.phase = "explore";
      setView("global");
      renderGlobal();
    };
    setView("weekStart");
    scheduleWeek1SoftTutorial(
      "w1_weekStart",
      "第一周 · 本周编辑部简报",
      [
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">本周从哪开始？</h4>
          <p class="tutorial-soft-lead">新一周从<strong>编辑部简报</strong>开场：这里会出现读者来信、线人爆料或势力函件。</p>
          <ul class="tutorial-soft-ul">
            <li>读完标题与正文，按界面提示处理即可。</li>
            <li>有选项时先看方向预告，再决定本周编辑部的处理口径。</li>
          </ul>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">接下来去哪？</h4>
          <ul class="tutorial-soft-ul">
            <li>处理完简报后，点<strong>进入本周取材地图</strong>，去各地取材。</li>
          </ul>
          <p class="tutorial-soft-note">点「知道了」或空白处可关窗；本周内同类提示不再弹出，新周目第一周会再出现。</p>
        </div>`,
      ],
    );
  }

  function globalRegionUnlockItems(region) {
    if (!region || region.unlocked) return [];
    if (region.id === "new_england") {
      const clippingDone = state.clues.some((c) => (c.title || "").includes("飞碟剪报")) || !!state.completedMissionIds.skin;
      return [
        { label: "声望", value: macro.声望, max: 55, gap: macro.声望 >= 55 ? "已满足" : `还差 ${55 - macro.声望}` },
        { label: "飞碟剪报", value: clippingDone ? 1 : 0, max: 1, gap: clippingDone ? "已完成" : "完成纽约深度链第一环" },
      ];
    }
    if (region.id === "western_archives") {
      return [
        { label: "公信", value: macro.公信, max: 60, gap: macro.公信 >= 60 ? "已满足" : `还差 ${60 - macro.公信}` },
        { label: "守序", value: macro.守序, max: 60, gap: macro.守序 >= 60 ? "已满足" : `还差 ${60 - macro.守序}` },
      ];
    }
    return [{ label: "线索", value: 0, max: 1, gap: "等待前置情报" }];
  }

  function globalProgressText(region) {
    if (!region || region.unlocked) return "";
    const items = globalRegionUnlockItems(region);
    if (!items.length) return "?";
    const best = Math.max(...items.map((x) => Math.round((Math.min(x.value, x.max) / Math.max(1, x.max)) * 100)));
    return `${best}%`;
  }

  function globalProgressGapText(region) {
    const progress = globalProgressText(region);
    const value = Number.parseInt(progress, 10);
    if (!Number.isFinite(value)) return "解锁进度未知";
    return `缺口 ${Math.max(0, 100 - value)}%`;
  }

  function globalRegionStats(data) {
    const nodes = data.visibleNodes || [];
    const leads = data.leads || [];
    return {
      targets: data.r.unlocked ? nodes.length : 0,
      timed: data.r.unlocked ? nodes.filter((n) => (n.checkType || "white") === "red" || n.deadlineDay != null || /突发/.test(n.name)).length : 0,
      leads: data.r.unlocked ? leads.length : 0,
      deep: data.r.unlocked ? nodes.filter((n) => n.chainType === "deep").length : 0,
    };
  }

  function globalSummaryCard(label, value, iconText, tone) {
    return `<div class="global-summary-card ${tone ? `tone-${escapeHtml(tone)}` : ""}">
      <div><span>${escapeHtml(label)}</span><span>${escapeHtml(iconText)}</span></div>
      <strong>${escapeHtml(value)}</strong>
    </div>`;
  }

  function globalIntelChip(text, tone) {
    return `<span class="global-intel-chip ${tone ? escapeHtml(tone) : ""}">${escapeHtml(text)}</span>`;
  }

  function globalNeedText(need) {
    return Object.entries(need || {})
      .map(([key, value]) => `${key}${value | 0}`)
      .join(" / ");
  }

  function globalNeedChips(need) {
    return Object.entries(need || {}).map(([key, value]) => globalIntelChip(`条件：${key}${value | 0}`, "condition"));
  }

  function globalRegionDecisionLabel(data) {
    if (!data || !data.r.unlocked) return "进度缺口";
    if (data.r.id === "us") return "难度：中等 | 推荐 ★★★";
    const hard = (data.visibleNodes || []).some((node) => node.difficulty === "hard" || node.riskTier === "high" || node.isBlackDiceTask);
    const timed = (data.visibleNodes || []).some((node) => (node.checkType || "white") === "red" || node.deadlineDay != null || /突发/.test(node.name));
    if (hard) return "难度：较高 | 推荐 ★★★★";
    if (timed) return "难度：中等 | 推荐 ★★★";
    return "难度：入门 | 推荐 ★★";
  }

  function globalRegionLogItems(data) {
    if (!data || !data.r.unlocked) return [];
    const items = [];
    const redNodes = (data.visibleNodes || [])
      .filter((node) => regionTaskTone(node) === "red")
      .map((node) => {
        const left = deadlineRemainingDays(node);
        return left != null ? `${node.name} 剩余 ${left} 天。` : `${node.name} 正在倒计时。`;
      });
    items.push(...redNodes);
    const running = state.activeMissions.filter((m) => m.status === "running" && m.regionId === data.r.id);
    if (running.length) items.push(`${running.length} 项任务正在执行，进入地区页查看队列。`);
    const deepCount = (data.visibleNodes || []).filter((node) => node.chainType === "deep").length;
    if (deepCount) items.push(`${deepCount} 条深度调查链有当前可推进环。`);
    const leadCount = (data.leads || []).length;
    if (leadCount) items.push(`${leadCount} 条线索可在地区页追查。`);
    return items.slice(0, 4);
  }

  function globalIntelRowHtml({ tone = "", mark = "目", title, chips = [] }) {
    return `<div class="global-intel-row ${escapeHtml(tone)}" aria-disabled="true">
      <span class="global-intel-mark">${escapeHtml(mark)}</span>
      <div class="global-intel-copy">
        <strong>${escapeHtml(title)}</strong>
        <div class="global-intel-meta">${chips.join("")}</div>
      </div>
    </div>`;
  }

  function globalNodePreviewHtml(regionId, node, locked = false) {
    const queued = findActiveMissionByNode(regionId, node.id);
    const tone = regionTaskTone(node);
    const deadlineLeft = tone === "red" ? deadlineRemainingDays(node) : null;
    const chips = [
      globalIntelChip(`成本 ${node.days || 1}天`, "cost"),
      ...globalNeedChips(node.need),
      node.enemyAttr ? globalIntelChip(`挑战：对手骰${node.enemyAttr}`, "challenge") : "",
      tone === "red" && deadlineLeft != null ? globalIntelChip(`成本 剩余${deadlineLeft}天`, "cost") : "",
      node.chainType === "deep" ? globalIntelChip(node.chainStage ? `信息 深度调查 · 当前任务${node.chainStage}` : "信息 深度调查", "info") : "",
      tone === "red" ? globalIntelChip("收益 截稿素材", "reward") : node.chainType === "deep" ? globalIntelChip("收益 阶段素材", "reward") : globalIntelChip("收益 常驻线索", "reward"),
      previousChainResult(node) ? globalIntelChip("信息 承接前序", "info") : "",
      queued ? globalIntelChip("状态 已派遣", "status") : "",
    ].filter(Boolean);
    return globalIntelRowHtml({
      tone: locked ? "locked" : tone,
      mark: locked ? "影" : tone === "red" ? "截" : node.chainType === "deep" ? "续" : "目",
      title: locked ? `${node.name}（轮廓）` : node.name,
      chips: locked ? [...chips, globalIntelChip("条件：待解锁", "condition")] : chips,
    });
  }

  function globalLeadPreviewHtml(regionId, lead) {
    const queued = findActiveMissionByLead(regionId, lead.id);
    const chips = [
      globalIntelChip(`成本 ${regionLeadDays(lead)}天`, "cost"),
      ...globalNeedChips(regionLeadNeed(lead)),
      globalIntelChip("信息 调查后生成任务", "info"),
      queued ? globalIntelChip("状态 已派遣", "status") : "",
    ].filter(Boolean);
    return globalIntelRowHtml({
      tone: "clue",
      mark: "线",
      title: lead.title,
      chips,
    });
  }

  function globalUnlockedPreviewHtml(data) {
    const rows = [
      ...data.leads.map((lead) => globalLeadPreviewHtml(data.r.id, lead)),
      ...data.visibleNodes.map((node) => globalNodePreviewHtml(data.r.id, node)),
    ];
    const shown = rows.slice(0, 4).join("");
    const more = Math.max(0, rows.length - 4);
    const logItems = globalRegionLogItems(data);
    return `<section class="global-preview-section">
      <div class="global-preview-head">
        <h4>区域情报预览</h4>
        <span>${rows.length} 条 · 进入后选择任务</span>
      </div>
      <div class="global-intel-list">${shown || `<div class="tip-inline">暂无可见情报。</div>`}</div>
      ${more ? `<div class="tip-inline">另有 ${more} 项情报将在地区页展开。</div>` : ""}
      <details class="global-action-log">
        <summary><span>本周记录</span><span>展开</span></summary>
        <ul>${(logItems.length ? logItems : ["本区暂无新日志，进入地区后开始派遣。"]).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      </details>
    </section>`;
  }

  function globalLockedPreviewHtml(data) {
    const unlocks = globalRegionUnlockItems(data.r).map((item) => {
      const pct = Math.max(0, Math.min(100, Math.round((Math.min(item.value, item.max) / Math.max(1, item.max)) * 100)));
      return `<div class="global-unlock-item">
        <div class="global-unlock-line">
          <strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.value)} / ${escapeHtml(item.max)}</span>
        </div>
        <div class="global-unlock-meter">
          <span style="width:${pct}%;"></span>
        </div>
        <div style="color:#94a3b8;font-size:12px;">${escapeHtml(item.gap)}</div>
      </div>`;
    }).join("");
    const previewNodes = (data.visibleNodes || [])
      .slice(0, 3)
      .map((node) => globalNodePreviewHtml(data.r.id, node, true))
      .join("");
    return `<section class="global-preview-section">
      <div class="global-preview-head">
        <h4>解锁进度</h4>
        <span>达成条件后进入地区</span>
      </div>
      <div class="global-unlock-list">${unlocks}</div>
      ${previewNodes ? `<div class="global-preview-head"><h4>锁定情报轮廓</h4><span>只读</span></div><div class="global-intel-list">${previewNodes}</div>` : `<div class="tip-inline">暂无可预览目标。</div>`}
    </section>`;
  }

  function globalRegionDetailHtml(data, mode) {
    const stats = globalRegionStats(data);
    const unlocked = data.r.unlocked;
    const summary = unlocked
      ? [
        globalSummaryCard("可见目标", stats.targets, "◎", ""),
        globalSummaryCard("限时机会", stats.timed, "◷", "red"),
        globalSummaryCard("线索", stats.leads, "□", "green"),
        globalSummaryCard("深度链", stats.deep, "▣", "violet"),
      ].join("")
      : [
        globalSummaryCard("可见目标", 0, "◎", ""),
        globalSummaryCard("缺口", globalRegionUnlockItems(data.r).length, "🔒", ""),
        globalSummaryCard("线索", "待开", "□", "green"),
        globalSummaryCard("深度链", "待开", "▣", "violet"),
      ].join("");
    const body = unlocked ? globalUnlockedPreviewHtml(data) : globalLockedPreviewHtml(data);
    return `<div class="global-detail">
      <div class="global-detail-head">
        <div class="global-detail-eyebrow">${mode === "preview" ? "悬停预览地区" : "当前选中地区"}</div>
        <div class="global-detail-titleline">
          <div>
          <h3>${escapeHtml(data.r.name)}</h3>
          <p>${escapeHtml(data.r.hint)}</p>
          </div>
          <span class="global-detail-status ${unlocked ? "open" : ""}">${escapeHtml(unlocked ? globalRegionDecisionLabel(data) : "进度缺口")}</span>
        </div>
      </div>
      <div class="global-summary-grid">${summary}</div>
      ${body}
    </div>`;
  }

  function renderGlobal() {
    unlockRegions();
    const elG = document.getElementById("view-global");
    const staffCount = dispatchStaffCounts();
    elG.innerHTML = `
      <div class="global-workflow-top">
        <button type="button" id="backFromGlobal" class="global-back-link">← 回合简报</button>
        <nav class="global-phase-rail" aria-label="本周流程">
          <span class="global-phase-step active"><b>1</b>探索</span>
          <span class="global-phase-divider" aria-hidden="true"></span>
          <span class="global-phase-step"><b>2</b>线索成稿</span>
          <span class="global-phase-divider" aria-hidden="true"></span>
          <span class="global-phase-step"><b>3</b>拖拽组版</span>
          <span class="global-phase-divider" aria-hidden="true"></span>
          <span class="global-phase-step"><b>4</b>结算</span>
        </nav>
        <div class="global-status-pills" aria-label="探索周状态">
          <span class="tag on">第 ${state.week} 周</span>
          <span class="tag">剩余 ${state.day} 日</span>
          <span class="tag">可派遣 ${staffCount.available}/${staffCount.total}</span>
        </div>
      </div>
      <div class="world-region-host" id="regionGrid"></div>`;
    const grid = document.getElementById("regionGrid");
    const regionData = REGIONS.map((r) => {
      const visibleNodes = getRegionNodes(r).filter(nodeVisible).filter(filterNodeTags);
      const leads = visibleRegionLeads(r.id);
      const eventCount = r.unlocked ? (visibleNodes.length + leads.length) : 0;
      const has = visibleNodes.length > 0;
      return { r, visibleNodes, leads, eventCount, has };
    });
    const dataById = Object.fromEntries(regionData.map((d) => [d.r.id, d]));
    if (!dataById[state.globalSelectedRegionId] || !dataById[state.globalSelectedRegionId].r.unlocked) {
      const firstUnlocked = regionData.find((d) => d.r.unlocked) || regionData[0];
      state.globalSelectedRegionId = firstUnlocked.r.id;
    }
    const selectedData = dataById[state.globalSelectedRegionId] || regionData[0];
    const pointsHtml = regionData.map(({ r, visibleNodes, eventCount, has }) => {
      const pos = REGION_MAP_POS[r.id] || { x: 50, y: 50, label: r.name };
      const selected = r.id === selectedData.r.id;
      const progress = !r.unlocked ? globalProgressText(r) : "";
      const countText = r.unlocked ? (eventCount > 0 ? (eventCount > 9 ? "9+" : eventCount) : "") : progress;
      const cls = `map-point ${r.unlocked ? "available" : "locked"} ${r.pulse && has ? "pulse" : ""} ${eventCount > 0 ? "has-event" : ""} ${countText ? "has-badge" : ""}`;
      const selectedStyle = selected ? "border-color:rgba(212,168,83,0.9);background:rgba(74,55,22,0.95);color:#fff4cf;box-shadow:0 0 0 1px rgba(212,168,83,0.22),0 14px 26px rgba(0,0,0,0.42);" : "";
      const hint = `${r.unlocked ? "可进入" : "未解锁"}${r.unlocked && has ? ` · 目标${visibleNodes.length}` : ""}${eventCount > 0 ? ` · 事件${eventCount}` : ""}${progress ? ` · ${globalProgressGapText(r)}` : ""}`;
      const badgeClass = r.unlocked ? "event-dot" : "event-dot lock-badge";
      const badgeHtml = countText ? `<span class="${badgeClass}">${escapeHtml(countText)}</span>` : "";
      const pointStyle = `left:${pos.x}%;top:${pos.y}%;${r.unlocked ? selectedStyle : ""}`;
      if (!r.unlocked) {
        return `<div class="${cls}" data-region="${r.id}" aria-disabled="true" style="${pointStyle}" title="${escapeHtml(hint)}"><span class="map-point-title">${escapeHtml(pos.label)}</span>${badgeHtml}</div>`;
      }
      return `<button type="button" class="${cls}" data-region="${r.id}" style="${pointStyle}" title="${escapeHtml(hint)}"><span class="map-point-title">${escapeHtml(pos.label)}</span>${badgeHtml}</button>`;
    }).join("");
    const choiceHtml = regionData.map((d) => {
      const selected = d.r.id === selectedData.r.id;
      const sub = d.r.unlocked ? globalRegionDecisionLabel(d) : `未解锁 · ${globalProgressGapText(d.r)}`;
      if (!d.r.unlocked) {
        return `<div class="global-region-choice is-locked" data-region="${d.r.id}" aria-disabled="true" title="${escapeHtml(sub)}">
        <strong>${escapeHtml(d.r.name)}</strong>
        <span>${escapeHtml(sub)}</span>
      </div>`;
      }
      return `<button type="button" class="global-region-choice ${selected ? "is-selected" : ""}" data-region="${d.r.id}">
        <strong>${escapeHtml(d.r.name)}</strong>
        <span>${escapeHtml(sub)}</span>
      </button>`;
    }).join("");
    grid.innerHTML = `
      <div class="world-map-wrap" style="grid-template-columns:repeat(auto-fit,minmax(min(360px,100%),1fr));align-items:stretch;">
        <div class="world-map" style="min-height:520px;height:min(720px,calc(100vh - 260px));background:linear-gradient(rgba(6,11,18,0.30),rgba(6,11,18,0.62)),url('Assets/world-map-background.svg') center/cover no-repeat,#07101e;">
          <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:0.72;">
            <path d="M30 38 C 32 33, 35 31, 39 30" fill="none" stroke="rgba(212,168,83,0.32)" stroke-width="0.8" stroke-dasharray="3 3"></path>
            <path d="M30 38 C 25 44, 21 48, 18 50" fill="none" stroke="rgba(212,168,83,0.28)" stroke-width="0.8" stroke-dasharray="3 3"></path>
            <path d="M18 50 C 25 44, 33 36, 39 30" fill="none" stroke="rgba(212,168,83,0.24)" stroke-width="0.8" stroke-dasharray="3 3"></path>
          </svg>
          ${pointsHtml}
          <div class="global-map-legend" aria-label="地图图例">
            <span class="tag on">选中区域可进入</span>
            <span class="tag global-tag-cost">限时机会</span>
            <span class="tag global-tag-info">深度链</span>
          </div>
        </div>
        <div class="map-side global-side">
          <div class="global-side-head">
            <div class="global-side-title">
              <h3><span class="global-step-badge">1</span><span>选择取材地区</span></h3>
              <p>查看地区情报预览，进入地区后再选择具体任务。</p>
            </div>
            <div class="global-region-selector" id="globalRegionChoices">${choiceHtml}</div>
            <div id="globalRegionDetail">${globalRegionDetailHtml(selectedData, "selected")}</div>
          </div>
          <div class="region-actions global-bottom-actions">
            <button type="button" id="btnEnterSelectedRegion" class="primary global-enter-action" ${selectedData.r.unlocked ? "" : "disabled"}>
              <span class="global-enter-icon" aria-hidden="true">${selectedData.r.unlocked ? "→" : "×"}</span>
              <span class="global-enter-label">${selectedData.r.unlocked ? `进入探索 · ${escapeHtml(selectedData.r.name)}` : `未解锁 · ${escapeHtml(selectedData.r.name)}`}</span>
            </button>
          </div>
        </div>
      </div>`;
    const paintLinkedState = (focusId, mode) => {
      const selectedId = state.globalSelectedRegionId;
      grid.querySelectorAll("[data-region]").forEach((node) => {
        const nodeId = node.getAttribute("data-region");
        const isChoice = node.classList.contains("global-region-choice");
        const locked = node.classList.contains("locked") || node.classList.contains("is-locked");
        const isFocused = nodeId === focusId;
        const isSelected = nodeId === selectedId;
        if (isChoice) {
          node.classList.toggle("is-selected", !locked && isSelected);
          node.classList.toggle("is-preview", !locked && isFocused && !isSelected && mode === "preview");
          return;
        }
        if (locked) {
          node.style.borderColor = "";
          node.style.background = "";
          node.style.color = "";
          node.style.boxShadow = "";
          return;
        }
        node.style.borderColor = isFocused || isSelected ? "rgba(212,168,83,0.9)" : "";
        node.style.background = isSelected ? "rgba(74,55,22,0.95)" : "";
        node.style.color = isSelected ? "#fff4cf" : "";
        node.style.boxShadow = isFocused || isSelected ? "0 0 0 1px rgba(212,168,83,0.26),0 16px 30px rgba(0,0,0,0.48)" : "";
      });
    };
    const updateEnterButton = (data) => {
      const enterBtn = document.getElementById("btnEnterSelectedRegion");
      if (!enterBtn || !data) return;
      enterBtn.disabled = !data.r.unlocked;
      const icon = enterBtn.querySelector(".global-enter-icon");
      const label = enterBtn.querySelector(".global-enter-label");
      if (icon) icon.textContent = data.r.unlocked ? "→" : "×";
      if (label) label.textContent = data.r.unlocked ? `进入探索 · ${data.r.name}` : `未解锁 · ${data.r.name}`;
    };
    const renderSelectedRegion = (id) => {
      const data = dataById[id] || selectedData;
      const detail = document.getElementById("globalRegionDetail");
      if (detail) detail.innerHTML = globalRegionDetailHtml(data, "selected");
      updateEnterButton(data);
      paintLinkedState(id, "selected");
    };
    const selectGlobalRegion = (id) => {
      const data = dataById[id];
      if (!data || !data.r.unlocked) return;
      state.globalSelectedRegionId = id;
      renderSelectedRegion(id);
    };
    const restoreSelected = () => paintLinkedState(state.globalSelectedRegionId, "selected");
    paintLinkedState(state.globalSelectedRegionId, "selected");
    grid.querySelectorAll(".map-point, .global-region-choice").forEach((div) => {
      const data = dataById[div.getAttribute("data-region")];
      if (!data || !data.r.unlocked) return;
      div.addEventListener("mouseenter", () => paintLinkedState(div.getAttribute("data-region"), "preview"));
      div.addEventListener("mouseleave", restoreSelected);
      div.addEventListener("click", () => {
        selectGlobalRegion(div.getAttribute("data-region"));
      });
    });
    const enterBtn = document.getElementById("btnEnterSelectedRegion");
    if (enterBtn) enterBtn.onclick = () => {
      const selected = dataById[state.globalSelectedRegionId];
      if (!selected || !selected.r.unlocked) return;
      state.regionId = selected.r.id;
      renderRegion();
      setView("region");
    };
    document.getElementById("backFromGlobal").onclick = () => renderWeekStart();
    updateNextDayButton();
    scheduleWeek1SoftTutorial(
      "w1_global",
      "第一周 · 美国取材地图",
      [
        `${tutorialSoftFigure(
          "Assets/tutorial-map-guide.svg",
          "取材地图示意：左侧可点区域，右侧显示选中区域详情",
          "上图为界面结构示意（非本局实时画面）。左：点陆块上的区域；右：只显示当前选中区域的目标、缺口与进入按钮。",
        )}<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">这张地图做什么用？</h4>
          <p class="tutorial-soft-lead">这是您的<strong>取材地图</strong>：先选一个区域，再进入当地版面。</p>
          <ul class="tutorial-soft-ul">
            <li>地图点和右侧小卡都可以<strong>预览 / 选中区域</strong>。</li>
            <li>主要操作在右下角：<strong>进入选中区域</strong>。</li>
          </ul>
        </div>`,
        `${tutorialSoftFigure(
          "Assets/tutorial-global-tags-guide.svg",
          "取材地图顶部题材筛选标签示意：科学、秘闻、大众",
          "与地图页顶栏一致：点标签可开关对应题材，地图点与右侧列表会随之隐藏或显示。",
        )}<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">筛选标签</h4>
          <p class="tutorial-soft-lead">顶部 <strong>科学 / 秘闻 / 大众</strong> 用来按题材口味筛目标，减少无关干扰。</p>
          <ul class="tutorial-soft-ul">
            <li>可<strong>多选</strong>：关掉的题材不会在地图与列表里碍眼。</li>
            <li>与正式取材地图页<strong>同一排按钮</strong>，进区域后仍可按需回想。</li>
          </ul>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">推进时间</h4>
          <ul class="tutorial-soft-ul">
            <li><strong>日程推进</strong>：进入当前地区后，在区域面板底部独立推进到下一天。</li>
            <li>时间推进后，到期的外派会<strong>依次结算</strong>。</li>
          </ul>
          <p class="tutorial-soft-note">本周内本提示只出现一次。</p>
        </div>`,
      ],
    );
  }

  function findActiveMission(predicate) {
    return state.activeMissions.find((x) => x.status === "running" && predicate(x));
  }

  function findActiveMissionByNode(regionId, nodeId) {
    return findActiveMission((x) => x.regionId === regionId && x.mission && x.mission.id === nodeId);
  }

  function findActiveMissionByLead(regionId, leadId) {
    return findActiveMission((x) => x.regionId === regionId && x.mission && x.mission.missionType === "leadInvestigation" && x.mission.leadId === leadId);
  }

  function staffAvatarsHtml(ids, extraClass = "", maxVisible = 4) {
    if (!ids || !ids.length) return "";
    const visible = ids.slice(0, maxVisible);
    const cls = extraClass ? ` ${extraClass}` : "";
    return `<span class="assigned-avatars${cls}">${visible
      .map((id, idx) => {
        const st = findStaff(id);
        if (!st) return "";
        const cut = idx === maxVisible - 1 && ids.length > maxVisible ? "cut-tail" : "";
        return `<img class="${cut}" src="${st.avatar}" title="${escapeHtml(st.name)}" alt="${escapeHtml(st.name)}"/>`;
      })
      .join("")}</span>`;
  }

  function mapAssignedAvatarsHtml(ids) {
    return staffAvatarsHtml(ids, "map-assigned-avatars", 3);
  }

  function assignedStaffNames(ids) {
    return (ids || [])
      .map((id) => findStaff(id))
      .filter(Boolean)
      .map((st) => st.name)
      .join("、");
  }

  function regionAssignedStatusHtml(queued, label = "已派遣") {
    if (!queued) return "";
    const names = assignedStaffNames(queued.staffIds);
    const title = names ? `${label}：${names}` : label;
    return `<span class="region-assigned-status" title="${escapeHtml(title)}">${escapeHtml(label)}</span>`;
  }

  function regionTaskTitleHtml(title, queued) {
    return `<h4 class="region-task-title"><span class="title-text">${escapeHtml(title)}</span>${regionAssignedStatusHtml(queued)}</h4>`;
  }

  function regionAssignedQueueInfoHtml(queued) {
    if (!queued) return "";
    const names = assignedStaffNames(queued.staffIds);
    const wait = Math.max(0, queued.remainingDays | 0);
    return `<div class="region-assigned-line">
      ${staffAvatarsHtml(queued.staffIds, "queue-assigned-avatars", 4)}
      <span class="region-assigned-copy">${names ? `执行中：${escapeHtml(names)}` : "执行中"}</span>
      <span class="region-assigned-wait">${wait}天后结算</span>
    </div>`;
  }

  function missionHeaderHtml(m, staffIds) {
    const region = REGIONS.find((x) => x.id === m.regionId);
    const regionName = region ? region.name : "未知区域";
    const typeLead = m.missionType === "leadInvestigation";
    const typeTag = typeLead ? "线索调查" : "探索任务";
    const typeCls = typeLead ? "lead" : "normal";
    const prog = state.dayResolutionInfo
      ? `当日结算 ${state.dayResolutionInfo.current}/${state.dayResolutionInfo.total}`
      : "单任务结算";
    const needText = Object.keys(m.need || {})
      .map((k) => `${k}${m.need[k] | 0}`)
      .join(" / ");
    const staffHtml = (staffIds || []).map((id) => {
      const st = findStaff(id);
      if (!st) return "";
      return `<span class="mission-staff-chip" data-staff-preview="${st.id}"><img src="${st.avatar}" alt="${escapeHtml(st.name)}"/><span class="nm">${escapeHtml(st.name)}</span></span>`;
    }).join("");
    return `<div class="mission-head">
      <div class="mission-head-top">
        <div class="mission-main">
          <span class="mission-tag ${typeCls}">${typeTag}</span>
          ${missionTypeBadgesHtml(m)}
          <span class="mission-name">${escapeHtml(m.name)}</span>
        </div>
        <span class="mission-prog">${prog}</span>
      </div>
      <div class="mission-meta">
        <span><b>区域</b>：${escapeHtml(regionName)}</span>
        <span><b>耗时</b>：${m.days | 0}天</span>
        <span><b>难度</b>：${m.difficulty === "hard" ? "困难" : m.difficulty === "easy" ? "简单" : "普通"}</span>
        <span><b>对手骰</b>：${m.enemyAttr | 0}</span>
        <span><b>需求</b>：${escapeHtml(needText || "无")}</span>
      </div>
      <div class="mission-staff">
        <span class="mission-staff-label">派遣队员</span>
        <div class="mission-staff-list">${staffHtml || `<span class="tip-inline">未配置</span>`}</div>
      </div>
    </div>`;
  }

  function bindMissionStaffHover(root) {
    const card = document.getElementById("staffHoverCard");
    if (!card || !root) return;
    const chips = root.querySelectorAll("[data-staff-preview]");
    if (!chips.length) return;
    const renderCard = (st) => {
      card.innerHTML = `<div class="staff-hover-head">
        <img src="${st.avatar}" alt="${escapeHtml(st.name)}"/>
        <div class="staff-hover-name">${escapeHtml(st.name)}</div>
      </div>
      <div class="staff-hover-grid">
        ${(st.specialty || []).map((a) => `<span>${escapeHtml(a)} 专精</span>`).join("") || "<span>综合角色</span>"}
      </div>`;
    };
    const place = (ev) => {
      const x = Math.min(window.innerWidth - 270, ev.clientX + 14);
      const y = Math.min(window.innerHeight - 170, ev.clientY + 12);
      card.style.left = `${Math.max(8, x)}px`;
      card.style.top = `${Math.max(8, y)}px`;
    };
    chips.forEach((chip) => {
      chip.addEventListener("mouseenter", (ev) => {
        const st = findStaff(chip.getAttribute("data-staff-preview"));
        if (!st) return;
        renderCard(st);
        card.classList.remove("hidden");
        place(ev);
      });
      chip.addEventListener("mousemove", place);
      chip.addEventListener("mouseleave", () => card.classList.add("hidden"));
    });
  }

  function assignedStaffSet() {
    const s = new Set();
    state.activeMissions.forEach((m) => {
      if (m && m.status !== "resolved") (m.staffIds || []).forEach((id) => s.add(id));
    });
    return s;
  }

  function isStaffAssigned(id, allowQueueId) {
    if (!id) return false;
    for (const m of state.activeMissions) {
      if (!m || m.status === "resolved") continue;
      if (allowQueueId && m.id === allowQueueId) continue;
      if ((m.staffIds || []).includes(id)) return true;
    }
    return false;
  }

  function dispatchStaffCounts() {
    const total = getAllStaff().length;
    const assigned = assignedStaffSet().size;
    return { available: total - assigned, total };
  }

  function dispatchCountSpanHtml() {
    const { available, total } = dispatchStaffCounts();
    return `<span class="dispatch-count" title="当前可派遣人数 / 队员总人数">（${available}/${total}）</span>`;
  }

  function runningMissionCount() {
    return state.activeMissions.filter((x) => x && x.status === "running").length;
  }

  function dueMissionCountAfterAdvance() {
    return state.activeMissions.filter((x) => x && x.status === "running" && (x.remainingDays | 0) <= 1).length;
  }

  function regionNextDayButtonText() {
    if (state.processingDayTick) return "结算中...";
    if ((state.day | 0) <= 0) return "进入结算";
    if ((state.day | 0) <= 1) return "结束探索周";
    return `推进到第 ${Math.min(7, dayIndexInWeek() + 1)} 天`;
  }

  function regionDayAdvanceSummaryText() {
    const running = runningMissionCount();
    const due = dueMissionCountAfterAdvance();
    if (running <= 0) return "尚未派遣任务；推进会消耗 1 天，并减少突发任务倒计时。";
    if (due > 0) return `已派遣 ${running} 项；推进后结算 ${due} 项到期任务，并减少突发任务倒计时。`;
    return `已派遣 ${running} 项；推进后减少任务剩余天数和突发任务倒计时。`;
  }

  function regionDayAdvanceHtml() {
    return `<div class="region-day-advance" role="group" aria-label="日程推进">
      <div class="region-day-copy">
        <strong>日程推进</strong>
        <span>${escapeHtml(regionDayAdvanceSummaryText())}</span>
      </div>
      <button type="button" id="btnNextDayRegion" class="region-day-button">
        <span class="arrow" aria-hidden="true"></span>
        <span class="region-day-button-label">${escapeHtml(regionNextDayButtonText())}</span>
      </button>
    </div>`;
  }

  function openQueuedMission(rec) {
    if (!rec || !rec.mission) return;
    state.mission = { ...rec.mission, missionQueueId: rec.id, toolDiceIds: (rec.toolDiceIds || []).slice() };
    state.selectedStaffIds = rec.staffIds.slice();
    state.selectedToolDiceIds = [];
    renderSetup();
    setView("setup");
  }

  function openNodeMission(regionId, node) {
    if (!node || node.chain === "locked") return;
    if (state.completedMissionIds[node.id]) return;
    const queued = findActiveMissionByNode(regionId, node.id);
    if (queued) {
      openQueuedMission(queued);
      return;
    }
    state.mission = { regionId, ...node };
    state.selectedStaffIds = [];
    state.selectedToolDiceIds = [];
    renderSetup();
    setView("setup");
  }

  function chainStatusText(n) {
    if (!n.chainType) return "";
    const total = n.chainStageTotal || (n.chainFinal ? n.chainStage : 4);
    const prefix = n.chainStage ? `第 ${n.chainStage}/${total} 环` : "连续任务";
    if (state.completedMissionIds[n.id]) return `${prefix} · 已完成`;
    if (n.isBlackDiceTask) return `${prefix} · 黑骰终局`;
    if (n.riskTier === "high") return `${prefix} · 危险`;
    return `${prefix} · 当前调查环`;
  }

  function previousChainResult(n) {
    if (!n.previousStageId) return "";
    return state.chainStageResults[n.previousStageId] || "";
  }

  function visibleRegionLeads(regionId) {
    return (state.regionLeadEvents[regionId] || []).filter((lead) => !lead.investigated);
  }

  const MAP_LABEL_CANDIDATES = (() => {
    const dxList = [0, -72, 72, -118, 118, -168, 168, -220, 220, -300, 300, -360, 360];
    const dyList = [0, -48, 48, -96, 96, -144, 144, -192, 192];
    const seen = new Set();
    const candidates = [];
    dyList.forEach((dy) => {
      dxList.forEach((dx) => {
        const key = `${dx}:${dy}`;
        if (seen.has(key)) return;
        seen.add(key);
        candidates.push({ dx, dy });
      });
    });
    return candidates.sort((a, b) => {
      const am = Math.abs(a.dx) + Math.abs(a.dy);
      const bm = Math.abs(b.dx) + Math.abs(b.dy);
      return am - bm || Math.abs(a.dy) - Math.abs(b.dy) || Math.abs(a.dx) - Math.abs(b.dx);
    });
  })();

  function mapLabelPriority(el) {
    if (el.classList.contains("region-chain-entry")) return el.classList.contains("is-open") ? 0 : 1;
    if (el.classList.contains("node-black")) return 2;
    if (el.classList.contains("node-danger") || el.classList.contains("node-red") || el.classList.contains("urgent")) return 3;
    if (el.classList.contains("lead")) return 5;
    return 4;
  }

  function unionRects(rects) {
    const valid = rects.filter((rect) => rect && rect.width > 0 && rect.height > 0);
    if (!valid.length) return null;
    return valid.reduce(
      (acc, rect) => ({
        left: Math.min(acc.left, rect.left),
        top: Math.min(acc.top, rect.top),
        right: Math.max(acc.right, rect.right),
        bottom: Math.max(acc.bottom, rect.bottom),
        width: Math.max(acc.right, rect.right) - Math.min(acc.left, rect.left),
        height: Math.max(acc.bottom, rect.bottom) - Math.min(acc.top, rect.top),
      }),
      {
        left: valid[0].left,
        top: valid[0].top,
        right: valid[0].right,
        bottom: valid[0].bottom,
        width: valid[0].width,
        height: valid[0].height,
      },
    );
  }

  function mapLabelRect(el) {
    if (!el.classList.contains("region-chain-entry")) return el.getBoundingClientRect();
    const chainRects = Array.from(el.querySelectorAll(".chain-card, .chain-link")).map((x) => x.getBoundingClientRect());
    return unionRects(chainRects) || el.getBoundingClientRect();
  }

  function showRegionMapHint(root, anchor, title, detail) {
    const map = root && root.querySelector ? root.querySelector(".region-map") : null;
    if (!map || !anchor || !anchor.getBoundingClientRect) {
      showToastMessage([title, detail].filter(Boolean).join("。"), "warn");
      return;
    }
    map.querySelectorAll(".region-map-hint").forEach((node) => node.remove());
    const mapRect = map.getBoundingClientRect();
    const anchorRect = anchor.getBoundingClientRect();
    const hint = document.createElement("div");
    const placeAbove = anchorRect.top - mapRect.top > 74;
    const x = Math.max(130, Math.min(mapRect.width - 130, anchorRect.left + anchorRect.width / 2 - mapRect.left));
    const y = placeAbove ? anchorRect.top - mapRect.top - 10 : anchorRect.bottom - mapRect.top + 10;
    hint.className = `region-map-hint${placeAbove ? "" : " is-below"}`;
    hint.style.left = `${Math.round(x)}px`;
    hint.style.top = `${Math.round(y)}px`;
    hint.innerHTML = `<strong>${escapeHtml(title)}</strong>${detail ? `<span>${escapeHtml(detail)}</span>` : ""}`;
    map.appendChild(hint);
    window.setTimeout(() => {
      if (hint.parentNode) hint.remove();
    }, 2600);
  }

  function inflateRect(rect, pad) {
    return {
      left: rect.left - pad,
      top: rect.top - pad,
      right: rect.right + pad,
      bottom: rect.bottom + pad,
      width: rect.width + pad * 2,
      height: rect.height + pad * 2,
    };
  }

  function overlapArea(a, b) {
    const w = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
    const h = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    return w * h;
  }

  function mapBoundsPenalty(rect, mapRect) {
    const pad = 8;
    return (
      Math.max(0, mapRect.left + pad - rect.left) +
      Math.max(0, rect.right - (mapRect.right - pad)) +
      Math.max(0, mapRect.top + pad - rect.top) +
      Math.max(0, rect.bottom - (mapRect.bottom - pad))
    );
  }

  function applyMapOffset(el, candidate) {
    el.style.setProperty("--map-offset-x", `${candidate.dx}px`);
    el.style.setProperty("--map-offset-y", `${candidate.dy}px`);
  }

  function resolveRegionMapLabelCollisions(root) {
    const map = root && root.querySelector ? root.querySelector(".region-map") : null;
    if (!map) return;
    const mapRect = map.getBoundingClientRect();
    const items = Array.from(map.querySelectorAll(".region-chain-entry, .region-point"))
      .map((el, index) => ({ el, index, priority: mapLabelPriority(el) }))
      .sort((a, b) => a.priority - b.priority || a.index - b.index);
    const previousTransitions = new Map();
    items.forEach(({ el }) => {
      previousTransitions.set(el, el.style.transition || "");
      el.style.transition = "none";
    });
    const placed = [];
    items.forEach(({ el }) => {
      applyMapOffset(el, MAP_LABEL_CANDIDATES[0]);
      let best = null;
      MAP_LABEL_CANDIDATES.forEach((candidate) => {
        applyMapOffset(el, candidate);
        const safePad = el.classList.contains("region-chain-entry") ? 34 : 14;
        const rect = inflateRect(mapLabelRect(el), safePad);
        const overlap = placed.reduce((sum, placedRect) => sum + overlapArea(rect, placedRect), 0);
        const bounds = mapBoundsPenalty(rect, mapRect);
        const movement = Math.abs(candidate.dx) + Math.abs(candidate.dy);
        const score = (overlap > 0 ? 1000000 + overlap * 1000 : 0) + bounds * 200 + movement * 0.25;
        if (!best || score < best.score) best = { candidate, rect, score };
      });
      if (!best) return;
      applyMapOffset(el, best.candidate);
      placed.push(best.rect);
    });
    const restoreTransitions = () => {
      items.forEach(({ el }) => {
        el.style.transition = previousTransitions.get(el) || "";
      });
    };
    if (window.requestAnimationFrame) window.requestAnimationFrame(restoreTransitions);
    else window.setTimeout(restoreTransitions, 0);
  }

  function scheduleRegionMapLabelLayout(root) {
    const run = () => resolveRegionMapLabelCollisions(root);
    if (window.requestAnimationFrame) window.requestAnimationFrame(run);
    else window.setTimeout(run, 0);
  }

  function deepChainMapEntryHtml(region, n, pos, meta) {
    const total = n.chainStageTotal || (n.chainFinal ? n.chainStage : 4);
    const stage = n.chainStage || 1;
    const nextStage = Math.min(total, stage + 1);
    const open = state.openDeepChainId === n.id;
    const expand = pos.x > 66 ? "expand-left" : "expand-right";
    const finalKind = n.isBlackDiceTask ? " chain-black" : n.riskTier === "high" ? " chain-danger" : "";
    const disabled = meta.disabled ? "disabled" : "";
    const queuedMark = meta.queued ? mapAssignedAvatarsHtml(meta.queued.staffIds) : "";
    const nextKicker = n.nextNode ? "下一条线索" : "终局";
    const nextTitle = n.nextNode ? "?" : "完结";
    const futureTitle = n.nextNode ? "?" : "";
    return `<button type="button" class="region-chain-entry ${expand}${open ? " is-open" : ""}${meta.match ? "" : " is-filtered"}${finalKind}" data-point-type="node" data-point-id="${n.id}" data-node="${n.id}" data-chain-entry="true" style="left:${pos.x}%;top:${pos.y}%;" ${disabled} title="${escapeHtml(n.name)} · ${meta.diffZh} · 深度链入口">
      <span class="chain-link" aria-hidden="true"></span>
      <span class="chain-card chain-future" aria-hidden="true" title="该任务未解锁">
        <span class="chain-stage">?</span>
        <span class="chain-copy"><span class="chain-kicker">未揭示</span><span class="chain-title">${escapeHtml(futureTitle || "?")}</span></span>
        <span class="chain-mark">?</span>
      </span>
      <span class="chain-card chain-next" title="该任务未解锁">
        <span class="chain-stage">${escapeHtml(nextStage)}</span>
        <span class="chain-copy"><span class="chain-kicker">${escapeHtml(nextKicker)}</span><span class="chain-title">${escapeHtml(nextTitle)}</span></span>
        <span class="chain-mark">?</span>
      </span>
      <span class="chain-card chain-current">
        <span class="chain-stage">${escapeHtml(stage)}</span>
        <span class="chain-copy"><span class="chain-kicker">深度调查</span><span class="chain-title">${escapeHtml(n.name)}</span></span>
        <span class="chain-mark">?</span>
      </span>
      ${queuedMark}
    </button>`;
  }

  function collectChainVisualNodes(region) {
    const out = [];
    const visit = (node) => {
      if (!node || node.chainType !== "deep" || !node.chainId) return;
      out.push(node);
      if (node.nextNode) visit(node.nextNode);
    };
    (region.nodes || []).forEach(visit);
    state.dynamicNodes
      .filter((x) => x.regionId === region.id)
      .forEach((x) => visit(x.node));
    const seen = new Set();
    return out
      .filter((n) => {
        if (seen.has(n.id)) return false;
        seen.add(n.id);
        return true;
      })
      .sort((a, b) => (a.chainId || "").localeCompare(b.chainId || "") || (a.chainStage || 0) - (b.chainStage || 0));
  }

  function chainOverlayHtml(region, visibleIds) {
    return "";
    const nodePos = NODE_MAP_POS[region.id] || {};
    const byChain = {};
    collectChainVisualNodes(region).forEach((n) => {
      if (!nodePos[n.id]) return;
      if (!byChain[n.chainId]) byChain[n.chainId] = [];
      byChain[n.chainId].push(n);
    });
    const lines = [];
    const ghosts = [];
    Object.values(byChain).forEach((list) => {
      list.sort((a, b) => (a.chainStage || 0) - (b.chainStage || 0));
      for (let i = 0; i < list.length - 1; i++) {
        const a = nodePos[list[i].id];
        const b = nodePos[list[i + 1].id];
        if (a && b) lines.push(`<line class="chain-line" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" />`);
      }
      list.forEach((n) => {
        if (visibleIds.has(n.id)) return;
        const p = nodePos[n.id];
        if (!p) return;
        const visual = missionVisualClass(n);
        const marker = n.isBlackDiceTask ? "▣" : (n.riskTier === "high" || n.isHighRisk) ? "!" : String(n.chainStage || "?");
        ghosts.push(`<span class="chain-ghost-point ${visual}" style="left:${p.x}%;top:${p.y}%;" title="${escapeHtml(n.name)}">${escapeHtml(marker)}</span>`);
      });
    });
    const svg = lines.length
      ? `<svg class="chain-lines" viewBox="0 0 100 100" preserveAspectRatio="none">${lines.join("")}</svg>`
      : "";
    return svg + ghosts.join("");
  }

  function deadlineRemainingDays(m) {
    if (!m || m.deadlineDay == null) return null;
    return Math.max(0, (m.deadlineDay | 0) - dayIndexInWeek());
  }

  function regionTaskTone(m) {
    if (m && m.isBlackDiceTask) return "black";
    if (m && (m.checkType || "white") === "red") return "red";
    if (m && m.chainType === "deep") return "deep";
    return "white";
  }

  function regionTaskIcon(m, fallback) {
    if (fallback === "clue") return "文";
    if (m && m.isBlackDiceTask) return "骰";
    if (m && (m.checkType || "white") === "red") return "截";
    if (m && m.chainType === "deep") return "续";
    if (m && (m.riskTier === "high" || m.isHighRisk)) return "!";
    return "↻";
  }

  function regionChip(text, cls) {
    return `<span class="region-task-chip ${cls || ""}">${escapeHtml(text)}</span>`;
  }

  function regionNeedChipsHtml(need) {
    return Object.entries(need || {})
      .map(([key, value]) => regionChip(`${key}${value | 0}`, "need"))
      .join("");
  }

  function regionLeadNeed(lead) {
    return lead.need || { 人脉: 2, 洞察: 2 };
  }

  function regionLeadDays(lead) {
    return lead.days || 2;
  }

  function regionNodeMetaHtml(n, queued) {
    const chips = [regionChip(`耗时 ${n.days}天`, "time")];
    if (!n.isBlackDiceTask && (n.riskTier === "high" || n.isHighRisk)) chips.push(regionChip("△ 危险", "danger"));
    if (n.isBlackDiceTask) chips.push(regionChip("骰 黑骰", "black"));
    if ((n.enemyAttr | 0) > 0) chips.push(regionChip(`▣ 对手骰 ${n.enemyAttr | 0}`, "enemy"));
    return chips.join("");
  }

  function regionDeepStageBadgeHtml(n) {
    if (!n || n.chainType !== "deep") return "";
    const stage = n.chainStage ? `当前任务 ${n.chainStage}` : "当前任务";
    return `<div class="region-task-chain-badge"><small>深度调查</small><strong>${escapeHtml(stage)}</strong></div>`;
  }

  function renderRegion() {
    const r = REGIONS.find((x) => x.id === state.regionId);
    const elR = document.getElementById("view-region");
    if (!r) return;
    const regionNodes = getRegionNodes(r);
    const leads = visibleRegionLeads(r.id);
    const nodePos = NODE_MAP_POS[r.id] || {};
    const visibleNodeList = regionNodes.filter(nodeVisible);
    const activeNodeList = visibleNodeList.filter((n) => !(n.chainType === "deep" && state.completedMissionIds[n.id]));
    const mapNodeList = activeNodeList;
    const chainOverlay = "";
    const pointHtmlNodes = mapNodeList
      .map((n) => {
        const match = filterNodeTags(n);
        const hiddenCls = n.kind === "hidden" ? "hidden-node" : "";
        const pos = n.mapPos || nodePos[n.id] || { x: 20 + Math.random() * 60, y: 20 + Math.random() * 60 };
        const diff = n.difficulty || "normal";
        const diffZh = diff === "easy" ? "简单" : diff === "hard" ? "困难" : "普通";
        const urgent = n.kind === "temp" || /突发/.test(n.name) || n.checkType === "red";
        const completed = !!state.completedMissionIds[n.id];
        const kindCls = `${n.kind === "temp" ? "temp" : ""} ${urgent ? "urgent" : ""} ${missionVisualClass(n)} ${hiddenCls} ${completed ? "completed-node" : ""}`.trim();
        const marker = completed ? "✓" : missionPointMark(n);
        const disabled = !match || n.chain === "locked" || completed;
        const queued = findActiveMissionByNode(r.id, n.id);
        if (n.chainType === "deep") {
          return deepChainMapEntryHtml(r, n, pos, { match, disabled, queued, diffZh });
        }
        const deadlineLeft = (n.checkType || "white") === "red" ? deadlineRemainingDays(n) : null;
        const markerHtml = deadlineLeft == null
          ? `<span class="point-mark">${marker}</span>`
          : `<span class="point-mark point-deadline">剩${deadlineLeft}天</span>`;
        return `<button type="button" class="region-point ${kindCls}${queued ? " has-assignees" : ""}" data-point-type="node" data-point-id="${n.id}" data-node="${n.id}" style="left:${pos.x}%;top:${pos.y}%;" ${disabled ? "disabled" : ""} title="${escapeHtml(n.name)} · ${diffZh} · ${escapeHtml(missionTypeTitle(n))}">
          ${markerHtml}<span class="point-title">${escapeHtml(n.name)}</span>${queued ? mapAssignedAvatarsHtml(queued.staffIds) : ""}
        </button>`;
      })
      .join("");
    const pointHtmlLeads = leads
      .map((lead, idx) => {
        const pos = nodePos[`lead_${lead.id}`] || { x: 16 + (idx % 3) * 20, y: 18 + Math.floor(idx / 3) * 16 };
        const queued = findActiveMissionByLead(r.id, lead.id);
        return `<button type="button" class="region-point lead${queued ? " has-assignees" : ""}" data-point-type="lead" data-point-id="${lead.id}" data-lead="${lead.id}" style="left:${pos.x}%;top:${pos.y}%;" title="${escapeHtml(lead.title)}">
          <span class="point-mark">?</span><span class="point-title">${escapeHtml(lead.title)}</span>${queued ? mapAssignedAvatarsHtml(queued.staffIds) : ""}
        </button>`;
      })
      .join("");
    const pointHtml = chainOverlay + pointHtmlNodes + pointHtmlLeads;
    const leadCards = leads
      .map((lead) => {
        const queued = findActiveMissionByLead(r.id, lead.id);
        return {
          queued,
          html: `<div class="lead-item region-task-card clue${queued ? " is-assigned" : " interactive"}" data-side-type="lead" data-side-id="${lead.id}">
        <div class="region-task-icon">${regionTaskIcon(null, "clue")}</div>
        <div class="region-task-main">
          ${regionTaskTitleHtml(lead.title, queued)}
          <div class="region-task-meta">
            ${regionChip(`耗时 ${regionLeadDays(lead)}天`, "time")}
            <span class="region-flow-chip">调查 -> 新任务</span>
          </div>
          <div class="region-task-needs">${regionNeedChipsHtml(regionLeadNeed(lead))}</div>
          ${lead.result ? `<div class="region-task-result">${escapeHtml(lead.result)}</div>` : ""}
          ${queued ? regionAssignedQueueInfoHtml(queued) : ""}
        </div>
      </div>`,
        };
      })
    const leadHtml = leadCards.filter((x) => !x.queued).map((x) => x.html).join("");
    const nodeCardHtml = (n) => {
        const match = filterNodeTags(n);
        const completed = !!state.completedMissionIds[n.id];
        const queued = findActiveMissionByNode(r.id, n.id);
        const interactive = match && !completed && !queued;
        const tone = regionTaskTone(n);
        const deadlineLeft = tone === "red" ? deadlineRemainingDays(n) : null;
        return {
          queued,
          html: `<div class="region-node-item region-task-card ${tone}${interactive ? " interactive" : ""}${match ? "" : " is-filtered"}${completed ? " is-completed" : ""}${queued ? " is-assigned" : ""}" data-side-type="node" data-side-id="${n.id}">
          <div class="region-task-icon">${completed ? "✓" : regionTaskIcon(n)}</div>
          <div class="region-task-main">
            ${regionTaskTitleHtml(n.name, queued)}
            <div class="region-task-meta">${regionNodeMetaHtml(n, queued)}</div>
            <div class="region-task-needs">${regionNeedChipsHtml(n.need)}</div>
            ${previousChainResult(n) ? `<div class="region-task-prev">前序线索：${escapeHtml(previousChainResult(n))}</div>` : ""}
            ${queued ? regionAssignedQueueInfoHtml(queued) : ""}
          </div>
          ${queued || deadlineLeft == null ? "" : `<div class="region-task-countdown"><small>剩余</small><strong>${deadlineLeft}天</strong></div>`}
          ${queued ? "" : regionDeepStageBadgeHtml(n)}
        </div>`,
        };
    };
    const nodeCards = activeNodeList.map(nodeCardHtml);
    const sideHtml = nodeCards.filter((x) => !x.queued).map((x) => x.html).join("");
    const assignedHtml = [...leadCards, ...nodeCards].filter((x) => x.queued).map((x) => x.html).join("");
    const assignedQueueHtml = assignedHtml
      ? `<section class="region-assigned-queue" aria-label="已派遣任务队列">
          <div class="region-assigned-queue-head">
            <span>已派遣 · 执行中</span>
            <small>${state.activeMissions.filter((x) => x.status === "running" && x.regionId === r.id).length} 项执行中</small>
          </div>
          <div class="region-assigned-list">${assignedHtml}</div>
        </section>`
      : "";
    elR.innerHTML = `<div class="view-title-row">
        <h2>${escapeHtml(r.name)}</h2>
        ${dispatchCountSpanHtml()}
      </div>
      <div class="region-map-wrap">
        <div class="region-map">${pointHtml}</div>
        <div class="region-node-side">
          <h3>区域节点情报</h3>
          <div class="region-task-list">${leadHtml}${sideHtml}${assignedQueueHtml}</div>
        </div>
      </div>
      ${regionDayAdvanceHtml()}`;
    const regionMap = elR.querySelector(".region-map");
    if (regionMap) {
      regionMap.addEventListener("click", (ev) => {
        if (!state.openDeepChainId) return;
        const target = ev.target && ev.target.closest ? ev.target : null;
        if (target && target.closest(".region-chain-entry, .region-point")) return;
        const closingChainId = state.openDeepChainId;
        state.openDeepChainId = null;
        if (state.regionLinkedTarget === `node:${closingChainId}`) state.regionLinkedTarget = null;
        renderRegion();
      });
    }
    elR.querySelectorAll(".region-point").forEach((btn) => {
      btn.addEventListener("click", () => {
        const pointType = btn.getAttribute("data-point-type");
        const pointId = btn.getAttribute("data-point-id");
        state.regionLinkedTarget = `${pointType}:${pointId}`;
        syncRegionLinkedState(elR, state.regionLinkedTarget);
        if (pointType === "lead") {
          investigateRegionLead(r.id, pointId);
          return;
        }
        if (pointType !== "node") return;
        const nid = btn.getAttribute("data-node");
        const n = regionNodes.find((x) => x.id === nid);
        openNodeMission(r.id, n);
      });
    });
    elR.querySelectorAll(".region-chain-entry").forEach((btn) => {
      btn.addEventListener("click", (ev) => {
        const pointId = btn.getAttribute("data-point-id");
        const n = regionNodes.find((x) => x.id === pointId);
        if (!n) return;
        const isOpen = state.openDeepChainId === pointId;
        const clickedCurrentRing = ev.target && ev.target.closest && ev.target.closest(".chain-current");
        const clickedLockedRing = ev.target && ev.target.closest && ev.target.closest(".chain-next, .chain-future");
        state.regionLinkedTarget = `node:${pointId}`;
        if (isOpen && clickedCurrentRing) {
          openNodeMission(r.id, n);
          return;
        }
        if (isOpen && clickedLockedRing) {
          showRegionMapHint(elR, clickedLockedRing, "该任务未解锁", "完成当前环后将解锁下一条线索。");
          syncRegionLinkedState(elR, state.regionLinkedTarget);
          return;
        }
        if (!isOpen) {
          state.openDeepChainId = pointId;
          renderRegion();
          return;
        }
        syncRegionLinkedState(elR, state.regionLinkedTarget);
      });
    });
    elR.querySelectorAll(".region-node-item.interactive[data-side-type='node']").forEach((row) => {
      row.addEventListener("click", (ev) => {
        if (ev.target && ev.target.closest && ev.target.closest("button")) return;
        const n = regionNodes.find((x) => x.id === row.getAttribute("data-side-id"));
        openNodeMission(r.id, n);
      });
    });
    elR.querySelectorAll(".lead-item.interactive[data-side-type='lead']").forEach((row) => {
      row.addEventListener("click", (ev) => {
        if (ev.target && ev.target.closest && ev.target.closest("button")) return;
        investigateRegionLead(r.id, row.getAttribute("data-side-id"));
      });
    });
    bindRegionLinking(elR);
    scheduleRegionMapLabelLayout(elR);
    const nd = document.getElementById("btnNextDayRegion");
    if (nd) nd.onclick = () => advanceOneDay();
    scheduleWeek1SoftTutorial(
      "w1_region",
      "第一周 · 区域版面",
      [
        `${tutorialSoftFigure(
          "Assets/tutorial-region-guide.svg",
          "区域版面示意：常隐感叹号派字、列表联动与三种点说明",
          "上图下方三条为图例摘要；左为地图点位，右为可与地图联动高亮的列表。",
        )}<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">图例在说什么？</h4>
          <ul class="tutorial-soft-ul">
            <li><strong>常</strong>：常驻探索点，一般始终在图上可见。</li>
            <li><strong>隐</strong>：隐藏点，需满足条件（如线索、进度）后才出现。</li>
            <li><strong>!</strong>：临时热点，常带截止天数，过期可能消失。</li>
            <li>已派人手的格子会标<strong>派</strong>，避免重复踩坑。</li>
          </ul>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">怎么出发？</h4>
          <p class="tutorial-soft-lead">点开一条线后，右侧可<strong>组小队</strong>。</p>
          <ul class="tutorial-soft-ul">
            <li>注意「调查」「现场」两侧的骰数门槛：凑够再派遣更稳妥。</li>
            <li>不够也能去，但成功率会吃亏。</li>
          </ul>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">线索类条目</h4>
          <p class="tutorial-soft-lead"><strong>线索</strong>走调查流程，跑通有机会<strong>解锁新节点</strong>。</p>
          <p class="tutorial-soft-note">关窗后本周不再用弹窗打断您。</p>
        </div>`,
      ],
    );
  }

  function syncRegionLinkedState(root, key) {
    root.querySelectorAll(".region-point, .region-chain-entry, .region-node-item, .lead-item").forEach((el) => el.classList.remove("is-linked"));
    if (!key) return;
    const split = key.indexOf(":");
    if (split < 0) return;
    const t = key.slice(0, split);
    const id = key.slice(split + 1);
    const p = root.querySelector(`.region-point[data-point-type="${t}"][data-point-id="${id}"], .region-chain-entry[data-point-type="${t}"][data-point-id="${id}"]`);
    const s = root.querySelector(`[data-side-type="${t}"][data-side-id="${id}"]`);
    if (p) p.classList.add("is-linked");
    if (s) s.classList.add("is-linked");
  }

  function bindRegionLinking(root) {
    const setLinked = (key) => syncRegionLinkedState(root, key || state.regionLinkedTarget);
    root.querySelectorAll("[data-side-type]").forEach((el) => {
      const t = el.getAttribute("data-side-type");
      const id = el.getAttribute("data-side-id");
      const key = `${t}:${id}`;
      el.addEventListener("mouseenter", () => setLinked(key));
      el.addEventListener("mouseleave", () => setLinked(null));
      el.addEventListener("click", (ev) => {
        state.regionLinkedTarget = key;
        syncRegionLinkedState(root, key);
      });
    });
    root.querySelectorAll(".region-point, .region-chain-entry").forEach((el) => {
      const t = el.getAttribute("data-point-type");
      const id = el.getAttribute("data-point-id");
      const key = `${t}:${id}`;
      el.addEventListener("mouseenter", () => setLinked(key));
      el.addEventListener("mouseleave", () => setLinked(null));
    });
    syncRegionLinkedState(root, state.regionLinkedTarget);
  }

  function showStaffDetail(staff, relevantNeed) {
    if (!staff) return;
    showConfirmPopup(
      `${staff.name} · 角色骰详情`,
      staffDetailHtml(staff, relevantNeed || (state.mission && state.mission.need) || {}),
      "角色骰系统",
    ).then((ok) => {
      if (!ok || state.view !== "setup" || !state.mission) return;
      if (!state.selectedStaffIds.includes(staff.id)) {
        const maxStaff = missionMaxStaff(state.mission);
        if (!canAddStaffToDispatch(staff, maxStaff)) return;
        state.selectedStaffIds.push(staff.id);
      }
      renderSetup();
    });
    setTimeout(() => {
      const ok = document.getElementById("confirmPopupOk");
      const cancel = document.getElementById("confirmPopupCancel");
      if (ok) ok.textContent = state.view === "setup" ? (state.selectedStaffIds.includes(staff.id) ? "已在本次骰池" : "加入本次骰池") : "确认";
      if (cancel) cancel.textContent = "返回";
    }, 0);
  }

  function dispatchCapacityMessage(staff, maxStaff) {
    const name = staff && staff.name ? staff.name : "该角色";
    return `本任务最多派遣 ${maxStaff} 人。请先手动撤下一名已选角色，再选择 ${name}。`;
  }

  function showToastMessage(message, tone = "") {
    if (!el.toast) el.toast = document.getElementById("toast");
    if (!el.toast) return;
    if (state.undoTimer) {
      clearTimeout(state.undoTimer);
      state.undoTimer = null;
    }
    state.lastReplaceAction = null;
    el.toast.innerHTML = `<span>${escapeHtml(message)}</span>`;
    el.toast.className = `nm-toast show ${tone}`.trim();
    state.undoTimer = setTimeout(() => {
      el.toast.classList.remove("show");
      el.toast.classList.remove(tone);
    }, 2200);
  }

  function canAddStaffToDispatch(staff, maxStaff) {
    if (state.selectedStaffIds.length < maxStaff) return true;
    showToastMessage(dispatchCapacityMessage(staff, maxStaff), "warn");
    return false;
  }

  function tempStringerStaff() {
    return TEMP_STAFF_POOL.find((s) => s.id === "temp_stringer");
  }

  function isTempStringerHired() {
    return state.tempStaffIds.includes("temp_stringer");
  }

  function isTempStringerSelected() {
    return state.selectedStaffIds.includes("temp_stringer");
  }

  function ensureTempStringerHired() {
    if (isTempStringerHired()) return;
    state.tempHireUsed = true;
    state.tempStaffIds.push("temp_stringer");
    addMacro({ 声望: -1 });
    log("本周雇佣临时线人：花费不菲，但获得一颗完整临时角色骰；之后可在候选角色中加入或撤回。");
  }

  function toggleTempStringerForDispatch(maxStaff) {
    const staff = tempStringerStaff();
    if (!staff) return false;
    if (isTempStringerHired()) return false;
    ensureTempStringerHired();
    showToastMessage("临时线人已加入候选角色；选择它会占用 1 个角色槽。");
    return true;
  }

  function capacitySlotsHtml(selected, max) {
    return `<span class="capacity-track" title="本任务人数容量">${Array.from({ length: max }, (_, i) => `<span class="capacity-slot ${i < selected ? "filled" : ""}"></span>`).join("")}</span>`;
  }

  function staffPoolCardHtml(staff, need) {
    const fit = staffFitSummary(staff, need || {});
    return `<div class="pool-card">
      <div class="pool-card-head">
        <img src="${staff.avatar}" alt="${escapeHtml(staff.name)}"/>
        <div>
          <div class="pool-card-name">${escapeHtml(staff.name)}${staff.temporary ? " · 临时" : ""}</div>
          <div class="risk-reason">${escapeHtml(fit.line)}</div>
        </div>
      </div>
      ${diceFacesHtml(diceFacesForStaff(staff), need || {}, "pool-dice-faces")}
    </div>`;
  }

  function toolPoolCardHtml(tool) {
    return `<div class="pool-card tool">
      <div class="pool-card-head">
        <span class="tool-avatar">道</span>
        <div>
          <div class="pool-card-name">${escapeHtml(tool.name)}</div>
          <div class="risk-reason">不占人数 · 使用后消耗</div>
        </div>
      </div>
      ${diceFacesHtml(tool.faces || [], state.mission ? state.mission.need : {}, "pool-dice-faces")}
    </div>`;
  }

  function dicePoolPreviewHtml(m, dicePreview, maxStaff) {
    const selectedStaff = (state.selectedStaffIds || []).map(findStaff).filter(Boolean);
    const selectedTools = (state.selectedToolDiceIds || [])
      .map((id) => state.toolDiceInventory.find((x) => x.id === id))
      .filter(Boolean);
    const emptyCount = Math.max(0, maxStaff - selectedStaff.length);
    const cards = [
      ...selectedStaff.map((s) => staffPoolCardHtml(s, m.need || {})),
      ...Array.from({ length: emptyCount }, (_, i) => `<div class="pool-card empty">可选角色槽 ${selectedStaff.length + i + 1}/${maxStaff}</div>`),
    ].join("");
    const tools = selectedTools.length
      ? `<div class="pool-tools-row">${selectedTools.map(toolPoolCardHtml).join("")}</div>`
      : `<div class="pool-tools-row"><div class="pool-card empty">道具骰空槽 · 可从下方选择一次性道具</div></div>`;
    return `<div class="dice-pool-preview">
      <div class="dice-pool-preview-head">
        <div class="dice-pool-preview-title">本次骰池预览</div>
        <div><strong>已选 ${selectedStaff.length}/${maxStaff} 人</strong> ${capacitySlotsHtml(selectedStaff.length, maxStaff)}</div>
        <div class="task-type-chip task-${dicePreview.risk === "高" ? "danger" : dicePreview.risk === "中" ? "high" : "white"}">风险：${escapeHtml(dicePreview.risk)}</div>
      </div>
      <div class="risk-reason">${escapeHtml(dicePreview.reason)}</div>
      <div class="pool-card-grid" style="margin-top:8px;">${cards}</div>
      ${tools}
    </div>`;
  }

  function dispatchLabSelectedTools() {
    return (state.selectedToolDiceIds || [])
      .map((id) => state.toolDiceInventory.find((x) => x.id === id && !x.used))
      .filter(Boolean);
  }

  function dispatchLabNeedStats(m, staffIds, tools) {
    const need = (m && m.need) || {};
    const needKeys = Object.keys(need);
    const values = {};
    let totalFaces = 0;
    let relevantFaces = 0;
    let blankFaces = 0;
    const faceLists = [];
    (staffIds || []).forEach((id) => {
      const staff = findStaff(id);
      if (!staff) return;
      const faces = diceFacesForStaff(staff);
      faceLists.push(faces);
      faces.forEach((face) => {
        totalFaces += 1;
        if (!face || face.blank) {
          blankFaces += 1;
          return;
        }
        if (face.attr && need[face.attr] != null) {
          relevantFaces += 1;
          values[face.attr] = (values[face.attr] || 0) + (face.value || 0);
        }
      });
    });
    (tools || []).forEach((tool) => {
      const faces = tool.faces || [];
      faceLists.push(faces);
      faces.forEach((face) => {
        totalFaces += 1;
        if (!face || face.blank) {
          blankFaces += 1;
          return;
        }
        if (face.attr && need[face.attr] != null) {
          relevantFaces += 1;
          values[face.attr] = (values[face.attr] || 0) + (face.value || 0);
        }
      });
    });
    const gaps = needKeys
      .map((k) => ({ k, gap: Math.max(0, (need[k] || 0) - (values[k] || 0)), value: values[k] || 0, need: need[k] || 0 }))
      .filter((x) => x.gap > 0);
    const needValue = needKeys.reduce((sum, k) => sum + (need[k] || 0), 0);
    const coveredValue = needKeys.reduce((sum, k) => sum + Math.min(values[k] || 0, need[k] || 0), 0);
    const selectedStaff = (staffIds || []).map(findStaff).filter(Boolean);
    const nonContributingStaff = selectedStaff.filter((staff) => !staffFitSummary(staff, need).covers.length).length;
    const targetValue = needTargetValue(need);
    const potentialValue = needKeys.reduce((sum, k) => sum + (values[k] || 0), 0);
    const successChance = successChanceForNeed(need, faceLists);
    const bestSingleStaffChance = selectedStaff.reduce((best, staff) => {
      return Math.max(best, successChanceForNeed(need, [diceFacesForStaff(staff)]));
    }, 0);
    return { need, needKeys, values, totalFaces, relevantFaces, blankFaces, gaps, needValue, coveredValue, nonContributingStaff, targetValue, potentialValue, successChance, bestSingleStaffChance };
  }

  function dispatchLabRisk(m, stats, selectedCount) {
    if (!selectedCount) return { label: "未评估", reason: "先选至少 1 名角色，系统会显示本次是否能达标。" };
    if (!stats.relevantFaces) return { label: "高", reason: "当前骰池没有可用需求面，建议换人或补道具骰。" };
    const chanceText = `实际达标率约 ${formatChance(stats.successChance)}`;
    const targetText = `有效点 ${stats.potentialValue || 0}/${stats.targetValue || 0}`;
    const lift = selectedCount > 1 ? formatDisplayedChanceLift(stats.successChance || 0, stats.bestSingleStaffChance || 0) : "";
    const liftText = lift ? `；较单人最佳 ${lift}` : "";
    const idleText = stats.nonContributingStaff ? `；${stats.nonContributingStaff} 名角色没有补到缺口` : "";
    if (stats.successChance <= 0) {
      return { label: "高", reason: `当前骰池还无法达标；${targetText}${idleText}。` };
    }
    if (stats.successChance >= 0.55) {
      return { label: "可搏", reason: `${chanceText}${liftText}；当前骰池已覆盖任务需求。` };
    }
    if (stats.successChance >= 0.3) {
      return { label: "偏险", reason: `${chanceText}${liftText}；${targetText}，可以尝试，也可继续补关键骰面。` };
    }
    return { label: "高", reason: `${chanceText} 偏低${liftText}；${targetText}，建议补关键骰面。` };
  }

  function dispatchRiskChipClass(label) {
    if (label === "高") return "danger";
    if (label === "偏险") return "high";
    return "white";
  }

  function dispatchLabActionDisabledReason(m) {
    if (!state.selectedStaffIds.length) return "先选择至少 1 名角色";
    if (m.days > state.day) return "剩余天数不足";
    if (state.missionResolving || state.processingDayTick) return "当前正在结算";
    return "";
  }

  function dispatchLabStaffSummaryHtml(staff, m) {
    const need = (m && m.need) || {};
    const fit = staffFitSummary(staff, need);
    return `<div class="dispatch-staff-summary">
      <div class="dispatch-staff-summary-row"><span>任务贡献</span><strong>${escapeHtml(fit.stats.relevantValues || 0)}</strong></div>
      <div class="dispatch-staff-summary-row"><span>相关面</span><strong>${escapeHtml(fit.stats.relevant || 0)}/6</strong></div>
      ${Object.keys(need).map((key) => {
        const value = diceFacesForStaff(staff).reduce((sum, face) => sum + (face && face.attr === key ? face.value || 0 : 0), 0);
        return `<div class="dispatch-staff-summary-row"><span>${escapeHtml(key)}来源</span><strong>${escapeHtml(value)}</strong></div>`;
      }).join("")}
    </div>`;
  }

  function dispatchLabNeedRowsHtml(m, stats) {
    const need = (m && m.need) || {};
    const keys = Object.keys(need);
    if (!keys.length) return `<div class="tip-inline">本任务没有明确需求。</div>`;
    const target = stats.needValue || keys.reduce((sum, k) => sum + (need[k] || 0), 0);
    const covered = stats.coveredValue || keys.reduce((sum, k) => sum + Math.min(stats.values[k] || 0, need[k] || 0), 0);
    const targetPct = target ? Math.max(0, Math.min(100, Math.round((covered / target) * 100))) : 100;
    const targetRow = `<div class="dispatch-need-summary">
      <div class="dispatch-need-row ${covered >= target ? "is-met" : ""}" style="margin-bottom:0;">
        <div class="dispatch-need-line"><strong>需求覆盖：${escapeHtml(covered)} / ${escapeHtml(target)}</strong><span>实掷达标率 ${escapeHtml(formatChance(stats.successChance))}</span></div>
        <div class="dispatch-meter"><span style="width:${targetPct}%"></span></div>
      </div>
    </div>`;
    const sourceRows = keys.map((k) => {
      const value = stats.values[k] || 0;
      const req = need[k] || 0;
      const pct = req ? Math.max(0, Math.min(100, Math.round((value / req) * 100))) : 100;
      const met = value >= req;
      const gap = Math.max(0, req - value);
      const stateText = met ? `已备 ${value}/${req}` : `还差 ${gap} · 已备 ${value}/${req}`;
      return `<div class="dispatch-need-row ${met ? "is-met" : ""}">
        <div class="dispatch-need-line"><strong>${escapeHtml(k)}</strong><span>${escapeHtml(stateText)}</span></div>
        <div class="dispatch-meter"><span style="width:${pct}%;"></span></div>
      </div>`;
    }).join("");
    return `${targetRow}<div class="dispatch-source-list">${sourceRows}</div>`;
  }

  function dispatchLabTaskSummaryHtml(m) {
    const red = (m.checkType || "white") === "red";
    const danger = m.riskTier === "high" || m.isHighRisk;
    const deadlineLeft = red ? deadlineRemainingDays(m) : null;
    const kindText = m.missionType === "leadInvestigation" ? "线索调查" : "探索任务";
    const meta = [
      kindText,
      `耗时 ${m.days}天`,
    ].filter(Boolean).join(" · ");
    const deadlineHtml = red ? `<div class="dispatch-deadline-block">
      <span>截稿关闭</span>
      <strong>${deadlineLeft == null ? "到期" : `剩余 ${deadlineLeft}天`}</strong>
    </div>` : "";
    const consequence = [
      red ? "成功或失败后都会结束" : "",
      danger ? "失败可能造成队员状态损伤" : "",
      m.chainType === "deep" ? "完成后推进线索" : "",
      m.isBlackDiceTask ? "进入黑骰特殊判定" : "",
    ].filter(Boolean).join("；");
    return `<section class="dispatch-lab-task">
      <div class="dispatch-task-head">
        <div>
          <div class="dispatch-task-title">${escapeHtml(m.name)}</div>
          <div class="dispatch-task-tags">${dispatchTaskBadgesHtml(m)}<span class="dispatch-task-meta">${escapeHtml(meta)}</span></div>
        </div>
        ${deadlineHtml}
      </div>
      ${consequence ? `<div class="dispatch-consequence">${escapeHtml(consequence)}</div>` : ""}
      ${missionStoryBriefHtml(m)}
    </section>`;
  }

  function dispatchLabStaffSlotHtml(staff, m) {
    return `<div class="dispatch-slot-card">
      <div class="dispatch-slot-head">
        <img src="${staff.avatar}" alt="${escapeHtml(staff.name)}"/>
        <div>
          <div class="dispatch-slot-name">${escapeHtml(staff.name)}${staff.temporary ? " · 临时" : ""}</div>
        </div>
        <button type="button" class="dispatch-slot-remove" data-remove-selected-staff="${escapeHtml(staff.id)}">移出</button>
      </div>
      ${diceNetHtml(diceFacesForStaff(staff), m.need || {}, "dispatch-dice-net dispatch-slot-net")}
    </div>`;
  }

  function dispatchLabPoolHtml(m, maxStaff) {
    const selectedStaff = (state.selectedStaffIds || []).map(findStaff).filter(Boolean);
    const tools = dispatchLabSelectedTools();
    const emptyCount = Math.max(0, maxStaff - selectedStaff.length);
    const slots = [
      ...selectedStaff.map((staff) => dispatchLabStaffSlotHtml(staff, m)),
      ...Array.from({ length: emptyCount }, (_, i) => `<div class="dispatch-slot-card empty">角色槽 ${selectedStaff.length + i + 1}/${maxStaff}<br/><span>点击下方角色加入骰池</span></div>`),
    ].join("");
    const toolCards = tools.map((tool) => `<div class="pool-card tool">
      <div class="pool-card-head"><span class="tool-avatar">道</span><div><div class="pool-card-name">${escapeHtml(tool.name)}</div><div class="risk-reason">不占人数 · 一次性</div></div></div>
      ${diceFacesHtml(tool.faces || [], m.need || {}, "pool-dice-faces")}
    </div>`).join("");
    return `<div class="dispatch-lab-panel">
      <div class="dispatch-lab-panel-title"><span>本次骰池</span><span>已选 ${selectedStaff.length}/${maxStaff} 人 ${capacitySlotsHtml(selectedStaff.length, maxStaff)}</span></div>
      <div class="dispatch-slot-grid">${slots}</div>
      <div class="dispatch-lab-tools">${toolCards || `<div class="pool-card empty" style="min-height:54px;">道具骰空槽 · 可在下方选择一次性道具</div>`}</div>
      ${dispatchLabResourcesHtml(maxStaff)}
    </div>`;
  }

  function dispatchLabRunBlockHtml(m, stats, risk, maxStaff) {
    const selectedCount = state.selectedStaffIds.length;
    const riskChance = selectedCount ? ` · ${formatChance(stats.successChance)}` : "";
    const disabledReason = dispatchLabActionDisabledReason(m);
    const buttonText = state.missionResolving
      ? "执行中..."
      : disabledReason
        ? (disabledReason === "先选择至少 1 名角色" ? "先选择角色后开始" : disabledReason)
        : `${m.missionType === "leadInvestigation" ? "开始线索调查" : "开始调查"}（${m.days}天后判定）`;
    return `<aside class="dispatch-lab-panel">
      <div class="dispatch-lab-panel-title"><span>需求覆盖</span><span class="task-type-chip task-${dispatchRiskChipClass(risk.label)}">风险：${escapeHtml(risk.label)}${escapeHtml(riskChance)}</span></div>
      ${dispatchLabNeedRowsHtml(m, stats)}
      <div class="dispatch-risk-box">${escapeHtml(risk.reason)}</div>
      <div class="dispatch-lab-actions">
        <button type="button" id="btnRun" class="primary" ${disabledReason ? "disabled" : ""}>${escapeHtml(buttonText)}</button>
        <div class="risk-reason">${disabledReason ? escapeHtml(disabledReason) : `可出发；最多 ${maxStaff} 人，当前 ${selectedCount} 人。`}</div>
      </div>
    </aside>`;
  }

  function dispatchDecisionGapText(stats) {
    if (!stats || !stats.needKeys || !stats.needKeys.length) return "本任务没有明确需求。";
    if (!stats.gaps || !stats.gaps.length) {
      return `需求面值已覆盖；覆盖 ${stats.coveredValue || 0}/${stats.needValue || 0}。`;
    }
    return `还差 ${stats.gaps.map((x) => `${x.k}${x.gap}`).join(" / ")}；覆盖 ${stats.coveredValue || 0}/${stats.needValue || 0}。`;
  }

  function dispatchDecisionReason(stats, selectedCount) {
    if (!selectedCount) return "先选至少 1 名角色，系统会显示本次是否能达标。";
    if (!stats || !stats.relevantFaces) return "当前骰池没有可用需求面，建议换人或补道具骰。";
    const chanceText = `实掷达标率约 ${formatChance(stats.successChance)}`;
    const gapText = dispatchDecisionGapText(stats);
    const lift = selectedCount > 1 ? formatDisplayedChanceLift(stats.successChance || 0, stats.bestSingleStaffChance || 0) : "";
    const liftText = lift ? `；较单人最佳 ${lift}` : "";
    const idleText = stats.nonContributingStaff ? `；${stats.nonContributingStaff} 名角色没有补到缺口` : "";
    return `${chanceText}；${gapText}${liftText}${idleText}`;
  }

  function dispatchDecisionSuccessText(m) {
    const story = missionStory(m);
    const copy = missionOutcomeCopy(m, "大成功") || missionOutcomeCopy(m, "小成功") || missionOutcomeCopy(m, "成功") || missionOutcomeCopy(m, "success_cost");
    if (copy && copy.clueTitle) return `拿到「${copy.clueTitle}」，进入本周线索池。`;
    if (story && story.objective) return `完成目标：${story.objective}`;
    if (m && m.chainType === "deep") return "推进深度链下一阶段，并带回可成稿素材。";
    return "带回可合成报道的现场素材。";
  }

  function dispatchDecisionFailureText(m) {
    const copy = missionOutcomeCopy(m, "失败") || missionOutcomeCopy(m, "fail_clue") || missionOutcomeCopy(m, "crit_fail");
    if (copy && copy.clueTitle) return `保留弱线索「${copy.clueTitle}」，但质量会下降。`;
    if ((m && m.checkType) === "red") return "截稿窗口会关闭；失败也会留下可疑碎片。";
    if (m && (m.riskTier === "high" || m.isHighRisk)) return "队伍可能受损，只留下不完整素材。";
    return "失败不会封死题材，但会消耗本周时间。";
  }

  function dispatchDecisionVerdictLabel(risk, selectedCount) {
    if (!selectedCount) return "先选人，再判断能不能搏";
    if (risk.label === "可搏") return "可以出发";
    if (risk.label === "偏险") return "能搏，但缺口仍刺眼";
    if (risk.label === "高") return "暂不建议出发";
    return "等待队伍配置";
  }

  function dispatchDecisionJudgementHtml(m, stats, risk, maxStaff) {
    const selectedCount = state.selectedStaffIds.length;
    const disabledReason = dispatchLabActionDisabledReason(m);
    const chance = selectedCount ? formatChance(stats.successChance) : "未评估";
    const chanceAngle = selectedCount ? Math.round((stats.successChance || 0) * 360) : 0;
    const buttonText = state.missionResolving
      ? "执行中..."
      : disabledReason
        ? (disabledReason === "先选择至少 1 名角色" ? "先选择角色后开始" : disabledReason)
        : `${m.missionType === "leadInvestigation" ? "派遣线索调查" : "派遣探索任务"}（${m.days}天后判定）`;
    const objective = (missionStory(m) && missionStory(m).objective) || missionTypeDesc(m);
    return `<section class="dispatch-decision-judgement" aria-label="本次派遣判断">
      <div class="dispatch-decision-head">
        <div>本次派遣判断</div>
        <span>已选 ${selectedCount}/${maxStaff} 人 · ${escapeHtml(chance)}</span>
      </div>
      <div class="dispatch-decision-verdict">
        <div class="dispatch-decision-ring" style="--chance-angle:${chanceAngle}deg;">${escapeHtml(chance)}</div>
        <div>
          <strong>${escapeHtml(dispatchDecisionVerdictLabel(risk, selectedCount))}</strong>
          <p>${escapeHtml(dispatchDecisionReason(stats, selectedCount))}</p>
        </div>
      </div>
      <div class="dispatch-decision-facts">
        <div class="dispatch-decision-fact">
          <b>要核实什么</b>
          <span>${escapeHtml(objective)}</span>
        </div>
        <div class="dispatch-decision-fact">
          <b>当前缺口</b>
          <span>${escapeHtml(dispatchDecisionGapText(stats))}</span>
        </div>
        <div class="dispatch-decision-fact is-reward">
          <b>成功拿到</b>
          <span>${escapeHtml(dispatchDecisionSuccessText(m))}</span>
        </div>
        <div class="dispatch-decision-fact is-risk">
          <b>失败边界</b>
          <span>${escapeHtml(dispatchDecisionFailureText(m))}</span>
        </div>
      </div>
      <div class="dispatch-decision-actions">
        <button type="button" id="btnRun" class="primary" ${disabledReason ? "disabled" : ""}>${escapeHtml(buttonText)}</button>
        <div class="risk-reason">${disabledReason ? escapeHtml(disabledReason) : "确认后派遣，不自动推进时间。"}</div>
      </div>
    </section>`;
  }

  function dispatchDecisionStaffContributionText(staff, need) {
    const keys = Object.keys(need || {});
    if (!keys.length) return "无指定需求";
    const sums = {};
    diceFacesForStaff(staff).forEach((face) => {
      if (!face || !keys.includes(face.attr)) return;
      sums[face.attr] = (sums[face.attr] || 0) + (face.value || 0);
    });
    const parts = keys
      .filter((key) => sums[key])
      .map((key) => `${key}${sums[key]}`);
    return parts.length ? parts.join(" / ") : "未补当前需求";
  }

  function dispatchDecisionGapFillValue(staff, gaps) {
    if (!staff || !Array.isArray(gaps) || !gaps.length) return 0;
    return diceFacesForStaff(staff).reduce((sum, face) => {
      if (!face) return sum;
      const gap = gaps.find((x) => x.k === face.attr);
      if (!gap) return sum;
      return sum + Math.min(face.value || 0, gap.gap || 0);
    }, 0);
  }

  function dispatchDecisionSortedStaff(staffList, m, stats) {
    const need = (m && m.need) || {};
    const gaps = stats && stats.gaps && stats.gaps.length
      ? stats.gaps
      : Object.keys(need).map((k) => ({ k, gap: need[k] || 0 }));
    return staffList.slice().sort((a, b) => {
      const selectedDelta = Number(state.selectedStaffIds.includes(b.id)) - Number(state.selectedStaffIds.includes(a.id));
      if (selectedDelta !== 0) return selectedDelta;
      const gapDelta = dispatchDecisionGapFillValue(b, gaps) - dispatchDecisionGapFillValue(a, gaps);
      if (gapDelta !== 0) return gapDelta;
      const af = staffFitSummary(a, need);
      const bf = staffFitSummary(b, need);
      const valueDelta = (bf.stats.relevantValues || 0) - (af.stats.relevantValues || 0);
      if (valueDelta !== 0) return valueDelta;
      return (STAFF_BASE_ORDER.get(a.id) ?? 999) - (STAFF_BASE_ORDER.get(b.id) ?? 999);
    });
  }

  function dispatchDecisionRosterHtml(m, stats, maxStaff) {
    const selectedStaff = (state.selectedStaffIds || []).map(findStaff).filter(Boolean);
    const selectedCount = selectedStaff.length;
    const emptyCount = Math.max(0, maxStaff - selectedCount);
    const visibleEmpty = maxStaff <= 6 ? emptyCount : Math.min(emptyCount, 2);
    const emptyHtml = Array.from({ length: visibleEmpty }, (_, i) => `<div class="dispatch-roster-chip empty">空位 ${selectedCount + i + 1}/${maxStaff}</div>`).join("");
    const moreEmpty = emptyCount > visibleEmpty ? `<div class="dispatch-roster-chip empty compact">还可加入 ${emptyCount - visibleEmpty} 人</div>` : "";
    const staffHtml = selectedStaff.map((staff) => `<div class="dispatch-roster-chip">
      <img src="${staff.avatar}" alt="${escapeHtml(staff.name)}"/>
      <div>
        <strong>${escapeHtml(staff.name)}${staff.temporary ? " · 临时" : ""}</strong>
        <small>${escapeHtml(dispatchDecisionStaffContributionText(staff, m.need || {}))}</small>
      </div>
      <button type="button" class="dispatch-slot-remove" data-remove-selected-staff="${escapeHtml(staff.id)}" title="移出 ${escapeHtml(staff.name)}" aria-label="移出 ${escapeHtml(staff.name)}">×</button>
    </div>`).join("");
    const toolHtml = (state.toolDiceInventory || []).map((tool) => {
      const used = !!tool.used;
      const selected = state.selectedToolDiceIds.includes(tool.id);
      return `<button type="button" class="dispatch-resource-card ${selected ? "selected" : ""}" data-tool-dice="${escapeHtml(tool.id)}" ${used ? "disabled" : ""}>
        <strong>${escapeHtml(tool.name)}</strong>
        <small>${used ? "已消耗" : "一次性道具 · 不占人数"}</small>
        ${diceFacesHtml(tool.faces || [], m.need || {}, "pool-dice-faces")}
      </button>`;
    }).join("");
    const gapText = dispatchDecisionGapText(stats);
    return `<section class="dispatch-decision-roster">
      <div class="dispatch-lab-panel-title">
        <span>本次骰池（参判席）</span>
        <span>已选 ${selectedCount}/${maxStaff} 人 ${capacitySlotsHtml(selectedCount, maxStaff)}</span>
      </div>
      <div class="dispatch-roster-summary">
        <strong>${escapeHtml(selectedCount ? gapText : "先从候选池选择角色。")}</strong>
        <span>${stats.gaps && stats.gaps.length ? "优先补缺口属性，候选池会同步排序。" : "已达标；继续换人只影响成功率与风险。"}</span>
      </div>
      <div class="dispatch-roster-list">${staffHtml || `<div class="dispatch-roster-chip empty">暂无参判角色</div>`}${emptyHtml}${moreEmpty}</div>
      <div class="dispatch-roster-support">
        <div class="dispatch-support-head"><span>辅助骰位</span><span class="risk-reason">道具不占人数；雇佣后进候选角色</span></div>
        <div class="dispatch-roster-tools">
          ${toolHtml || `<span class="tip-inline">暂无道具骰</span>`}
          <button type="button" id="btnHireTemp" class="dispatch-resource-card">
            <strong>${isTempStringerHired() ? "线人已进入候选池" : "雇佣本周临时线人"}</strong>
            <small>${isTempStringerHired() ? "选择它会占用 1 个角色位" : "$1200 · 加入候选池"}</small>
          </button>
        </div>
      </div>
    </section>`;
  }

  function dispatchDecisionCoverageCompactHtml(m, stats, risk) {
    const need = (m && m.need) || {};
    const keys = Object.keys(need);
    const hasGaps = !!(stats && stats.gaps && stats.gaps.length);
    const status = hasGaps
      ? `缺口：${stats.gaps.map((x) => `${x.k}${x.gap}`).join(" / ")}`
      : `已达标：${stats.coveredValue || 0}/${stats.needValue || 0}`;
    const chips = keys.map((key) => {
      const value = stats && stats.values ? (stats.values[key] || 0) : 0;
      const target = need[key] || 0;
      const met = value >= target;
      return `<span class="dispatch-coverage-chip ${met ? "is-met" : "is-gap"}">${escapeHtml(key)} ${escapeHtml(value)}/${escapeHtml(target)}</span>`;
    }).join("");
    return `<section class="dispatch-coverage-compact ${hasGaps ? "has-gap" : ""}">
      <div class="dispatch-coverage-compact-head">
        <span>达标摘要</span>
        <span class="task-type-chip task-${dispatchRiskChipClass(risk.label)}">风险：${escapeHtml(risk.label)}</span>
      </div>
      <strong>${escapeHtml(status)} · ${escapeHtml(formatChance(stats.successChance))}</strong>
      <div class="dispatch-coverage-chips">${chips}</div>
      <details class="dispatch-coverage-details">
        <summary>展开属性明细（${keys.length}项）</summary>
        ${dispatchLabNeedRowsHtml(m, stats)}
      </details>
    </section>`;
  }

  function dispatchLabResourcesHtml(maxStaff) {
    const tempHired = isTempStringerHired();
    const tempCardHtml = tempHired
      ? `<div class="dispatch-resource-card is-spent">
          <strong>线人已进入候选池</strong>
          <small>作为临时角色加入时，占用 1 个角色槽。</small>
        </div>`
      : `<button type="button" id="btnHireTemp" class="dispatch-resource-card">
          <strong>雇佣本周临时线人</strong>
          <small>$1200 · 雇佣后出现在候选角色，加入时占角色槽。</small>
        </button>`;
    const toolCards = (state.toolDiceInventory || []).map((tool) => {
      const used = !!tool.used;
      const selected = state.selectedToolDiceIds.includes(tool.id);
      return `<button type="button" class="dispatch-resource-card ${selected ? "selected" : ""}" data-tool-dice="${tool.id}" ${used ? "disabled" : ""}>
        <strong>${escapeHtml(tool.name)}</strong>
        <small>${used ? "已消耗" : "一次性道具 · 不占人数"}</small>
        ${diceFacesHtml(tool.faces || [], state.mission ? state.mission.need : {}, "pool-dice-faces")}
      </button>`;
    }).join("");
    return `<div class="dispatch-support-strip">
      <div class="dispatch-support-head"><span>辅助骰位</span><span class="risk-reason">道具不占人数；雇佣会进入候选角色</span></div>
      <div class="dispatch-resource-grid">
        ${toolCards || `<span class="tip-inline">暂无道具骰</span>`}
        ${tempCardHtml}
      </div>
    </div>`;
  }

  function dispatchLabStaffCardHtml(staff, m, maxStaff) {
    const selected = state.selectedStaffIds.includes(staff.id);
    const unavailable = !selected && state.selectedStaffIds.length >= maxStaff;
    const fit = staffFitSummary(staff, m.need || {});
    const fitClass = fit.fit === "高" ? "high" : fit.fit === "中" ? "mid" : "low";
    const body = state.displayMode === "numeric"
      ? dispatchLabStaffSummaryHtml(staff, m)
      : diceNetHtml(diceFacesForStaff(staff), m.need || {}, "dispatch-dice-net");
    return `<div class="dispatch-staff-card ${selected ? "selected" : ""} ${unavailable ? "unavailable" : ""}" data-staff="${staff.id}">
      <div class="dispatch-staff-head">
        <img src="${staff.avatar}" alt="${escapeHtml(staff.name)}"/>
        <div>
          <div class="dispatch-staff-name">${escapeHtml(staff.name)}${staff.temporary ? " · 临时" : ""}</div>
          <div class="dispatch-card-verdict ${fitClass}">${escapeHtml(fit.fit)}适配 · ${escapeHtml(fit.stats.relevant)}/6 相关</div>
        </div>
      </div>
      ${body}
      <div class="dispatch-staff-actions">
        <button type="button" class="staff-detail-btn" data-staff-detail="${staff.id}">详情</button>
      </div>
    </div>`;
  }

  function dispatchLabSortedStaff(staffList, need) {
    const rank = { 高: 3, 中: 2, 低: 1 };
    return staffList.slice().sort((a, b) => {
      const af = staffFitSummary(a, need || {});
      const bf = staffFitSummary(b, need || {});
      if (rank[af.fit] !== rank[bf.fit]) return rank[bf.fit] - rank[af.fit];
      const valueDelta = (bf.stats.relevantValues || 0) - (af.stats.relevantValues || 0);
      if (valueDelta !== 0) return valueDelta;
      return (STAFF_BASE_ORDER.get(a.id) ?? 999) - (STAFF_BASE_ORDER.get(b.id) ?? 999);
    });
  }

  function renderDispatchDecisionSetup() {
    const m = state.mission;
    const elS = document.getElementById("view-setup");
    if (!m) return;
    const maxStaff = missionMaxStaff(m);
    const relevantNeed = m.need || {};
    const selectedTools = dispatchLabSelectedTools();
    const stats = dispatchLabNeedStats(m, state.selectedStaffIds, selectedTools);
    const risk = dispatchLabRisk(m, stats, state.selectedStaffIds.length);
    const allowQueueId = m && m.missionQueueId ? m.missionQueueId : null;
    const staffList = dispatchLabSortedStaff(
      getAllStaff().filter((p) => !isStaffAssigned(p.id, allowQueueId) || state.selectedStaffIds.includes(p.id)),
      relevantNeed,
    );
    const heading = m.missionType === "leadInvestigation" ? "线索调查配置" : "探索配置";
    elS.innerHTML = `<div class="dispatch-decision-shell">
      <div class="dispatch-lab-top">
        <div>
          <h2>${escapeHtml(heading)}</h2>
          <div class="risk-reason">选择本次骰池，确认达标、后果和时间成本后派遣。</div>
        </div>
      </div>
      <div class="dispatch-decision-main">
        ${dispatchDecisionJudgementHtml(m, stats, risk, maxStaff)}
        ${dispatchLabTaskSummaryHtml(m)}
      </div>
      <div class="dispatch-decision-secondary">
        ${dispatchDecisionRosterHtml(m, stats, maxStaff)}
        ${dispatchDecisionCoverageCompactHtml(m, stats, risk)}
      </div>
      <section class="dispatch-lab-panel">
        <div class="dispatch-candidate-head">
          <div class="dispatch-lab-panel-title" style="margin:0;"><span>候选角色</span><span class="risk-reason">按本任务适配排序；点击后主判定即时更新</span></div>
          <span class="mode-toggle" id="modeToggle">
            <button type="button" data-mode="dice" class="${state.displayMode === "dice" ? "on" : ""}">骰面</button>
            <button type="button" data-mode="numeric" class="${state.displayMode === "numeric" ? "on" : ""}">汇总</button>
          </span>
        </div>
        <div class="dispatch-staff-grid" id="staffPick">${staffList.map((p) => dispatchLabStaffCardHtml(p, m, maxStaff)).join("")}</div>
      </section>
      <p class="row" style="margin-top:0;">
        ${m.missionQueueId ? `<button type="button" id="btnUndoDispatch">撤销派遣</button>` : ""}
        <button type="button" id="btnCancelSetup" class="nm-sec nav-return-button">返回区域</button>
      </p>
      <p class="tip-inline">已派遣待判定任务：${state.activeMissions.length}。返回区域后在底部「日程推进」条继续推进，并触发到期判定。</p>
    </div>`;

    document.querySelectorAll("#modeToggle button").forEach((b) => {
      b.onclick = () => {
        state.displayMode = b.getAttribute("data-mode");
        renderSetup();
      };
    });
    document.querySelectorAll("[data-tool-dice]").forEach((btn) => {
      btn.onclick = () => {
        const id = btn.getAttribute("data-tool-dice");
        if (state.selectedToolDiceIds.includes(id)) state.selectedToolDiceIds = state.selectedToolDiceIds.filter((x) => x !== id);
        else state.selectedToolDiceIds.push(id);
        renderSetup();
      };
    });
    const hireBtn = document.getElementById("btnHireTemp");
    if (hireBtn) {
      hireBtn.onclick = () => {
        if (toggleTempStringerForDispatch(maxStaff)) renderSetup();
      };
    }
    document.querySelectorAll("[data-remove-selected-staff]").forEach((btn) => {
      btn.onclick = (ev) => {
        ev.stopPropagation();
        const id = btn.getAttribute("data-remove-selected-staff");
        state.selectedStaffIds = state.selectedStaffIds.filter((staffId) => staffId !== id);
        renderSetup();
      };
    });
    document.querySelectorAll("#staffPick .dispatch-staff-card").forEach((c) => {
      c.addEventListener("click", (ev) => {
        if (ev && ev.target && ev.target.closest && ev.target.closest("button")) return;
        const id = c.getAttribute("data-staff");
        const i = state.selectedStaffIds.indexOf(id);
        if (i >= 0) state.selectedStaffIds.splice(i, 1);
        else {
          if (!canAddStaffToDispatch(findStaff(id), maxStaff)) return;
          state.selectedStaffIds.push(id);
        }
        renderSetup();
      });
    });
    document.querySelectorAll("[data-staff-detail]").forEach((btn) => {
      btn.onclick = (ev) => {
        ev.stopPropagation();
        showStaffDetail(findStaff(btn.getAttribute("data-staff-detail")), relevantNeed);
      };
    });
    document.getElementById("btnRun").onclick = () => {
      if (!state.mission || state.selectedStaffIds.length === 0) return;
      if (state.mission.days > state.day) return;
      if (state.missionResolving) return;
      enqueueCurrentMission();
      renderRegion();
      setView("region");
    };
    const undoBtn = document.getElementById("btnUndoDispatch");
    if (undoBtn) {
      undoBtn.onclick = () => {
        const idx = state.activeMissions.findIndex((x) => x.id === m.missionQueueId);
        if (idx >= 0) {
          const rec = state.activeMissions[idx];
          if (rec.mission && rec.mission.missionType === "leadInvestigation") {
            const leads = state.regionLeadEvents[rec.regionId] || [];
            const lead = leads.find((x) => x.id === rec.mission.leadId);
            if (lead && !lead.investigated) lead.assigned = false;
          }
          (rec.toolDiceIds || []).forEach((id) => {
            const tool = state.toolDiceInventory.find((x) => x.id === id);
            if (tool) tool.used = false;
          });
          state.activeMissions.splice(idx, 1);
          log(`已撤销派遣：${m.name}`);
        }
        state.mission = null;
        state.selectedStaffIds = [];
        state.selectedToolDiceIds = [];
        renderRegion();
        setView("region");
      };
    }
    document.getElementById("btnCancelSetup").onclick = () => {
      if (state.mission && state.mission.missionType === "leadInvestigation" && !state.mission.missionQueueId) {
        const leads = state.regionLeadEvents[state.mission.regionId] || [];
        const lead = leads.find((x) => x.id === state.mission.leadId);
        if (lead && !lead.investigated) lead.assigned = false;
      }
      state.mission = null;
      state.selectedStaffIds = [];
      state.selectedToolDiceIds = [];
      renderRegion();
      setView("region");
    };
  }

  function renderSetupLab() {
    renderDispatchDecisionSetup();
  }

  function renderSetup() {
    if (!state.dispatchOldSetupMode) {
      renderSetupLab();
      return;
    }
    const m = state.mission;
    const elS = document.getElementById("view-setup");
    if (!m) return;
    const ok = meetsNeed(m.need, state.selectedStaffIds);
    const prob = computeExplorationP(m, state.selectedStaffIds);
    const dicePreview = computeCharacterDicePreview(m, state.selectedStaffIds);
    const maxStaff = missionMaxStaff(m);
    const relevantNeed = m.need || {};
    const toolDiceHtml = (state.toolDiceInventory || []).map((tool) => {
      const used = !!tool.used;
      const sel = state.selectedToolDiceIds.includes(tool.id);
      return `<button type="button" class="tool-dice-pick ${sel ? "selected" : ""}" data-tool-dice="${tool.id}" ${used ? "disabled" : ""}>
        <strong>${escapeHtml(tool.name)}</strong>
        <span>${used ? "已消耗" : "一次性道具骰"}</span>
      </button>`;
    }).join("");
    const tempHired = isTempStringerHired();
    const tempButtonHtml = tempHired
      ? ""
      : `<p style="margin:0.45rem 0 0;"><button type="button" id="btnHireTemp">雇佣本周临时线人（$1200，加入候选角色）</button></p>`;
    elS.innerHTML = `
      <h2>${m.missionType === "leadInvestigation" ? "线索调查配置" : "探索配置"} · ${escapeHtml(m.name)}</h2>
      ${missionTypePanelHtml(m, false)}
      ${missionStoryBriefHtml(m)}
      ${dicePoolPreviewHtml(m, dicePreview, maxStaff)}
      <div class="prob-box">
        <div><strong>一次性道具骰</strong> <span class="tip-inline">不占人数；使用后消耗；计入总骰数。</span></div>
        <div class="tool-dice-row">${toolDiceHtml || `<span class="tip-inline">暂无道具骰</span>`}</div>
        ${tempButtonHtml}
        <div style="margin-top:0.35rem;font-size:0.72rem;color:#64748b;">旧 split 预览：调查池 ${prob.nA} / 现场池 ${prob.nB}${ok ? "" : " · 原属性未达门槛"}</div>
      </div>
      <p style="font-size:0.85rem;margin-top:0.5rem;">展示：
        <span class="mode-toggle" id="modeToggle">
          <button type="button" data-mode="dice" class="${state.displayMode === "dice" ? "on" : ""}">骰子</button>
          <button type="button" data-mode="numeric" class="${state.displayMode === "numeric" ? "on" : ""}">汇总</button>
        </span></p>
      <div class="cards" id="staffPick"></div>
      <p class="row" style="margin-top:0.75rem;">
        <button type="button" id="btnRun" class="primary" ${state.selectedStaffIds.length === 0 || m.days > state.day || state.missionResolving || state.processingDayTick ? "disabled" : ""}>${state.missionResolving ? "执行中..." : `${m.missionType === "leadInvestigation" ? "派遣线索调查" : "派遣探索任务"}（预计 ${m.days} 天后判定）`}</button>
        ${m.missionQueueId ? `<button type="button" id="btnUndoDispatch">撤销派遣</button>` : ""}
        <button type="button" id="btnCancelSetup" class="nm-sec nav-return-button">返回区域</button>
      </p>
      ${m.days > state.day ? `<p style="color:var(--danger);font-size:0.85rem;">剩余天数不足，无法在本周内完成。</p>` : ""}
      <p class="tip-inline" style="margin-top:0.5rem;">已派遣待判定任务：${state.activeMissions.length}。返回区域后在底部「日程推进」条继续推进，并触发到期判定。</p>`;
    document.querySelectorAll("#modeToggle button").forEach((b) => {
      b.onclick = () => {
        state.displayMode = b.getAttribute("data-mode");
        renderSetup();
      };
    });
    document.querySelectorAll("[data-tool-dice]").forEach((btn) => {
      btn.onclick = () => {
        const id = btn.getAttribute("data-tool-dice");
        if (state.selectedToolDiceIds.includes(id)) state.selectedToolDiceIds = state.selectedToolDiceIds.filter((x) => x !== id);
        else state.selectedToolDiceIds.push(id);
        renderSetup();
      };
    });
    const hireBtn = document.getElementById("btnHireTemp");
    if (hireBtn) {
      hireBtn.onclick = () => {
        if (toggleTempStringerForDispatch(maxStaff)) renderSetup();
      };
    }
    const pick = document.getElementById("staffPick");
    const allowQueueId = m && m.missionQueueId ? m.missionQueueId : null;
    const staffList = getAllStaff().filter((p) => !isStaffAssigned(p.id, allowQueueId) || state.selectedStaffIds.includes(p.id));
    pick.innerHTML = staffList.map((p) => {
      const sel = state.selectedStaffIds.includes(p.id);
      const fit = staffFitSummary(p, relevantNeed);
      return `<div class="staff-card ${sel ? "selected" : ""}" data-staff="${p.id}">
        <img class="portrait" src="${p.avatar}" alt="${escapeHtml(p.name)}"/>
        <div class="t">${escapeHtml(p.name)}${p.temporary ? " · 临时" : ""}</div>
        <div class="staff-spec">${specialtyHtml(p)}</div>
        <div class="risk-reason">${escapeHtml(fit.line)} · ${escapeHtml(fit.contribution)}</div>
        <div class="staff-dice-mini">${diceFacesHtml(diceFacesForStaff(p), relevantNeed, "staff-pick-faces")}</div>
        <p class="row" style="margin:0.35rem 0 0;">
          <button type="button" class="staff-detail-btn" data-staff-detail="${p.id}">详情</button>
          ${p.temporary ? "" : `<button type="button" class="staff-detail-btn" data-staff-upgrade="${p.id}">升级预览</button>`}
        </p>
      </div>`;
    }).join("");
    pick.querySelectorAll(".staff-card").forEach((c) => {
      c.addEventListener("click", (ev) => {
        if (ev && ev.target && ev.target.closest && ev.target.closest("button")) return;
        const id = c.getAttribute("data-staff");
        const i = state.selectedStaffIds.indexOf(id);
        if (i >= 0) state.selectedStaffIds.splice(i, 1);
        else {
          if (!canAddStaffToDispatch(findStaff(id), maxStaff)) return;
          state.selectedStaffIds.push(id);
        }
        renderSetup();
      });
    });
    pick.querySelectorAll("[data-staff-detail]").forEach((btn) => {
      btn.onclick = (ev) => {
        ev.stopPropagation();
        showStaffDetail(findStaff(btn.getAttribute("data-staff-detail")), relevantNeed);
      };
    });
    pick.querySelectorAll("[data-staff-upgrade]").forEach((btn) => {
      btn.onclick = (ev) => {
        ev.stopPropagation();
        showUpgradeModal(findStaff(btn.getAttribute("data-staff-upgrade")));
      };
    });
    document.getElementById("btnRun").onclick = async () => {
      if (!state.mission || state.selectedStaffIds.length === 0) return;
      if (state.mission.days > state.day) return;
      if (state.missionResolving) return;
      enqueueCurrentMission();
      renderRegion();
      setView("region");
    };
    const undoBtn = document.getElementById("btnUndoDispatch");
    if (undoBtn) {
      undoBtn.onclick = () => {
        const idx = state.activeMissions.findIndex((x) => x.id === m.missionQueueId);
        if (idx >= 0) {
          const rec = state.activeMissions[idx];
          if (rec.mission && rec.mission.missionType === "leadInvestigation") {
            const leads = state.regionLeadEvents[rec.regionId] || [];
            const lead = leads.find((x) => x.id === rec.mission.leadId);
            if (lead && !lead.investigated) lead.assigned = false;
          }
          (rec.toolDiceIds || []).forEach((id) => {
            const tool = state.toolDiceInventory.find((x) => x.id === id);
            if (tool) tool.used = false;
          });
          state.activeMissions.splice(idx, 1);
          log(`已撤销派遣：${m.name}`);
        }
        state.mission = null;
        state.selectedStaffIds = [];
        state.selectedToolDiceIds = [];
        renderRegion();
        setView("region");
      };
    }
    document.getElementById("btnCancelSetup").onclick = () => {
      if (state.mission && state.mission.missionType === "leadInvestigation" && !state.mission.missionQueueId) {
        const leads = state.regionLeadEvents[state.mission.regionId] || [];
        const lead = leads.find((x) => x.id === state.mission.leadId);
        if (lead && !lead.investigated) lead.assigned = false;
      }
      state.mission = null;
      state.selectedStaffIds = [];
      renderRegion();
      setView("region");
    };
    scheduleWeek1SoftTutorial(
      "w1_setup",
      "第一周 · 组队与出发",
      [
        `${tutorialSoftFigure(
          "Assets/tutorial-setup-guide.svg",
          "组队界面示意：概率区、队员选择与派遣",
          "示意：上方为成功率参考；中间选队员；底部确认派遣。",
        )}<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">组小队</h4>
          <ul class="tutorial-soft-ul">
            <li>点选队员卡片：非黑骰任务最多 <strong>3</strong> 人；黑骰任务最多 <strong>5</strong> 人。</li>
            <li>卡片上展示专精；点「详情」可查看完整 6 面角色骰。</li>
            <li>上方风险预览是本次外拍的参考。</li>
            <li>可在<strong>骰子</strong>与<strong>纯数字</strong>两种展示间切换。</li>
          </ul>
        </div>`,
        `<div class="tutorial-soft-sheet">
          <h4 class="tutorial-soft-h4">派遣之后</h4>
          <ul class="tutorial-soft-ul">
            <li>点<strong>派遣</strong>后，任务占用本周若干天。</li>
            <li>到点用底部<strong>日程推进</strong>条推进，系统会依次播报结果。</li>
          </ul>
          <p class="tutorial-soft-note">按自己的节奏即可，不必为引导多点无关按钮。本周内本提示只出现一次。</p>
        </div>`,
      ],
    );
  }

  function renderDiceRow(rolls, voidSet, label) {
    if (!rolls.length) return `<div class="tip-inline">${label}：无骰</div>`;
    const cells = rolls
      .map((hit, i) => {
        const v = voidSet.has(i);
        const cls = v ? "die void" : hit ? "die hit" : "die miss";
        const ch = v ? "" : hit ? "✓" : "×";
        return `<span class="${cls}">${ch}</span>`;
      })
      .join("");
    return `<div class="dice-pool"><h3>${label}</h3><div class="dice-row">${cells}</div></div>`;
  }

  function rollingFacePlaceholder(idx) {
    const pool = ["探索?", "生存?", "理性?", "洞察?", "诡思?", "空"];
    return pool[Math.abs((idx | 0) + Math.floor(Date.now() / 160)) % pool.length];
  }

  function contributionProgressHtml(sum, need, ready) {
    const keys = Object.keys(need || {});
    if (!keys.length) return `<div class="dice-need-panel"><div class="dice-need-line">本任务没有明确需求。</div></div>`;
    const target = needTargetValue(need);
    const currentTotal = ready ? contributionTotalForNeed(need, sum || {}) : 0;
    const totalMet = currentTotal >= target;
    const totalPct = target ? Math.max(0, Math.min(100, Math.round((currentTotal / target) * 100))) : 100;
    const totalRow = `<div class="dice-need-row${totalMet ? " is-met" : ""}">
      <div class="dice-need-line"><span>有效点</span><strong>${ready ? `${currentTotal}/${target}` : `0/${target}`}</strong></div>
      <div class="dice-need-meter"><span style="width:${ready ? totalPct : 0}%"></span></div>
    </div>`;
    const rows = keys.map((k) => {
      const current = sum && sum[k] ? sum[k] : 0;
      const target = need[k] || 0;
      const met = current >= target;
      const pct = Math.max(0, Math.min(100, Math.round((current / Math.max(1, target)) * 100)));
      return `<div class="dice-need-row${met ? " is-met" : ""}">
        <div class="dice-need-line"><span>${escapeHtml(k)}</span><strong>${ready ? `${current}/${target}` : `0/${target}`}</strong></div>
        <div class="dice-need-meter"><span style="width:${ready ? pct : 0}%"></span></div>
      </div>`;
    }).join("");
    return `<div class="dice-need-panel">
      <div class="dice-need-title">${ready ? "已计入 / 有效点目标" : "等待停骰"}</div>
      ${totalRow}
      <div class="dice-need-title">相关属性贡献</div>
      ${rows}
    </div>`;
  }

  function diceSelectCountText(rolls, selectedIds, ready, revealCount) {
    if (!ready) return `停骰 ${Math.min(revealCount || 0, (rolls || []).length)}/${(rolls || []).length}`;
    return `计入 ${(selectedIds || []).length}/${(rolls || []).length}`;
  }

  function diceSelectSummaryHtml(sum, need, ready) {
    const target = needTargetValue(need || {});
    const total = ready ? contributionTotalForNeed(need || {}, sum || {}) : 0;
    const met = target ? total >= target : true;
    const missing = Math.max(0, target - total);
    const angle = target ? Math.round(Math.min(1, total / target) * 360) : 360;
    const title = !ready
      ? "等待停骰"
      : met
        ? "已达标"
        : `未达标 · 还差 ${missing} 点`;
    const copy = !ready
      ? "停骰后选择要计入的骰面。"
      : met
        ? "现在确认会按达标结果推进。"
        : "可继续调整计入骰面后再确认。";
    const rows = Object.keys(need || {}).map((key) => {
      const current = ready ? Math.max(0, (sum && sum[key]) || 0) : 0;
      const goal = Math.max(0, need[key] || 0);
      const pct = goal ? Math.max(0, Math.min(100, Math.round((current / goal) * 100))) : 100;
      return `<div class="dice-need-compact-row">
        <span>${escapeHtml(key)}</span>
        <em><i style="--fill:${pct}%"></i></em>
        <b>${current}/${goal}</b>
      </div>`;
    }).join("");
    return `<section class="dice-summary-card" aria-label="判定摘要">
      <div class="dice-section-head"><strong>判定摘要</strong><span>${ready ? "结果口径" : "等待"}</span></div>
      <div class="dice-summary-top">
        <div class="dice-score-ring" style="--score-angle:${angle}deg">
          <div><strong>${total}/${target}</strong><small>有效点</small></div>
        </div>
        <div class="dice-summary-copy"><strong>${escapeHtml(title)}</strong><span>${escapeHtml(copy)}</span></div>
      </div>
      <div class="dice-need-stack">${rows}</div>
    </section>`;
  }

  function diceSubmitPreviewHtml(success, ready) {
    if (!ready) return "";
    return `<section class="dice-submit-preview" aria-label="提交后果">
      <strong>提交后果</strong>
      ${success
        ? "<div>满足任务需求，按达标结果结算。</div>"
        : "<div>未满足任务需求，按低结果收束。</div>"}
    </section>`;
  }

  function blackDiceInterventionHtml(context) {
    const ctx = context || {};
    const blackDice = ctx.blackDice || [];
    const notes = ctx.blackNotes || [];
    if (!blackDice.length && !notes.length) return "";
    const dice = blackDice.map((b) => `<span class="black-intervention-die">${escapeHtml(faceText(b.face))}</span>`).join("");
    const lines = notes.map((n) => `<li>${escapeHtml(n)}</li>`).join("");
    return `<div class="black-intervention-panel${ctx.active ? " is-active" : ""}">
      <div class="black-intervention-head">
        <strong>黑骰介入</strong>
        <span>${blackDice.length ? `已掷出 ${blackDice.length} 颗黑骰` : "异常压力已生效"}</span>
      </div>
      ${dice ? `<div class="black-intervention-row">${dice}</div>` : ""}
      ${lines ? `<ul>${lines}</ul>` : ""}
    </div>`;
  }

  function selectedDiceTrayHtml(rolls, selectedIds, need, ready) {
    if (!ready) {
      return `<div class="selected-dice-tray is-waiting">
        <div class="selected-dice-head"><strong>计入槽</strong><span>停骰后选择</span></div>
        <div class="selected-dice-empty">等待选择计入判定的骰面</div>
      </div>`;
    }
    const selected = new Set(selectedIds || []);
    const picked = (rolls || []).filter((r) => selected.has(r.id));
    const chips = picked.map((r) => {
      const contributes = r.face && r.face.attr && need && need[r.face.attr] != null && !r.black;
      const waste = !contributes && !r.black;
      const tag = r.black ? "黑骰" : contributes ? "补需求" : "不计";
      const source = r.staffName ? `${r.staffName} · ${tag}` : tag;
      return `<span class="selected-dice-chip${contributes ? " contributes" : ""}${r.black ? " black" : ""}${waste ? " waste" : ""}">
        <b>${escapeHtml(faceText(r.face))}</b><small>${escapeHtml(source)}</small>
      </span>`;
    }).join("");
    const contributeCount = picked.filter((r) => r.face && r.face.attr && need && need[r.face.attr] != null && !r.black).length;
    const blackCount = picked.filter((r) => r.black).length;
    const wasteCount = Math.max(0, picked.length - contributeCount - blackCount);
    const summary = picked.length
      ? [`${picked.length} 颗已选`, contributeCount ? `${contributeCount} 颗补需求` : "", blackCount ? `${blackCount} 颗黑骰` : "", wasteCount ? `${wasteCount} 颗不计` : ""].filter(Boolean).join(" · ")
      : "未选择";
    return `<div class="selected-dice-tray">
      <div class="selected-dice-head"><strong>计入槽</strong><span>${escapeHtml(summary)}</span></div>
      <div class="selected-dice-list">${chips || `<div class="selected-dice-empty">没有骰面计入，本次将按 0 贡献结算</div>`}</div>
    </div>`;
  }

  function diceImpactMeta(roll, need, selectedNow) {
    if (!roll) {
      return {
        tone: "idle",
        badge: "待选择",
        title: "停骰后选择骰面",
        copy: "点击骰面会把它加入或移出计入槽。",
      };
    }
    const text = faceText(roll.face);
    if (roll.black) {
      return {
        tone: "black",
        badge: selectedNow ? "黑骰已计入" : "黑骰压力",
        title: `${text} · ${roll.staffName || ""}`,
        copy: selectedNow ? "已进入计入槽；不会补任务需求，但会把异常压力带入本次判定。" : "来自黑骰介入；可选择，但不会补任务需求。",
      };
    }
    if (!roll.face || roll.face.blank) {
      return {
        tone: "muted",
        badge: selectedNow ? "空面已选" : "空面",
        title: `${text} · ${roll.staffName || ""}`,
        copy: selectedNow ? "空面已进入计入槽；本次不提供需求贡献。" : "不提供需求贡献，默认不推荐计入。",
      };
    }
    const relevant = roll.face.attr && need && need[roll.face.attr] != null;
    if (relevant) {
      return {
        tone: selectedNow ? "good selected" : "good",
        badge: selectedNow ? "正在补需求" : "可补需求",
        title: `${roll.face.attr}+${roll.face.value} · ${roll.staffName || ""}`,
        copy: selectedNow ? `已计入 ${roll.face.attr}+${roll.face.value}。` : `点击后计入 ${roll.face.attr}+${roll.face.value}。`,
      };
    }
    return {
      tone: "muted",
      badge: selectedNow ? "已选但不计" : "任务外骰面",
      title: `${text} · ${roll.staffName || ""}`,
      copy: selectedNow ? "已进入计入槽，但当前任务不读取这个属性。" : "当前任务不读取这个属性，通常不需要计入。",
    };
  }

  function diceImpactPanelHtml(rolls, selectedIds, need, focusId, ready) {
    if (!ready) {
      return `<div class="dice-impact-panel is-waiting">
        <div class="dice-impact-head"><strong>骰面影响</strong><span>等待停骰</span></div>
        <div class="dice-impact-copy">停骰后会显示当前骰面对任务需求的影响。</div>
      </div>`;
    }
    const selected = new Set(selectedIds || []);
    const source = rolls || [];
    const focus = source.find((r) => r.id === focusId)
      || source.find((r) => selected.has(r.id) && r.face && r.face.attr && need && need[r.face.attr] != null && !r.black)
      || source.find((r) => selected.has(r.id))
      || source.find((r) => r.face && r.face.attr && need && need[r.face.attr] != null && !r.black)
      || source[0];
    const meta = diceImpactMeta(focus, need, focus ? selected.has(focus.id) : false);
    return `<div class="dice-impact-panel ${escapeHtml(meta.tone)}">
      <div class="dice-impact-head"><strong>骰面影响</strong><span>${escapeHtml(meta.badge)}</span></div>
      <div class="dice-impact-title">${escapeHtml(meta.title)}</div>
      <div class="dice-impact-copy">${escapeHtml(meta.copy)}</div>
    </div>`;
  }

  const DICE_MODEL_PALETTE = {
    field: { top: "#d97706", front: "#86440f", side: "#a35c16", c: "#fed7aa" },
    cog: { top: "#3b82f6", front: "#1f4fa3", side: "#1d3f7f", c: "#bfdbfe" },
    content: { top: "#ca8a04", front: "#7c4a03", side: "#94600a", c: "#fde68a" },
    social: { top: "#10b981", front: "#087545", side: "#0b5f3c", c: "#bbf7d0" },
    blank: { top: "#7c8798", front: "#3d4654", side: "#566172", c: "#e2e8f0" },
    black: { top: "#b91c1c", front: "#5f1015", side: "#3f0b10", c: "#fecaca" },
  };
  const DICE_MODEL_PROFILE = { duration: 1.05, turns: 4.8 };
  const diceModelRegistry = new Map();
  let diceModelRaf = 0;

  function diceModelHash(text) {
    return String(text || "").split("").reduce((acc, ch) => ((acc << 5) - acc + ch.charCodeAt(0)) | 0, 0);
  }

  function diceModelType(roll) {
    const f = roll && roll.face;
    if (roll && roll.black) return "black";
    if (f && f.black) return "black";
    if (!f || f.blank) return "blank";
    return DOMAIN_CLASS[ATTR_DOMAIN[f.attr]] || "blank";
  }

  function diceModelMakeDie(roll, index) {
    const seed = diceModelHash(`${roll && roll.id ? roll.id : index}-${faceText(roll && roll.face)}`);
    const rand = (offset) => {
      const x = Math.sin(seed * 0.001 + offset) * 10000;
      return x - Math.floor(x);
    };
    const finalYaw = Math.PI * 0.5 + (rand(17) - 0.5) * 0.08;
    return {
      id: roll && roll.id ? roll.id : `roll_${index}`,
      label: faceText(roll && roll.face).replace(/[?？]/g, ""),
      type: diceModelType(roll),
      delay: index * 0.045,
      phase: rand(2) * Math.PI * 2,
      spinBoost: 0.88 + rand(5) * 0.24,
      settle: [Math.PI * 0.5, (rand(11) - 0.5) * 0.04, finalYaw],
      stopAt: null,
      stopBase: 0,
    };
  }

  function diceModelNormalize(v) {
    const len = Math.hypot(v[0], v[1], v[2]) || 1;
    return [v[0] / len, v[1] / len, v[2] / len];
  }

  function diceModelSub(a, b) {
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  }

  function diceModelCross(a, b) {
    return [
      a[1] * b[2] - a[2] * b[1],
      a[2] * b[0] - a[0] * b[2],
      a[0] * b[1] - a[1] * b[0],
    ];
  }

  function diceModelFaceNormal(points) {
    return diceModelNormalize(diceModelCross(diceModelSub(points[1], points[0]), diceModelSub(points[2], points[1])));
  }

  function diceModelColorMix(hex, amount) {
    const n = parseInt(hex.slice(1), 16);
    const r = Math.min(255, Math.floor(((n >> 16) & 255) * amount));
    const g = Math.min(255, Math.floor(((n >> 8) & 255) * amount));
    const b = Math.min(255, Math.floor((n & 255) * amount));
    return `rgb(${r},${g},${b})`;
  }

  function diceModelFaceBrightness(normal) {
    const light = diceModelNormalize([0.42, 0.88, 0.54]);
    const dot = Math.max(0, normal[0] * light[0] + normal[1] * light[1] + normal[2] * light[2]);
    return 0.34 + dot * 0.66;
  }

  function diceModelSolidFaceColor(hex, normal) {
    return diceModelColorMix(hex, 0.86 + diceModelFaceBrightness(normal) * 0.18);
  }

  function diceModelSignedArea(points) {
    let area = 0;
    for (let i = 0; i < points.length; i += 1) {
      const next = points[(i + 1) % points.length];
      area += points[i][0] * next[1] - next[0] * points[i][1];
    }
    return area / 2;
  }

  function diceModelArea(points) {
    return Math.abs(diceModelSignedArea(points));
  }

  function diceModelProject(p, origin, scale) {
    const camera = 4.7;
    const depth = camera - p[2] * 0.38;
    const perspective = camera / depth;
    return [
      origin[0] + p[0] * scale * perspective,
      origin[1] - p[1] * scale * perspective + p[2] * scale * 0.18,
      p[2],
    ];
  }

  function diceModelRotate(p, rx, ry, rz) {
    let [x, y, z] = p;
    let c = Math.cos(rx), s = Math.sin(rx);
    let y1 = y * c - z * s;
    let z1 = y * s + z * c;
    y = y1; z = z1;
    c = Math.cos(ry); s = Math.sin(ry);
    let x1 = x * c + z * s;
    z1 = -x * s + z * c;
    x = x1; z = z1;
    c = Math.cos(rz); s = Math.sin(rz);
    x1 = x * c - y * s;
    y1 = x * s + y * c;
    return [x1, y1, z];
  }

  function diceModelDrawFace(ctx, points, fill) {
    ctx.beginPath();
    ctx.moveTo(points[0][0], points[0][1]);
    for (let i = 1; i < points.length; i += 1) ctx.lineTo(points[i][0], points[i][1]);
    ctx.closePath();
    ctx.fillStyle = fill;
    ctx.fill();
  }

  function diceModelMakeFaceTexture(fill, color, content) {
    const size = 192;
    const tex = document.createElement("canvas");
    tex.width = size;
    tex.height = size;
    const t = tex.getContext("2d");
    t.fillStyle = fill;
    t.fillRect(0, 0, size, size);
    const glow = t.createLinearGradient(0, 0, size, size);
    glow.addColorStop(0, "rgba(255,255,255,0.2)");
    glow.addColorStop(0.38, "rgba(255,255,255,0.04)");
    glow.addColorStop(1, "rgba(0,0,0,0.2)");
    t.fillStyle = glow;
    t.fillRect(0, 0, size, size);
    const topGloss = t.createRadialGradient(size * 0.28, size * 0.18, 0, size * 0.3, size * 0.2, size * 0.72);
    topGloss.addColorStop(0, "rgba(255,255,255,0.18)");
    topGloss.addColorStop(0.42, "rgba(255,255,255,0.05)");
    topGloss.addColorStop(1, "rgba(255,255,255,0)");
    t.fillStyle = topGloss;
    t.fillRect(0, 0, size, size);
    const lowerShade = t.createLinearGradient(0, size * 0.52, 0, size);
    lowerShade.addColorStop(0, "rgba(0,0,0,0)");
    lowerShade.addColorStop(1, "rgba(0,0,0,0.24)");
    t.fillStyle = lowerShade;
    t.fillRect(0, 0, size, size);
    t.lineJoin = "round";
    t.strokeStyle = "rgba(255,255,255,0.08)";
    t.lineWidth = 8;
    t.strokeRect(8, 8, size - 16, size - 16);
    t.strokeStyle = "rgba(2,6,23,0.22)";
    t.lineWidth = 10;
    t.strokeRect(5, 5, size - 10, size - 10);
    if (content && content.type === "label") {
      const text = content.text || "";
      const lines = text.length > 3 ? [text.slice(0, 2), text.slice(2)] : [text];
      const fontSize = text.length <= 1 ? 74 : text.length <= 3 ? 56 : 42;
      const lineHeight = fontSize * 1.06;
      t.textAlign = "center";
      t.textBaseline = "middle";
      t.font = `900 ${fontSize}px Microsoft YaHei, sans-serif`;
      t.lineJoin = "round";
      t.lineWidth = Math.max(8, fontSize * 0.18);
      t.strokeStyle = "rgba(2, 6, 23, 0.92)";
      t.fillStyle = color;
      t.shadowColor = "rgba(0,0,0,0.48)";
      t.shadowBlur = 5;
      lines.forEach((line, lineIndex) => {
        const y = size * 0.52 + (lineIndex - (lines.length - 1) / 2) * lineHeight;
        t.strokeText(line, size * 0.5, y);
        t.fillText(line, size * 0.5, y);
      });
    }
    return tex;
  }

  function diceModelMapTriangle(ctx, image, src, dst) {
    const den = src[0][0] * (src[1][1] - src[2][1]) +
      src[1][0] * (src[2][1] - src[0][1]) +
      src[2][0] * (src[0][1] - src[1][1]);
    if (Math.abs(den) < 0.001) return;
    const a = (dst[0][0] * (src[1][1] - src[2][1]) +
      dst[1][0] * (src[2][1] - src[0][1]) +
      dst[2][0] * (src[0][1] - src[1][1])) / den;
    const b = (dst[0][1] * (src[1][1] - src[2][1]) +
      dst[1][1] * (src[2][1] - src[0][1]) +
      dst[2][1] * (src[0][1] - src[1][1])) / den;
    const c = (dst[0][0] * (src[2][0] - src[1][0]) +
      dst[1][0] * (src[0][0] - src[2][0]) +
      dst[2][0] * (src[1][0] - src[0][0])) / den;
    const d = (dst[0][1] * (src[2][0] - src[1][0]) +
      dst[1][1] * (src[0][0] - src[2][0]) +
      dst[2][1] * (src[1][0] - src[0][0])) / den;
    const e = (dst[0][0] * (src[1][0] * src[2][1] - src[2][0] * src[1][1]) +
      dst[1][0] * (src[2][0] * src[0][1] - src[0][0] * src[2][1]) +
      dst[2][0] * (src[0][0] * src[1][1] - src[1][0] * src[0][1])) / den;
    const f = (dst[0][1] * (src[1][0] * src[2][1] - src[2][0] * src[1][1]) +
      dst[1][1] * (src[2][0] * src[0][1] - src[0][0] * src[2][1]) +
      dst[2][1] * (src[0][0] * src[1][1] - src[1][0] * src[0][1])) / den;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(dst[0][0], dst[0][1]);
    ctx.lineTo(dst[1][0], dst[1][1]);
    ctx.lineTo(dst[2][0], dst[2][1]);
    ctx.closePath();
    ctx.clip();
    ctx.transform(a, b, c, d, e, f);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(image, 0, 0);
    ctx.restore();
  }

  function diceModelDrawTexturedQuad(ctx, points, texture) {
    const size = texture.width;
    const src = [[0, size], [size, size], [size, 0], [0, 0]];
    diceModelMapTriangle(ctx, texture, [src[0], src[1], src[2]], [points[0], points[1], points[2]]);
    diceModelMapTriangle(ctx, texture, [src[0], src[2], src[3]], [points[0], points[2], points[3]]);
  }

  function diceModelMotion(die, elapsed, now) {
    const local = Math.max(0, elapsed - die.delay);
    let spinLeft = 1;
    let phase = (local / DICE_MODEL_PROFILE.duration) * DICE_MODEL_PROFILE.turns * Math.PI * 2 * die.spinBoost;
    if (die.stopAt) {
      const stopLocal = Math.max(0, (now - die.stopAt) / 1000);
      const t = Math.min(stopLocal / 0.36, 1);
      spinLeft = Math.pow(1 - t, 2.15);
      phase = die.stopBase + (1 - spinLeft) * Math.PI * 0.8;
    }
    const rot = [
      die.settle[0] + phase * spinLeft,
      die.settle[1] + Math.sin(phase + die.phase) * 0.1 * spinLeft,
      die.settle[2] + Math.cos(phase * 0.8 + die.phase) * 0.09 * spinLeft,
    ];
    const lift = Math.sin(Math.min(local / DICE_MODEL_PROFILE.duration, 1) * Math.PI) * 0.08 * spinLeft;
    return { spinLeft, rot, lift, t: Math.min(local / DICE_MODEL_PROFILE.duration, 1) };
  }

  function diceModelDrawSpinCue(ctx, x, z, size, motion, color) {
    if (motion.spinLeft < 0.08) return;
    ctx.save();
    ctx.globalAlpha = Math.min(0.5, motion.spinLeft * 0.64);
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.2;
    ctx.lineCap = "round";
    ctx.shadowColor = color;
    ctx.shadowBlur = 9;
    for (let i = 0; i < 2; i += 1) {
      const start = motion.t * 11 + i * Math.PI;
      ctx.beginPath();
      ctx.ellipse(x + 2, z + 4, 18 * size, 42 * size, -0.08, start, start + Math.PI * 0.9);
      ctx.stroke();
    }
    ctx.restore();
  }

  function diceModelDrawDie(ctx, die, elapsed, now, compact) {
    const [x, z] = die.target;
    const motion = diceModelMotion(die, elapsed, now);
    const size = compact ? 0.9 : 1;
    const half = 0.58 * size;
    const origin = [x, z + motion.lift * -9];
    const base = DICE_MODEL_PALETTE[die.type] || DICE_MODEL_PALETTE.blank;
    ctx.save();
    ctx.beginPath();
    ctx.ellipse(x + 7, z + 25, 34 * size * (1 - motion.lift * 0.2), 12 * size * (1 - motion.lift * 0.16), -0.16, 0, Math.PI * 2);
    ctx.fillStyle = die.type === "black" ? "rgba(248, 113, 113, 0.2)" : "rgba(0,0,0,0.46)";
    ctx.filter = "blur(2.4px)";
    ctx.fill();
    ctx.filter = "none";
    const rawVerts = [
      [-half, -half, -half], [half, -half, -half], [half, -half, half], [-half, -half, half],
      [-half, half, -half], [half, half, -half], [half, half, half], [-half, half, half],
    ];
    const modelVerts = rawVerts.map((p) => diceModelRotate(p, motion.rot[0], motion.rot[1], motion.rot[2]));
    const verts = modelVerts.map((p) => diceModelProject(p, origin, compact ? 46 : 42));
    const faces = [
      { name: "bottom", ids: [0, 1, 2, 3], tone: base.side },
      { name: "top", ids: [4, 7, 6, 5], tone: base.top },
      { name: "front", ids: [3, 2, 6, 7], tone: base.front },
      { name: "back", ids: [0, 4, 5, 1], tone: base.side },
      { name: "right", ids: [1, 5, 6, 2], tone: base.side },
      { name: "left", ids: [0, 3, 7, 4], tone: base.side },
    ].map((face) => {
      const world = face.ids.map((id) => modelVerts[id]);
      return {
        ...face,
        world,
        normal: diceModelFaceNormal(world),
        avgDepth: world.reduce((sum, p) => sum + p[2], 0) / world.length,
      };
    });
    const visibleFaces = faces
      .map((face) => {
        const pts = face.ids.map((id) => verts[id]);
        return { ...face, pts, screenSignedArea: diceModelSignedArea(pts), screenArea: diceModelArea(pts) };
      })
      .filter((face) => face.screenSignedArea < -80)
      .sort((a, b) => a.avgDepth - b.avgDepth);
    visibleFaces.forEach((face) => {
      const fillColor = diceModelSolidFaceColor(face.tone, face.normal);
      diceModelDrawFace(ctx, face.pts, fillColor);
      const content = face.name === "top" ? { type: "label", text: die.label } : null;
      diceModelDrawTexturedQuad(ctx, face.pts, diceModelMakeFaceTexture(fillColor, base.c, content));
    });
    const edgeSet = new Set();
    visibleFaces.forEach((face) => {
      for (let i = 0; i < face.ids.length; i += 1) {
        const a = face.ids[i];
        const b = face.ids[(i + 1) % face.ids.length];
        edgeSet.add(a < b ? `${a}-${b}` : `${b}-${a}`);
      }
    });
    ctx.strokeStyle = diceModelColorMix(base.c, 0.58);
    ctx.lineWidth = 1.35;
    ctx.lineJoin = "round";
    ctx.globalAlpha = 0.58;
    edgeSet.forEach((key) => {
      const [a, b] = key.split("-").map(Number);
      ctx.beginPath();
      ctx.moveTo(verts[a][0], verts[a][1]);
      ctx.lineTo(verts[b][0], verts[b][1]);
      ctx.stroke();
    });
    ctx.globalAlpha = 1;
    ctx.restore();
  }

  function diceModelDrawCard(state, now) {
    const canvas = state.canvas;
    if (!canvas || !document.body.contains(canvas)) return false;
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = Math.max(52, Math.floor(rect.width || 82));
    const height = Math.max(52, Math.floor(rect.height || 74));
    if (canvas.width !== Math.floor(width * dpr) || canvas.height !== Math.floor(height * dpr)) {
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
    }
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, width, height);
    state.die.target = [width * 0.5, height * 0.42, 0];
    const elapsed = (now - state.start) / 1000;
    diceModelDrawDie(ctx, state.die, elapsed, now, true);
    return state.rolling || (state.die.stopAt && now - state.die.stopAt < 520);
  }

  function diceModelCardsFrame(now) {
    let keepAnimating = false;
    diceModelRegistry.forEach((state, key) => {
      if (!state.canvas || !document.body.contains(state.canvas)) {
        diceModelRegistry.delete(key);
        return;
      }
      keepAnimating = diceModelDrawCard(state, now) || keepAnimating;
    });
    window.diceModelAudit = {
      renderer: "canvas-model-card",
      effectMode: "tumble-horizontal",
      resultPose: "top-face-up",
      diceCount: diceModelRegistry.size,
      active: keepAnimating,
    };
    if (diceModelRegistry.size && keepAnimating) {
      diceModelRaf = requestAnimationFrame(diceModelCardsFrame);
    } else {
      diceModelRaf = 0;
    }
  }

  function ensureDiceModelLoop() {
    if (!diceModelRaf) diceModelRaf = requestAnimationFrame(diceModelCardsFrame);
  }

  function mountCharacterDiceModels(rolls) {
    const byId = new Map((rolls || []).map((roll, index) => [String(roll.id || `roll_${index}`), { roll, index }]));
    document.querySelectorAll("#confirmPopup .roll-die-canvas").forEach((canvas) => {
      const id = canvas.getAttribute("data-dice-model-id") || "";
      const item = byId.get(id);
      if (!item) return;
      const rolling = canvas.getAttribute("data-dice-model-rolling") === "1";
      const roll = item.roll;
      let state = diceModelRegistry.get(id);
      if (!state) {
        state = {
          canvas,
          start: performance.now(),
          rolling,
          die: diceModelMakeDie(roll, item.index),
        };
        if (!rolling) {
          state.die.stopAt = performance.now() - 600;
          state.die.stopBase = 0;
        }
        diceModelRegistry.set(id, state);
      }
      state.canvas = canvas;
      state.die.label = faceText(roll.face).replace(/[?？]/g, "");
      state.die.type = diceModelType(roll);
      if (rolling && !state.rolling) {
        state.start = performance.now();
        state.die.stopAt = null;
        state.die.stopBase = 0;
      }
      if (!rolling && state.rolling && !state.die.stopAt) {
        const now = performance.now();
        const local = Math.max(0, (now - state.start) / 1000 - state.die.delay);
        state.die.stopAt = now;
        state.die.stopBase = (local / DICE_MODEL_PROFILE.duration) * DICE_MODEL_PROFILE.turns * Math.PI * 2 * state.die.spinBoost;
      }
      if (!rolling && !state.rolling && !state.die.stopAt) {
        state.die.stopAt = performance.now() - 600;
        state.die.stopBase = 0;
      }
      state.rolling = rolling;
      diceModelDrawCard(state, performance.now());
    });
    ensureDiceModelLoop();
  }

  function renderCharacterRollsHtml(rolls, selectedIds, need, options) {
    const opts = options || {};
    const selected = new Set(selectedIds || []);
    const stage = opts.stage || "select";
    const revealCount = opts.revealCount == null ? (rolls || []).length : opts.revealCount;
    const readOnly = !!opts.readOnly;
    return `<div class="character-roll-grid${stage === "rolling" ? " is-rolling-stage" : ""}">${(rolls || []).map((r, idx) => {
      const revealed = stage !== "rolling" || idx < revealCount;
      const isRolling = !revealed;
      const isLanding = stage === "rolling" && revealed && idx === revealCount - 1;
      const selectedCls = selected.has(r.id) ? " selected" : "";
      const relevant = r.face && r.face.attr && need && need[r.face.attr] != null ? " relevant" : "";
      const locked = r.locked ? " locked" : "";
      const avatar = r.avatar ? `<img src="${r.avatar}" alt="${escapeHtml(r.staffName)}"/>` : `<span class="tool-avatar">道</span>`;
      const black = r.black ? " black-roll" : "";
      const grounded = r.grounded ? " grounded-roll" : "";
      const disabled = isRolling || readOnly ? "disabled" : "";
      const faceLabel = isRolling ? rollingFacePlaceholder(idx) : faceText(r.face);
      const faceCls = isRolling ? "face-rolling" : faceClass(r.face);
      const selectedNow = selected.has(r.id);
      const stateText = isRolling
        ? "摇骰中"
        : r.black
          ? (selectedNow ? "黑骰计入" : "黑骰压力")
          : !r.face || r.face.blank
            ? "空面"
            : selectedNow && relevant
              ? "计入判定"
              : selectedNow
                ? "已选 · 不计需求"
                : relevant
                  ? "可计入"
                  : "本任务不计入";
      return `<button type="button" class="character-roll${selectedCls}${relevant}${locked}${black}${grounded}${isRolling ? " is-rolling" : ""}${isLanding ? " is-landing" : ""}${opts.blackActive && r.black ? " is-black-entering" : ""}${readOnly ? " is-readonly" : ""}" data-roll-id="${r.id}" aria-pressed="${selectedNow ? "true" : "false"}" title="${escapeHtml(diceImpactMeta(r, need, selectedNow).copy)}" ${disabled}>
        <span class="roll-die model-die ${faceCls}">
          <canvas class="roll-die-canvas" data-dice-model-id="${escapeHtml(r.id)}" data-dice-model-rolling="${isRolling ? "1" : "0"}" aria-label="${escapeHtml(faceLabel)}"></canvas>
          <span class="roll-die-face">${escapeHtml(faceLabel)}</span>
        </span>
        <span class="roll-owner">${avatar}<span>${escapeHtml(r.staffName)}</span></span>
        <span class="roll-state">${escapeHtml(stateText)}</span>
      </button>`;
    }).join("")}</div>`;
  }

  function animateDiceToTray(sourceButton) {
    if (!sourceButton || !document.body) return;
    const die = sourceButton.querySelector(".roll-die");
    const tray = document.querySelector("#confirmPopup .selected-dice-list") || document.querySelector("#confirmPopup .selected-dice-tray");
    if (!die || !tray) return;
    const start = die.getBoundingClientRect();
    const target = tray.getBoundingClientRect();
    if (!start.width || !start.height || !target.width || !target.height) return;
    const ghost = die.cloneNode(true);
    ghost.className = `${die.className} dice-fly-ghost`;
    ghost.style.left = `${start.left}px`;
    ghost.style.top = `${start.top}px`;
    ghost.style.width = `${start.width}px`;
    ghost.style.height = `${start.height}px`;
    ghost.style.setProperty("--fly-dx", `${target.left + Math.min(28, target.width / 2) - start.left}px`);
    ghost.style.setProperty("--fly-dy", `${target.top + Math.min(18, target.height / 2) - start.top}px`);
    document.body.appendChild(ghost);
    sourceButton.classList.remove("is-select-pulse");
    void sourceButton.offsetWidth;
    sourceButton.classList.add("is-select-pulse");
    window.setTimeout(() => {
      ghost.remove();
    }, 620);
  }

  function contributionText(sum, need) {
    const keys = Object.keys(need || {});
    if (!keys.length) return "无需求";
    const target = needTargetValue(need);
    const total = contributionTotalForNeed(need, sum || {});
    return `有效点 ${total}/${target} · ${keys.map((k) => `${k} ${sum[k] || 0}/${need[k] || 0}`).join(" · ")}`;
  }

  function renderCharacterDiceResolutionHtml(mission, check, tier) {
    const need = (mission && mission.need) || {};
    const met = needMetByContribution(need, check.contribution || {});
    const tierText = tier || check.tier || "";
    const tierClass = tierText === "大成功"
      ? "result-crit"
      : tierText === "成功"
        ? "result-success"
        : tierText === "大失败"
          ? "result-bad"
          : "result-fail";
    return `<div class="dice-resolution-card ${met ? "is-met" : "is-miss"} ${tierClass}">
      <div class="dice-resolution-head">
        <div>
          <strong>角色骰收束</strong>
          <span>${escapeHtml(mission && mission.name ? mission.name : "本次判定")}</span>
        </div>
        <em>${escapeHtml(tierText)}</em>
      </div>
      ${contributionProgressHtml(check.contribution || {}, need, true)}
      ${blackDiceInterventionHtml(check)}
      ${selectedDiceTrayHtml(check.rolls || [], check.selectedIds || [], need, true)}
      <div class="dice-resolution-rolls">
        ${renderCharacterRollsHtml(check.rolls || [], check.selectedIds || [], need, { stage: "final", readOnly: true })}
      </div>
    </div>`;
  }

  function showDiceSelectionPopup(mission, rolls, context) {
    const ctx = context || {};
    const baseRolls = ctx.baseRolls && ctx.baseRolls.length ? ctx.baseRolls : rolls;
    const hasBlackIntervention = !!((ctx.blackDice && ctx.blackDice.length) || (ctx.blackNotes && ctx.blackNotes.length));
    const auto = autoSelectRollsForNeed(rolls, mission.need || {});
    let selectedIds = [];
    let stage = "rolling";
    let revealCount = 0;
    let resolved = false;
    let focusRollId = null;
    return new Promise((resolve) => {
      const wrap = document.getElementById("confirmPopup");
      const body = document.getElementById("confirmPopupBody");
      const date = document.getElementById("confirmPopupDate");
      const ttl = document.getElementById("confirmPopupTitle");
      const ok = document.getElementById("confirmPopupOk");
      const cancel = document.getElementById("confirmPopupCancel");
      if (!wrap || !body || !date || !ttl || !ok || !cancel) {
        resolve({ selectedIds, sum: rollContribution(rolls, selectedIds), success: needMetByContribution(mission.need || {}, rollContribution(rolls, selectedIds)) });
        return;
      }
      wrap.classList.add("dice-select-modal");
      ttl.textContent = "角色骰判定";
      date.textContent = mission.name || "";
      const render = () => {
        const currentRolls = stage === "rolling" ? baseRolls : rolls;
        const sum = rollContribution(rolls, selectedIds);
        const okNow = needMetByContribution(mission.need || {}, sum);
        const finalReady = stage !== "rolling";
        const selectReady = stage === "select";
        const stageText = stage === "rolling"
          ? `基础骰摇骰中 · ${revealCount}/${baseRolls.length}`
          : stage === "black"
            ? "黑骰介入 · 骰池被改写"
            : "停骰完成 · 选择计入判定的骰面";
        const helperText = stage === "rolling"
          ? "每名参判角色正在生成本轮骰面。"
          : stage === "black"
            ? "异常正在改写本轮骰池。"
            : "点击骰子计入或移出。";
        const stageBadge = stage === "rolling"
          ? "摇骰中"
          : stage === "black"
            ? "黑骰介入"
            : "选择阶段";
        body.innerHTML = `<div class="dice-select-shell">
          <div class="dice-select-head">
            <div>
              <div class="dice-select-stage">${escapeHtml(stageText)}</div>
              <p>${escapeHtml(helperText)}</p>
            </div>
            <div class="dice-select-result">${escapeHtml(stageBadge)}</div>
          </div>
          ${missionDiceDialogueHtml(mission, stage)}
          <div class="dice-select-layout">
            <section class="dice-workbench-panel" aria-label="本轮骰面">
              <div class="dice-section-head"><strong>本轮骰面</strong><span>${escapeHtml(diceSelectCountText(currentRolls, selectedIds, selectReady, revealCount))}</span></div>
              ${renderCharacterRollsHtml(currentRolls, selectedIds, mission.need || {}, { stage: stage === "rolling" ? "rolling" : "select", revealCount, readOnly: stage === "black", blackActive: stage === "black" })}
            </section>
            <aside class="dice-side-stack" aria-label="判定摘要与提交后果">
              ${diceSelectSummaryHtml(sum, mission.need || {}, selectReady)}
              ${stage === "black" || selectReady ? blackDiceInterventionHtml({ ...ctx, active: stage === "black" }) : ""}
              ${diceSubmitPreviewHtml(okNow, selectReady)}
            </aside>
          </div>
        </div>`;
        mountCharacterDiceModels(currentRolls);
        body.querySelectorAll("[data-roll-id]").forEach((btn) => {
          const id = btn.getAttribute("data-roll-id");
          btn.onfocus = () => {
            if (!selectReady) return;
            focusRollId = id;
            render();
          };
          btn.onclick = () => {
            if (!selectReady) return;
            focusRollId = id;
            if (selectedIds.includes(id)) {
              selectedIds = selectedIds.filter((x) => x !== id);
            } else {
              animateDiceToTray(btn);
              selectedIds.push(id);
            }
            render();
          };
        });
        ok.disabled = !selectReady;
        cancel.disabled = !selectReady;
        ok.textContent = "确认计入";
        cancel.textContent = selectReady ? "采用推荐" : "等待停骰";
      };
      const cleanup = (result) => {
        resolved = true;
        wrap.classList.add("hidden");
        wrap.classList.remove("dice-select-modal");
        ok.disabled = false;
        cancel.disabled = false;
        ok.removeEventListener("click", onOk);
        cancel.removeEventListener("click", onCancel);
        resolve(result);
      };
      const onOk = () => {
        if (stage !== "select") return;
        const sum = rollContribution(rolls, selectedIds);
        cleanup({ selectedIds: selectedIds.slice(), sum, success: needMetByContribution(mission.need || {}, sum) });
      };
      const onCancel = () => {
        if (stage !== "select") return;
        selectedIds = autoSelectRollsForNeed(rolls, mission.need || {});
        const sum = rollContribution(rolls, selectedIds);
        cleanup({ selectedIds: selectedIds.slice(), sum, success: needMetByContribution(mission.need || {}, sum) });
      };
      ok.textContent = "确认计入";
      cancel.textContent = "采用推荐";
      ok.addEventListener("click", onOk);
      cancel.addEventListener("click", onCancel);
      wrap.classList.remove("hidden");
      render();
      (async () => {
        await sleep(480);
        for (let i = 1; i <= (baseRolls || []).length; i++) {
          if (resolved) return;
          revealCount = i;
          render();
          await sleep(260);
        }
        if (resolved) return;
        if (hasBlackIntervention) {
          stage = "black";
          revealCount = rolls.length;
          render();
          await sleep(900);
          if (resolved) return;
        }
        stage = "select";
        selectedIds = auto.slice();
        focusRollId = selectedIds[0] || (rolls[0] && rolls[0].id) || null;
        render();
      })();
    });
  }

  function enqueueCurrentMission() {
    const m = state.mission;
    if (!m) return;
    if (m.missionQueueId) {
      const idx = state.activeMissions.findIndex((x) => x.id === m.missionQueueId);
      if (idx >= 0) {
        if (state.selectedStaffIds.some((id) => isStaffAssigned(id, m.missionQueueId))) {
          log("派遣更新失败：队员已被其他任务占用。");
          return;
        }
        state.activeMissions[idx].staffIds = state.selectedStaffIds.slice();
        state.activeMissions[idx].toolDiceIds = state.activeMissions[idx].toolDiceIds || [];
        state.activeMissions[idx].mission = { ...state.activeMissions[idx].mission, toolDiceIds: state.activeMissions[idx].toolDiceIds.slice() };
        log(`已更新派遣：${m.name}（仍需 ${state.activeMissions[idx].remainingDays} 天判定）`);
      }
      state.mission = null;
      state.selectedStaffIds = [];
      state.selectedToolDiceIds = [];
      updateNextDayButton();
      return;
    }
    const toolDiceIds = (state.selectedToolDiceIds || []).filter((id) => {
      const tool = state.toolDiceInventory.find((x) => x.id === id);
      return tool && !tool.used;
    });
    const rec = {
      id: `q_${Date.now()}_${Math.floor(Math.random() * 10000)}`,
      mission: { ...m, toolDiceIds },
      staffIds: state.selectedStaffIds.slice(),
      toolDiceIds,
      remainingDays: m.days | 0,
      regionId: m.regionId,
      status: "running",
    };
    if (rec.staffIds.some((id) => isStaffAssigned(id, null))) {
      log("派遣失败：队员已被其他任务占用。");
      return;
    }
    toolDiceIds.forEach((id) => {
      const tool = state.toolDiceInventory.find((x) => x.id === id);
      if (tool) tool.used = true;
    });
    state.activeMissions.push(rec);
    log(`已派遣：${m.name}（预计 ${rec.remainingDays} 天后判定）${toolDiceIds.length ? "；已消耗一次性道具骰。" : ""}`);
    state.mission = null;
    state.selectedStaffIds = [];
    state.selectedToolDiceIds = [];
    updateNextDayButton();
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function calcAnimPace(check) {
    const total = check.rollsA.length + check.rollsB.length;
    const warmupDelay = total >= 24 ? 760 : total >= 16 ? 860 : 980;
    const stepDelay = total >= 24 ? 84 : total >= 16 ? 96 : 108;
    const revealStepA = 1;
    const revealStepB = 1;
    const voidStep = Math.max(1, Math.ceil((check.voidA.size + check.voidB.size) / 5));
    const settleDelay = total >= 24 ? 520 : 620;
    return { warmupDelay, stepDelay, revealStepA, revealStepB, voidStep, settleDelay };
  }

  function finalStateFromRoll(hit, isVoid) {
    if (isVoid) return { text: "", cls: "die void" };
    return hit ? { text: "✓", cls: "die hit reveal-pop" } : { text: "×", cls: "die miss reveal-pop" };
  }

  function randomRollFace() {
    return ROLL_FACES[Math.floor(Math.random() * ROLL_FACES.length)];
  }

  function setRollingFace(el, face) {
    el.textContent = face || "";
    if (face === "✓") {
      el.style.color = "#22c55e";
      el.style.borderColor = "#22c55e";
      el.style.boxShadow = "0 0 0 1px rgba(34,197,94,0.22) inset, 0 0 12px rgba(34,197,94,0.32)";
    } else if (face === "×") {
      el.style.color = "#ef4444";
      el.style.borderColor = "#ef4444";
      el.style.boxShadow = "0 0 0 1px rgba(239,68,68,0.2) inset, 0 0 12px rgba(239,68,68,0.28)";
    } else if (face === "?") {
      el.style.color = "#60a5fa";
      el.style.borderColor = "#60a5fa";
      el.style.boxShadow = "0 0 0 1px rgba(96,165,250,0.25) inset, 0 0 12px rgba(59,130,246,0.35)";
    } else {
      el.style.color = "#93c5fd";
      el.style.borderColor = "#94a3b8";
      el.style.boxShadow = "0 0 0 1px rgba(148,163,184,0.16) inset, 0 0 9px rgba(148,163,184,0.22)";
    }
  }

  function setFinalFace(el, text, cls) {
    el.style.color = "";
    el.style.borderColor = "";
    el.style.boxShadow = "";
    el.className = cls;
    el.textContent = text || "";
  }

  function createRollingDiceRow(container, label, count) {
    const pool = document.createElement("div");
    pool.className = "dice-pool";
    const h3 = document.createElement("h3");
    h3.textContent = label;
    pool.appendChild(h3);
    if (!count) {
      const tip = document.createElement("div");
      tip.className = "tip-inline";
      tip.textContent = `${label}：无骰`;
      pool.appendChild(tip);
      container.appendChild(pool);
      return [];
    }
    const row = document.createElement("div");
    row.className = "dice-row";
    const els = [];
    for (let i = 0; i < count; i++) {
      const span = document.createElement("span");
      span.className = "die rolling";
      setRollingFace(span, randomRollFace());
      row.appendChild(span);
      els.push(span);
    }
    pool.appendChild(row);
    container.appendChild(pool);
    return els;
  }

  async function animateDiceReveal(_elRes, check) {
    const holder = document.getElementById("diceAnim");
    if (!holder) return;
    const pace = calcAnimPace(check);
    holder.innerHTML = `<div class="dice-rolling-hint"><span class="dice-spinner"></span><span id="dicePhaseText">摇骰中...</span></div><div id="diceRowsHost"></div>`;
    const host = document.getElementById("diceRowsHost");
    if (!host) return;
    const aEls = createRollingDiceRow(host, "调查池", check.rollsA.length);
    const bEls = createRollingDiceRow(host, "现场池", check.rollsB.length);
    const phaseText = () => document.getElementById("dicePhaseText");
    const ticker = window.setInterval(() => {
      const dice = holder.querySelectorAll(".die.rolling");
      dice.forEach((d) => setRollingFace(d, randomRollFace()));
    }, 92);
    await sleep(pace.warmupDelay);

    for (let i = 0; i < aEls.length; i += pace.revealStepA) {
      const end = Math.min(aEls.length, i + pace.revealStepA);
      const p = phaseText();
      if (p) p.textContent = `调查池停骰 ${end}/${aEls.length}`;
      for (let k = i; k < end; k++) {
        const d = finalStateFromRoll(check.rollsA[k], false);
        setFinalFace(aEls[k], d.text, d.cls);
      }
      await sleep(pace.stepDelay);
    }
    for (let i = 0; i < bEls.length; i += pace.revealStepB) {
      const end = Math.min(bEls.length, i + pace.revealStepB);
      const p = phaseText();
      if (p) p.textContent = `现场池停骰 ${end}/${bEls.length}`;
      for (let k = i; k < end; k++) {
        const d = finalStateFromRoll(check.rollsB[k], false);
        setFinalFace(bEls[k], d.text, d.cls);
      }
      await sleep(pace.stepDelay);
    }

    const pDone = phaseText();
    if (pDone) pDone.textContent = "基础结果已揭示";
    await sleep(260);

    // 对手作废阶段：按顺序逐颗作废
    const voidSeq = [];
    for (const idx of check.voidA) voidSeq.push({ pool: "A", idx });
    for (const idx of check.voidB) voidSeq.push({ pool: "B", idx });
    for (let i = 0; i < voidSeq.length; i += pace.voidStep) {
      const end = Math.min(voidSeq.length, i + pace.voidStep);
      const p = phaseText();
      if (p) p.textContent = `对手作废中... ${end}/${voidSeq.length}`;
      for (let k = i; k < end; k++) {
        const s = voidSeq[k];
        const d = s.pool === "A"
          ? finalStateFromRoll(check.rollsA[s.idx], true)
          : finalStateFromRoll(check.rollsB[s.idx], true);
        const target = s.pool === "A" ? aEls[s.idx] : bEls[s.idx];
        if (target) setFinalFace(target, d.text, d.cls);
      }
      await sleep(pace.stepDelay + 18);
    }
    window.clearInterval(ticker);

    // 最终态面板
    holder.innerHTML = `<div>
      ${renderDiceRow(check.rollsA, new Set(), "调查池（基础）")}
      ${renderDiceRow(check.rollsB, new Set(), "现场池（基础）")}
      <div class="phase-label" style="margin-top:0.5rem;">对手作废 ${check.enemyAttr} 颗</div>
      ${renderDiceRow(check.rollsA, check.voidA, "调查·作废后")}
      ${renderDiceRow(check.rollsB, check.voidB, "现场·作废后")}
    </div>`;
    await sleep(pace.settleDelay);
  }

  async function runMission(onContinue) {
    const m = state.mission;
    if (!m) return;
    const useCharacterDice = true;
    let check = null;
    let tier = "失败";
    let diceSelection = null;
    if (useCharacterDice) {
      const missionToolDiceIds = Array.isArray(m.toolDiceIds) ? m.toolDiceIds : state.selectedToolDiceIds;
      const baseRolls = rollCharacterDice(m, state.selectedStaffIds, missionToolDiceIds);
      const blackDice = blackDiceForMission(m, baseRolls);
      const blackApplied = applyBlackDiceToRolls(m, baseRolls, blackDice);
      const rolls = blackApplied.rolls;
      diceSelection = await showDiceSelectionPopup(m, rolls, { baseRolls, blackDice, blackNotes: blackApplied.notes, blackPressure: blackApplied.pressure });
      const selectedRolls = rolls.filter((r) => diceSelection.selectedIds.includes(r.id));
      tier = m.isBlackDiceTask
        ? blackDiceTier(m, diceSelection.success, diceSelection.sum, blackApplied.pressure, selectedRolls)
        : diceSelection.success ? "小成功" : "失败";
      check = { characterDice: true, rolls, selectedIds: diceSelection.selectedIds, contribution: diceSelection.sum, tier, blackDice, blackNotes: blackApplied.notes, blackPressure: blackApplied.pressure };
    } else {
      check = runSplitCheck(m, state.selectedStaffIds);
      tier = check.tier;
    }
    const highTier = mapHighRiskTier(m, tier);
    const lines = [];
    const rewards = [];
    if (m.missionType === "leadInvestigation") {
      const lead = (state.regionLeadEvents[m.regionId] || []).find((x) => x.id === m.leadId);
      if (lead && !lead.investigated) {
        lead.investigated = true;
        lead.assigned = false;
        if (tier === "大成功" || tier === "小成功") {
          const node = lead.spawn();
          addDynamicNode(m.regionId, node, lead.durationWeeks || 1);
          lead.result = `调查${tier}：发现真实事件点「${node.name}」。`;
          lines.push(`线索调查${tier}：已解锁新事件点。`);
          rewards.push({ icon: "🗺", title: `新事件点：${node.name}`, desc: "已加入区域地图，可继续派遣探索。" });
          log(`线索事件成功：${lead.title} -> ${node.name}`);
          macro.声望 = Math.min(100, macro.声望 + (tier === "大成功" ? 2 : 1));
        } else {
          lead.result = `调查${tier}：线索不可靠，未发现有效事件。`;
          lines.push(`线索调查${tier}：未发现有效事件。`);
          log(`线索事件失败：${lead.title}`);
          macro.声望 = Math.max(0, macro.声望 - (tier === "大失败" ? 2 : 1));
        }
      }
    } else if (m.isBlackDiceTask) {
      (check.blackNotes || []).forEach((x) => lines.push(x));
      if (tier === "大成功") {
        addMacro({ 声望: 6, 诡名: 3 });
        lines.push(missionOutcomeLine(m, "大成功", "黑骰任务大成功：你拿到了危险素材，并暂时避开主要反噬。"));
        addMissionClue(m, "黑骰强素材", 3, rewards, "黑骰任务：大成功（Tier 3）", "大成功");
      } else if (tier === "成功") {
        addMacro({ 声望: 4, 诡名: 2, 狂性: 1 });
        lines.push(missionOutcomeLine(m, "成功", "黑骰任务成功：关键素材到手，但异常留下了轻微回声。"));
        addMissionClue(m, "黑骰关键素材", 3, rewards, "黑骰任务：成功（Tier 3，轻微反噬）", "成功");
      } else if (tier === "失败") {
        addMacro({ 声望: -1, 狂性: 2 });
        lines.push(missionOutcomeLine(m, "失败", "黑骰任务失败：没有拿稳真相，但留下了弱线索和压力。"));
        addMissionClue(m, "黑骰弱线索", 1, rewards, "黑骰任务：失败（Tier 1）", "失败");
      } else {
        addMacro({ 公信: -2, 守序: -3, 狂性: 5 });
        lines.push(missionOutcomeLine(m, "大失败", "黑骰任务大失败：异常反过来污染了队伍，本局后续风险上升。"));
        state.staffDebuffs[state.selectedStaffIds[0] || "global"] = { riskFace: true, source: m.name };
        rewards.push({ icon: "!", title: "黑骰大失败 debuff", desc: "一名队员获得风险面标记；本局后续同类任务会更危险。" });
      }
    } else {
      applyStandardOutcome(m, tier, lines, rewards);
    }
    if (m.missionType !== "leadInvestigation") {
      recordWhiteInvestigation(m, lines);
      advanceDeepChain(m, lines, rewards);
      retireRedMission(m, lines);
    }
    ["公信", "诡名", "声望", "守序", "狂性"].forEach((k) => {
      macro[k] = Math.max(0, Math.min(100, macro[k]));
    });
    log(`${m.name} → 「${m.isBlackDiceTask ? highTier.label : tier}」`);
    const elRes = document.getElementById("view-result");
    const showDice = state.displayMode === "dice";
    const missionHead = missionHeaderHtml(m, state.selectedStaffIds);
    elRes.innerHTML = `
      <h2>${m.missionType === "leadInvestigation" ? "线索调查结算" : "探索结算"}</h2>
      ${missionHead}
      ${missionFieldIntroHtml(m)}
      <div class="result-banner" id="tierBanner">判定中...</div>
      ${showDice ? `<div id="diceAnim"><div class="dice-rolling-hint"><span class="dice-spinner"></span><span>摇骰中...</span></div></div>`
        : `<div class="prob-box" id="diceAnim">计算中...</div>`}
      <p class="result-story-lines">${lines.map(escapeHtml).join("<br/>")}</p>
      <div id="bonusOutcome"></div>
      <p>剩余 <strong>${state.day}</strong> 日</p>
      <button type="button" class="primary" id="btnAfterResult" disabled>继续</button>`;
    bindMissionStaffHover(elRes);
    setView("result");
    renderMacro();
    if (check.characterDice) {
      const h = document.getElementById("diceAnim");
      if (h) h.innerHTML = renderCharacterDiceResolutionHtml(m, check, tier);
      mountCharacterDiceModels(check.rolls || []);
      await sleep(450);
    } else if (showDice) {
      await animateDiceReveal(elRes, check);
    } else {
      await sleep(450);
      const h = document.getElementById("diceAnim");
      if (h) h.innerHTML = `<div class="prob-box">调查 ${check.hitsA}/${check.nAe}（≥${check.kA}）· 现场 ${check.hitsB}/${check.nBe}（≥${check.kB}）</div>`;
    }
    const tbBeforeRewards = document.getElementById("tierBanner");
    if (tbBeforeRewards) tbBeforeRewards.textContent = tier;
    await showRewardsPopup(rewards);
    if (shouldOfferPushBonus(m, highTier)) {
      await resolvePushBonus(m, showDice);
    }
    if (week1TutorialActive() && !state.tutorialSoftW1.w1_result) {
      if (tutorialsGloballyDisabled()) {
        state.tutorialSoftW1.w1_result = true;
      } else {
        await showWeek1SoftTutorialModal(
          "w1_result",
          "第一周 · 外拍结算",
          [
            `${tutorialSoftFigure(
              "Assets/tutorial-result-guide.svg",
              "结算示意：调查与现场双线判定",
              "示意：调查池与现场池各自过线，合起来决定本次档位。",
            )}<div class="tutorial-soft-sheet">
              <h4 class="tutorial-soft-h4">双线结果</h4>
              <p class="tutorial-soft-lead">「调查」与「现场」<strong>各自过线</strong>，合在一起决定大获全胜、平稳交差、失手或闹大。</p>
              <ul class="tutorial-soft-ul">
                <li>奖励弹窗可逐条翻看。</li>
              </ul>
            </div>`,
            `<div class="tutorial-soft-sheet">
              <h4 class="tutorial-soft-h4">点「继续」之后</h4>
              <ul class="tutorial-soft-ul">
                <li>若本周还有天数：回到<strong>区域</strong>继续安排。</li>
                <li>若本周时间用尽：编辑部会请您进<strong>合成台</strong>把料收成稿。</li>
              </ul>
              <p class="tutorial-soft-note">关窗后本周不再重复本提示。</p>
            </div>`,
          ],
        );
      }
    }
    const tb = document.getElementById("tierBanner");
    if (tb && !/^再追一次/.test(tb.textContent || "")) tb.textContent = tier;
    const goBtn = document.getElementById("btnAfterResult");
    if (goBtn) goBtn.disabled = false;
    document.getElementById("btnAfterResult").onclick = () => {
      state.mission = null;
      state.selectedStaffIds = [];
      state.selectedToolDiceIds = [];
      renderMacro();
      if (typeof onContinue === "function") {
        onContinue();
        return;
      }
      if (state.day <= 0) enterSynthesisPhase();
      else {
        renderRegion();
        setView("region");
      }
    };
  }

  function renderCurrentRegionOrGlobal() {
    if (state.regionId && REGIONS.some((r) => r.id === state.regionId)) {
      renderRegion();
      setView("region");
      return;
    }
    renderGlobal();
    setView("global");
  }

  function resolveQueuedMissions() {
    if (!state.todayResolutionQueue.length) {
      state.processingDayTick = false;
      state.dayResolutionInfo = null;
      updateNextDayButton();
      if (state.day <= 0) {
        enterSynthesisPhase();
      } else {
        // 每日判定队列结束后回到当前地区，继续安排本地区派遣。
        renderCurrentRegionOrGlobal();
      }
      return;
    }
    const total = state.dayResolutionInfo ? state.dayResolutionInfo.total : state.todayResolutionQueue.length;
    const next = state.todayResolutionQueue.shift();
    state.dayResolutionInfo = { current: total - state.todayResolutionQueue.length, total };
    state.mission = { ...next.mission, toolDiceIds: (next.toolDiceIds || []).slice() };
    state.selectedStaffIds = next.staffIds.slice();
    state.selectedToolDiceIds = (next.toolDiceIds || []).slice();
    state.missionResolving = true;
    runMission(() => {
      next.status = "resolved";
      state.activeMissions = state.activeMissions.filter((x) => x.id !== next.id);
      state.missionResolving = false;
      resolveQueuedMissions();
    }).catch(() => {
      state.missionResolving = false;
      state.processingDayTick = false;
      updateNextDayButton();
    });
  }

  async function advanceOneDay() {
    if (state.phase !== "explore" || state.processingDayTick) return;
    if (state.day <= 0) {
      enterSynthesisPhase();
      return;
    }
    const runningCount = state.activeMissions.filter((x) => x.status === "running").length;
    if (runningCount <= 0) {
      const ok = await showConfirmPopup(
        "未进行探索",
        "<p style=\"margin:0;\">您未进行任何探索，是否进入下一天？</p>",
        dayDateLabel()
      );
      if (!ok) return;
    }
    state.processingDayTick = true;
    state.day -= 1;
    for (const rec of state.activeMissions) {
      if (rec.status === "running") rec.remainingDays -= 1;
    }
    const due = state.activeMissions.filter((x) => x.status === "running" && x.remainingDays <= 0);
    due.forEach((x) => { x.status = "due"; });
    state.todayResolutionQueue = due.slice();
    log(`推进至下一天：当前剩余 ${state.day} 日。${due.length ? `到期任务 ${due.length} 项，开始判定。` : "暂无到期任务。"}`);
    tickHeader();
    updateNextDayButton();
    await showDayPopup();
    if (!due.length) {
      state.processingDayTick = false;
      updateNextDayButton();
      renderCurrentRegionOrGlobal();
      if (state.day <= 0) enterSynthesisPhase();
      return;
    }
    state.dayResolutionInfo = { current: 0, total: due.length };
    resolveQueuedMissions();
  }

  function dayIndexInWeek() {
    return Math.max(1, Math.min(7, 8 - state.day));
  }

  function dayDateLabel() {
    return `第 ${state.week} 周 · 第 ${dayIndexInWeek()} 天（余 ${state.day} / 7 日）`;
  }

  function explorationDayFlavorPool() {
    const pool = [];
    const running = (state.activeMissions || []).filter((x) => x.status === "running" && x.mission);
    if (running.length) {
      const rec = running[0];
      const story = missionStory(rec.mission);
      pool.push([
        `外勤组从「${rec.mission.name}」发回一条断续语音。`,
        story && story.objective ? `你在便签上重写本次目标：${story.objective}` : "你只听清最后一句：别急着定标题。",
      ]);
      pool.push([
        `编辑部白板上，「${rec.mission.name}」下面多了一个红圈。`,
        rec.remainingDays > 1 ? `还要 ${rec.remainingDays} 天才会有结果，但债主不会等那么久。` : "明天就要见分晓，没人愿意先把版面留空。",
      ]);
    }
    if ((state.clues || []).length) {
      const clue = state.clues[state.clues.length - 1];
      pool.push([
        `昨晚拿到的「${clue.title}」被压在咖啡杯下面。`,
        "杯底水痕刚好圈住最值得追的那一行。",
      ]);
    }
    if (state.regionId === "us") {
      pool.push([
        "纽约市警用电台短暂串进编辑部收音机。",
        "你听到一个巡警说：别把那辆末班车写进报告。",
      ]);
      pool.push([
        "哈德逊河方向传来一阵低频杂音。",
        "窗玻璃轻轻发抖，像有人在水面下调试麦克风。",
      ]);
    }
    return pool;
  }

  function randomDayFlavor() {
    const basePool = [
      ["咖啡渍在版面上扩散。", "你把杯子挪开，假装什么都没发生。"],
      ["深夜电话响了三次才接通。", "对方只说：\"别去港口区。\""],
      ["打印机吐出一张空白纸。", "纸上却有淡淡的指纹，像刚从雨里捞出来。"],
      ["实习生递来一袋热乎的甜甜圈。", "你突然觉得今天也许不会太糟。"],
      ["电台播报的声音忽远忽近。", "你听到其中夹着一句不属于任何语言的低语。"],
      ["编辑部的灯闪了两下。", "每个人都下意识看向地图。"],
      ["邮筒里多了一封没有寄件人的信。", "你拆开，里面只有一小片金属。"],
      ["街角橱窗里的电视忽然无声闪烁。", "画面停在一张你还没派人拍过的街口。"],
    ];
    const explorationPool = explorationDayFlavorPool();
    const useExploration = explorationPool.length && Math.random() < 0.38;
    const pool = useExploration ? explorationPool : basePool;
    const pick = pool[Math.floor(Math.random() * pool.length)];
    return `${useExploration ? `<div class="day-flavor-tag">探索余波</div>` : ""}
      <p style="margin:0 0 0.35rem;">${escapeHtml(pick[0])}</p>
      <p style="margin:0;color:#94a3b8;">${escapeHtml(pick[1])}</p>`;
  }

  function showDayPopup() {
    const wrap = document.getElementById("dayPopup");
    const body = document.getElementById("dayPopupBody");
    const date = document.getElementById("dayPopupDate");
    const ok = document.getElementById("dayPopupOk");
    if (!wrap || !body || !date || !ok) return Promise.resolve();
    date.textContent = dayDateLabel();
    body.innerHTML = randomDayFlavor();
    wrap.classList.remove("hidden");
    return new Promise((resolve) => {
      const done = () => {
        wrap.classList.add("hidden");
        ok.removeEventListener("click", done);
        wrap.removeEventListener("click", onMask);
        resolve();
      };
      const onMask = (ev) => {
        if (ev.target === wrap) done();
      };
      ok.addEventListener("click", done);
      wrap.addEventListener("click", onMask);
    });
  }

  function showConfirmPopup(title, bodyHtml, dateText) {
    const wrap = document.getElementById("confirmPopup");
    const body = document.getElementById("confirmPopupBody");
    const date = document.getElementById("confirmPopupDate");
    const ttl = document.getElementById("confirmPopupTitle");
    const ok = document.getElementById("confirmPopupOk");
    const cancel = document.getElementById("confirmPopupCancel");
    if (!wrap || !body || !date || !ttl || !ok || !cancel) return Promise.resolve(false);
    ttl.textContent = title || "提示";
    date.textContent = dateText || "";
    body.innerHTML = bodyHtml || "";
    ok.textContent = "确认";
    cancel.textContent = "取消";
    wrap.classList.remove("hidden");
    return new Promise((resolve) => {
      const done = (v) => {
        wrap.classList.add("hidden");
        ok.removeEventListener("click", onOk);
        cancel.removeEventListener("click", onCancel);
        wrap.removeEventListener("click", onMask);
        resolve(v);
      };
      const onOk = () => done(true);
      const onCancel = () => done(false);
      const onMask = (ev) => { if (ev.target === wrap) done(false); };
      ok.addEventListener("click", onOk);
      cancel.addEventListener("click", onCancel);
      wrap.addEventListener("click", onMask);
    });
  }

  function rewardIconByType(type) {
    if (type === "sci") return "🔬";
    if (type === "occult") return "✦";
    if (type === "pop") return "🗞";
    return "🎁";
  }

  function showRewardsPopup(rewards) {
    const list = rewards && rewards.length ? rewards : [{ icon: "…", title: "未获得额外奖励", desc: "本次仅完成任务判定。" }];
    const wrap = document.getElementById("rewardPopup");
    const body = document.getElementById("rewardPopupBody");
    const step = document.getElementById("rewardPopupStep");
    const next = document.getElementById("rewardPopupNext");
    if (!wrap || !body || !step || !next) return Promise.resolve();
    let idx = 0;
    const render = () => {
      const r = list[idx] || list[0];
      step.textContent = `${idx + 1}/${list.length}`;
      body.innerHTML = `<div class="reward-box">
        <div class="reward-icon">${escapeHtml(r.icon || "🎁")}</div>
        <div>
          <div class="reward-title">${escapeHtml(r.title || "奖励")}</div>
          <div class="reward-desc">${escapeHtml(r.desc || "")}</div>
        </div>
      </div>`;
      next.textContent = idx >= list.length - 1 ? "完成" : "下一项";
    };
    wrap.classList.remove("hidden");
    render();
    return new Promise((resolve) => {
      const onNext = () => {
        if (idx >= list.length - 1) {
          wrap.classList.add("hidden");
          next.removeEventListener("click", onNext);
          resolve();
          return;
        }
        idx += 1;
        render();
      };
      next.addEventListener("click", onNext);
    });
  }

  function updateNextDayButton() {
    const floatingNextDay = document.getElementById("btnNextDay");
    const hideFloatingNext = state.view === "weekStart" || state.view === "global" || state.view === "setup" || state.view === "region" || state.view === "result" || state.phase !== "explore";
    if (floatingNextDay) floatingNextDay.classList.toggle("hidden", hideFloatingNext);
    const backToGlobal = document.getElementById("btnBackToGlobal");
    if (backToGlobal) {
      const canBack = state.phase === "explore" && state.view === "region" && !state.processingDayTick && !state.missionResolving;
      backToGlobal.classList.toggle("hidden", !canBack);
      backToGlobal.disabled = !canBack;
    }
    const btns = [document.getElementById("btnNextDay"), document.getElementById("btnNextDayRegion")].filter(Boolean);
    if (!btns.length) return;
    const disabled = state.phase !== "explore" || state.processingDayTick || state.missionResolving || state.view === "result";
    btns.forEach((btn) => {
      btn.disabled = disabled;
      const label = btn.querySelector("span:last-child");
      const text = btn.id === "btnNextDayRegion" ? regionNextDayButtonText() : (state.processingDayTick ? "结算中..." : "下一天");
      if (label) label.textContent = text;
      else btn.textContent = text;
    });
  }

  function returnToGlobalMap() {
    if (state.phase !== "explore") return;
    if (state.regionId) state.globalSelectedRegionId = state.regionId;
    state.openDeepChainId = null;
    state.regionLinkedTarget = null;
    renderGlobal();
    setView("global");
    updateNextDayButton();
  }

  function newCardId() {
    return `c${state.nextCardId++}`;
  }

  function qualityFromScore(score) {
    if (score >= 220) return QUALITY[2];
    if (score >= 140) return QUALITY[1];
    return QUALITY[0];
  }

  function initSynthesisFromClues() {
    state.phenomenonCards = [];
    state.intelCards = [];
    state.cognitionCards = [];
    state.toolCards = [];
    state.craftedReports = [];
    state.topicSynthOrder = {};
    state.synthRecipe = "r1";
    initSynthSlotsForRecipe("r1");
    state.tipOffCards = [];
    ensureStaffInternalDefaults();
    state.synthStaffCards = STAFF.map((s) => ({
      id: `sc_${s.id}`,
      kind: "staff",
      staffId: s.id,
      name: `${s.name}（主笔）`,
    }));
    state.therapyCards = [{ id: "th_pack_1", kind: "therapy", name: "心理干预包", uses: 1 }];
    if (state.pendingClues.length) {
      state.tipOffCards.push({
        id: newCardId(),
        kind: "tipoff",
        name: `匿名爆料摘录（${rand(["线人密件", "旁听记录", "加密邮件残段", "档案缺页复印件"])}）`,
        tier: Math.max(1, Math.min(3, state.pendingClues.length)),
      });
    }
    state.synthTab = "phenomenon";
    state.synthPollution = 0;
    for (const clue of state.pendingClues) {
      if (!clue.topicKey) clue.topicKey = newTopicKey();
      const tk = clue.topicKey;
      state.phenomenonCards.push({
        id: newCardId(),
        kind: "phenomenon",
        name: clue.title.replace("·", "样本·"),
        domain: clue.type,
        evidenceValue: 35 + clue.tier * 16,
        mysteryBias: clue.type === "occult" ? 70 : clue.type === "pop" ? 45 : 30,
        tier: clue.tier,
        topicKey: tk,
      });
      state.intelCards.push({
        id: newCardId(),
        kind: "intel",
        name: `${clue.title.split("·")[0]} 相关情报`,
        sourceType: clue.type,
        evidenceValue: 25 + clue.tier * 10,
        rumorValue: clue.type === "pop" ? 32 : 18,
        tier: clue.tier,
        topicKey: tk,
      });
    }
    const toolN = Math.max(1, Math.min(3, Math.floor(state.pendingClues.length / 2)));
    for (let i = 0; i < toolN; i++) {
      state.toolCards.push({
        id: newCardId(),
        kind: "tool",
        name: rand(TOOL_NAME_POOL),
        durability: 2,
        bonus: 8 + randomInt(0, 6),
      });
    }
  }

  function getInventoryByTab(tab) {
    if (tab === "phenomenon") return state.phenomenonCards;
    if (tab === "intel") return state.intelCards;
    if (tab === "cognition") return state.cognitionCards;
    if (tab === "tipoff") return state.tipOffCards;
    if (tab === "staff") return state.synthStaffCards || [];
    if (tab === "therapy") return state.therapyCards || [];
    return state.toolCards;
  }

  function getCardById(id) {
    if (!id) return null;
    const all = [
      ...state.phenomenonCards,
      ...state.intelCards,
      ...state.cognitionCards,
      ...state.toolCards,
      ...state.tipOffCards,
      ...(state.synthStaffCards || []),
      ...(state.therapyCards || []),
    ];
    return all.find((c) => c.id === id) || null;
  }

  const SYNTH_KIND_ZH = {
    phenomenon: "现象",
    intel: "情报",
    cognition: "认知",
    tool: "工具",
    tipoff: "爆料卡",
    staff: "人物",
    therapy: "干预",
  };

  function ensureStaffInternalDefaults() {
    for (const s of STAFF) {
      if (!state.staffInternal[s.id]) {
        state.staffInternal[s.id] = { san: 100, nextInternalOkSession: 0 };
      }
    }
  }

  /** 恐怖/违反常理：玄学域或现象神秘偏高 */
  function phenomenonIsDisturbing(phen) {
    if (!phen) return false;
    if (phen.domain === "occult") return true;
    return (phen.mysteryBias || 0) >= 52;
  }

  function staffInternalMeta(staffId) {
    ensureStaffInternalDefaults();
    return state.staffInternal[staffId];
  }

  function canStaffInternalThisSession(staffId) {
    const m = staffInternalMeta(staffId);
    return state.synthSessionId >= (m.nextInternalOkSession || 0);
  }

  /** 公开报道取向：仅 r2/r3/r4 用认知主导；r1 无 */
  function derivePublicStance(recipe, cards) {
    if (recipe === "r1") return null;
    const cogs = cards.filter((c) => c.kind === "cognition");
    if (!cogs.length) return null;
    const score = { sci: 0, occult: 0, pop: 0 };
    for (const c of cogs) {
      const k = c.sourceType === "occult" ? "occult" : c.sourceType === "pop" ? "pop" : "sci";
      score[k] += (c.level || 1) * 2 + 1;
    }
    if (score.sci >= score.occult && score.sci >= score.pop) return "sci";
    if (score.occult >= score.pop) return "occult";
    return "pop";
  }

  /** 结算时：公开取向矛盾惩罚（仅深度/专栏/爆料稿带 publicStance；快讯不计） */
  function stanceClashMultiplierForPlaced(placedPairs) {
    const lastForTopic = {};
    for (const { story } of placedPairs) {
      if (!story.fromExplore || !story.primaryTopicKey || !story.publicStance) continue;
      lastForTopic[story.primaryTopicKey] = story.publicStance;
    }
    let clashes = 0;
    for (const pk of Object.keys(lastForTopic)) {
      const next = lastForTopic[pk];
      const prev = state.lastPublicStanceByTopic[pk];
      if (prev && prev !== next) clashes += 1;
      state.lastPublicStanceByTopic[pk] = next;
    }
    if (!clashes) return 1;
    return Math.max(0.72, 1 - 0.09 * clashes);
  }

  /** 不写入状态，供组版预览 */
  function peekStanceClashDemandMult(placedPairs) {
    const lastForTopic = {};
    for (const { story } of placedPairs) {
      if (!story.fromExplore || !story.primaryTopicKey || !story.publicStance) continue;
      lastForTopic[story.primaryTopicKey] = story.publicStance;
    }
    let clashes = 0;
    for (const pk of Object.keys(lastForTopic)) {
      const next = lastForTopic[pk];
      const prev = state.lastPublicStanceByTopic[pk];
      if (prev && prev !== next) clashes += 1;
    }
    if (!clashes) return 1;
    return Math.max(0.72, 1 - 0.09 * clashes);
  }

  function synthSlotLayout(recipe) {
    const tool = { key: "tool", kind: "tool", required: false, label: "工具（可选）" };
    if (recipe === "internal") {
      return [
        { key: "phenomenon", kind: "phenomenon", required: true, label: "现象（内审素材）" },
        { key: "staff", kind: "staff", required: false, label: "主笔人物（可选·提高高等级认知）" },
        { key: "therapy", kind: "therapy", required: false, label: "心理干预（可选·解除主笔疲劳）" },
      ];
    }
    if (recipe === "r1") {
      return [
        { key: "phenomenon", kind: "phenomenon", required: true, label: "现象（必要）" },
        { key: "intel", kind: "intel", required: true, label: "情报（必要）" },
        tool,
      ];
    }
    if (recipe === "r2") {
      return [
        { key: "phenomenon", kind: "phenomenon", required: true, label: "现象（必要）" },
        { key: "cognition", kind: "cognition", required: true, label: "认知（必要）" },
        tool,
      ];
    }
    if (recipe === "r3") {
      return [
        { key: "cognition1", kind: "cognition", required: true, label: "认知 ①（必要）" },
        { key: "cognition2", kind: "cognition", required: true, label: "认知 ②（必要）" },
        tool,
      ];
    }
    return [
      { key: "phenomenon", kind: "phenomenon", required: true, label: "现象（必要）" },
      { key: "cognition", kind: "cognition", required: true, label: "认知（必要）" },
      { key: "tipoff", kind: "tipoff", required: true, label: "爆料卡（必要）" },
      tool,
    ];
  }

  function initSynthSlotsForRecipe(recipe) {
    const layout = synthSlotLayout(recipe);
    const o = {};
    layout.forEach((s) => {
      o[s.key] = null;
    });
    state.synthCraftSlots = o;
  }

  function clearCardFromAllCraftSlots(cardId) {
    if (!cardId || !state.synthCraftSlots) return;
    const slots = state.synthCraftSlots;
    Object.keys(slots).forEach((k) => {
      if (slots[k] === cardId) slots[k] = null;
    });
  }

  function assignCardToCraftSlot(slotKey, cardId) {
    const layout = synthSlotLayout(state.synthRecipe);
    const def = layout.find((s) => s.key === slotKey);
    if (!def) return false;
    const card = getCardById(cardId);
    if (!card || card.kind !== def.kind) return false;
    clearCardFromAllCraftSlots(cardId);
    state.synthCraftSlots[slotKey] = cardId;
    return true;
  }

  function selectedSynthCards() {
    const layout = synthSlotLayout(state.synthRecipe);
    const out = [];
    for (const s of layout) {
      const id = state.synthCraftSlots[s.key];
      if (!id) continue;
      const c = getCardById(id);
      if (c) out.push(c);
    }
    return out;
  }

  function recipeLabel(recipe) {
    if (recipe === "internal") return "编辑部内审定调（非公开 · 现象 → 认知）";
    if (recipe === "r1") return "抢先快讯（现象+情报 + 可选工具）";
    if (recipe === "r2") return "深度报道（现象+认知 + 可选工具）";
    if (recipe === "r3") return "个人专栏（双认知 + 可选工具）";
    return "爆炸性新闻（现象+认知+爆料卡 + 可选工具 · 高赌注）";
  }

  function validateRecipe(recipe, cards) {
    const nPhen = cards.filter((c) => c.kind === "phenomenon").length;
    const nIntel = cards.filter((c) => c.kind === "intel").length;
    const nCog = cards.filter((c) => c.kind === "cognition").length;
    const nTip = cards.filter((c) => c.kind === "tipoff").length;
    if (recipe === "internal") return nPhen >= 1;
    if (recipe === "r1") return nPhen >= 1 && nIntel >= 1;
    if (recipe === "r2") return nPhen >= 1 && nCog >= 1;
    if (recipe === "r3") return nCog >= 2;
    if (recipe === "r4") return nPhen >= 1 && nCog >= 1 && nTip >= 1;
    return false;
  }

  function recipeBaseSuccess(recipe) {
    if (recipe === "internal") return 1;
    if (recipe === "r1") return 0.85;
    if (recipe === "r2") return 0.75;
    if (recipe === "r3") return 0.65;
    return 0.52;
  }

  function buildSynthPreview(recipe, cards) {
    if (recipe === "internal") {
      if (!cards.length) return "内审定调：请将 1 张现象牌拖入蓝色槽；可选拖入主笔人物、心理干预包。认知仅由内审生成，不直接上版。";
      const names = cards.map((c) => c.name).join(" + ");
      const ok = validateRecipe(recipe, cards);
      const phen = cards.find((c) => c.kind === "phenomenon");
      const st = cards.find((c) => c.kind === "staff");
      const disturbing = phenomenonIsDisturbing(phen);
      const staffLine = st
        ? canStaffInternalThisSession(st.staffId)
          ? `主笔 ${st.name}：SAN ${staffInternalMeta(st.staffId).san}，可执行内审。`
          : `主笔 ${st.name}：本阶段尚在休整，需下一合成阶段或心理干预后再试。`
        : "无主笔：低等级认知概率高，高等级概率很低；异常题材尝试仍可能波动编辑部狂性。";
      const odds = st
        ? "（有主笔）失败约 12%；成功时 Lv.4+ 约 12%。"
        : "（无主笔）失败约 8%；成功时多为 Lv.1–2，Lv.3+ 很低。";
      const occ = disturbing ? "\n本现象偏异常：每次尝试可能伤主笔 SAN；成功则宏观「狂性」上升。" : "";
      return `${recipeLabel(recipe)}\n槽内：${names}\n${ok ? `可执行内审判定。${odds}\n${staffLine}${occ}` : "至少需要 1 张现象牌。"}`;
    }
    if (!cards.length) return "尚未放入素材。请将左侧卡牌拖入右侧红色必要槽；虚线槽为可选工具位。爆炸性新闻需另拖入「爆料卡」（仅特殊途径获得，不可合成）。";
    const names = cards.map((c) => c.name).join(" + ");
    const valid = validateRecipe(recipe, cards);
    const toolBonus = cards.filter((c) => c.kind === "tool").reduce((a, b) => a + b.bonus, 0);
    const successRate = clamp(recipeBaseSuccess(recipe) + toolBonus / 100 - Math.max(0, cards.length - 3) * 0.05, 0.15, 0.95);
    const substanceForTopic = cards.filter((c) => c.kind !== "tipoff" && c.kind !== "tool");
    const phenCard = substanceForTopic.find((c) => c.kind === "phenomenon");
    const pk = phenCard?.topicKey || substanceForTopic.find((c) => c.topicKey)?.topicKey;
    const prevN = pk ? state.topicSynthOrder[pk] || 0 : 0;
    const nextOrd = prevN + 1;
    let topicLine = "\n公开合成：现象、认知牌不消耗；情报为材料会消耗；爆料与工具按规则消耗。";
    if (pk && prevN > 0) {
      topicLine += `\n该题材本周已公开合成 ${prevN} 篇；若本次成功，本条为第 ${nextOrd} 篇，上版时报纸结算基础值将按同题疲劳折算（先发抢先再发深度总加成低于单发深度）`;
    } else if (pk) {
      topicLine += `\n该题材本周首次公开合成，上版按满额基础值计入（仍受版面其它乘数影响）。`;
    }
    return `${recipeLabel(recipe)}\n素材：${names}\n预计成功率：${(successRate * 100).toFixed(1)}%\n${valid ? "配方合法，可执行合成。" : "配方不合法，请调整素材组合。"}\n当前失实风险：${state.synthPollution}${topicLine}`;
  }

  function consumeCards(ids) {
    const remove = new Set(ids);
    state.phenomenonCards = state.phenomenonCards.filter((c) => !remove.has(c.id));
    state.intelCards = state.intelCards.filter((c) => !remove.has(c.id));
    state.cognitionCards = state.cognitionCards.filter((c) => !remove.has(c.id));
    state.toolCards = state.toolCards
      .map((t) => (remove.has(t.id) ? { ...t, durability: t.durability - 1 } : t))
      .filter((t) => t.durability > 0);
    state.tipOffCards = state.tipOffCards.filter((c) => !remove.has(c.id));
  }

  /** 公开报道合成：只消耗情报、爆料、工具；现象与认知保留 */
  function consumePublicSynthMaterials(cards) {
    const ids = [];
    for (const c of cards) {
      if (c.kind === "intel" || c.kind === "tipoff") ids.push(c.id);
      if (c.kind === "tool") ids.push(c.id);
    }
    consumeCards(ids);
  }

  const TOPIC_REPEAT_BASE_MULT = 0.72;
  const TOPIC_DEEP_NOT_FIRST_MULT = 0.9;

  function shortTopicLabel(topicKey) {
    if (!topicKey) return "";
    return topicKey.startsWith("topic_") ? `#${topicKey.slice(6)}` : topicKey;
  }

  /** 报刊结算用：同题材第 2 篇起打折，深度/专栏/爆炸再叠乘 */
  function effectiveStoryBase(story) {
    if (!story) return 0;
    const intrinsic = story.intrinsicBaseValue != null ? story.intrinsicBaseValue : story.baseValue;
    if (!story.fromExplore || !story.primaryTopicKey) return intrinsic;
    const order = story.synthTopicOrder || 0;
    if (order <= 0) return intrinsic;
    let m = 1;
    if (order >= 2) m *= TOPIC_REPEAT_BASE_MULT;
    if (order >= 2 && (story.recipeType === "r2" || story.recipeType === "r3" || story.recipeType === "r4")) m *= TOPIC_DEEP_NOT_FIRST_MULT;
    return Math.max(1, Math.round(intrinsic * m));
  }

  function synthToStory(recipe, cards) {
    const substance = cards.filter((c) => c.kind !== "tipoff");
    const hasTipoff = cards.some((c) => c.kind === "tipoff");
    const hasSci = substance.some((c) => c.sourceType === "sci" || c.domain === "sci");
    const hasOccult = substance.some((c) => c.sourceType === "occult" || c.domain === "occult");
    const hasPop = substance.some((c) => c.sourceType === "pop" || c.domain === "pop");
    const tags = [];
    if (hasSci) tags.push("Politics");
    if (hasOccult) tags.push("Gossip");
    if (hasPop || !tags.length) tags.push("Shopping");
    if (tags.length === 1 && Math.random() < 0.5) tags.push(rand(TAGS.filter((t) => t !== tags[0])));
    const evidence = substance.reduce((a, c) => a + (c.evidenceValue || 0), 0);
    const mystery = substance.reduce((a, c) => a + (c.mysteryBias || c.mysteryBonus || 0), 0);
    const cognitionLv = substance.reduce((a, c) => a + (c.level || 0), 0);
    let sensational = recipe === "r3" ? 72 : recipe === "r4" ? 88 : recipe === "r1" ? 64 : 58;
    if (hasTipoff) sensational += 14;
    const credibility = clamp(evidence * 0.65 + cognitionLv * 4 - (recipe === "r4" ? 45 : recipe === "r3" ? 22 : 0), 8, 95);
    const mysteryScore = clamp(mystery * 0.7 + (recipe === "r3" ? 20 : 0), 10, 95);
    const gaze = clamp((recipe === "r4" ? 26 : 12) + Math.round(mysteryScore * 0.25) + Math.round(cognitionLv * 0.8), 6, 90);
    const qualityScore = sensational + credibility + mysteryScore + gaze;
    const q = qualityFromScore(qualityScore);
    const negatives = [];
    if (recipe === "r3" && Math.random() < 0.45) negatives.push("thin_source");
    if (recipe === "r4") {
      if (Math.random() < 0.8) negatives.push("fabrication");
      if (Math.random() < 0.4) negatives.push("bias_overreach");
    }
    if (credibility < 40 && Math.random() < 0.35) negatives.push("sloppy_writing");
    const titlePrefix =
      recipe === "r2" ? "深度报道" : recipe === "r3" ? "个人专栏" : recipe === "r4" ? "爆炸性新闻" : "抢先快讯";
    const titleSeed = substance[0] || cards[0];
    const title = `${titlePrefix}：${titleSeed?.name?.replace("样本", "").replace("相关情报", "") || buildNewsTitle(tags)}`;
    const substanceForTopic = cards.filter((c) => c.kind !== "tipoff" && c.kind !== "tool");
    const topicKeys = [...new Set(substanceForTopic.map((c) => c.topicKey).filter(Boolean))];
    const phenCard = substanceForTopic.find((c) => c.kind === "phenomenon");
    const primaryTopicKey = phenCard?.topicKey || substanceForTopic.find((c) => c.topicKey)?.topicKey || null;
    const publicStance = derivePublicStance(recipe, cards);
    return {
      id: state.nextStoryId++,
      title,
      tags,
      quality: q.key,
      baseValue: q.value,
      intrinsicBaseValue: q.value,
      primaryTopicKey,
      topicKeys,
      synthTopicOrder: null,
      negatives,
      fromExplore: true,
      attrs: { sensational, credibility, mystery: mysteryScore, gaze },
      recipeType: recipe,
      publicStance,
    };
  }

  function isCardPlacedInSynth(id) {
    if (!id) return false;
    return Object.values(state.synthCraftSlots || {}).some((v) => v === id);
  }

  function renderSynthInventory() {
    const list = getInventoryByTab(state.synthTab);
    if (!el.synInventory) return;
    if (!list.length) {
      el.synInventory.innerHTML = `<div class="syn-help">当前分类暂无卡牌。</div>`;
      return;
    }
    el.synInventory.innerHTML = list
      .map((c) => {
        const placed = isCardPlacedInSynth(c.id);
        const topicChip =
          c.topicKey && (c.kind === "phenomenon" || c.kind === "intel" || c.kind === "cognition")
            ? `<span class="syn-badge">题材${shortTopicLabel(c.topicKey)}</span>`
            : "";
        const badge =
          c.kind === "tool"
            ? `<span class="syn-badge">耐久 ${c.durability}</span><span class="syn-badge">加成 +${c.bonus}%</span>`
            : c.kind === "cognition"
              ? `<span class="syn-badge">等级 ${c.level}</span>`
              : c.kind === "tipoff"
                ? `<span class="syn-badge">特殊</span><span class="syn-badge">不可合成</span>`
                : c.kind === "staff"
                  ? `<span class="syn-badge">SAN ${staffInternalMeta(c.staffId).san}</span>${
                      canStaffInternalThisSession(c.staffId)
                        ? `<span class="syn-badge">可内审</span>`
                        : `<span class="syn-badge" style="border-color:#f87171;color:#fecaca">休整中</span>`
                    }`
                  : c.kind === "therapy"
                    ? `<span class="syn-badge">解除疲劳</span>`
                    : `<span class="syn-badge">证据 ${c.evidenceValue || 0}</span>`;
        return `<div class="syn-item syn-item-draggable${placed ? " syn-item-slotted" : ""}" draggable="true" data-card="${c.id}" data-kind="${c.kind}" title="拖到右侧卡槽">
          <strong>${escapeHtml(c.name)}</strong>
          <div class="syn-badges"><span class="syn-badge">${c.kind}</span>${topicChip}${badge}</div>
          ${placed ? `<div class="syn-slotted-hint">已在槽位</div>` : ""}
        </div>`;
      })
      .join("");
    el.synInventory.querySelectorAll(".syn-item-draggable").forEach((node) => {
      node.addEventListener("dragstart", (ev) => {
        const id = node.getAttribute("data-card");
        ev.dataTransfer.setData("text/plain", id);
        ev.dataTransfer.effectAllowed = "move";
      });
    });
  }

  function synthSlotInnerHtml(slotKey, cardId, kind) {
    if (!cardId) {
      return `<span class="syn-slot-placeholder">拖入${SYNTH_KIND_ZH[kind] || ""}</span>`;
    }
    const c = getCardById(cardId);
    if (!c) return `<span class="syn-slot-placeholder">空</span>`;
    return `<div class="syn-slot-filled">
      <span class="syn-slot-chip-title">${escapeHtml(c.name)}</span>
      <button type="button" class="syn-slot-clear" data-clear-slot="${slotKey}" title="移出卡槽">×</button>
    </div>`;
  }

  function bindSynthWorkbenchDrag() {
    const root = el.synWorkbench;
    if (!root) return;
    root.querySelectorAll(".syn-drop-slot").forEach((zone) => {
      zone.addEventListener("dragover", (ev) => {
        ev.preventDefault();
        ev.dataTransfer.dropEffect = "move";
      });
      zone.addEventListener("drop", (ev) => {
        ev.preventDefault();
        const id = ev.dataTransfer.getData("text/plain");
        if (!id) return;
        const key = zone.getAttribute("data-slot-key");
        if (!key) return;
        if (assignCardToCraftSlot(key, id)) renderSynthesis();
        else log(`类型不符：此槽需要「${SYNTH_KIND_ZH[zone.getAttribute("data-accept")] || ""}」牌。`);
      });
    });
    root.querySelectorAll("[data-clear-slot]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const key = btn.getAttribute("data-clear-slot");
        if (key && state.synthCraftSlots) state.synthCraftSlots[key] = null;
        renderSynthesis();
      });
    });
  }

  function renderSynthWorkbench() {
    if (!el.synWorkbench) return;
    const layout = synthSlotLayout(state.synthRecipe);
    const archCls = state.synthRecipe === "internal" ? "syn-slots-arch syn-slots-internal-mode" : "syn-slots-arch";
    const cells = layout
      .map((s) => {
        const id = state.synthCraftSlots[s.key];
        const cls =
          state.synthRecipe === "internal"
            ? s.required
              ? "syn-slot-cell syn-slot-internal"
              : "syn-slot-cell syn-slot-internal syn-slot-optional"
            : s.required
              ? "syn-slot-cell syn-slot-required"
              : "syn-slot-cell syn-slot-optional";
        const inner = synthSlotInnerHtml(s.key, id, s.kind);
        return `<div class="${cls}">
          <div class="syn-slot-label">${escapeHtml(s.label)}</div>
          <div class="syn-drop-slot${id ? " syn-drop-has-card" : ""}" data-slot-key="${s.key}" data-accept="${s.kind}">${inner}</div>
        </div>`;
      })
      .join("");
    el.synWorkbench.innerHTML = `<div class="${archCls}">${cells}</div>`;
    bindSynthWorkbenchDrag();
  }

  function renderSynthReports() {
    if (!el.synReports) return;
    if (!state.craftedReports.length) {
      el.synReports.innerHTML = `<div class="syn-help">尚未合成报道。至少制作 1 篇后可进入组版。</div>`;
      return;
    }
    el.synReports.innerHTML = state.craftedReports
      .map((r) => {
        const pk = r.primaryTopicKey;
        const ord = r.synthTopicOrder;
        const topicLine =
          pk && ord
            ? `<span class="syn-badge">题材${shortTopicLabel(pk)}</span><span class="syn-badge">本周公开第${ord}篇</span>`
            : pk
              ? `<span class="syn-badge">题材${shortTopicLabel(pk)}</span>`
              : "";
        const eff = effectiveStoryBase(r);
        const intr = r.intrinsicBaseValue != null ? r.intrinsicBaseValue : r.baseValue;
        const effLine = intr !== eff ? `<span class="syn-badge">上版有效基础 ${eff}</span>` : `<span class="syn-badge">基础 ${intr}</span>`;
        return `<div class="syn-report">
        <strong>${escapeHtml(r.title)}</strong>
        <div class="syn-badges" style="margin-top:4px;">
          ${topicLine}
          <span class="syn-badge">类型 ${r.recipeType}</span>
          <span class="syn-badge">质量 ${r.quality}</span>
          ${effLine}
          <span class="syn-badge">轰动 ${r.attrs.sensational}</span>
          <span class="syn-badge">可信 ${r.attrs.credibility}</span>
          <span class="syn-badge">神秘 ${r.attrs.mystery}</span>
          <span class="syn-badge">诡视 ${r.attrs.gaze}</span>
        </div>
      </div>`;
      })
      .join("");
  }

  function renderSynthesis() {
    renderSynthInventory();
    renderSynthWorkbench();
    const cards = selectedSynthCards();
    if (el.synSynthPreview) el.synSynthPreview.textContent = buildSynthPreview(state.synthRecipe, cards);
    if (el.synthesisHint) {
      if (state.synthRecipe === "internal") {
        el.synthesisHint.textContent =
          "内审独立于报道合成：现象→认知；可选主笔（提高高等级概率、承担 SAN）。心理干预可解除主笔本阶段疲劳。异常题材成功会增加宏观「狂性」。抢先快讯不计公开取向，深度/专栏/爆料若与既往同题取向矛盾，上版时需求受罚。";
      } else {
        el.synthesisHint.textContent = `配方说明：${recipeLabel(state.synthRecipe)}。现象与认知可反复用于公开报道；情报为材料每次合成会消耗。爆料与工具按原规则。同题材本周多篇公开稿上版时报纸结算基础值递减。`;
      }
    }
    const craftBtn = document.getElementById("craftBtn");
    if (craftBtn) {
      craftBtn.disabled = !validateRecipe(state.synthRecipe, cards);
      craftBtn.textContent = state.synthRecipe === "internal" ? "生成认知" : "执行合成";
    }
    ["recipe1", "recipe2", "recipe3", "recipe4"].forEach((bid, i) => {
      const b = document.getElementById(bid);
      if (b) b.classList.toggle("primary", state.synthRecipe === ["r1", "r2", "r3", "r4"][i]);
    });
    const ri = document.getElementById("recipeInternal");
    if (ri) ri.classList.toggle("primary", state.synthRecipe === "internal");
    renderSynthReports();
  }

  function craftReport() {
    const cards = selectedSynthCards();
    const recipe = state.synthRecipe;
    if (recipe === "internal") {
      const phen = cards.find((c) => c.kind === "phenomenon");
      const staffCard = cards.find((c) => c.kind === "staff");
      const therapyCard = cards.find((c) => c.kind === "therapy");
      if (!phen || !validateRecipe(recipe, cards)) {
        log("内审失败：请将 1 张现象牌拖入蓝色卡槽。");
        renderSynthesis();
        return;
      }
      if (therapyCard) {
        if (staffCard) {
          staffInternalMeta(staffCard.staffId).nextInternalOkSession = 0;
        } else {
          for (const s of STAFF) staffInternalMeta(s.id).nextInternalOkSession = 0;
        }
        state.therapyCards = (state.therapyCards || []).filter((c) => c.id !== therapyCard.id);
        if (state.synthCraftSlots) state.synthCraftSlots.therapy = null;
        log("心理干预已使用：解除主笔内审疲劳（本合成阶段可再试）。");
      }
      if (staffCard && !canStaffInternalThisSession(staffCard.staffId)) {
        log("该主笔尚在休整，本阶段无法再次内审（请用心理干预或待下一周合成阶段）。");
        renderSynthesis();
        return;
      }
      const disturbing = phenomenonIsDisturbing(phen);
      if (staffCard && disturbing && Math.random() < 0.3) {
        const m = staffInternalMeta(staffCard.staffId);
        m.san = clamp(m.san - randomInt(2, 6), 0, 100);
        log(`接触异常题材尝试：${staffCard.name.replace("（主笔）", "")} SAN 波动（剩余 ${m.san}）。`);
      }
      const hasStaff = !!staffCard;
      const failP = hasStaff ? 0.12 : 0.08;
      if (Math.random() < failP) {
        if (staffCard) {
          const m = staffInternalMeta(staffCard.staffId);
          m.nextInternalOkSession = state.synthSessionId + 1;
          if (disturbing && Math.random() < 0.42) m.san = clamp(m.san - randomInt(3, 9), 0, 100);
          else if (Math.random() < 0.28) m.san = clamp(m.san - randomInt(1, 5), 0, 100);
        }
        log(`内审判定失败（成功率 ${((1 - failP) * 100).toFixed(0)}%）。${hasStaff ? "主笔需休整至下一合成阶段方可再内审。" : ""}`);
        renderMacro();
        renderSynthesis();
        return;
      }
      let level = 1;
      if (hasStaff) {
        const t = Math.random();
        if (t < 0.22) level = 2;
        else if (t < 0.58) level = 3;
        else if (t < 0.88) level = 4;
        else level = 5;
      } else {
        const t = Math.random();
        if (t < 0.7) level = 1;
        else if (t < 0.95) level = 2;
        else level = 3;
      }
      level = clamp(level + Math.floor((phen.tier || 1) / 3), 1, 8);
      if (disturbing) {
        macro.狂性 = Math.min(100, macro.狂性 + randomInt(1, 4));
        log("异常题材认知成立：编辑部宏观「狂性」上升。");
      }
      const newCog = {
        id: newCardId(),
        kind: "cognition",
        name: rand(COGNITION_NAME_POOL),
        level,
        sourceType: phen.domain || "sci",
        credibilityBonus: phen.evidenceValue > 60 ? 16 : 10,
        mysteryBonus: phen.mysteryBias > 55 ? 16 : 8,
        topicKey: phen.topicKey || null,
      };
      state.cognitionCards.push(newCog);
      log(`内审定调完成：获得认知牌「${newCog.name}」（Lv.${newCog.level}），现象牌仍保留。`);
      initSynthSlotsForRecipe("internal");
      renderMacro();
      renderSynthesis();
      return;
    }
    if (!validateRecipe(recipe, cards)) {
      log("合成失败：素材不满足当前配方。");
      renderSynthesis();
      return;
    }
    const toolBonus = cards.filter((c) => c.kind === "tool").reduce((a, b) => a + b.bonus, 0);
    const successRate = clamp(recipeBaseSuccess(recipe) + toolBonus / 100 - Math.max(0, cards.length - 3) * 0.05, 0.15, 0.95);
    if (Math.random() > successRate) {
      consumePublicSynthMaterials(cards);
      initSynthSlotsForRecipe(recipe);
      state.synthPollution += recipe === "r4" ? 5 : recipe === "r3" ? 2 : 0;
      log(`合成失败：${recipeLabel(recipe)}（成功率 ${(successRate * 100).toFixed(1)}%）。`);
      renderSynthesis();
      return;
    }
    const story = synthToStory(recipe, cards);
    if (story.primaryTopicKey) {
      state.topicSynthOrder[story.primaryTopicKey] = (state.topicSynthOrder[story.primaryTopicKey] || 0) + 1;
      story.synthTopicOrder = state.topicSynthOrder[story.primaryTopicKey];
    } else {
      story.synthTopicOrder = null;
    }
    state.craftedReports.push(story);
    consumePublicSynthMaterials(cards);
    initSynthSlotsForRecipe(recipe);
    if (recipe === "r3") state.synthPollution += 4;
    if (recipe === "r4") state.synthPollution += 10;
    log(`合成成功：${story.title}（${story.quality}）。`);
    renderSynthesis();
  }

  function enterSynthesisPhase() {
    state.phase = "synthesis";
    state.pendingClues = state.clues.slice();
    state.clues = [];
    initSynthesisFromClues();
    state.synthSessionId = (state.synthSessionId || 0) + 1;
    document.getElementById("phase-explore").classList.add("hidden");
    document.getElementById("phase-synthesis").classList.remove("hidden");
    document.getElementById("phase-editorial").classList.add("hidden");
    document.getElementById("phase-summary").classList.add("hidden");
    document.getElementById("synthesisSub").textContent = `第 ${state.week} 周 · 已带入探索线索 ${state.pendingClues.length} 条。请将素材拖入卡槽合成报道，再进入组版。`;
    el.synInventory = document.getElementById("synInventory");
    el.synWorkbench = document.getElementById("synWorkbench");
    el.synSynthPreview = document.getElementById("synSynthPreview");
    el.synReports = document.getElementById("synReports");
    el.synthesisHint = document.getElementById("synthesisHint");
    renderSynthesis();
    log("进入故事合成台：现象/认知/情报可合成报道。");
    if (week1TutorialActive() && !state.tutorialSoftW1.w1_synthesis) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          void runWeek1SynthesisOnboarding();
        });
      });
    }
  }

  function toZhTag(tag) {
    const map = { Politics: "时政", Military: "军事", Economy: "经济", Sport: "体育", Gossip: "花边新闻", Pets: "猫狗", Humor: "幽默", Shopping: "购物" };
    return map[tag] || tag;
  }

  function buildNewsTitle(tags) {
    const mainTag = tags[0];
    const secondTag = tags[1];
    const location = rand(LOCATIONS);
    const org = rand(ORGS);
    const subject = rand(SUBJECTS[mainTag] || ["焦点事件"]);
    const action = rand(ACTIONS);
    if (secondTag) return `${location}${org}就${subject}${action}，${toZhTag(secondTag)}线索同步浮现`;
    return `${location}${org}${subject}${action}`;
  }

  function buildStory(id) {
    const tag1 = rand(TAGS);
    const tag2 = Math.random() < 0.55 ? rand(TAGS.filter((t) => t !== tag1)) : null;
    const quality = rand(QUALITY);
    const negativeCount = Math.random() < 0.28 ? randomInt(1, 2) : 0;
    const negatives = [];
    for (let i = 0; i < negativeCount; i++) negatives.push(rand(NEGATIVE_TYPES));
    return {
      id,
      title: buildNewsTitle(tag2 ? [tag1, tag2] : [tag1]),
      tags: tag2 ? [tag1, tag2] : [tag1],
      quality: quality.key,
      baseValue: quality.value,
      negatives,
      fromExplore: false,
    };
  }

  function clueToStory(clue, id) {
    const main = TYPE_TO_TAG[clue.type] || "Politics";
    const second = Math.random() < 0.45 ? rand(TAGS.filter((t) => t !== main)) : null;
    const tier = clue.tier || 2;
    const q = tier >= 3 ? QUALITY[2] : tier >= 2 ? QUALITY[1] : QUALITY[0];
    const negN = tier === 1 ? (Math.random() < 0.35 ? randomInt(1, 2) : 0) : Math.random() < 0.12 ? 1 : 0;
    const negatives = [];
    for (let i = 0; i < negN; i++) negatives.push(rand(NEGATIVE_TYPES));
    return {
      id,
      title: clue.title,
      tags: second ? [main, second] : [main],
      quality: q.key,
      baseValue: q.value,
      negatives,
      fromExplore: true,
    };
  }

  function buildEditorialPool() {
    const craftedBase = (state.pendingReports && state.pendingReports.length) ? state.pendingReports : [];
    const target = Math.max(10, craftedBase.length || state.pendingClues.length);
    let cur = state.nextStoryId;
    const exploreStories = craftedBase.length
      ? craftedBase.map((r) => ({ ...r, id: cur++ }))
      : state.pendingClues.map((c) => clueToStory(c, cur++));
    const filler = [];
    while (exploreStories.length + filler.length < target) filler.push(buildStory(cur++));
    state.nextStoryId = cur;
    state.stories = [...exploreStories, ...filler];
    for (const s of slots) state.placed[s.id] = null;
  }

  function enterEditorialPhase() {
    state.phase = "editorial";
    buildEditorialPool();
    document.getElementById("phase-synthesis").classList.add("hidden");
    document.getElementById("phase-explore").classList.add("hidden");
    document.getElementById("phase-editorial").classList.remove("hidden");
    document.getElementById("phase-summary").classList.add("hidden");
    document.getElementById("editorialSub").textContent = `第 ${state.week} 周 · 已导入合成报道 ${state.pendingReports.length || state.pendingClues.length} 条，请组版后结算。`;
    el.storyList = document.getElementById("storyList");
    el.slotList = document.getElementById("slotList");
    el.liveStats = document.getElementById("liveStats");
    el.resultBox = document.getElementById("resultBox");
    el.toast = document.getElementById("toast");
    renderStories();
    renderSlots();
    renderLiveStats();
    el.resultBox.innerHTML = `<div class="k">尚未结算</div><div class="nm-tip">拖拽报道到版位，再点「结算本期」。</div>`;
    log("进入编辑部：把本周稿件拖入版位，准备结算本期。");
    if (week1TutorialActive() && !state.paperLabMode) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          void runWeek1EditorialOnboarding();
        });
      });
    }
  }

  function getAllPlaced() {
    return slots.map((s) => ({ slot: s, story: state.placed[s.id] })).filter((x) => x.story);
  }

  function calculate(isSettle) {
    const placed = getAllPlaced();
    const emptySlots = slots.length - placed.length;
    let sumIntrinsicBase = 0;
    const totalBaseValue = placed.reduce((acc, x) => {
      const s = x.story;
      sumIntrinsicBase += s.intrinsicBaseValue != null ? s.intrinsicBaseValue : s.baseValue;
      return acc + effectiveStoryBase(s);
    }, 0);
    const topicFatigueLoss = Math.max(0, Math.round(sumIntrinsicBase - totalBaseValue));
    const allTags = placed.flatMap((x) => x.story.tags);
    const uniqueTags = new Set(allTags).size;
    const negPenaltyPoints = placed.reduce((acc, x) => acc + x.story.negatives.length, 0);
    const tagCountMap = {};
    for (const t of allTags) tagCountMap[t] = (tagCountMap[t] || 0) + 1;
    const comboRaw = Object.values(tagCountMap).reduce((acc, n) => acc + Math.pow(Math.max(0, n - 1), 0.8), 0);
    const linkedTags = Object.entries(tagCountMap)
      .filter(([, count]) => count >= 2 && count <= 3)
      .map(([tag]) => tag);
    const linkCount = linkedTags.length;
    const publicCount = allTags.filter((t) => PUBLIC_AFFAIRS.has(t)).length;
    const massCount = allTags.filter((t) => MASS_APPEAL.has(t)).length;
    const lightCount = allTags.filter((t) => LIFESTYLE_LIGHT.has(t)).length;
    const totalTagCount = allTags.length || 1;
    const publicRatio = publicCount / totalTagCount;
    const massRatio = massCount / totalTagCount;
    const lightRatio = lightCount / totalTagCount;
    const dominantRatio = Math.max(publicRatio, massRatio, lightRatio);
    const profileNormalized = (state.editorialProfile + 100) / 200;
    const frontWeight = placed.reduce((acc, x) => acc + x.slot.weight, 0) / 2.95;
    const mQuality = Math.min(1.85, 1 + 0.0008 * totalBaseValue);
    const comboBase = Math.min(1.35, 1 + 0.06 * Math.log(1 + comboRaw));
    const comboProfileBoost = 1 + 0.2 * Math.max(0, profileNormalized - 0.5);
    const mCombo = Math.min(1.45, comboBase * comboProfileBoost);
    const mDiversityBase = Math.min(1.3, 1 + 0.05 * Math.log(1 + uniqueTags));
    const diversityStyleBoost = 1 + 0.25 * Math.max(0, 0.5 - profileNormalized) * publicRatio;
    const mDiversity = Math.min(1.45, mDiversityBase * diversityStyleBoost);
    const mLayout = 1 + 1.2 * frontWeight;
    const mEmpty = Math.max(0.7, 1 - 0.06 * emptySlots);
    const mPenalty = Math.max(0.6, 1 - 0.025 * negPenaltyPoints);
    const mLink = Math.min(1.25, 1 + 0.05 * linkCount);
    let mBias = 1;
    if (dominantRatio > 0.7) {
      const overflow = (dominantRatio - 0.7) / 0.3;
      mBias = Math.max(0.75, 1 - 0.25 * overflow);
    }
    const mBalance = publicRatio >= 0.25 && publicRatio <= 0.55 && lightRatio >= 0.2 && lightRatio <= 0.5 ? 1.06 : 1;
    const mStanceClash = isSettle ? stanceClashMultiplierForPlaced(placed) : 1;
    const demand =
      state.baseDemand * mQuality * mCombo * mDiversity * mLayout * mEmpty * mPenalty * mLink * mBalance * mBias * mStanceClash;
    const sold = Math.min(Math.round(demand), state.printCapacity);
    const stockoutRate = demand <= 0 ? 0 : Math.max(0, (demand - sold) / demand);
    const circulationRevenue = sold * state.coverPrice;
    const newSubRate = 0.004 + 0.0008 * uniqueTags + 0.0006 * Math.sqrt(Math.max(1, totalBaseValue / 150));
    const churnRate = 0.003 + 0.0012 * negPenaltyPoints + 0.002 * stockoutRate;
    const newSubs = sold * newSubRate;
    const lostSubs = state.subscribers * churnRate;
    const subDelta = Math.round(newSubs - lostSubs);
    const nextSubs = Math.max(0, state.subscribers + subDelta);
    const subscriptionRevenue = nextSubs * state.subUnitValue;
    const adProfileBonus = 1 + 0.15 * (1 - Math.abs(state.editorialProfile) / 100);
    const adMatch = Math.min(1, (state.adMatchBase + uniqueTags * 0.05 - negPenaltyPoints * 0.03) * adProfileBonus);
    const adUnit = 180 + 320 * adMatch;
    const adsRevenue = state.adSlots * adUnit;
    const paperPacks = Math.ceil(state.printCapacity / 1000);
    const paperCost = paperPacks * state.paperPackCost;
    const totalCost = paperCost + state.salaryCost + state.opsCost;
    const grossRevenue = circulationRevenue + subscriptionRevenue + adsRevenue;
    const profit = grossRevenue - totalCost;
    if (isSettle) state.subscribers = nextSubs;
    return {
      placedCount: placed.length,
      emptySlots,
      totalBaseValue,
      sumIntrinsicBase,
      topicFatigueLoss,
      uniqueTags,
      comboRaw,
      publicRatio,
      massRatio,
      lightRatio,
      dominantRatio,
      linkedTags,
      linkCount,
      negPenaltyPoints,
      multipliers: {
        mQuality,
        comboBase,
        comboProfileBoost,
        mCombo,
        mDiversityBase,
        diversityStyleBoost,
        mDiversity,
        mLayout,
        mEmpty,
        mPenalty,
        mLink,
        mBalance,
        mBias,
        mStanceClash,
      },
      demand,
      sold,
      stockoutRate,
      circulationRevenue,
      subscriptionRevenue,
      adsRevenue,
      grossRevenue,
      costs: { paperCost, salaryCost: state.salaryCost, opsCost: state.opsCost, totalCost },
      profit,
      nextSubs,
    };
  }

  function calculateWithPlacement(slotId, storyId) {
    const old = state.placed[slotId];
    const story = state.stories.find((s) => s.id === Number(storyId));
    state.placed[slotId] = story || null;
    const result = calculate(false);
    state.placed[slotId] = old;
    return result;
  }

  function analyzeTagEffects(placedStories) {
    const map = {};
    for (const st of placedStories) {
      for (const tag of st.tags) map[tag] = (map[tag] || 0) + 1;
    }
    const linked = Object.entries(map)
      .filter(([, count]) => count >= 2 && count <= 3)
      .map(([tag]) => tag);
    const tags = Object.entries(map).flatMap(([tag, count]) => Array.from({ length: count }, () => tag));
    const publicCount = tags.filter((t) => PUBLIC_AFFAIRS.has(t)).length;
    const massCount = tags.filter((t) => MASS_APPEAL.has(t)).length;
    const lightCount = tags.filter((t) => LIFESTYLE_LIGHT.has(t)).length;
    const total = tags.length || 1;
    const publicRatio = publicCount / total;
    const massRatio = massCount / total;
    const lightRatio = lightCount / total;
    const dominantRatio = Math.max(publicRatio, massRatio, lightRatio);
    let dominantType = "轻内容";
    if (dominantRatio === publicRatio) dominantType = "公共事务";
    else if (dominantRatio === massRatio) dominantType = "大众关注";
    return { linked, publicRatio, massRatio, lightRatio, dominantRatio, dominantType };
  }

  function placeStory(slotId, storyId) {
    const story = state.stories.find((s) => s.id === Number(storyId));
    state.placed[slotId] = story || null;
    renderSlots();
    renderLiveStats();
  }

  function renderStories() {
    el.storyList.innerHTML = "";
    for (const story of state.stories) {
      const card = document.createElement("div");
      card.className = "nm-story";
      card.draggable = true;
      card.dataset.storyId = String(story.id);
      const negatives = story.negatives.length
        ? `<span class="nm-chip" style="color:#fca5a5">负面:${story.negatives.join("/")}</span>`
        : `<span class="nm-chip">负面:无</span>`;
      const ex = story.fromExplore ? `<span class="nm-chip ex">探索稿</span>` : "";
      const effB = effectiveStoryBase(story);
      const intrB = story.intrinsicBaseValue != null ? story.intrinsicBaseValue : story.baseValue;
      const stanceChip =
        story.publicStance && story.fromExplore
          ? `<span class="nm-chip">公开取向:${story.publicStance === "sci" ? "科学纪实" : story.publicStance === "occult" ? "神秘玄学" : "世俗流量"}</span>`
          : "";
      const baseChip =
        story.fromExplore && story.primaryTopicKey
          ? `<span class="nm-chip">上版有效基础:${effB}${intrB !== effB ? `（稿内${intrB}）` : ""}</span><span class="nm-chip">题材${shortTopicLabel(story.primaryTopicKey)}</span>${
              story.synthTopicOrder ? `<span class="nm-chip">本周稿序${story.synthTopicOrder}</span>` : ""
            }${stanceChip}`
          : `<span class="nm-chip">基础值:${story.baseValue}</span>`;
      card.innerHTML = `
        <div class="nm-story-title">${escapeHtml(story.title)}</div>
        <div class="nm-chips">
          ${ex}
          <span class="nm-chip">标签:${story.tags.map(toZhTag).join(" / ")}</span>
          <span class="nm-chip">质量:${story.quality}</span>
          ${baseChip}
          ${negatives}
        </div>`;
      const tip = document.createElement("div");
      tip.className = "nm-tip";
      tip.textContent = "拖到中间版位";
      card.appendChild(tip);
      card.addEventListener("dragstart", (ev) => {
        state.draggingStoryId = story.id;
        ev.dataTransfer.setData("text/plain", String(story.id));
        card.classList.add("dragging");
      });
      card.addEventListener("dragend", () => {
        state.draggingStoryId = null;
        card.classList.remove("dragging");
        clearDropPreview();
      });
      el.storyList.appendChild(card);
    }
  }

  function clearDropPreview() {
    el.slotList.querySelectorAll(".nm-slot").forEach((node) => {
      node.classList.remove("drag-over", "good-preview", "bad-preview", "synergy");
    });
    el.slotList.querySelectorAll("[data-impact]").forEach((n) => {
      n.textContent = "拖入报道可预览该版位影响";
    });
  }

  function applySynergyHighlights(projectedLinkedTags) {
    const linkSet = new Set(projectedLinkedTags || []);
    el.slotList.querySelectorAll(".nm-slot").forEach((node) => {
      const slotId = node.dataset.slotId;
      const story = state.placed[slotId];
      if (!story) return;
      node.classList.toggle("synergy", story.tags.some((t) => linkSet.has(t)));
    });
  }

  function renderImpactRows(baseline, projected, extraText) {
    const core = [
      { name: "预计利润", delta: Math.round(projected.profit - baseline.profit), suffix: "" },
      { name: "预计销量", delta: projected.sold - baseline.sold, suffix: "份" },
      { name: "关键原因", delta: 0, text: extraText || "无明显变化" },
    ];
    const detail = [
      { name: "连携题材数", delta: projected.linkCount - baseline.linkCount, suffix: "" },
      { name: "多样性乘数", delta: projected.multipliers.mDiversity - baseline.multipliers.mDiversity, suffix: "x", fixed: 2 },
      { name: "偏科惩罚乘数", delta: projected.multipliers.mBias - baseline.multipliers.mBias, suffix: "x", fixed: 2 },
      { name: "负面惩罚点", delta: projected.negPenaltyPoints - baseline.negPenaltyPoints, suffix: "" },
    ];
    const renderRow = (d) => {
      if (d.text) return `<div class="nm-impact-row neu"><span class="name">${d.name}</span><span class="delta">${d.text}</span></div>`;
      const cls = d.delta > 0 ? "pos" : d.delta < 0 ? "neg" : "neu";
      const abs = d.fixed != null ? Math.abs(d.delta).toFixed(d.fixed) : Math.abs(d.delta);
      const prefix = d.delta > 0 ? "+" : d.delta < 0 ? "-" : "±";
      return `<div class="nm-impact-row ${cls}"><span class="name">${d.name}</span><span class="delta">${prefix}${abs}${d.suffix}</span></div>`;
    };
    return `<div class="nm-impact-list">${core.map(renderRow).join("")}</div>
      <details style="margin-top:6px;"><summary style="cursor:pointer;color:#94a3b8;font-size:12px;">详情</summary>
      <div class="nm-impact-list" style="margin-top:6px;">${detail.map(renderRow).join("")}</div></details>`;
  }

  function showReplaceToast(prevStory, newStory) {
    if (state.undoTimer) {
      clearTimeout(state.undoTimer);
      state.undoTimer = null;
    }
    el.toast.innerHTML = `<span>已替换：${escapeHtml(prevStory.title)} → ${escapeHtml(newStory.title)}</span>
      <button class="nm-sec" id="undoBtn">撤销</button>`;
    el.toast.className = "nm-toast show";
    document.getElementById("undoBtn").onclick = () => {
      if (!state.lastReplaceAction) return;
      state.placed[state.lastReplaceAction.slotId] = state.lastReplaceAction.prevStory;
      state.lastReplaceAction = null;
      el.toast.classList.remove("show");
      renderSlots();
      renderLiveStats();
    };
    state.undoTimer = setTimeout(() => {
      state.lastReplaceAction = null;
      el.toast.classList.remove("show");
      el.toast.classList.remove("warn");
    }, 2000);
  }

  function renderSlots() {
    el.slotList.innerHTML = "";
    const baseline = calculate(false);

    const layout = [
      { page: 1, kind: "main", slotId: "front-main", label: "头版" },
      { page: 1, kind: "subL", slotId: "front-side", label: "子版 A" },
      { page: 1, kind: "subR", slotId: "feature-1", label: "子版 B" },
      { page: 2, kind: "main", slotId: "feature-2", label: "次头版" },
      { page: 2, kind: "subL", slotId: "inner-1", label: "子版 C" },
      { page: 2, kind: "subR", slotId: "inner-2", label: "子版 D" },
    ];

    const attrsDots = (story) => {
      const tags = (story && story.tags) || [];
      const dots = [];
      for (let i = 0; i < Math.min(4, tags.length); i++) dots.push(`<span class="paper-attr t${(i % 4) + 1}" title="${escapeHtml(toZhTag(tags[i]))}"></span>`);
      if (story && story.negatives && story.negatives.length) dots.push(`<span class="paper-attr t1" title="负面词条"></span>`);
      return `<div class="paper-attrs">${dots.join("")}</div>`;
    };

    const bodyMask = () => `<div class="paper-body">
      <span>**** **** **** **** **** ****</span>
      <span>**** **** **** **** **** ****</span>
      <span>**** **** **** **** **** ****</span>
      <span>**** **** **** **** **** ****</span>
    </div>`;

    const renderSlotInner = (slot, isMain, labelText) => {
      const current = state.placed[slot.id];
      const mult = (1 + 2 * slot.weight).toFixed(1);
      if (!current) {
        const multHint = slot.id === "front-main"
          ? `<div class="paper-multi empty">头版奖励系数 x${mult}</div>`
          : `<div class="paper-multi">系数 x${mult}</div>`;
        return `
          <div class="paper-slot-header"><span>${escapeHtml(labelText)}</span>${multHint}</div>
          <div class="paper-empty">拖拽报道到此处</div>
        `;
      }
      const titleCls = isMain ? "" : "small";
      const removeBtn = `<button class="nm-sec" data-remove="${slot.id}" style="justify-self:end;">移除</button>`;
      return `
        <div class="paper-slot-header">
          <span>${escapeHtml(labelText)}</span>
          <span class="paper-multi">系数 x${mult}</span>
        </div>
        <div>
          <div class="paper-story-title ${titleCls}">${escapeHtml(current.title)}</div>
          ${attrsDots(current)}
        </div>
        <div class="paper-img" aria-label="报道图片占位"></div>
        ${bodyMask()}
        ${removeBtn}
      `;
    };

    const slotById = Object.fromEntries(slots.map((s) => [s.id, s]));
    const page = (num) => {
      const items = layout.filter((x) => x.page === num);
      const main = items.find((x) => x.kind === "main");
      const subL = items.find((x) => x.kind === "subL");
      const subR = items.find((x) => x.kind === "subR");
      const header = num === 1
        ? `<div class="paper-header"><div class="paper-name">DOG NEWS</div><div class="paper-meta"><span>1930年3月</span><span>第${state.week}周</span><span>第${num}页</span></div></div>`
        : `<div class="paper-header"><div class="paper-name" style="font-size:18px;letter-spacing:0.06em;">DOG NEWS</div><div class="paper-meta"><span>1930年3月</span><span>第${state.week}周</span><span>第${num}页</span></div></div>`;
      return `<section class="paper-page">
        ${header}
        <div class="paper-grid">
          <div class="paper-slot" data-slot="${main.slotId}">${renderSlotInner(slotById[main.slotId], true, main.label)}</div>
          <div class="paper-row2">
            <div class="paper-slot" data-slot="${subL.slotId}">${renderSlotInner(slotById[subL.slotId], false, subL.label)}</div>
            <div class="paper-slot" data-slot="${subR.slotId}">${renderSlotInner(slotById[subR.slotId], false, subR.label)}</div>
          </div>
        </div>
      </section>`;
    };

    const modeCls = state.paperLayoutMode === "fluid" ? "paper-mode-fluid" : "paper-mode-fixed";
    const visualCls = state.paperVisualMode === "enhanced" ? "paper-visual-enhanced" : "paper-visual-normal";
    el.slotList.innerHTML = `<div class="paper-spread ${modeCls} ${visualCls}">${page(1)}${page(2)}</div>`;

    // drag/drop handlers
    el.slotList.querySelectorAll(".paper-slot").forEach((div) => {
      const slotId = div.getAttribute("data-slot");
      const slot = slotById[slotId];
      if (!slot) return;
      div.addEventListener("dragover", (ev) => {
        if (!state.draggingStoryId) return;
        ev.preventDefault();
        div.classList.add("drag-over");
        const projected = calculateWithPlacement(slot.id, state.draggingStoryId);
        const profitDelta = Math.round(projected.profit - baseline.profit);
        div.classList.toggle("good-preview", profitDelta > 0);
        div.classList.toggle("bad-preview", profitDelta < 0);
        applySynergyHighlights(projected.linkedTags);
      });
      div.addEventListener("dragleave", () => {
        div.classList.remove("drag-over", "good-preview", "bad-preview", "synergy");
      });
      div.addEventListener("drop", (ev) => {
        ev.preventDefault();
        const storyId = ev.dataTransfer.getData("text/plain") || String(state.draggingStoryId || "");
        if (!storyId) return;
        const newStory = state.stories.find((s) => s.id === Number(storyId));
        const prevStory = state.placed[slot.id];
        if (prevStory && newStory) {
          state.lastReplaceAction = { slotId: slot.id, prevStory };
          showReplaceToast(prevStory, newStory);
        }
        placeStory(slot.id, storyId);
        clearDropPreview();
      });
    });

    el.slotList.querySelectorAll("[data-remove]").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.placed[btn.getAttribute("data-remove")] = null;
        renderSlots();
        renderLiveStats();
      });
    });
  }

  function renderLiveStats() {
    const r = calculate(false);
    const placed = getAllPlaced();
    const peekMult = peekStanceClashDemandMult(placed);
    const effects = analyzeTagEffects(placed.map((x) => x.story));
    const profileLabel = state.editorialProfile <= -35 ? "信息型" : state.editorialProfile >= 35 ? "热度型" : "平衡型";
    el.liveStats.innerHTML = `
      <div class="k">已填版位</div><div class="v">${r.placedCount}/${slots.length}</div>
      <div class="k">编辑定位</div><div class="v">${profileLabel} (${Math.round(state.editorialProfile)})</div>
      <div class="k">独特标签数</div><div class="v">${r.uniqueTags}</div>
      <div class="k">重复成组分</div><div class="v">${r.comboRaw.toFixed(2)}</div>
      <div class="k">连携题材</div><div class="v ${effects.linked.length ? "nm-ok" : "nm-warn"}">${effects.linked.length ? effects.linked.map(toZhTag).join("、") : "无"}</div>
      <div class="k">三轴 P/M/L</div><div class="v ${effects.dominantRatio > 0.7 ? "nm-bad" : "nm-ok"}">${Math.round(effects.publicRatio * 100)}/${Math.round(effects.massRatio * 100)}/${Math.round(effects.lightRatio * 100)}%</div>
      <div class="k">预计需求</div><div class="v">${Math.round(r.demand * peekMult).toLocaleString("zh-CN")}${peekMult < 1 ? "（已乘取向预览）" : ""}</div>
      <div class="k">订阅基数</div><div class="v">${state.subscribers.toLocaleString("zh-CN")}</div>
      <div class="k">有效基础（版内）</div><div class="v">${r.totalBaseValue}${r.topicFatigueLoss > 0 ? ` <span style="color:#fca5a5">−${r.topicFatigueLoss}同题</span>` : ""}</div>
      <div class="k">公开取向（预览）</div><div class="v ${peekMult < 1 ? "nm-warn" : "nm-ok"}">${peekMult >= 1 ? "与既往刊登无冲突" : `若本期结算，需求约×${peekMult.toFixed(2)}（深度/专栏取向与既往同题不一致）`}</div>`;
  }

  function compactEchoTitle(title, maxLen) {
    const text = String(title || "本期头版未定稿");
    const limit = maxLen || 34;
    return text.length > limit ? `${text.slice(0, limit)}…` : text;
  }

  function primaryPublicationPair(placedPairs) {
    return placedPairs.find((x) => x.slot && x.slot.id === "front-main") || placedPairs[0] || null;
  }

  function publicationStanceLabel(story, axis) {
    if (story && story.publicStance === "sci") return "科学纪实 / 交叉证据 / 谨慎追踪";
    if (story && story.publicStance === "occult") return "神秘玄学 / 异常目击 / 连载追踪";
    if (story && story.publicStance === "pop") return "世俗流量 / 读者投稿 / 保留质疑";
    if (axis && axis.dominantType === "公共事务") return "公共事务 / 证据整理 / 谨慎追踪";
    if (axis && axis.dominantType === "大众关注") return "大众关注 / 城市传闻 / 继续征集";
    return "异常目击 / 读者投稿 / 谨慎追踪";
  }

  function publicationEchoProfile(story, axis) {
    const title = story ? story.title : "本期空版";
    const haystack = `${title} ${(story && story.tags ? story.tags.join(" ") : "")}`;
    if (/M330|末班车|调度|车次|站牌|公交/.test(haystack)) {
      return {
        key: "bus330",
        themeTitle: "M330 末班车",
        stance: "异常目击 / 读者投稿 / 谨慎追踪",
        reactions: [
          { label: "读者来信", text: "有人称 2:17 在皇后区也听见同一车铃。" },
          { label: "公交公司公函", text: "要求撤下未上车乘客名单，并否认调度室仍在使用。", pressure: true },
          { label: "匿名电话", text: "别再追调度室。电话断线前能听见刷卡声。", pressure: true },
        ],
        nodeRegionId: "us",
        node: {
          id: `echo_bus330_dispatch_${state.week}`,
          kind: "temp",
          name: "皇后区旧调度室 · 读者回响",
          days: 2,
          need: { 人脉: 2, 洞察: 2 },
          tags: ["occult", "pop"],
          difficulty: "normal",
          enemyAttr: 2,
          checkType: "white",
          deadlineDay: 5,
          mapPos: { x: 34, y: 54 },
          story: {
            brief: "发刊后，三封读者来信把同一个皇后区旧调度室圈了出来，公交公司的公函反而让地址更可疑。",
            objective: "核实旧调度室是否仍保留 M330 的夜班调度页、乘客名单和刷卡记录。",
            stakes: "发刊回响节点。它来自读者与机构反应，会在下周地图上保留一个追踪窗口。",
            fieldIntro: "调度室门口的玻璃贴着停用告示，里面却有一台打卡机还在吐纸。",
            dice: {
              rolling: "线人：如果这里真的停用了，为什么昨晚还有人往里面送咖啡？",
              select: "主编：先找能把来信、名单和调度页接上的证据。",
            },
            outcomes: {
              大成功: { line: "大成功：调度页、刷卡声和读者来信的时间戳完整闭合。", clueTitle: "调度室回响证据", clueDesc: "发刊回响强素材，足以开启下一轮 M330 追踪。" },
              小成功: { line: "成功：旧车次表拍到了，但名单最后一页被撕走。", clueTitle: "缺页车次表", clueDesc: "可用素材。它把读者来信转成现场证据。" },
              成功: { line: "成功：旧车次表拍到了，但名单最后一页被撕走。", clueTitle: "缺页车次表", clueDesc: "可用素材。它把读者来信转成现场证据。" },
              失败: { line: "失败：调度室被清过场，只留下重复打印的 2:17。", clueTitle: "重复打印时间戳", clueDesc: "弱线索。失败仍保留继续追查的口子。" },
            },
          },
        },
        writebacks: [
          { label: "新增地图节点", text: "皇后区旧调度室会在下周纽约市地图出现。", writeback: true },
          { label: "旧线索升温", text: "调度页改动时间被读者来信再次指向。", writeback: true },
          { label: "档案回写", text: `M330 / 第 ${state.week} 周 / 异常交通。`, writeback: true },
        ],
      };
    }
    if (/火球|电场|磁化|气象|接地/.test(haystack)) {
      return {
        key: "ball_lightning",
        themeTitle: "布鲁克林厨房火球",
        stance: "科学纪实 / 异常现象 / 继续复核",
        reactions: [
          { label: "住户来信", text: "同一栋楼有三户报告餐具在凌晨自行贴向冰箱门。" },
          { label: "电力公司回复", text: "否认峰值异常，并要求提供照片原片。", pressure: true },
          { label: "实验室便签", text: "磁化叉子的残留读数在发刊后又升了一次。" },
        ],
        nodeRegionId: "us",
        node: {
          id: `echo_ball_lightning_${state.week}`,
          kind: "temp",
          name: "布鲁克林电力回访 · 读者回响",
          days: 2,
          need: { 理性: 2, 洞察: 2 },
          tags: ["sci", "occult"],
          difficulty: "normal",
          enemyAttr: 2,
          checkType: "white",
          deadlineDay: 5,
          mapPos: { x: 38, y: 29 },
          story: {
            brief: "火球报道发出后，读者把同一时间段的电表读数寄到编辑部。",
            objective: "核对住户读数、电力公司口径和磁化样本。",
            stakes: "发刊回响节点。读者证据可能把厨房火球推向城市电网。",
            fieldIntro: "楼道里的灯每隔七秒暗一次，房东说这是老楼毛病。",
          },
        },
        writebacks: [
          { label: "新增地图节点", text: "布鲁克林电力回访会在下周纽约市地图出现。", writeback: true },
          { label: "旧线索升温", text: "磁化叉子与电场峰值被重新关联。", writeback: true },
          { label: "档案回写", text: `厨房火球 / 第 ${state.week} 周 / 城市电网。`, writeback: true },
        ],
      };
    }
    if (/飞碟|雷达|港务|回波|屋顶|空白/.test(haystack)) {
      return {
        key: "radar_echo",
        themeTitle: "哈德逊异常回波",
        stance: "公共质询 / 雷达抄本 / 谨慎追踪",
        reactions: [
          { label: "船员来信", text: "有人寄来一张航道手绘图，圈出第二个倒影。" },
          { label: "港务局公函", text: "要求停止引用夜班雷达抄本。", pressure: true },
          { label: "电台留言", text: "回放被剪掉的三秒里，听众听到同一段低频。" },
        ],
        nodeRegionId: "us",
        node: {
          id: `echo_radar_echo_${state.week}`,
          kind: "temp",
          name: "港务夜班抄本 · 读者回响",
          days: 2,
          need: { 人脉: 2, 理性: 2 },
          tags: ["sci", "pop"],
          difficulty: "normal",
          enemyAttr: 2,
          checkType: "white",
          deadlineDay: 5,
          mapPos: { x: 58, y: 50 },
          story: {
            brief: "报道发出后，港务局越是否认，越多夜班人员开始匿名递纸条。",
            objective: "核对雷达抄本、航道图和电台剪辑记录。",
            stakes: "发刊回响节点。机构压力会把新证人推向地下。",
            fieldIntro: "值班室窗帘拉得很低，复印机旁边放着一张没有署名的航道图。",
          },
        },
        writebacks: [
          { label: "新增地图节点", text: "港务夜班抄本会在下周纽约市地图出现。", writeback: true },
          { label: "旧线索升温", text: "第二倒影证词与低频空白重新连到一起。", writeback: true },
          { label: "档案回写", text: `哈德逊回波 / 第 ${state.week} 周 / 港务记录。`, writeback: true },
        ],
      };
    }
    const dominant = axis && axis.dominantType ? axis.dominantType : "城市传闻";
    return {
      key: `generic_${story ? story.id : "empty"}`,
      themeTitle: "城市回响",
      stance: publicationStanceLabel(story, axis),
      reactions: [
        { label: "读者来信", text: `三位读者把「${compactEchoTitle(title, 18)}」里同一处地名圈出来，要求继续追踪。` },
        { label: dominant === "公共事务" ? "市政厅回函" : "发行站反馈", text: dominant === "公共事务" ? "要求周刊补充证据来源，并暗示会约谈相关受访者。" : "报摊老板称这篇稿让旧线索重新被读者点名。", pressure: dominant === "公共事务" },
        { label: "匿名便条", text: "别只看稿子里写出的部分，去找被删掉的那一行。" },
      ],
      nodeRegionId: "us",
      node: {
        id: `echo_reader_followup_${state.week}`,
        kind: "temp",
        name: "读者回响追踪 · 本期头版",
        days: 2,
        need: { 人脉: 2, 洞察: 2 },
        tags: story && story.tags && story.tags.includes("Politics") ? ["sci", "pop"] : ["pop", "occult"],
        difficulty: "normal",
        enemyAttr: 2,
        checkType: "white",
        deadlineDay: 5,
        mapPos: { x: 24, y: 48 },
        story: {
          brief: "本期发出后，读者、报摊和匿名便条把同一个未追完的问题推回编辑部。",
          objective: "确认回响来自真实世界对象，还是被人借周刊版面投喂的新诱饵。",
          stakes: "发刊回响节点。它把结算结果转成下周可追踪入口。",
          fieldIntro: "编辑部门缝里塞着一只厚信封，里面只有一张被红笔圈过的报纸。",
        },
      },
      writebacks: [
        { label: "新增地图节点", text: "读者回响追踪会在下周纽约市地图出现。", writeback: true },
        { label: "旧线索升温", text: `「${compactEchoTitle(title, 18)}」的未解释对象被重新标记。`, writeback: true },
        { label: "档案回写", text: `本期头版 / 第 ${state.week} 周 / ${dominant}。`, writeback: true },
      ],
    };
  }

  function registerPublicationEcho(echo) {
    if (!echo) return;
    if (echo.node && echo.nodeRegionId) {
      const exists = state.dynamicNodes.some((x) => x.node && x.node.id === echo.node.id);
      if (!exists && !state.completedMissionIds[echo.node.id]) addDynamicNode(echo.nodeRegionId, echo.node, 2);
    }
    state.lastPublicationEcho = echo;
    state.publicationArchive.push({
      week: state.week,
      title: echo.headline || "",
      stance: echo.stance || "",
      writebacks: (echo.writebacks || []).map((x) => x.text),
    });
  }

  function renderPublicationEchoItem(item) {
    const cls = item.writeback ? " is-writeback" : item.pressure ? " is-pressure" : "";
    return `<div class="publication-echo-item${cls}">
      <strong>${escapeHtml(item.label)}</strong>
      <span>${escapeHtml(item.text)}</span>
    </div>`;
  }

  function buildPublicationEcho(r, placedPairs, axis) {
    const primaryPair = primaryPublicationPair(placedPairs);
    const primaryStory = primaryPair && primaryPair.story;
    const profile = publicationEchoProfile(primaryStory, axis);
    const headline = primaryStory ? primaryStory.title : "本期头版空缺：读者只记住了空白";
    const stance = profile.stance || publicationStanceLabel(primaryStory, axis);
    const issueMeta = `第 ${state.week} 周 · 上版 ${placedPairs.length}/${slots.length} 篇`;
    const tags = primaryStory && primaryStory.tags && primaryStory.tags.length
      ? primaryStory.tags.map(toZhTag).join(" / ")
      : "无主标签";
    const echo = {
      ...profile,
      headline,
      stance,
      issueMeta,
      slotLabel: primaryPair && primaryPair.slot ? primaryPair.slot.name : "头版",
      tags,
      stats: [
        { label: "销量", value: `${r.sold.toLocaleString("zh-CN")} 份` },
        { label: "订阅", value: r.nextSubs.toLocaleString("zh-CN") },
        { label: "净利润", value: fmtMoney(r.profit), tone: r.profit >= 0 ? "good" : "bad" },
      ],
    };
    registerPublicationEcho(echo);
    return echo;
  }

  function renderPublicationEcho(echo) {
    const titleEl = document.getElementById("summaryTitle");
    if (titleEl) {
      const baseTitle = echo.themeTitle || "本期头版";
      titleEl.textContent = baseTitle.endsWith("回响") ? baseTitle : `${baseTitle}回响`;
    }
    const metaEl = document.getElementById("summaryIssueMeta");
    if (metaEl) metaEl.textContent = echo.issueMeta;
    const statHtml = (echo.stats || []).map((s) => `<div class="publication-echo-stat">
      <span>${escapeHtml(s.label)}</span>
      <strong class="${s.tone === "good" ? "nm-ok" : s.tone === "bad" ? "nm-bad" : ""}">${escapeHtml(s.value)}</strong>
    </div>`).join("");
    return `
      <section class="publication-echo-col">
        <h3>本期刊出了什么</h3>
        <div class="publication-echo-headline">
          <span>${escapeHtml(echo.slotLabel || "头版")}</span>
          <strong>《${escapeHtml(echo.headline)}》</strong>
        </div>
        <div class="publication-echo-copy">公开口径：${escapeHtml(echo.stance)}</div>
        <div class="publication-echo-copy">题材标签：${escapeHtml(echo.tags)}</div>
        <div class="publication-echo-stats">${statHtml}</div>
      </section>
      <section class="publication-echo-col">
        <h3>谁有反应</h3>
        <div class="publication-echo-list">${(echo.reactions || []).map(renderPublicationEchoItem).join("")}</div>
      </section>
      <section class="publication-echo-col">
        <h3>写入下周</h3>
        <div class="publication-echo-list">${(echo.writebacks || []).map(renderPublicationEchoItem).join("")}</div>
      </section>`;
  }

  function settlePaper() {
    const r = calculate(true);
    const placedPairs = getAllPlaced();
    const placed = placedPairs.map((x) => x.story);
    const axis = analyzeTagEffects(placed);
    const profileDelta = (axis.lightRatio - axis.publicRatio) * 24 - axis.massRatio * 4;
    state.editorialProfile = clamp(state.editorialProfile + profileDelta, -100, 100);
    macro.声望 = Math.min(100, macro.声望 + Math.min(5, Math.floor(state.pendingClues.length / 2)));
    const profitClass = r.profit >= 0 ? "nm-ok" : "nm-bad";
    el.resultBox.innerHTML = `
      <div class="k">本期净利润</div>
      <div class="nm-big ${profitClass}">${fmtMoney(r.profit)}</div>
      <div class="nm-sum-grid">
        <div class="k">卖报</div><div class="v">${fmtMoney(r.circulationRevenue)}</div>
        <div class="k">订阅</div><div class="v">${fmtMoney(r.subscriptionRevenue)}</div>
        <div class="k">广告</div><div class="v">${fmtMoney(r.adsRevenue)}</div>
        <div class="k">总成本</div><div class="v">${fmtMoney(-r.costs.totalCost)}</div>
        <div class="k">实际销量</div><div class="v">${r.sold.toLocaleString("zh-CN")}</div>
        <div class="k">订阅（下期）</div><div class="v">${r.nextSubs.toLocaleString("zh-CN")}</div>
      </div>
      <div class="nm-tip">乘数：质量 ${r.multipliers.mQuality.toFixed(2)} / 重复 ${r.multipliers.mCombo.toFixed(2)} / 多样性 ${r.multipliers.mDiversity.toFixed(2)} / 版位 ${r.multipliers.mLayout.toFixed(2)} / 偏科 ${r.multipliers.mBias.toFixed(2)}</div>
      <div class="nm-tip" style="margin-top:6px;">同题报道：稿内基础合计 ${r.sumIntrinsicBase} → 上版有效合计 ${r.totalBaseValue}${r.topicFatigueLoss > 0 ? `（同题疲劳折损 ${r.topicFatigueLoss} 点基础值）` : "（无同题折损）"}</div>
      ${
        r.multipliers.mStanceClash < 1
          ? `<div class="nm-tip" style="margin-top:6px;color:#fca5a5;">本期存在<strong>同题公开取向</strong>与既往深度/专栏/爆料不一致，需求已按 ×${r.multipliers.mStanceClash.toFixed(2)} 折算（抢先快讯不计取向）。</div>`
          : ""
      }`;
    renderLiveStats();
    const echo = buildPublicationEcho(r, placedPairs, axis);
    document.getElementById("summaryText").innerHTML = renderPublicationEcho(echo);
    document.getElementById("phase-editorial").classList.add("hidden");
    document.getElementById("phase-summary").classList.remove("hidden");
    log(`报刊结算完成：利润 ${Math.round(r.profit)}`);
  }

  function nextWeek() {
    state.tutorialSoftW1 = {};
    state.week += 1;
    state.day = 7;
    state.weekEvent = null;
    state.weekEventResolved = false;
    state.weekEventResult = "";
    state.weekEventResultLines = [];
    state.weekEventChoiceIndex = null;
    state.activeMissions = [];
    state.todayResolutionQueue = [];
    state.processingDayTick = false;
    state.dayResolutionInfo = null;
    state.pendingClues = [];
    state.pendingReports = [];
    state.topicSynthOrder = {};
    state.pushBudgetWeekly = 1;
    state.tempStaffIds = [];
    state.tempHireUsed = false;
    state.selectedToolDiceIds = [];
    state.toolDiceInventory.forEach((x) => { x.used = false; });
    cleanupWeekScopedEffects();
    initRegionLeadEvents();
    state.phase = "explore";
    document.getElementById("phase-explore").classList.remove("hidden");
    document.getElementById("phase-synthesis").classList.add("hidden");
    document.getElementById("phase-summary").classList.add("hidden");
    log("———— 新的一周 ————");
    renderMacro();
    tickHeader();
    renderWeekStart();
  }

  function tickHeader() {
    const wl = document.getElementById("weekLabel");
    const dl = document.getElementById("dayLabel");
    if (wl) wl.textContent = `第 ${state.week} 周`;
    if (dl) dl.textContent = `剩余 ${state.day} / 7 日`;
    updateNextDayButton();
  }

  function bindEditorialUi() {
    const clearBtn = document.getElementById("clearBtn");
    if (clearBtn) clearBtn.onclick = () => {
      for (const s of slots) state.placed[s.id] = null;
      renderSlots();
      renderLiveStats();
      el.resultBox.innerHTML = `<div class="k">尚未结算</div><div class="nm-tip">版面已清空。</div>`;
    };
    document.getElementById("settleBtn").onclick = settlePaper;
    document.getElementById("btnNextWeek").onclick = nextWeek;
  }

  function bindSynthesisUi() {
    document.getElementById("tabPhenomenon").onclick = () => {
      state.synthTab = "phenomenon";
      renderSynthesis();
    };
    document.getElementById("tabIntel").onclick = () => {
      state.synthTab = "intel";
      renderSynthesis();
    };
    document.getElementById("tabCognition").onclick = () => {
      state.synthTab = "cognition";
      renderSynthesis();
    };
    document.getElementById("tabTool").onclick = () => {
      state.synthTab = "tool";
      renderSynthesis();
    };
    document.getElementById("recipe1").onclick = () => {
      state.synthRecipe = "r1";
      initSynthSlotsForRecipe("r1");
      renderSynthesis();
    };
    document.getElementById("recipe2").onclick = () => {
      state.synthRecipe = "r2";
      initSynthSlotsForRecipe("r2");
      renderSynthesis();
    };
    document.getElementById("recipe3").onclick = () => {
      state.synthRecipe = "r3";
      initSynthSlotsForRecipe("r3");
      renderSynthesis();
    };
    document.getElementById("recipe4").onclick = () => {
      state.synthRecipe = "r4";
      initSynthSlotsForRecipe("r4");
      renderSynthesis();
    };
    document.getElementById("clearSelection").onclick = () => {
      initSynthSlotsForRecipe(state.synthRecipe);
      renderSynthesis();
    };
    document.getElementById("craftBtn").onclick = craftReport;
    document.getElementById("tabTipOff").onclick = () => {
      state.synthTab = "tipoff";
      renderSynthesis();
    };
    const tabStaff = document.getElementById("tabStaff");
    if (tabStaff) {
      tabStaff.onclick = () => {
        state.synthTab = "staff";
        renderSynthesis();
      };
    }
    const tabTherapy = document.getElementById("tabTherapy");
    if (tabTherapy) {
      tabTherapy.onclick = () => {
        state.synthTab = "therapy";
        renderSynthesis();
      };
    }
    document.getElementById("recipeInternal").onclick = () => {
      state.synthRecipe = "internal";
      initSynthSlotsForRecipe("internal");
      renderSynthesis();
    };
    const btnSynthDemo = document.getElementById("btnSynthDemoLab");
    if (btnSynthDemo) btnSynthDemo.onclick = () => openSynthDemoLab();
    document.getElementById("toEditorialBtn").onclick = () => {
      state.pendingReports = state.craftedReports.slice();
      if (!state.pendingReports.length) {
        log("未合成报道，系统将使用探索线索自动转稿。");
      }
      enterEditorialPhase();
    };
  }

  document.getElementById("btnBackToGlobal").onclick = () => returnToGlobalMap();
  document.getElementById("btnNextDay").onclick = () => advanceOneDay();

  function createPaperLabReports() {
    const mk = (title, tags, quality, baseValue, negatives, attrs, recipeType, labTopicIdx) => {
      const pk = `topic_paperlab_${labTopicIdx}`;
      const publicStance =
        recipeType === "r1" ? null : recipeType === "r3" || recipeType === "r4" ? "occult" : "sci";
      return {
        id: state.nextStoryId++,
        title,
        tags,
        quality,
        baseValue,
        intrinsicBaseValue: baseValue,
        primaryTopicKey: pk,
        topicKeys: [pk],
        synthTopicOrder: 1,
        negatives,
        fromExplore: true,
        attrs,
        recipeType,
        publicStance,
      };
    };
    return [
      mk("塔夫脱辞去大法官职务：历史性领导层更迭", ["Politics", "Economy"], "Gold", 450, [], { sensational: 64, credibility: 88, mystery: 28, gaze: 18 }, "r2", 0),
      mk("港务局夜间封锁：三号码头出现异常回波", ["Military", "Gossip"], "Silver", 300, ["thin_source"], { sensational: 72, credibility: 55, mystery: 52, gaze: 34 }, "r1", 1),
      mk("东区剧院失踪档案重现：署名来自未来日期", ["Gossip", "Humor"], "Silver", 300, [], { sensational: 76, credibility: 48, mystery: 67, gaze: 46 }, "r3", 2),
      mk("市政预算暗线曝光：采购名单出现重复身份", ["Politics", "Shopping"], "Gold", 450, ["bias_overreach"], { sensational: 68, credibility: 79, mystery: 35, gaze: 24 }, "r2", 3),
      mk("复活节岛热异常追踪：石像群温差超出历史记录", ["Economy", "Sport"], "Silver", 300, [], { sensational: 58, credibility: 74, mystery: 44, gaze: 23 }, "r1", 4),
      mk("夜班电台误播神秘频段：听众报告同频耳鸣", ["Gossip", "Pets"], "Bronze", 150, ["sloppy_writing"], { sensational: 70, credibility: 38, mystery: 62, gaze: 41 }, "r3", 5),
      mk("法庭速记员匿名口供：判词在宣读前已泄露", ["Politics", "Military"], "Gold", 450, [], { sensational: 66, credibility: 86, mystery: 31, gaze: 20 }, "r2", 6),
      mk("雨夜轨道尽头的白灯：巡检员口供互相矛盾", ["Sport", "Humor"], "Bronze", 150, ["fabrication"], { sensational: 81, credibility: 27, mystery: 71, gaze: 52 }, "r4", 7),
      mk("联邦仓库短时断电：监控画面出现空白帧", ["Economy", "Gossip"], "Silver", 300, [], { sensational: 63, credibility: 66, mystery: 49, gaze: 29 }, "r1", 8),
      mk("午夜来信附带金属碎片：材质与军标不匹配", ["Military", "Shopping"], "Silver", 300, ["thin_source"], { sensational: 74, credibility: 52, mystery: 59, gaze: 37 }, "r3", 9),
    ];
  }

  function maybeEnterPaperLabMode() {
    const p = new URLSearchParams(window.location.search || "");
    const enabled = p.get("paperlab") === "1" || (window.location.hash || "").toLowerCase() === "#paperlab";
    if (!enabled) return false;
    state.paperLabMode = true;
    state.paperLayoutMode = "fixed";
    state.paperVisualMode = "enhanced";
    state.phase = "editorial";
    state.pendingReports = createPaperLabReports();
    state.pendingClues = [];
    state.clues = [];
    log("已进入报纸填充实验模式：拟物增强版面 + 新手引导与填入演示（效果 B）。");
    enterEditorialPhase();
    requestAnimationFrame(() => runPaperLabOnboarding());
    return true;
  }

  function maybeEnableDebugBlackDice() {
    const p = new URLSearchParams(window.location.search || "");
    if (p.get("debugBlackDice") !== "1") return;
    addDynamicNode("us", {
      id: "debug_bus330_tape",
      kind: "temp",
      name: "M330 末班车 · 车载录像最后三秒（调试）",
      days: 1,
      need: { 胆识: 3, 诡思: 3, 洞察: 2 },
      tags: ["occult"],
      difficulty: "hard",
      enemyAttr: 4,
      checkType: "white",
      riskTier: "high",
      isBlackDiceTask: true,
      blackDiceTheme: "bus330",
      chainType: "deep",
      chainStage: 4,
      chainStageTotal: 4,
      chainId: "bus330",
      chainFinal: true,
      taskTypeTitle: "黑骰任务 · M330 末班车终局",
      taskTypeDesc: "调试入口：鬼混入乘客之中。黑骰会混入或替换你的骰子。",
    }, 1);
  }

  function createDirectDebugBlackDiceMission() {
    return {
      id: "debug_bus330_tape",
      kind: "temp",
      name: "M330 末班车 · 车载录像最后三秒（调试）",
      days: 1,
      need: { 胆识: 3, 诡思: 3, 洞察: 2 },
      tags: ["occult"],
      difficulty: "hard",
      enemyAttr: 4,
      checkType: "white",
      riskTier: "high",
      isBlackDiceTask: true,
      blackDiceTheme: "bus330",
      chainType: "deep",
      chainStage: 4,
      chainStageTotal: 4,
      chainId: "bus330",
      chainFinal: true,
      taskTypeTitle: "黑骰任务 · M330 末班车终局",
      taskTypeDesc: "调试入口：鬼混入乘客之中。黑骰会混入或替换你的骰子。",
    };
  }

  function maybeEnterDebugBlackDiceMode() {
    const p = new URLSearchParams(window.location.search || "");
    const mode = p.get("debugBlackDice");
    if (!["1", "roll"].includes(mode)) return false;
    if (state.tutorialSoftW1) {
      Object.keys(state.tutorialSoftW1).forEach((key) => { state.tutorialSoftW1[key] = true; });
    }
    state.phase = "explore";
    state.debugSkipTutorials = true;
    state.regionId = "us";
    state.mission = { regionId: "us", ...createDirectDebugBlackDiceMission() };
    state.selectedStaffIds = ["s8", "s1", "s2", "s3", "s4"];
    state.selectedToolDiceIds = [];
    state.dayResolutionInfo = { current: 1, total: 1 };
    state.processingDayTick = true;
    renderRegion();
    setView("region");
    updateNextDayButton();
    requestAnimationFrame(() => {
      runMission(() => {
        state.processingDayTick = false;
        state.dayResolutionInfo = null;
        state.mission = null;
        state.selectedStaffIds = [];
        state.selectedToolDiceIds = [];
        renderRegion();
        setView("region");
        updateNextDayButton();
      }).catch((err) => {
        console.error(err);
        state.processingDayTick = false;
        updateNextDayButton();
      });
    });
    return true;
  }

  function createDirectDebugDispatchMission() {
    return {
      id: "debug_dispatch_ux",
      kind: "temp",
      name: "港务局夜间封锁：三号码头异常回波",
      days: 2,
      need: { 人脉: 2, 洞察: 2, 理性: 2 },
      tags: ["sci", "occult"],
      difficulty: "hard",
      enemyAttr: 3,
      checkType: "red",
      deadlineDay: 4,
      riskTier: "high",
      missionType: "leadInvestigation",
      useCharacterDice: true,
      maxStaffOverride: 6,
      regionId: "us",
      leadId: "debug_dispatch_ux",
      story: {
        brief: "夜班船员寄来一张航道手绘图，港务局随即封锁三号码头，并要求周刊停止引用雷达抄本。",
        objective: "核对雷达抄本、航道图和电台剪辑记录，确认第二个倒影是否真实存在。",
        stakes: "红色截稿。成功或失败后窗口都会关闭；拖到下周，港务局会先一步清场。",
        fieldIntro: "值班室窗帘拉得很低，复印机旁边放着一张没有署名的航道图。",
        outcomes: {
          大成功: { line: "大成功：雷达抄本、航道图和电台空白三秒完整对上。", clueTitle: "港务三重回波证据", clueDesc: "红色截稿强素材，可直接进入本周头版候选。" },
          小成功: { line: "成功：航道图和回波时间能对上，电台剪辑仍缺一段原带。", clueTitle: "夜班雷达回波抄本", clueDesc: "可用素材。它能支撑一篇谨慎追踪稿。" },
          成功: { line: "成功：航道图和回波时间能对上，电台剪辑仍缺一段原带。", clueTitle: "夜班雷达回波抄本", clueDesc: "可用素材。它能支撑一篇谨慎追踪稿。" },
          失败: { line: "失败：港务局先一步清场，但船员留下第二个倒影的手绘方位。", clueTitle: "第二倒影手绘方位", clueDesc: "弱线索。失败后仍可保留一个后续钩子。" },
        },
      },
    };
  }

  function maybeEnterDebugDispatchSetupMode() {
    const p = new URLSearchParams(window.location.search || "");
    if (p.get("debugDispatch") !== "1" && p.get("dispatchjudge") !== "1") return false;
    state.phase = "explore";
    state.debugSkipTutorials = true;
    state.regionId = "us";
    state.mission = createDirectDebugDispatchMission();
    state.dispatchDecisionExperimentMode = p.get("dispatchjudge") === "1";
    state.selectedStaffIds = state.dispatchDecisionExperimentMode || p.get("dispatchState") === "selected" ? ["s5", "s7", "s2", "s3", "s6"] : [];
    state.selectedToolDiceIds = state.dispatchDecisionExperimentMode || p.get("tool") === "hotline" ? ["tool_tip_1"] : [];
    state.displayMode = p.get("displayMode") === "numeric" ? "numeric" : "dice";
    renderSetup();
    setView("setup");
    updateNextDayButton();
    return true;
  }

  function maybeConfigureDispatchSetupMode() {
    const p = new URLSearchParams(window.location.search || "");
    const hash = (window.location.hash || "").toLowerCase();
    state.dispatchDecisionExperimentMode = p.get("dispatchjudge") === "1" || hash === "#dispatchjudge";
    state.dispatchOldSetupMode = p.get("dispatchold") === "1" || p.get("oldsetup") === "1" || hash === "#dispatchold";
    if (state.dispatchDecisionExperimentMode) state.dispatchOldSetupMode = false;
    if (p.get("dispatchlab") === "1" || hash === "#dispatchlab") state.dispatchOldSetupMode = false;
  }

  function init() {
    renderMacro();
    tickHeader();
    setInterval(tickHeader, 500);
    initRegionLeadEvents();
    maybeConfigureDispatchSetupMode();
    maybeEnableDebugBlackDice();
    bindSynthesisUi();
    bindEditorialUi();
    bindPaperDemoLabUi();
    bindSynthDemoLabUi();
    log("本周编辑部简报已送达。");
    if (!maybeEnterPaperLabMode()) {
      if (maybeEnterDebugBlackDiceMode()) return;
      if (maybeEnterDebugDispatchSetupMode()) return;
      renderWeekStart();
      updateNextDayButton();
    }
  }

  init();
})();
