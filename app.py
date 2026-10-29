import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="운빨존많겜: 무한 실시간 디펜스",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 앱 스타일링 (여백 최적화)
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
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

# 60FPS HTML5 Canvas 기반의 완전한 실시간 모바일 디펜스 게임 엔진
html_game_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body { background-color: #0d0e15; color: #fff; font-family: 'Pretendard', 'Noto Sans KR', sans-serif; overflow: hidden; }
    
    #game-container {
        display: flex;
        flex-direction: row;
        width: 100vw;
        height: 100vh;
        background: #12131c;
    }

    #canvas-container {
        position: relative;
        flex: 1;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #090a0f;
    }

    canvas {
        border: 2px solid #2a2d3d;
        border-radius: 12px;
        box-shadow: 0 0 30px rgba(0,0,0,0.8);
        background: #141622;
    }

    #ui-panel {
        width: 420px;
        height: 100%;
        background: #1a1c29;
        border-left: 2px solid #2e3248;
        display: flex;
        flex-direction: column;
        padding: 15px;
        gap: 12px;
        overflow-y: auto;
    }

    .status-bar {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        background: #232638;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #363b57;
    }

    .status-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .status-label { font-size: 11px; color: #8e95b3; font-weight: bold; }
    .status-value { font-size: 18px; color: #ffd700; font-weight: 800; }

    .action-btn {
        background: linear-gradient(135deg, #4a5270, #2f3448);
        color: white;
        border: 1px solid #5d668c;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.15s ease;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .action-btn:hover { background: linear-gradient(135deg, #5c668c, #3d435e); transform: translateY(-1px); }
    .action-btn:active { transform: translateY(1px); }
    .action-btn.primary { background: linear-gradient(135deg, #ff9900, #cc7a00); border-color: #ffaa22; color: #111; font-size: 16px; }

    .section-title { font-size: 14px; font-weight: bold; color: #4deeea; margin-top: 5px; border-bottom: 1px solid #2e3248; padding-bottom: 4px; }

    .gacha-rates { font-size: 11px; color: #a0a7cc; background: #12131a; padding: 8px; border-radius: 6px; }

    /* 조합 공방 스타일 */
    .tab-container { display: flex; gap: 5px; }
    .tab-btn { flex: 1; padding: 8px; font-size: 12px; background: #25283b; border: none; color: #8890b5; border-radius: 6px; cursor: pointer; }
    .tab-btn.active { background: #3b4263; color: #fff; font-weight: bold; }

    .recipe-card {
        background: #212435;
        border: 1px solid #323752;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .recipe-info { font-size: 12px; }
    .recipe-name { font-weight: bold; color: #ff0055; }
    .recipe-req { font-size: 10px; color: #9aa1c4; }

    /* 모달 */
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
    #game-over-screen h1 { font-size: 48px; color: #ff3366; text-shadow: 0 0 20px #ff0055; margin-bottom: 10px; }
</style>
</head>
<body>

<div id="game-container">
    <div id="canvas-container">
        <canvas id="gameCanvas" width="750" height="750"></canvas>
        <div id="game-over-screen">
            <h1>GAME OVER</h1>
            <p id="final-wave-text" style="font-size: 20px; color: #ccc; margin-bottom: 20px;">최대 웨이브: 1</p>
            <button class="action-btn primary" onclick="resetGame()" style="width: 200px; justify-content: center;">🔄 다시 시작</button>
        </div>
    </div>

    <div id="ui-panel">
        <h2 style="text-align: center; color: #ffcc00; font-size: 20px; letter-spacing: 1px;">🎲 운빨존많겜 60FPS</h2>
        
        <div class="status-bar">
            <div class="status-item"><span class="status-label">보유 골드</span><span id="ui-gold" class="status-value">300 G</span></div>
            <div class="status-item"><span class="status-label">현재 웨이브</span><span id="ui-wave" class="status-value" style="color:#00ffcc;">1</span></div>
            <div class="status-item"><span class="status-label">웨이브 남은시간</span><span id="ui-timer" class="status-value" style="color:#ff6699;">15.0초</span></div>
            <div class="status-item"><span class="status-label">필드 적 / 최대</span><span id="ui-enemies" class="status-value" style="color:#ff4444;">0 / 100</span></div>
        </div>

        <button class="action-btn primary" onclick="drawUnit()">
            <span>🎲 유닛 뽑기</span>
            <span id="ui-gacha-cost">50 G</span>
        </button>

        <button class="action-btn" onclick="upgradeGachaRates()">
            <span>📈 뽑기 확률 강화</span>
            <span id="ui-rate-up-cost">80 G</span>
        </button>

        <div class="gacha-rates" id="ui-rates-text">
            일반: 75.0% | 희귀: 20.0% | 영웅: 4.0% | 전설: 1.0%
        </div>

        <div class="section-title">⚔️ 등급별 공격력 강화</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
            <button class="action-btn" onclick="upgradeClass('common')" style="font-size:11px;">일반 (Lv.<span id="lvl-common">1</span>)<br><span id="cost-common">30G</span></button>
            <button class="action-btn" onclick="upgradeClass('rare')" style="font-size:11px; border-color:#1e90ff;">희귀 (Lv.<span id="lvl-rare">1</span>)<br><span id="cost-rare">60G</span></button>
            <button class="action-btn" onclick="upgradeClass('epic')" style="font-size:11px; border-color:#9932cc;">영웅 (Lv.<span id="lvl-epic">1</span>)<br><span id="cost-epic">120G</span></button>
            <button class="action-btn" onclick="upgradeClass('legendary')" style="font-size:11px; border-color:#ff8c00;">전설 (Lv.<span id="lvl-legendary">1</span>)<br><span id="cost-legendary">250G</span></button>
        </div>

        <div class="section-title">🧪 유닛 합성 & 신화 소환</div>
        <div style="display: flex; gap: 6px;">
            <button class="action-btn" onclick="combineSub('common')" style="flex:1; font-size:11px; justify-content:center;">일반 3개 ➔ 희귀</button>
            <button class="action-btn" onclick="combineSub('rare')" style="flex:1; font-size:11px; justify-content:center;">희귀 3개 ➔ 영웅</button>
        </div>

        <div class="section-title">👑 신화 소환 공방 (전설 필수)</div>
        <div id="mythic-recipes-list"></div>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// --- [유닛 데이터베이스] ---
const UNITS_DB = {
    common: [
        { id: "c1", name: "돌멩이 골렘", atk: 15, color: "#a0a0a0", icon: "🪨" },
        { id: "c2", name: "견습 궁수", atk: 18, color: "#8b5a2b", icon: "🏹" },
        { id: "c3", name: "아기 슬라임", atk: 12, color: "#55efc4", icon: "🟢" },
        { id: "c4", name: "꼬마 법사", atk: 22, color: "#74b9ff", icon: "🪄" }
    ],
    rare: [
        { id: "r1", name: "화염 마법사", atk: 60, color: "#ff7675", icon: "🔥" },
        { id: "r2", name: "강철 기사", atk: 55, color: "#0984e3", icon: "🛡️" },
        { id: "r3", name: "바람의 암살자", atk: 70, color: "#00b894", icon: "🗡️" },
        { id: "r4", name: "번개 사제", atk: 65, color: "#fdcb6e", icon: "⚡" }
    ],
    epic: [
        { id: "e1", name: "서리 여왕", atk: 220, color: "#00cec9", icon: "❄️" },
        { id: "e2", name: "광전사 발키리", atk: 260, color: "#d63031", icon: "🪓" },
        { id: "e3", name: "메카 캐논", atk: 240, color: "#e17055", icon: "🤖" },
        { id: "e4", name: "암흑 소울킹", atk: 210, color: "#6c5ce7", icon: "💀" }
    ],
    legendary: [
        { id: "l1", name: "천공 드래곤", atk: 850, color: "#fd79a8", icon: "🐉" },
        { id: "l2", name: "지옥 파괴신", atk: 950, color: "#ff4757", icon: "👹" },
        { id: "l3", name: "시간 수호자", atk: 800, color: "#eccc68", icon: "⏳" },
        { id: "l4", name: "빛의 성심주", atk: 900, color: "#ffffff", icon: "🌟" }
    ],
    mythic: [
        { id: "m1", name: "🔥 혼돈 종말자", atk: 4000, color: "#ff0055", icon: "🌌", req: "전설 1개 소모" },
        { id: "m2", name: "⚡ 제우스 현신", atk: 4500, color: "#ffff00", icon: "🌩️", req: "전설 1개 소모" },
        { id: "m3", name: "❄️ 절대영도 여신", atk: 3800, color: "#00ffff", icon: "🧊", req: "전설 1개 소모" },
        { id: "m4", name: "💀 심연의 군주", atk: 5000, color: "#a000ff", icon: "👑", req: "전설 1개 소모" },
        { id: "m5", name: "🌟 창조의 스피릿", atk: 6000, color: "#ffffff", icon: "☸️", req: "전설 1개 소모" }
    ]
};

// --- [게임 글로벌 상태] ---
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
    board: new Array(20).fill(null), // 20칸 필드
    enemies: [],
    projectiles: [],
    particles: [],
    spawnTimer: 0,
    lastTime: performance.now()
};

// 트랙 정보 (원형 트랙: 중심 (375,375), 반지름 300)
const TRACK = {
    centerX: 375,
    centerY: 375,
    radius: 290
};

// 타일 그리드 배치 (5행 4열 = 20칸, 중앙 240x240 영역)
const GRID_TILES = [];
const rows = 5, cols = 4;
const startX = 225, startY = 200, tileSize = 70, gap = 10;
for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
        GRID_TILES.push({
            x: startX + c * (tileSize + gap),
            y: startY + r * (tileSize + gap),
            size: tileSize
        });
    }
}

// 초기화
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

// --- [스폰 & 몬스터 로직] ---
function spawnEnemy() {
    const isBoss = (gameState.wave % 5 === 0) && (gameState.enemies.filter(e => e.isBoss).length === 0);
    const baseHp = 100 * Math.pow(1.28, gameState.wave - 1);
    
    gameState.enemies.push({
        id: Math.random(),
        angle: 0, // 0 라디안에서 시작 (원형 이동)
        speed: isBoss ? 0.4 : 0.7,
        hp: isBoss ? baseHp * 8 : baseHp,
        maxHp: isBoss ? baseHp * 8 : baseHp,
        isBoss: isBoss,
        radius: isBoss ? 26 : 14,
        color: isBoss ? "#ff0055" : (gameState.wave % 5 === 0 ? "#ff9900" : "#a29bfe")
    });
}

// --- [가챠 & 강화 시스템] ---
function drawUnit() {
    if (gameState.gold < gameState.gachaCost) return alert("골드가 부족합니다!");
    
    // 빈 칸 찾기
    let emptyIdx = gameState.board.findIndex(slot => slot === null);
    if (emptyIdx === -1) return alert("필드 20칸이 가득 찼습니다! 유닛을 합성하세요.");

    gameState.gold -= gameState.gachaCost;

    // 확률 계산
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
        attackSpeed: 1.0 // 초당 공격
    };

    updateUI();
}

function upgradeGachaRates() {
    if (gameState.gold < gameState.rateCost) return alert("골드가 부족합니다!");
    if (gameState.rates.common <= 20) return alert("최대 강화 단계입니다!");

    gameState.gold -= gameState.rateCost;
    gameState.rates.common -= 5;
    gameState.rates.rare += 3;
    gameState.rates.epic += 1.5;
    gameState.rates.legendary += 0.5;

    updateUI();
}

function upgradeClass(grade) {
    const cost = { common: 30, rare: 60, epic: 120, legendary: 250 }[grade] * gameState.upgrades[grade];
    if (gameState.gold < cost) return alert("골드가 부족합니다!");

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

    if (matches.length < 3) return alert(`${grade.toUpperCase()} 유닛이 3마리 이상 필요합니다!`);

    // 3마리 제거
    let removed = 0;
    for (let idx of matches) {
        if (removed >= 3) break;
        gameState.board[idx].count--;
        if (gameState.board[idx].count === 0) gameState.board[idx] = null;
        removed++;
    }

    // 새 희귀/영웅 배치
    let emptyIdx = gameState.board.findIndex(slot => slot === null);
    const template = UNITS_DB[targetGrade][Math.floor(Math.random() * UNITS_DB[targetGrade].length)];
    gameState.board[emptyIdx] = {
        ...template,
        grade: targetGrade,
        count: 1,
        lastAttack: 0,
        attackSpeed: 1.0
    };

    updateUI();
}

function summonMythic(mIndex) {
    const legIdx = gameState.board.findIndex(slot => slot && slot.grade === "legendary");
    if (legIdx === -1) return alert("소환 재료인 [전설 유닛]이 필드에 최소 1개 필요합니다!");

    // 전설 유닛 1개 소모
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

    // 폭죽 효과
    for(let i=0; i<30; i++) {
        gameState.particles.push({
            x: GRID_TILES[emptyIdx].x + 35,
            y: GRID_TILES[emptyIdx].y + 35,
            vx: (Math.random() - 0.5) * 8,
            vy: (Math.random() - 0.5) * 8,
            color: template.color,
            life: 1.0
        });
    }

    updateUI();
}

function renderMythicRecipes() {
    const container = document.getElementById("mythic-recipes-list");
    container.innerHTML = "";
    UNITS_DB.mythic.forEach((m, idx) => {
        container.innerHTML += `
            <div class="recipe-card">
                <div class="recipe-info">
                    <span class="recipe-name">${m.icon} ${m.name}</span>
                    <div class="recipe-req">ATK: ${m.atk} | ${m.req}</div>
                </div>
                <button class="action-btn" style="padding:4px 8px; font-size:11px; border-color:#ff0055;" onclick="summonMythic(${idx})">소환</button>
            </div>
        `;
    });
}

// --- [60FPS 메인 게임 루프] ---
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
    // 1. 웨이브 타이머
    gameState.waveTimer -= dt;
    if (gameState.waveTimer <= 0) {
        gameState.wave++;
        gameState.waveTimer = 15.0;
    }

    // 2. 몬스터 스폰 (웨이브 지속적으로 일정간격 스폰)
    gameState.spawnTimer += dt;
    const spawnInterval = Math.max(0.4, 1.2 - gameState.wave * 0.03);
    if (gameState.spawnTimer >= spawnInterval) {
        gameState.spawnTimer = 0;
        spawnEnemy();
    }

    // 3. 몬스터 위치 이동 (원형 궤도 돌기)
    gameState.enemies.forEach(e => {
        e.angle += (e.speed * dt); // 라디안 이동
    });

    // 4. 게임 오버 조건 체크 (적 100명 이상)
    if (gameState.enemies.length >= gameState.maxEnemies) {
        gameState.gameOver = true;
        document.getElementById("final-wave-text").innerText = `최대 달성 웨이브: ${gameState.wave} 단계`;
        document.getElementById("game-over-screen").style.display = "flex";
    }

    // 5. 유닛 공격 타겟팅 및 투사체 발생
    const currentTime = performance.now() / 1000;
    gameState.board.forEach((slot, tileIdx) => {
        if (!slot) return;

        if (currentTime - slot.lastAttack >= (1 / slot.attackSpeed)) {
            // 사거리 내 가장 가까운/앞선 적 탐색
            const tile = GRID_TILES[tileIdx];
            const ux = tile.x + 35, uy = tile.y + 35;

            let closestEnemy = null;
            let minDist = 320; // 공격 사거리

            gameState.enemies.forEach(e => {
                const ex = TRACK.centerX + Math.cos(e.angle) * TRACK.radius;
                const ey = TRACK.centerY + Math.sin(e.angle) * TRACK.radius;
                const dist = Math.hypot(ex - ux, ey - uy);
                if (dist < minDist) {
                    minDist = dist;
                    closestEnemy = e;
                }
            });

            if (closestEnemy) {
                slot.lastAttack = currentTime;
                // 공격 투사체 발사
                const upLvl = gameState.upgrades[slot.grade] || 1;
                const finalAtk = slot.atk * slot.count * (1 + (upLvl - 1) * 0.25);

                gameState.projectiles.push({
                    x: ux, y: uy,
                    target: closestEnemy,
                    damage: finalAtk,
                    color: slot.color,
                    speed: 600
                });
            }
        }
    });

    // 6. 투사체 이동 및 적 피격
    for (let i = gameState.projectiles.length - 1; i >= 0; i--) {
        const p = gameState.projectiles[i];
        if (!gameState.enemies.includes(p.target)) {
            gameState.projectiles.splice(i, 1);
            continue;
        }

        const ex = TRACK.centerX + Math.cos(p.target.angle) * TRACK.radius;
        const ey = TRACK.centerY + Math.sin(p.target.angle) * TRACK.radius;
        const dx = ex - p.x;
        const dy = ey - p.y;
        const dist = Math.hypot(dx, dy);

        if (dist < 15) {
            // 히트!
            p.target.hp -= p.damage;
            
            // 피격 이펙트 입자
            for(let k=0; k<5; k++) {
                gameState.particles.push({
                    x: ex, y: ey,
                    vx: (Math.random() - 0.5) * 4,
                    vy: (Math.random() - 0.5) * 4,
                    color: p.color,
                    life: 0.4
                });
            }

            // 적 사망 처리
            if (p.target.hp <= 0) {
                const killReward = p.target.isBoss ? 150 : 12;
                gameState.gold += killReward;
                const eIdx = gameState.enemies.indexOf(p.target);
                if (eIdx !== -1) gameState.enemies.splice(eIdx, 1);
            }

            gameState.projectiles.splice(i, 1);
        } else {
            p.x += (dx / dist) * p.speed * dt;
            p.y += (dy / dist) * p.speed * dt;
        }
    }

    // 7. 입자(파티클) 업데이트
    for (let i = gameState.particles.length - 1; i >= 0; i--) {
        const pt = gameState.particles[i];
        pt.x += pt.vx;
        pt.y += pt.vy;
        pt.life -= dt * 2;
        if (pt.life <= 0) gameState.particles.splice(i, 1);
    }

    updateUI();
}

// --- [60FPS 캔버스 렌더링] ---
function renderGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. 원형 몬스터 이동 트랙 그리기
    ctx.beginPath();
    ctx.arc(TRACK.centerX, TRACK.centerY, TRACK.radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#2e3450";
    ctx.lineWidth = 28;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(TRACK.centerX, TRACK.centerY, TRACK.radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#434b73";
    ctx.lineWidth = 2;
    ctx.setLineDash([8, 8]);
    ctx.stroke();
    ctx.setLineDash([]);

    // 2. 20칸 필드 타일 그리기
    GRID_TILES.forEach((tile, idx) => {
        const unit = gameState.board[idx];

        ctx.fillStyle = "#1b1d2e";
        ctx.strokeStyle = "#2c314a";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.roundRect(tile.x, tile.y, tile.size, tile.size, 8);
        ctx.fill();
        ctx.stroke();

        if (unit) {
            // 유닛 후광 및 테두리
            ctx.fillStyle = unit.color + "22";
            ctx.beginPath();
            ctx.roundRect(tile.x+2, tile.y+2, tile.size-4, tile.size-4, 6);
            ctx.fill();

            ctx.strokeStyle = unit.color;
            ctx.lineWidth = 2;
            ctx.stroke();

            // 유닛 아이콘 & 이름
            ctx.font = "24px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(unit.icon, tile.x + 35, tile.y + 28);

            // 유닛 중첩 수 및 이름
            ctx.font = "bold 10px sans-serif";
            ctx.fillStyle = "#ffffff";
            ctx.fillText(`${unit.name}`, tile.x + 35, tile.y + 52);

            if (unit.count > 1) {
                ctx.fillStyle = "#ffcc00";
                ctx.font = "bold 11px sans-serif";
                ctx.fillText(`x${unit.count}`, tile.x + 60, tile.y + 15);
            }
        } else {
            ctx.font = "10px sans-serif";
            ctx.fillStyle = "#484f73";
            ctx.textAlign = "center";
            ctx.fillText(`#${idx+1}`, tile.x + 35, tile.y + 38);
        }
    });

    // 3. 몬스터 렌더링
    gameState.enemies.forEach(e => {
        const ex = TRACK.centerX + Math.cos(e.angle) * TRACK.radius;
        const ey = TRACK.centerY + Math.sin(e.angle) * TRACK.radius;

        // 몬스터 체력바
        const hpPercent = Math.max(0, e.hp / e.maxHp);
        ctx.fillStyle = "#ff0000";
        ctx.fillRect(ex - 15, ey - e.radius - 8, 30, 4);
        ctx.fillStyle = "#00ffcc";
        ctx.fillRect(ex - 15, ey - e.radius - 8, 30 * hpPercent, 4);

        // 몬스터 바디
        ctx.beginPath();
        ctx.arc(ex, ey, e.radius, 0, Math.PI * 2);
        ctx.fillStyle = e.color;
        ctx.fill();
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = e.isBoss ? 3 : 1;
        ctx.stroke();

        // 보스 표시
        if (e.isBoss) {
            ctx.font = "bold 12px sans-serif";
            ctx.fillStyle = "#ffffff";
            ctx.textAlign = "center";
            ctx.fillText("👑BOSS", ex, ey - e.radius - 12);
        }
    });

    // 4. 공격 투사체 렌더링
    gameState.projectiles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
    });

    // 5. 파티클 이펙트
    gameState.particles.forEach(pt => {
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 3 * pt.life, 0, Math.PI * 2);
        ctx.fillStyle = pt.color;
        ctx.fill();
    });
}

function updateUI() {
    document.getElementById("ui-gold").innerText = `${gameState.gold} G`;
    document.getElementById("ui-wave").innerText = `${gameState.wave} 단계`;
    document.getElementById("ui-timer").innerText = `${gameState.waveTimer.toFixed(1)}초`;
    document.getElementById("ui-enemies").innerText = `${gameState.enemies.length} / ${gameState.maxEnemies}`;

    const r = gameState.rates;
    document.getElementById("ui-rates-text").innerText = 
        `일반: ${r.common.toFixed(1)}% | 희귀: ${r.rare.toFixed(1)}% | 영웅: ${r.epic.toFixed(1)}% | 전설: ${r.legendary.toFixed(1)}%`;

    ["common", "rare", "epic", "legendary"].forEach(g => {
        document.getElementById(`lvl-${g}`).innerText = gameState.upgrades[g];
    });
}

function resetGame() {
    initGame();
}

// 게임 실행
initGame();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

# Streamlit 내부에 60FPS 모바일 게임 캔버스 삽입
components.html(html_game_code, height=780, scrolling=False)
