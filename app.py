import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="운빨존많겜: 마스터 디펜스",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 60FPS 레퍼런스 스타일 고품질 아바타 & 타일 터치 조합 엔진
html_game_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body { background-color: #0b0c10; color: #fff; font-family: 'Pretendard', sans-serif; overflow: hidden; }
    
    #game-container {
        display: flex;
        flex-direction: row;
        width: 100vw;
        height: 100vh;
        background: #0f1017;
    }

    #canvas-container {
        position: relative;
        flex: 1;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #07080c;
    }

    canvas {
        border: 2px solid #222639;
        border-radius: 12px;
        box-shadow: 0 0 40px rgba(0,0,0,0.9);
        background: #121520;
    }

    #ui-panel {
        width: 420px;
        height: 100%;
        background: #161824;
        border-left: 2px solid #23273a;
        display: flex;
        flex-direction: column;
        padding: 15px;
        gap: 10px;
        overflow-y: auto;
    }

    .status-bar {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        background: #1e2233;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #2f354f;
    }

    .status-item { display: flex; flex-direction: column; align-items: center; }
    .status-label { font-size: 11px; color: #8c93b5; font-weight: bold; }
    .status-value { font-size: 17px; color: #ffd700; font-weight: 800; }

    .action-btn {
        background: linear-gradient(135deg, #3d4463, #252a3f);
        color: white;
        border: 1px solid #505982;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.1s ease;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .action-btn:hover { background: linear-gradient(135deg, #4d567d, #323852); transform: translateY(-1px); }
    .action-btn:active { transform: translateY(1px); }
    .action-btn.primary { background: linear-gradient(135deg, #ff8800, #dd6600); border-color: #ffa433; color: #fff; font-size: 15px; }
    .action-btn.speed { background: linear-gradient(135deg, #8e44ad, #5e2a84); border-color: #9b59b6; }

    .section-title { font-size: 13px; font-weight: bold; color: #00ffcc; margin-top: 2px; border-bottom: 1px solid #2a2f45; padding-bottom: 3px; }
    .gacha-rates { font-size: 11px; color: #9da4c7; background: #0d0e15; padding: 6px; border-radius: 6px; text-align: center; }

    .recipe-card {
        background: #1a1e2d;
        border: 1px solid #2b314d;
        padding: 6px 10px;
        border-radius: 6px;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .recipe-info { font-size: 11px; }
    .recipe-name { font-weight: bold; color: #ff3366; }
    .recipe-req { font-size: 9px; color: #8d95bd; }

    #game-over-screen {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.85);
        display: none;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 100;
    }
    #game-over-screen h1 { font-size: 46px; color: #ff2255; text-shadow: 0 0 20px #ff0044; margin-bottom: 10px; }
</style>
</head>
<body>

<div id="game-container">
    <div id="canvas-container">
        <canvas id="gameCanvas" width="750" height="750"></canvas>
        <div id="game-over-screen">
            <h1>GAME OVER</h1>
            <p id="final-wave-text" style="font-size: 18px; color: #ddd; margin-bottom: 20px;">최종 웨이브: 1</p>
            <button class="action-btn primary" onclick="resetGame()" style="width: 180px; justify-content: center;">🔄 다시 도전</button>
        </div>
    </div>

    <div id="ui-panel">
        <h2 style="text-align: center; color: #ffcc00; font-size: 18px;">🎲 운빨존많겜: 마스터 디펜스</h2>
        
        <div class="status-bar">
            <div class="status-item"><span class="status-label">보유 골드</span><span id="ui-gold" class="status-value">400 G</span></div>
            <div class="status-item"><span class="status-label">현재 웨이브</span><span id="ui-wave" class="status-value" style="color:#00ffcc;">1</span></div>
            <div class="status-item"><span class="status-label">웨이브 타이머</span><span id="ui-timer" class="status-value" style="color:#ff6699;">10.0초</span></div>
            <div class="status-item"><span class="status-label">적 / 최대한도</span><span id="ui-enemies" class="status-value" style="color:#ff4444;">0 / 100</span></div>
        </div>

        <div style="display: flex; gap: 8px;">
            <button class="action-btn primary" onclick="drawUnit()" style="flex: 2;">
                <span>🎲 유닛 뽑기</span>
                <span id="ui-gacha-cost">40 G</span>
            </button>
            <button class="action-btn speed" onclick="toggleSpeed()" id="ui-speed-btn" style="flex: 1; justify-content: center;">
                ⚡ 1배속
            </button>
        </div>

        <button class="action-btn" onclick="upgradeGachaRates()">
            <span>📈 가챠 확률 강화</span>
            <span id="ui-rate-up-cost">60 G</span>
        </button>

        <div class="gacha-rates" id="ui-rates-text">일반: 70% | 희귀: 22% | 영웅: 6% | 전설: 2%</div>

        <div class="section-title">⚔️ 등급별 공격력 강화</div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px;">
            <button class="action-btn" onclick="upgradeClass('common')" style="font-size:10px; flex-direction:column; padding:6px;">일반(Lv.<span id="lvl-common">1</span>)<br>25G</button>
            <button class="action-btn" onclick="upgradeClass('rare')" style="font-size:10px; flex-direction:column; padding:6px; border-color:#1e90ff;">희귀(Lv.<span id="lvl-rare">1</span>)<br>50G</button>
            <button class="action-btn" onclick="upgradeClass('epic')" style="font-size:10px; flex-direction:column; padding:6px; border-color:#9932cc;">영웅(Lv.<span id="lvl-epic">1</span>)<br>100G</button>
            <button class="action-btn" onclick="upgradeClass('legendary')" style="font-size:10px; flex-direction:column; padding:6px; border-color:#ff8c00;">전설(Lv.<span id="lvl-legendary">1</span>)<br>200G</button>
        </div>

        <div class="section-title">👑 신화 등급 전용 조합식</div>
        <div id="mythic-recipes-list"></div>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// --- [유닛 데이터베이스: 레퍼런스 스타일 고품질 아바타 및 무기 디자인] ---
const UNITS_DB = {
    common: [
        { id: "c1", name: "돌멩이 도끼병", atk: 18, skin: "axe_boy", color: "#a0a0a0" },
        { id: "c2", name: "견습 꼬마궁수", atk: 20, skin: "archer", color: "#d2b48c" },
        { id: "c3", name: "초록 슬라임펫", atk: 15, skin: "slime", color: "#2ecc71" },
        { id: "c4", name: "단검 도적", atk: 22, skin: "rogue", color: "#e67e22" }
    ],
    rare: [
        { id: "r1", name: "화염 마법사", atk: 70, skin: "wizard", color: "#ff6b6b" },
        { id: "r2", name: "철갑 라이거 기사", atk: 65, skin: "knight", color: "#3498db" },
        { id: "r3", name: "흑표범 암살자", atk: 80, skin: "assassin", color: "#2c3e50" },
        { id: "r4", name: "번개 사제", atk: 75, skin: "priest", color: "#f1c40f" }
    ],
    epic: [
        { id: "e1", name: "서리여왕 엘프", atk: 260, skin: "ice_queen", color: "#00d2d3" },
        { id: "e2", name: "광전사 울버린", atk: 300, skin: "berserker", color: "#ff5252" },
        { id: "e3", name: "메카 사이보그 사자", atk: 280, skin: "mecha", color: "#ff9f43" },
        { id: "e4", name: "암흑 소울 흑마법사", atk: 250, skin: "dark_mage", color: "#8854d0" }
    ],
    legendary: [
        { id: "l1", name: "천공 드래곤", atk: 1000, skin: "dragon", color: "#fffa65" },
        { id: "l2", name: "지옥 아수라왕", atk: 1150, skin: "asura", color: "#ff3838" },
        { id: "l3", name: "시간 수호자", atk: 950, skin: "timelord", color: "#48dbfb" },
        { id: "l4", name: "빛의 성기사", atk: 1050, skin: "paladin", color: "#ffffff" }
    ],
    mythic: [
        { id: "m1", name: "🔥 혼돈 종말자", atk: 4800, skin: "myth_dragon", color: "#ff0055", recipeReq: "천공 드래곤 + 도끼병" },
        { id: "m2", name: "⚡ 제우스 현신", atk: 5300, skin: "myth_zeus", color: "#ffff00", recipeReq: "지옥 아수라왕 + 화염 마법사" },
        { id: "m3", name: "❄️ 절대영도 여신", atk: 4600, skin: "myth_queen", color: "#00ffff", recipeReq: "시간 수호자 + 서리여왕" },
        { id: "m4", name: "💀 심연의 군주", atk: 5800, skin: "myth_lord", color: "#9b59b6", recipeReq: "빛의 성기사 + 광전사" },
        { id: "m5", name: "🌟 창조의 스피릿", atk: 6800, skin: "myth_spirit", color: "#ffffff", recipeReq: "천공 드래곤 + 지옥 아수라왕" }
    ]
};

let gameState = {
    gold: 400,
    wave: 1,
    waveTimer: 10.0,
    maxEnemies: 100,
    gameOver: false,
    gachaCost: 40,
    rateCost: 60,
    gameSpeed: 1,
    rates: { common: 70.0, rare: 22.0, epic: 6.0, legendary: 2.0 },
    upgrades: { common: 1, rare: 1, epic: 1, legendary: 1 },
    board: new Array(20).fill(null),
    enemies: [],
    projectiles: [],
    meleeEffects: [],
    spawnTimer: 0,
    lastTime: performance.now()
};

const TRACK = { centerX: 375, centerY: 375, radius: 290 };

const GRID_TILES = [];
const rows = 5, cols = 4;
const startX = 225, startY = 200, tileSize = 70, gap = 10;
for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
        GRID_TILES.push({ x: startX + c * (tileSize + gap), y: startY + r * (tileSize + gap), size: tileSize });
    }
}

function initGame() {
    gameState.gold = 400;
    gameState.wave = 1;
    gameState.waveTimer = 10.0;
    gameState.gameOver = false;
    gameState.board = new Array(20).fill(null);
    gameState.enemies = [];
    gameState.projectiles = [];
    gameState.meleeEffects = [];
    gameState.rates = { common: 70.0, rare: 22.0, epic: 6.0, legendary: 2.0 };
    gameState.upgrades = { common: 1, rare: 1, epic: 1, legendary: 1 };
    document.getElementById("game-over-screen").style.display = "none";
    updateUI();
    renderMythicRecipes();
}

function toggleSpeed() {
    gameState.gameSpeed = gameState.gameSpeed === 1 ? 2 : 1;
    document.getElementById("ui-speed-btn").innerText = `⚡ ${gameState.gameSpeed}배속`;
}

function spawnEnemy() {
    const isBoss = (gameState.wave % 5 === 0) && (gameState.enemies.filter(e => e.isBoss).length === 0);
    const baseHp = 90 * Math.pow(1.22, gameState.wave - 1);
    const mTypes = ["zombie", "orc_grunt", "skeleton", "mutant_ogre"];
    const chosenType = isBoss ? (gameState.wave % 10 === 0 ? "boss_necromancer" : "boss_ogre_lord") : mTypes[Math.floor(Math.random() * mTypes.length)];

    gameState.enemies.push({
        id: Math.random(),
        angle: 0,
        speed: (isBoss ? 0.35 : (chosenType === "skeleton" ? 0.9 : 0.65)) * 1.2,
        hp: isBoss ? baseHp * 8 : baseHp,
        maxHp: isBoss ? baseHp * 8 : baseHp,
        isBoss: isBoss,
        type: chosenType,
        radius: isBoss ? 26 : 14,
        color: isBoss ? "#ff0055" : (chosenType === "zombie" ? "#55efc4" : "#e17055")
    });
}

// --- [자동 3마리 뭉치기 뽑기 시스템] ---
function drawUnit() {
    if (gameState.gold < gameState.gachaCost) { alert("❌ 골드가 부족합니다!"); return; }
    
    // 무작위 등급 결정
    const rand = Math.random() * 100;
    let grade = "common";
    if (rand < gameState.rates.legendary) grade = "legendary";
    else if (rand < gameState.rates.legendary + gameState.rates.epic) grade = "epic";
    else if (rand < gameState.rates.legendary + gameState.rates.epic + gameState.rates.rare) grade = "rare";

    const template = UNITS_DB[grade][Math.floor(Math.random() * UNITS_DB[grade].length)];

    // 1. 이미 필드에 같은 종류(id)의 유닛이 존재하고, 그 칸의 count가 3 미만이면 자동 합류!
    let targetIdx = gameState.board.findIndex(slot => slot && slot.id === template.id && slot.count < 3);

    if (targetIdx !== -1) {
        gameState.gold -= gameState.gachaCost;
        gameState.board[targetIdx].count++;
    } else {
        // 2. 같은 유닛이 없거나 3마리 꽉 찼다면 빈 칸 찾기
        let emptyIdx = gameState.board.findIndex(slot => slot === null);
        if (emptyIdx === -1) { alert("⚠️ 필드 20칸이 가득 찼습니다!"); return; }
        gameState.gold -= gameState.gachaCost;
        gameState.board[emptyIdx] = {
            ...template,
            grade: grade,
            count: 1,
            lastAttack: 0,
            attackSpeed: 1.3,
            animTimer: 0
        };
    }
    updateUI();
}

// --- [타일 클릭 조합 시스템 (3마리 뭉친 칸에서 조합)] ---
function handleTileClick(idx) {
    const slot = gameState.board[idx];
    if (!slot) return;

    if (slot.count < 3) {
        alert("⚠️ 같은 유닛이 3마리 뭉쳐야 조합할 수 있습니다! (현재 " + slot.count + "마리)");
        return;
    }

    // 등급별 자동 상위 조합
    if (slot.grade === "common") {
        // 일반 3마리 ➔ 무작위 희귀
        const template = UNITS_DB.rare[Math.floor(Math.random() * UNITS_DB.rare.length)];
        gameState.board[idx] = { ...template, grade: "rare", count: 1, lastAttack: 0, attackSpeed: 1.3, animTimer: 0 };
        alert("✨ 일반 3마리 조합 성공! 희귀 등급 획득!");
    } else if (slot.grade === "rare") {
        // 희귀 3마리 ➔ 무작위 영웅
        const template = UNITS_DB.epic[Math.floor(Math.random() * UNITS_DB.epic.length)];
        gameState.board[idx] = { ...template, grade: "epic", count: 1, lastAttack: 0, attackSpeed: 1.3, animTimer: 0 };
        alert("🔥 희귀 3마리 조합 성공! 영웅 등급 획득!");
    } else if (slot.grade === "epic") {
        // 영웅 3마리 ➔ 무작위 전설 (요청사항 반영)
        const template = UNITS_DB.legendary[Math.floor(Math.random() * UNITS_DB.legendary.length)];
        gameState.board[idx] = { ...template, grade: "legendary", count: 1, lastAttack: 0, attackSpeed: 1.5, animTimer: 0 };
        alert("👑 영웅 3마리 조합 성공! 전설 등급 강림!");
    } else {
        alert("이 유닛은 더 이상 일반 조합을 할 수 없습니다.");
    }
    updateUI();
}

// 신화 전용 조합 (공방 버튼)
function summonMythicRecipe(mIndex) {
    const mythTemplate = UNITS_DB.mythic[mIndex];
    // 간단 검증: 필드에 전설 유닛이 1개 이상 있으면 소환 가능
    const legIdx = gameState.board.findIndex(s => s && s.grade === "legendary");
    if (legIdx === -1) { alert("⚠️ 재료가 될 [전설 유닛]이 필드에 필요합니다!"); return; }

    gameState.board[legIdx].count--;
    if (gameState.board[legIdx].count === 0) gameState.board[legIdx] = null;

    let emptyIdx = gameState.board.findIndex(s => s === null);
    if (emptyIdx === -1) emptyIdx = legIdx;

    gameState.board[emptyIdx] = {
        ...mythTemplate,
        grade: "mythic",
        count: 1,
        lastAttack: 0,
        attackSpeed: 1.8,
        animTimer: 0
    };
    alert(`🎊 신화 등급 [${mythTemplate.name}] 강림 완료!`);
    updateUI();
}

function renderMythicRecipes() {
    const container = document.getElementById("mythic-recipes-list");
    container.innerHTML = "";
    UNITS_DB.mythic.forEach((m, idx) => {
        container.innerHTML += `
            <div class="recipe-card">
                <div class="recipe-info">
                    <span class="recipe-name">${m.name}</span>
                    <div class="recipe-req">ATK: ${m.atk} | 재료: ${m.recipeReq}</div>
                </div>
                <button class="action-btn" style="padding:4px 8px; font-size:11px; border-color:#ff0055;" onclick="summonMythicRecipe(${idx})">강림</button>
            </div>
        `;
    });
}

function upgradeGachaRates() {
    if (gameState.gold < gameState.rateCost) { alert("골드 부족!"); return; }
    gameState.gold -= gameState.rateCost;
    gameState.rates.common = Math.max(20, gameState.rates.common - 6);
    gameState.rates.rare += 3;
    gameState.rates.epic += 2;
    gameState.rates.legendary += 1;
    updateUI();
}

function upgradeClass(grade) {
    const costMap = { common: 25, rare: 50, epic: 100, legendary: 200 };
    const cost = costMap[grade] * gameState.upgrades[grade];
    if (gameState.gold < cost) { alert("골드 부족!"); return; }
    gameState.gold -= cost;
    gameState.upgrades[grade]++;
    updateUI();
}

// --- [60FPS 게임 엔진 루프] ---
function gameLoop(now) {
    const rawDt = (now - gameState.lastTime) / 1000;
    gameState.lastTime = now;
    const dt = rawDt * gameState.gameSpeed;

    if (!gameState.gameOver) updateGame(dt);
    renderGame();
    requestAnimationFrame(gameLoop);
}

function updateGame(dt) {
    gameState.waveTimer -= dt;
    if (gameState.waveTimer <= 0) {
        gameState.wave++;
        gameState.waveTimer = 10.0;
    }

    gameState.spawnTimer += dt;
    const spawnInterval = Math.max(0.25, 0.9 - gameState.wave * 0.025);
    if (gameState.spawnTimer >= spawnInterval) {
        gameState.spawnTimer = 0;
        spawnEnemy();
    }

    gameState.enemies.forEach(e => { e.angle += (e.speed * dt); });

    if (gameState.enemies.length >= gameState.maxEnemies) {
        gameState.gameOver = true;
        document.getElementById("final-wave-text").innerText = `최종 달성 웨이브: ${gameState.wave} 단계`;
        document.getElementById("game-over-screen").style.display = "flex";
    }

    const currentTime = performance.now() / 1000;
    gameState.board.forEach((slot, tileIdx) => {
        if (!slot) return;
        if (slot.animTimer > 0) slot.animTimer -= dt;

        if (currentTime - slot.lastAttack >= (1 / slot.attackSpeed)) {
            const tile = GRID_TILES[tileIdx];
            const ux = tile.x + 35, uy = tile.y + 35;
            let closestEnemy = null;
            let minDist = 340;

            gameState.enemies.forEach(e => {
                const ex = TRACK.centerX + Math.cos(e.angle) * TRACK.radius;
                const ey = TRACK.centerY + Math.sin(e.angle) * TRACK.radius;
                const dist = Math.hypot(ex - ux, ey - uy);
                if (dist < minDist) { minDist = dist; closestEnemy = e; }
            });

            if (closestEnemy) {
                slot.lastAttack = currentTime;
                slot.animTimer = 0.35;
                const upLvl = gameState.upgrades[slot.grade] || 1;
                const finalAtk = slot.atk * slot.count * (1 + (upLvl - 1) * 0.3);

                const ex = TRACK.centerX + Math.cos(closestEnemy.angle) * TRACK.radius;
                const ey = TRACK.centerY + Math.sin(closestEnemy.angle) * TRACK.radius;

                if (slot.skin === "axe_boy" || slot.skin === "rogue" || slot.skin === "knight" || slot.skin === "assassin" || slot.skin === "berserker" || slot.skin === "asura") {
                    gameState.meleeEffects.push({ x: ex, y: ey, type: "slash", color: slot.color, life: 0.25 });
                    closestEnemy.hp -= finalAtk;
                    checkEnemyDeath(closestEnemy);
                } else {
                    gameState.projectiles.push({ x: ux, y: uy, target: closestEnemy, damage: finalAtk, color: slot.color, speed: 700 });
                }
            }
        }
    });

    for (let i = gameState.projectiles.length - 1; i >= 0; i--) {
        const p = gameState.projectiles[i];
        if (!gameState.enemies.includes(p.target)) { gameState.projectiles.splice(i, 1); continue; }

        const ex = TRACK.centerX + Math.cos(p.target.angle) * TRACK.radius;
        const ey = TRACK.centerY + Math.sin(p.target.angle) * TRACK.radius;
        const dx = ex - p.x, dy = ey - p.y;
        const dist = Math.hypot(dx, dy);

        if (dist < 18) {
            p.target.hp -= p.damage;
            checkEnemyDeath(p.target);
            gameState.projectiles.splice(i, 1);
        } else {
            p.x += (dx / dist) * p.speed * dt;
            p.y += (dy / dist) * p.speed * dt;
        }
    }

    for (let i = gameState.meleeEffects.length - 1; i >= 0; i--) {
        gameState.meleeEffects[i].life -= dt;
        if (gameState.meleeEffects[i].life <= 0) gameState.meleeEffects.splice(i, 1);
    }

    updateUI();
}

function checkEnemyDeath(enemy) {
    if (enemy.hp <= 0) {
        gameState.gold += enemy.isBoss ? 200 : 16;
        const eIdx = gameState.enemies.indexOf(enemy);
        if (eIdx !== -1) gameState.enemies.splice(eIdx, 1);
    }
}

// --- [고급 아바타 및 일러스트 렌더러] ---
function drawUnitAvatar(ctx, unit, x, y, size) {
    ctx.save();
    ctx.translate(x + size/2, y + size/2);

    let jumpOffset = 0;
    if (unit.animTimer > 0) {
        jumpOffset = -6 * Math.sin((0.35 - unit.animTimer) / 0.35 * Math.PI);
        ctx.translate(0, jumpOffset);
    }

    // 등급별 아라
    ctx.fillStyle = unit.color + "33";
    ctx.beginPath(); ctx.arc(0, 0, size/2 - 2, 0, Math.PI*2); ctx.fill();

    // 캐릭터 본체 (사람/영웅형 외형)
    ctx.fillStyle = unit.color;
    ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI*2); ctx.fill();
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();

    // 얼굴 및 모자 디자인
    ctx.fillStyle = "#fff";
    ctx.fillRect(-5, -4, 4, 4); ctx.fillRect(2, -4, 4, 4);
    ctx.fillStyle = "#000";
    ctx.fillRect(-4, -3, 2, 2); ctx.fillRect(3, -3, 2, 2);

    // 무기/장비 렌더링
    if (unit.skin === "axe_boy" || unit.skin === "berserker") {
        ctx.fillStyle = "#8b4513"; ctx.fillRect(10, -12, 3, 16); // 도끼 자루
        ctx.fillStyle = "#ccc"; ctx.fillRect(8, -16, 8, 6); // 도끼날
    } else if (unit.skin === "archer") {
        ctx.strokeStyle = "#deb887"; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(0, 0, 14, -Math.PI/2, Math.PI/2); ctx.stroke();
    } else if (unit.skin === "wizard" || unit.skin === "dark_mage") {
        ctx.fillStyle = "#9b59b6";
        ctx.beginPath(); ctx.moveTo(0, -26); ctx.lineTo(-12, -12); ctx.lineTo(12, -12); ctx.fill();
    }

    ctx.restore();
}

function renderGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 트랙
    ctx.beginPath();
    ctx.arc(TRACK.centerX, TRACK.centerY, TRACK.radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#23283d"; ctx.lineWidth = 28; ctx.stroke();
    ctx.beginPath();
    ctx.arc(TRACK.centerX, TRACK.centerY, TRACK.radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#3b4366"; ctx.lineWidth = 2; ctx.setLineDash([8, 8]); ctx.stroke();
    ctx.setLineDash([]);

    // 20칸 타일 (3마리 뭉쳤을 때 [조합] 버튼 텍스트 표시)
    GRID_TILES.forEach((tile, idx) => {
        const unit = gameState.board[idx];
        ctx.fillStyle = "#151824"; ctx.strokeStyle = "#252b42"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.roundRect(tile.x, tile.y, tile.size, tile.size, 8); ctx.fill(); ctx.stroke();

        if (unit) {
            drawUnitAvatar(ctx, unit, tile.x, tile.y, tile.size);
            ctx.font = "bold 10px sans-serif"; ctx.fillStyle = "#fff"; ctx.textAlign = "center";
            ctx.fillText(unit.name.substring(0, 7), tile.x + 35, tile.y + 60);

            if (unit.count > 1) {
                ctx.fillStyle = "#ffcc00"; ctx.font = "bold 11px sans-serif";
                ctx.fillText(`x${unit.count}`, tile.x + 55, tile.y + 15);
            }

            // 3마리가 뭉쳤을 때 [ 🔄 조합 ] 버튼 오버레이 표시
            if (unit.count >= 3 && unit.grade !== "mythic" && unit.grade !== "legendary") {
                ctx.fillStyle = "rgba(255, 100, 0, 0.85)";
                ctx.beginPath(); ctx.roundRect(tile.x + 5, tile.y + 22, tile.size - 10, 22, 4); ctx.fill();
                ctx.fillStyle = "#fff"; ctx.font = "bold 11px sans-serif";
                ctx.fillText("🔄 조합하기", tile.x + 35, tile.y + 37);
            }
        } else {
            ctx.font = "10px sans-serif"; ctx.fillStyle = "#3f466b"; ctx.textAlign = "center";
            ctx.fillText(`#${idx+1}`, tile.x + 35, tile.y + 38);
        }
    });

    // 몬스터 렌더링
    gameState.enemies.forEach(e => {
        const ex = TRACK.centerX + Math.cos(e.angle) * TRACK.radius;
        const ey = TRACK.centerY + Math.sin(e.angle) * TRACK.radius;

        const hpPct = Math.max(0, e.hp / e.maxHp);
        ctx.fillStyle = "#ff0000"; ctx.fillRect(ex - 16, ey - e.radius - 9, 32, 4);
        ctx.fillStyle = "#00ffcc"; ctx.fillRect(ex - 16, ey - e.radius - 9, 32 * hpPct, 4);

        ctx.save();
        ctx.translate(ex, ey);
        ctx.fillStyle = e.color;
        ctx.beginPath(); ctx.arc(0, 0, e.isBoss ? 24 : 14, 0, Math.PI*2); ctx.fill();
        ctx.strokeStyle = e.isBoss ? "#ffd700" : "#fff"; ctx.lineWidth = e.isBoss ? 3 : 1; ctx.stroke();
        ctx.fillStyle = "#ff3333";
        ctx.fillRect(-4, -4, 3, 3); ctx.fillRect(2, -4, 3, 3);
        ctx.restore();

        if (e.isBoss) {
            ctx.font = "bold 11px sans-serif"; ctx.fillStyle = "#ff3366"; ctx.textAlign = "center";
            ctx.fillText("👑 BOSS", ex, ey - e.radius - 14);
        }
    });

    // 근접 참격 이펙트
    gameState.meleeEffects.forEach(m => {
        ctx.save();
        ctx.translate(m.x, m.y);
        ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.arc(0, 0, 20, -Math.PI/2, Math.PI/2); ctx.stroke();
        ctx.restore();
    });

    // 투사체
    gameState.projectiles.forEach(p => {
        ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI*2); ctx.fillStyle = p.color; ctx.fill();
        ctx.strokeStyle = "#fff"; ctx.lineWidth = 1; ctx.stroke();
    });
}

// 타일 클릭 이벤트 (3마리 뭉쳤을 때 조합 실행)
canvas.addEventListener("click", function(event) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    GRID_TILES.forEach((tile, idx) => {
        if (mouseX >= tile.x && mouseX <= tile.x + tile.size && mouseY >= tile.y && mouseY <= tile.y + tile.size) {
            handleTileClick(idx);
        }
    });
});

function updateUI() {
    document.getElementById("ui-gold").innerText = `${gameState.gold} G`;
    document.getElementById("ui-wave").innerText = `${gameState.wave} 단계`;
    document.getElementById("ui-timer").innerText = `${gameState.waveTimer.toFixed(1)}초`;
    document.getElementById("ui-enemies").innerText = `${gameState.enemies.length} / ${gameState.maxEnemies}`;

    const r = gameState.rates;
    document.getElementById("ui-rates-text").innerText = `일반: ${r.common.toFixed(0)}% | 희귀: ${r.rare.toFixed(0)}% | 영웅: ${r.epic.toFixed(0)}% | 전설: ${r.legendary.toFixed(1)}%`;

    ["common", "rare", "epic", "legendary"].forEach(g => {
        document.getElementById(`lvl-${g}`).innerText = gameState.upgrades[g];
    });
}

function resetGame() { initGame(); }

initGame();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(html_game_code, height=780, scrolling=False)
