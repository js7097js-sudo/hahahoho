import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="운빨존많겜: 몬스터&디펜스 파라다이스",
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

# 60FPS HTML5 Canvas + 고급 커스텀 아바타 디펜스 엔진
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
        background: #11131d;
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
    .status-value { font-size: 18px; color: #ffd700; font-weight: 800; }

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
        <h2 style="text-align: center; color: #ffcc00; font-size: 18px;">🎲 운빨존많겜 디펜스</h2>
        
        <div class="status-bar">
            <div class="status-item"><span class="status-label">보유 골드</span><span id="ui-gold" class="status-value">300 G</span></div>
            <div class="status-item"><span class="status-label">현재 웨이브</span><span id="ui-wave" class="status-value" style="color:#00ffcc;">1</span></div>
            <div class="status-item"><span class="status-label">웨이브 타이머</span><span id="ui-timer" class="status-value" style="color:#ff6699;">15.0초</span></div>
            <div class="status-item"><span class="status-label">적 / 최대한도</span><span id="ui-enemies" class="status-value" style="color:#ff4444;">0 / 100</span></div>
        </div>

        <button class="action-btn primary" onclick="drawUnit()">
            <span>🎲 유닛 뽑기 (동물/사람)</span>
            <span id="ui-gacha-cost">50 G</span>
        </button>

        <button class="action-btn" onclick="upgradeGachaRates()">
            <span>📈 가챠 확률 강화</span>
            <span id="ui-rate-up-cost">80 G</span>
        </button>

        <div class="gacha-rates" id="ui-rates-text">일반: 75% | 희귀: 20% | 영웅: 4% | 전설: 1%</div>

        <div class="section-title">⚔️ 등급별 공격력 강화</div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px;">
            <button class="action-btn" onclick="upgradeClass('common')" style="font-size:10px; flex-direction:column; padding:6px;">일반(Lv.<span id="lvl-common">1</span>)<br><span id="cost-common">30G</span></button>
            <button class="action-btn" onclick="upgradeClass('rare')" style="font-size:10px; flex-direction:column; padding:6px; border-color:#1e90ff;">희귀(Lv.<span id="lvl-rare">1</span>)<br><span id="cost-rare">60G</span></button>
            <button class="action-btn" onclick="upgradeClass('epic')" style="font-size:10px; flex-direction:column; padding:6px; border-color:#9932cc;">영웅(Lv.<span id="lvl-epic">1</span>)<br><span id="cost-epic">120G</span></button>
            <button class="action-btn" onclick="upgradeClass('legendary')" style="font-size:10px; flex-direction:column; padding:6px; border-color:#ff8c00;">전설(Lv.<span id="lvl-legendary">1</span>)<br><span id="cost-legendary">250G</span></button>
        </div>

        <div class="section-title">🧪 유닛 합성소</div>
        <div style="display: flex; gap: 6px;">
            <button class="action-btn" onclick="combineSub('common')" style="flex:1; font-size:11px; justify-content:center;">일반 3개 ➔ 희귀</button>
            <button class="action-btn" onclick="combineSub('rare')" style="flex:1; font-size:11px; justify-content:center;">희귀 3개 ➔ 영웅</button>
        </div>

        <div class="section-title">👑 신화 등급 강림 (전설 소모)</div>
        <div id="mythic-recipes-list"></div>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// --- [유닛 데이터베이스: 동물 & 사람 형상 컨셉] ---
const UNITS_DB = {
    common: [
        { id: "c1", name: "돌맹이 꼬마전사", atk: 14, type: "human_boy", color: "#a0a0a0" },
        { id: "c2", name: "견습 아기궁수", atk: 16, type: "elf_kid", color: "#d2b48c" },
        { id: "c3", name: "초록 둥글 슬라임", atk: 11, type: "slime_pet", color: "#2ecc71" },
        { id: "c4", name: "다람쥐 투사", atk: 18, type: "squirrel", color: "#e67e22" }
    ],
    rare: [
        { id: "r1", name: "화염 마법사", atk: 55, type: "wizard", color: "#ff6b6b" },
        { id: "r2", name: "철갑 라이거 騎士", atk: 50, type: "liger_knight", color: "#3498db" },
        { id: "r3", name: "흑표범 암살자", atk: 65, type: "panther_assassin", color: "#2c3e50" },
        { id: "r4", name: "번개 호랑이 사제", atk: 60, type: "tiger_priest", color: "#f1c40f" }
    ],
    epic: [
        { id: "e1", name: "서리여왕 엘프", atk: 200, type: "ice_queen", color: "#00d2d3" },
        { id: "e2", name: "광전사 울버린", atk: 240, type: "berserker", color: "#ff5252" },
        { id: "e3", name: "메카 사이보그 사자", atk: 220, type: "mecha_lion", color: "#ff9f43" },
        { id: "e4", name: "암흑 흑마법사", atk: 190, type: "dark_wizard", color: "#8854d0" }
    ],
    legendary: [
        { id: "l1", name: "천공의 황금 드래곤", atk: 800, type: "golden_dragon", color: "#fffa65" },
        { id: "l2", name: "지옥의 아수라왕", atk: 900, type: "asura_demon", color: "#ff3838" },
        { id: "l3", name: "시간의 수호자 울프", atk: 750, type: "time_wolf", color: "#48dbfb" },
        { id: "l4", name: "빛의 성기사 판다", atk: 850, type: "holy_panda", color: "#ffffff" }
    ],
    mythic: [
        { id: "m1", name: "🔥 혼돈의 마신 드래곤", atk: 3800, type: "mythic_dragon", color: "#ff0055", req: "전설 1개 소모" },
        { id: "m2", name: "⚡ 제우스 라이거 갓", atk: 4300, type: "mythic_liger", color: "#ffff00", req: "전설 1개 소모" },
        { id: "m3", name: "❄️ 절대영도 빙원 여신", atk: 3600, type: "mythic_queen", color: "#00ffff", req: "전설 1개 소모" },
        { id: "m4", name: "💀 심연의 아수라 군주", atk: 4800, type: "mythic_asura", color: "#9b59b6", req: "전설 1개 소모" },
        { id: "m5", name: "🌟 창조의 신성 백호", atk: 5800, type: "mythic_tiger", color: "#ffffff", req: "전설 1개 소모" }
    ]
};

let gameState = {
    gold: 300,
    wave: 1,
    waveTimer: 15.0,
    maxEnemies: 100,
    gameOver: false,
    gachaCost: 50,
    rateCost: 80,
    rates: { common: 75.0, rare: 20.0, epic: 4.0, legendary: 1.0 },
    upgrades: { common: 1, rare: 1, epic: 1, legendary: 1 },
    board: new Array(20).fill(null),
    enemies: [],
    projectiles: [],
    particles: [],
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
    gameState.gold = 300;
    gameState.wave = 1;
    gameState.waveTimer = 15.0;
    gameState.gameOver = false;
    gameState.board = new Array(20).fill(null);
    gameState.enemies = [];
    gameState.projectiles = [];
    gameState.particles = [];
    gameState.rates = { common: 75.0, rare: 20.0, epic: 4.0, legendary: 1.0 };
    gameState.upgrades = { common: 1, rare: 1, epic: 1, legendary: 1 };
    document.getElementById("game-over-screen").style.display = "none";
    updateUI();
    renderMythicRecipes();
}

// --- [몬스터 생성 (오거/좀비 및 보스)] ---
function spawnEnemy() {
    const isBoss = (gameState.wave % 5 === 0) && (gameState.enemies.filter(e => e.isBoss).length === 0);
    const baseHp = 100 * Math.pow(1.28, gameState.wave - 1);
    
    // 몬스터 외형 타입 분류 (오거, 좀비, 보스 아머오거/네크로맨서)
    const mTypes = ["zombie", "orc_grunt", "skeleton", "mutant_ogre"];
    const chosenType = isBoss ? (gameState.wave % 10 === 0 ? "boss_necromancer" : "boss_ogre_lord") : mTypes[Math.floor(Math.random() * mTypes.length)];

    gameState.enemies.push({
        id: Math.random(),
        angle: 0,
        speed: isBoss ? 0.38 : (chosenType === "skeleton" ? 0.85 : 0.6),
        hp: isBoss ? baseHp * 9 : baseHp,
        maxHp: isBoss ? baseHp * 9 : baseHp,
        isBoss: isBoss,
        type: chosenType,
        radius: isBoss ? 28 : 15,
        color: isBoss ? "#ff0055" : (chosenType === "zombie" ? "#55efc4" : "#e17055")
    });
}

// --- [뽑기 및 안전 검증] ---
function drawUnit() {
    if (gameState.gold < gameState.gachaCost) {
        alert("❌ 골드가 부족합니다! 적을 처치하여 골드를 모으세요!");
        return;
    }
    
    let emptyIdx = gameState.board.findIndex(slot => slot === null);
    if (emptyIdx === -1) {
        alert("⚠️ 필드 20칸이 가득 찼습니다! 유닛을 합성하거나 해제하세요.");
        return;
    }

    gameState.gold -= gameState.gachaCost;

    const rand = Math.random() * 100;
    let grade = "common";
    if (rand < gameState.rates.legendary) grade = "legendary";
    else if (rand < gameState.rates.legendary + gameState.rates.epic) grade = "epic";
    else if (rand < gameState.rates.legendary + gameState.rates.epic + gameState.rates.rare) grade = "rare";

    const template = UNITS_DB[grade][Math.floor(Math.random() * UNITS_DB[grade].length)];

    gameState.board[emptyIdx] = {
        ...template,
        grade: grade,
        count: 1,
        lastAttack: 0,
        attackSpeed: 1.1
    };

    updateUI();
}

function upgradeGachaRates() {
    if (gameState.gold < gameState.rateCost) { alert("골드가 부족합니다!"); return; }
    if (gameState.rates.common <= 20) { alert("최대 확률입니다!"); return; }

    gameState.gold -= gameState.rateCost;
    gameState.rates.common -= 5;
    gameState.rates.rare += 3;
    gameState.rates.epic += 1.5;
    gameState.rates.legendary += 0.5;
    updateUI();
}

function upgradeClass(grade) {
    const costMap = { common: 30, rare: 60, epic: 120, legendary: 250 };
    const cost = costMap[grade] * gameState.upgrades[grade];
    if (gameState.gold < cost) { alert("골드가 부족합니다!"); return; }

    gameState.gold -= cost;
    gameState.upgrades[grade]++;
    updateUI();
}

function combineSub(grade) {
    const targetGrade = grade === "common" ? "rare" : "epic";
    let matches = [];
    gameState.board.forEach((slot, idx) => {
        if (slot && slot.grade === grade) {
            for (let i = 0; i < slot.count; i++) matches.push(idx);
        }
    });

    if (matches.length < 3) { alert(`${grade.toUpperCase()} 유닛이 3마리 이상 필요합니다!`); return; }

    let removed = 0;
    for (let idx of matches) {
        if (removed >= 3) break;
        gameState.board[idx].count--;
        if (gameState.board[idx].count === 0) gameState.board[idx] = null;
        removed++;
    }

    let emptyIdx = gameState.board.findIndex(slot => slot === null);
    const template = UNITS_DB[targetGrade][Math.floor(Math.random() * UNITS_DB[targetGrade].length)];
    gameState.board[emptyIdx] = {
        ...template,
        grade: targetGrade,
        count: 1,
        lastAttack: 0,
        attackSpeed: 1.1
    };
    updateUI();
}

function summonMythic(mIndex) {
    const legIdx = gameState.board.findIndex(slot => slot && slot.grade === "legendary");
    if (legIdx === -1) { alert("⚠️ 소환 재료인 [전설 유닛]이 필드에 필요합니다!"); return; }

    gameState.board[legIdx].count--;
    if (gameState.board[legIdx].count === 0) gameState.board[legIdx] = null;

    let emptyIdx = gameState.board.findIndex(slot => slot === null);
    if (emptyIdx === -1) emptyIdx = legIdx;

    const template = UNITS_DB.mythic[mIndex];
    gameState.board[emptyIdx] = {
        ...template,
        grade: "mythic",
        count: 1,
        lastAttack: 0,
        attackSpeed: 1.5
    };
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
                    <div class="recipe-req">ATK: ${m.atk} | ${m.req}</div>
                </div>
                <button class="action-btn" style="padding:4px 8px; font-size:11px; border-color:#ff0055;" onclick="summonMythic(${idx})">강림</button>
            </div>
        `;
    });
}

// --- [60FPS 루프 및 그래픽 렌더러] ---
function gameLoop(now) {
    const dt = (now - gameState.lastTime) / 1000;
    gameState.lastTime = now;

    if (!gameState.gameOver) {
        updateGame(dt);
    }
    renderGame();
    requestAnimationFrame(gameLoop);
}

function updateGame(dt) {
    gameState.waveTimer -= dt;
    if (gameState.waveTimer <= 0) {
        gameState.wave++;
        gameState.waveTimer = 15.0;
    }

    gameState.spawnTimer += dt;
    const spawnInterval = Math.max(0.35, 1.2 - gameState.wave * 0.03);
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

    // 공격 및 투사체 발사
    const currentTime = performance.now() / 1000;
    gameState.board.forEach((slot, tileIdx) => {
        if (!slot) return;

        if (currentTime - slot.lastAttack >= (1 / slot.attackSpeed)) {
            const tile = GRID_TILES[tileIdx];
            const ux = tile.x + 35, uy = tile.y + 35;
            let closestEnemy = null;
            let minDist = 320;

            gameState.enemies.forEach(e => {
                const ex = TRACK.centerX + Math.cos(e.angle) * TRACK.radius;
                const ey = TRACK.centerY + Math.sin(e.angle) * TRACK.radius;
                const dist = Math.hypot(ex - ux, ey - uy);
                if (dist < minDist) { minDist = dist; closestEnemy = e; }
            });

            if (closestEnemy) {
                slot.lastAttack = currentTime;
                const upLvl = gameState.upgrades[slot.grade] || 1;
                const finalAtk = slot.atk * slot.count * (1 + (upLvl - 1) * 0.25);

                gameState.projectiles.push({
                    x: ux, y: uy, target: closestEnemy, damage: finalAtk, color: slot.color, speed: 650
                });
            }
        }
    });

    // 투사체 처리
    for (let i = gameState.projectiles.length - 1; i >= 0; i--) {
        const p = gameState.projectiles[i];
        if (!gameState.enemies.includes(p.target)) { gameState.projectiles.splice(i, 1); continue; }

        const ex = TRACK.centerX + Math.cos(p.target.angle) * TRACK.radius;
        const ey = TRACK.centerY + Math.sin(p.target.angle) * TRACK.radius;
        const dx = ex - p.x, dy = ey - p.y;
        const dist = Math.hypot(dx, dy);

        if (dist < 15) {
            p.target.hp -= p.damage;
            if (p.target.hp <= 0) {
                gameState.gold += p.target.isBoss ? 160 : 12;
                const eIdx = gameState.enemies.indexOf(p.target);
                if (eIdx !== -1) gameState.enemies.splice(eIdx, 1);
            }
            gameState.projectiles.splice(i, 1);
        } else {
            p.x += (dx / dist) * p.speed * dt;
            p.y += (dy / dist) * p.speed * dt;
        }
    }
    updateUI();
}

// --- [고급 캐릭터 및 몬스터 캔버스 드로잉 아티스트 루틴] ---
function drawMonster(ctx, e, x, y) {
    ctx.save();
    ctx.translate(x, y);

    if (e.type === "zombie") {
        // 좀비 아바타 (초록 피부, 넝마 옷)
        ctx.fillStyle = "#55efc4";
        ctx.beginPath(); ctx.arc(0, -2, 11, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = "#ff3333"; // 눈
        ctx.fillRect(-4, -5, 3, 3); ctx.fillRect(2, -5, 3, 3);
        ctx.fillStyle = "#2d3436"; // 누더기 몸통
        ctx.fillRect(-8, 8, 16, 12);
    } else if (e.type === "orc_grunt" || e.type === "mutant_ogre") {
        // 오거/오크 아바타 (송곳니, 녹갈색 근육)
        ctx.fillStyle = e.type === "mutant_ogre" ? "#81ecec" : "#e17055";
        ctx.beginPath(); ctx.arc(0, -2, e.isBoss ? 22 : 14, 0, Math.PI*2); ctx.fill();
        // 뿔 / 송곳니
        ctx.fillStyle = "#fff";
        ctx.beginPath(); ctx.moveTo(-6, 8); ctx.lineTo(-10, 14); ctx.lineTo(-2, 10); ctx.fill();
        ctx.beginPath(); ctx.moveTo(6, 8); ctx.lineTo(10, 14); ctx.lineTo(2, 10); ctx.fill();
    } else if (e.isBoss) {
        // 보스 아바타 (왕관 쓴 네크로맨서 / 오거 수장)
        ctx.fillStyle = "#ff0055";
        ctx.beginPath(); ctx.arc(0, 0, 24, 0, Math.PI*2); ctx.fill();
        ctx.strokeStyle = "#ffd700"; ctx.lineWidth = 3; ctx.stroke();
        // 왕관
        ctx.fillStyle = "#ffd700";
        ctx.beginPath(); ctx.moveTo(-10, -20); ctx.lineTo(-15, -30); ctx.lineTo(0, -22); ctx.lineTo(15, -30); ctx.lineTo(10, -20); ctx.fill();
    } else {
        // 해골/기본 적
        ctx.fillStyle = "#dfe6e9";
        ctx.beginPath(); ctx.arc(0, 0, 12, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = "#000";
        ctx.fillRect(-4, -4, 3, 3); ctx.fillRect(2, -4, 3, 3);
    }
    ctx.restore();
}

function drawUnitAvatar(ctx, unit, x, y, size) {
    ctx.save();
    ctx.translate(x + size/2, y + size/2);

    // 등급별 오라
    ctx.fillStyle = unit.color + "33";
    ctx.beginPath(); ctx.arc(0, 0, size/2 - 4, 0, Math.PI*2); ctx.fill();

    // 사람/동물 형상 프로그래밍 아트
    if (unit.grade === "common") {
        // 귀여운 동물/꼬마 형상
        ctx.fillStyle = unit.color;
        ctx.beginPath(); ctx.arc(0, 2, 16, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = "#fff";
        ctx.fillRect(-5, -3, 4, 4); ctx.fillRect(2, -3, 4, 4);
    } else if (unit.grade === "rare") {
        // 무협/마법사 사람 형상
        ctx.fillStyle = unit.color;
        ctx.beginPath(); ctx.arc(0, -4, 14, 0, Math.PI*2); ctx.fill();
        // 모자/마법 로브
        ctx.fillStyle = "#ffffff";
        ctx.beginPath(); ctx.moveTo(0, -26); ctx.lineTo(-12, -10); ctx.lineTo(12, -10); ctx.fill();
    } else if (unit.grade === "epic") {
        // 강력한 엘프/전사 형상
        ctx.fillStyle = unit.color;
        ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI*2); ctx.fill();
        ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();
    } else if (unit.grade === "legendary") {
        // 전설의 드래곤/수호자 형상
        ctx.fillStyle = unit.color;
        ctx.beginPath(); ctx.arc(0, 0, 22, 0, Math.PI*2); ctx.fill();
        ctx.shadowBlur = 12; ctx.shadowColor = unit.color;
        ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3; ctx.stroke();
    } else {
        // 신화 등급 강림 형상 (오라 번쩍임)
        ctx.fillStyle = unit.color;
        ctx.beginPath(); ctx.arc(0, 0, 25, 0, Math.PI*2); ctx.fill();
        ctx.shadowBlur = 20; ctx.shadowColor = "#ff0055";
        ctx.strokeStyle = "#ffd700"; ctx.lineWidth = 4; ctx.stroke();
    }

    ctx.restore();
}

function renderGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 원형 트랙
    ctx.beginPath();
    ctx.arc(TRACK.centerX, TRACK.centerY, TRACK.radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#23283d"; ctx.lineWidth = 28; ctx.stroke();
    ctx.beginPath();
    ctx.arc(TRACK.centerX, TRACK.centerY, TRACK.radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#3b4366"; ctx.lineWidth = 2; ctx.setLineDash([8, 8]); ctx.stroke();
    ctx.setLineDash([]);

    // 20칸 타일
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

        drawMonster(ctx, e, ex, ey);

        if (e.isBoss) {
            ctx.font = "bold 11px sans-serif"; ctx.fillStyle = "#ff3366"; ctx.textAlign = "center";
            ctx.fillText("👑 BOSS", ex, ey - e.radius - 14);
        }
    });

    // 투사체
    gameState.projectiles.forEach(p => {
        ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, Math.PI*2); ctx.fillStyle = p.color; ctx.fill();
    });
}

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
