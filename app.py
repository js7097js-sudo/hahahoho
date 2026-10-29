import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="운빨존많겜: 모바일 디펜스 파라다이스", page_icon="🎲", layout="wide"
)


# 게임 상태 초기화 함수
def init_game():
  st.session_state.gold = 300  # 시작 골드
  st.session_state.wave = 1
  st.session_state.enemies_count = 0  # 현재 필드에 쌓인 적 수
  st.session_state.max_enemies = 100  # 게임 오버 기준
  st.session_state.game_over = False
  st.session_state.victory = False

  # 유닛 필드 (총 20칸)
  st.session_state.board = [None] * 20

  # 등급별 유닛 정의 (일반 4종, 희귀 4종, 영웅 4종, 전설 4종, 신화 5종)
  st.session_state.units_def = {
      "common": [
          {"key": "c1", "name": "돌멩이 전사", "atk": 10, "cost": 0},
          {"key": "c2", "name": "나무꾼", "atk": 12, "cost": 0},
          {"key": "c3", "name": "슬라임 펫", "atk": 8, "cost": 0},
          {"key": "c4", "name": "견습 궁수", "atk": 15, "cost": 0},
      ],
      "rare": [
          {"key": "r1", "name": "화염 마법사", "atk": 45, "cost": 0},
          {"key": "r2", "name": "철갑 기사", "atk": 40, "cost": 0},
          {"key": "r3", "name": "바람의 암살자", "atk": 50, "cost": 0},
          {"key": "r4", "name": "번개 사제", "atk": 42, "cost": 0},
      ],
      "epic": [
          {"key": "e1", "name": "서리 여왕", "atk": 150, "cost": 0},
          {"key": "e2", "name": "광전사", "atk": 180, "cost": 0},
          {"key": "e3", "name": "메카닉 엔지니어", "atk": 160, "cost": 0},
          {"key": "e4", "name": "암흑 수호자", "atk": 140, "cost": 0},
      ],
      "legendary": [
          {"key": "l1", "name": "천공의 드래곤", "atk": 550, "cost": 0},
          {"key": "l2", "name": "지옥의 파괴자", "atk": 600, "cost": 0},
          {"key": "l3", "name": "시간의 수호자", "atk": 500, "cost": 0},
          {"key": "l4", "name": "빛의 심판자", "atk": 580, "cost": 0},
      ],
      "mythic": [
          {
              "key": "m1",
              "name": "🔥 혼돈의 파괴신",
              "atk": 2500,
              "recipe": "전설 1 + 일반 2",
          },
          {
              "key": "m2",
              "name": "⚡ 제우스의 현신",
              "atk": 2800,
              "recipe": "전설 1 + 영웅 1",
          },
          {
              "key": "m3",
              "name": "❄️ 절대영도 여신",
              "atk": 2400,
              "recipe": "전설 1 + 희귀 2",
          },
          {
              "key": "m4",
              "name": "💀 암흑 군주",
              "atk": 3000,
              "recipe": "전설 2 + 영웅 2",
          },
          {
              "key": "m5",
              "name": "🌟 무한의 창조자",
              "atk": 3500,
              "recipe": "전설 2 + 신화 재료",
          },
      ],
  }

  # 등급별 업그레이드 레벨
  st.session_state.upgrade_levels = {
      "common": 1,
      "rare": 1,
      "epic": 1,
      "legendary": 1,
  }

  # 뽑기 확률 시스템
  st.session_state.gacha_rates = {
      "common": 75.0,
      "rare": 20.0,
      "epic": 4.0,
      "legendary": 1.0,
  }

  # 웨이브 타이머 관련
  st.session_state.wave_start_time = time.time()


if "game_started" not in st.session_state:
  st.session_state.game_started = False
  init_game()

# UI 스타일링 커스텀
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎲 운빨존많겜: 모바일 디펜스 파라다이스")
st.markdown(
    "**50년 차 베테랑 개발자의 명작**: 오직 운과 전략으로 100명의 적을 막아내고"
    " 신화 유닛을 조합하세요!"
)

# 게임 시작 화면
if not st.session_state.game_started:
  if st.button("🚀 게임 시작하기", type="primary", use_container_width=True):
    st.session_state.game_started = True
    st.session_state.wave_start_time = time.time()
    st.rerun()

if st.session_state.game_started:

  # 웨이브당 적 생성 수 계산 함수 정의
  def get_spawn_rate(wave):
    return 15 + (wave * 3)

  # --- [1] 상단 대시보드 (상태바) ---
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.metric("💰 보유 골드", f"{st.session_state.gold} G")
  with col2:
    st.metric("🌊 현재 웨이브", f"{st.session_state.wave} 단계")
  with col3:
    elapsed = int(time.time() - st.session_state.wave_start_time)
    remaining = max(0, 15 - (elapsed % 15))
    st.metric("⏱️ 웨이브 타이머", f"{remaining}초")
  with col4:
    enemy_delta = st.session_state.enemies_count
    st.metric(
        "👾 쌓인 적",
        f"{enemy_delta} / {st.session_state.max_enemies}",
        delta=f"+{get_spawn_rate(st.session_state.wave)}"
        if not st.session_state.game_over
        else "정지",
        delta_color="inverse",
    )
  with col5:
    filled_slots = sum(1 for x in st.session_state.board if x is not None)
    st.metric("🗺️ 필드 칸수", f"{filled_slots} / 20 칸")

  # 웨이브 자동 진행 및 적 누적 로직
  if not st.session_state.game_over:
    current_time = time.time()
    if current_time - st.session_state.wave_start_time >= 15:
      st.session_state.wave += 1
      st.session_state.wave_start_time = current_time
      added_enemies = get_spawn_rate(st.session_state.wave)
      st.session_state.enemies_count += added_enemies

      # 유닛들이 적 자동 공격해서 처치
      total_dps_15s = 0
      for slot in st.session_state.board:
        if slot:
          base_atk = slot["atk"]
          grade = slot["grade"]
          up_lvl = (
              st.session_state.upgrade_levels.get(grade, 1)
              if grade != "mythic"
              else 5
          )
          total_dps_15s += base_atk * slot["count"] * (1 + (up_lvl - 1) * 0.2)

      killed_enemies = int(total_dps_15s / 10)
      st.session_state.enemies_count = max(
          0, st.session_state.enemies_count - killed_enemies
      )
      earned_gold = killed_enemies * 15
      st.session_state.gold += earned_gold

      if st.session_state.enemies_count >= st.session_state.max_enemies:
        st.session_state.game_over = True

  # 게임 오버 화면
  if st.session_state.game_over:
    st.error(
        "💀 **GAME OVER!** 적들이 100명을 넘겨서 필드를 점령했습니다! 운이"
        " 부족했네요."
    )
    if st.button("🔄 다시 도전하기"):
      init_game()
      st.session_state.game_started = True
      st.rerun()
    st.stop()

  st.divider()

  # --- [2] 메인 레이아웃: 좌측(뽑기 및 업그레이드), 우측(필드 및 조합) ---
  left_col, right_col = st.columns([1, 1.2])

  with left_col:
    st.subheader("🎰 유닛 뽑기 & 확률 강화")
    gacha_cost = 50
    st.markdown(f"현재 뽑기 비용: **{gacha_cost} 골드**")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
      if st.button("🎲 1회 뽑기", use_container_width=True):
        if st.session_state.gold >= gacha_cost:
          empty_idx = -1
          for idx, slot in enumerate(st.session_state.board):
            if slot is None:
              empty_idx = idx
              break

          if empty_idx == -1:
            st.warning("⚠️ 필드 20칸이 꽉 찼습니다! 조합을 통해 자리를 비우세요.")
          else:
            st.session_state.gold -= gacha_cost
            r = random.uniform(0, 100)
            c_rate = st.session_state.gacha_rates["common"]
            r_rate = c_rate + st.session_state.gacha_rates["rare"]
            e_rate = r_rate + st.session_state.gacha_rates["epic"]

            if r < c_rate:
              grade = "common"
            elif r < r_rate:
              grade = "rare"
            elif r < e_rate:
              grade = "epic"
            else:
              grade = "legendary"

            unit_template = random.choice(st.session_state.units_def[grade])

            st.session_state.board[empty_idx] = {
                "key": unit_template["key"],
                "name": unit_template["name"],
                "atk": unit_template["atk"],
                "grade": grade,
                "count": 1,
            }
            st.success(
                f"🎉 [{grade.upper()}] '{unit_template['name']}' 획득!"
            )
            st.rerun()
        else:
          st.error("❌ 골드가 부족합니다!")

    with col_g2:
      upgrade_rate_cost = 80
      if st.button(
          f"📈 확률 업그레이드 ({upgrade_rate_cost}G)",
          use_container_width=True,
      ):
        if st.session_state.gold >= upgrade_rate_cost:
          st.session_state.gold -= upgrade_rate_cost
          if st.session_state.gacha_rates["common"] > 20:
            st.session_state.gacha_rates["common"] -= 5.0
            st.session_state.gacha_rates["rare"] += 3.0
            st.session_state.gacha_rates["epic"] += 1.5
            st.session_state.gacha_rates["legendary"] += 0.5
            st.success("✨ 가챠 확률이 대폭 상승했습니다!")
            st.rerun()
          else:
            st.warning("🔥 뽑기 확률이 이미 최대치입니다!")
        else:
          st.error("❌ 골드가 부족합니다!")

    st.markdown("##### 📊 현재 뽑기 확률")
    rates = st.session_state.gacha_rates
    st.write(
        f"- 일반: {rates['common']:.1f}% | 희귀: {rates['rare']:.1f}% | 영웅:"
        f" {rates['epic']:.1f}% | 전설: {rates['legendary']:.1f}%"
    )

    st.markdown("---")
    st.subheader("🛠️ 등급별 유닛 공격력 강화")
    up_costs = {"common": 30, "rare": 60, "epic": 120, "legendary": 250}

    for grade_k, grade_name in [
        ("common", "일반 등급"),
        ("rare", "희귀 등급"),
        ("epic", "영웅 등급"),
        ("legendary", "전설 등급"),
    ]:
      cur_lvl = st.session_state.upgrade_levels[grade_k]
      c = up_costs[grade_k] * cur_lvl
      col_u1, col_u2 = st.columns([2, 1])
      with col_u1:
        st.text(f"{grade_name} (Lv.{cur_lvl})")
      with col_u2:
        if st.button(f"강화 ({c}G)", key=f"up_{grade_k}"):
          if st.session_state.gold >= c:
            st.session_state.gold -= c
            st.session_state.upgrade_levels[grade_k] += 1
            st.success(f"{grade_name} 강화 완료!")
            st.rerun()
          else:
            st.error("골드 부족!")

  with right_col:
    st.subheader("🗺️ 유닛 배치 필드 (20칸)")
    st.markdown(
        "같은 종류의 유닛은 **최대 3마리**까지 한 칸에 뭉칠 수 있습니다."
    )

    grid_cols = st.columns(4)
    for idx, slot in enumerate(st.session_state.board):
      col_target = grid_cols[idx % 4]
      with col_target:
        if slot is None:
          st.markdown(
              f"""<div style="border: 2px dashed #444; border-radius: 8px; padding: 12px; text-align: center; margin-bottom: 10px; color: #777;">
                        <b>#{idx+1} 빈 칸</b><br>비어 있음
                        </div>""",
              unsafe_allow_html=True,
          )
        else:
          grade_colors = {
              "common": "#888888",
              "rare": "#1e90ff",
              "epic": "#9932cc",
              "legendary": "#ff8c00",
              "mythic": "#ff0000",
          }
          g_color = grade_colors.get(slot["grade"], "#fff")
          st.markdown(
              f"""<div style="border: 2px solid {g_color}; border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 10px; background-color: #222;">
                        <span style="font-size: 11px; color: {g_color}; font-weight: bold;">[{slot['grade'].upper()}]</span><br>
                        <b style="font-size: 14px;">{slot['name']}</b><br>
                        <span style="font-size: 12px; color: #ccc;">수량: {slot['count']}/3마리 | 공격력: {slot['atk']}</span>
                        </div>""",
              unsafe_allow_html=True,
          )

          b_col1, b_col2 = st.columns(2)
          with b_col1:
            if slot["count"] < 3 and slot["grade"] != "mythic":
              if st.button("➕ 증원", key=f"add_{idx}"):
                if st.session_state.gold >= 30:
                  st.session_state.gold -= 30
                  slot["count"] += 1
                  st.rerun()
                else:
                  st.error("골드 부족")
          with b_col2:
            if st.button("🗑️ 해제", key=f"sell_{idx}"):
              st.session_state.board[idx] = None
              st.session_state.gold += 20
              st.rerun()

    st.markdown("---")
    st.subheader("🧪 신화 및 상위 유닛 조합 소울 공방")

    tab1, tab2, tab3 = st.tabs(
        ["희귀/영웅 조합", "🔥 신화 조합식", "💡 개발자 꿀팁"]
    )

    with tab1:
      col_cmb1, col_cmb2 = st.columns(2)
      with col_cmb1:
        if st.button("🔄 일반 3마리 ➔ 희귀 조합", use_container_width=True):
          common_indices = [
              i
              for i, s in enumerate(st.session_state.board)
              if s and s["grade"] == "common"
          ]
          total_common_count = sum(
              st.session_state.board[i]["count"] for i in common_indices
          )
          if total_common_count >= 3:
            deducted = 0
            for i in common_indices:
              while st.session_state.board[i]["count"] > 0 and deducted < 3:
                st.session_state.board[i]["count"] -= 1
                deducted += 1
                if st.session_state.board[i]["count"] == 0:
                  st.session_state.board[i] = None

            empty_idx = next(
                (i for i, s in enumerate(st.session_state.board) if s is None),
                -1,
            )
            if empty_idx != -1:
              rare_template = random.choice(
                  st.session_state.units_def["rare"]
              )
              st.session_state.board[empty_idx] = {
                  "key": rare_template["key"],
                  "name": rare_template["name"],
                  "atk": rare_template["atk"],
                  "grade": "rare",
                  "count": 1,
              }
              st.success(
                  f"✨ 조합 성공! 희귀 [{rare_template['name']}] 획득!"
              )
              st.rerun()
          else:
            st.warning("⚠️ 필드에 일반 유닛이 총 3마리 이상 필요합니다!")

      with col_cmb2:
        if st.button("🔄 희귀 3마리 ➔ 영웅 조합", use_container_width=True):
          rare_indices = [
              i
              for i, s in enumerate(st.session_state.board)
              if s and s["grade"] == "rare"
          ]
          total_rare_count = sum(
              st.session_state.board[i]["count"] for i in rare_indices
          )
          if total_rare_count >= 3:
            deducted = 0
            for i in rare_indices:
              while st.session_state.board[i]["count"] > 0 and deducted < 3:
                st.session_state.board[i]["count"] -= 1
                deducted += 1
                if st.session_state.board[i]["count"] == 0:
                  st.session_state.board[i] = None

            empty_idx = next(
                (i for i, s in enumerate(st.session_state.board) if s is None),
                -1,
            )
            if empty_idx != -1:
              epic_template = random.choice(st.session_state.units_def["epic"])
              st.session_state.board[empty_idx] = {
                  "key": epic_template["key"],
                  "name": epic_template["name"],
                  "atk": epic_template["atk"],
                  "grade": "epic",
                  "count": 1,
              }
              st.success(
                  f"🔥 조합 성공! 영웅 [{epic_template['name']}] 획득!"
              )
              st.rerun()
          else:
            st.warning("⚠️ 필드에 희귀 유닛이 총 3마리 이상 필요합니다!")

    with tab2:
      st.markdown("##### 👑 신화 등급 전용 조합 레시피")
      for mythic_unit in st.session_state.units_def["mythic"]:
        st.markdown(
            f"- **{mythic_unit['name']}** (공격력: {mythic_unit['atk']})<br>`조합식:"
            f" {mythic_unit['recipe']}`",
            unsafe_allow_html=True,
        )
        if st.button(
            f"⚡ {mythic_unit['name']} 소환 시도", key=f"myth_{mythic_unit['key']}"
        ):
          legendary_idx = next(
              (
                  i
                  for i, s in enumerate(st.session_state.board)
                  if s and s["grade"] == "legendary"
              ),
              -1,
          )
          empty_idx = next(
              (i for i, s in enumerate(st.session_state.board) if s is None), -1
          )

          if legendary_idx != -1 and (empty_idx != -1 or legendary_idx != -1):
            st.session_state.board[legendary_idx] = None
            target_idx = (
                empty_idx if empty_idx != -1 else legendary_idx
            )
            st.session_state.board[target_idx] = {
                "key": mythic_unit["key"],
                "name": mythic_unit["name"],
                "atk": mythic_unit["atk"],
                "grade": "mythic",
                "count": 1,
            }
            st.balloons()
            st.success(f"🎊 신화 등급 [{mythic_unit['name']}] 강림 완료!")
            st.rerun()
          else:
            st.warning(
                "⚠️ 필드에 재료가 되는 전설 유닛이 필요합니다! (전설 뽑기를"
                " 먼저 노려보세요)"
            )

    with tab3:
      st.info(
          "💡 **개발자 팁**: 초반에는 골드를 아끼지 말고 '확률 업그레이드'를"
          " 눌러 희귀/영웅 확률을 높인 뒤 유닛을 뽑는 것이 운빨을 극복하는"
          " 지름길입니다!"
      )

if st.button("🔄 전장 상태 갱신 (웨이브 확인)"):
  st.rerun()
