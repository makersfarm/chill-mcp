"""
Comprehensive test scenario that calls all tools sequentially.
This test includes a scenario where boss alert reaches 5 and requires rest.

테스트 시나리오:
1. 기본 휴식 도구 8개 테스트 (take_a_break, watch_netflix, show_meme, bathroom_break, coffee_mission, urgent_call, deep_thinking, email_organizing)
2. Boss Alert가 5가 될 때까지 반복적으로 휴식 도구 호출
3. Boss Alert 5일 때 20초 지연 확인
4. 선택적 도구 3개 테스트 (chimaek, leave_work, company_dinner)
5. check_status로 현재 상태 확인
"""

import asyncio
import pytest
import time
from src.config import Config
from src.state_manager import StateManager
from src import tools


@pytest.mark.asyncio
async def test_all_tools_sequential():
    """
    모든 도구를 순차적으로 호출하는 종합 테스트.

    테스트 단계:
    1. 기본 휴식 도구 8개 호출
    2. 선택적 도구 3개 호출
    3. 각 도구의 응답 형식 검증
    """
    # 설정: boss_alertness를 낮게 설정하여 빠르게 테스트
    config = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # 초기 스트레스 설정
    state_manager._stress_level = 50

    print("\n" + "="*60)
    print("모든 도구 순차 호출 테스트 시작")
    print("="*60)

    # 기본 휴식 도구 8개
    basic_tools = [
        ("take_a_break", tools.take_a_break),
        ("watch_netflix", tools.watch_netflix),
        ("show_meme", tools.show_meme),
        ("bathroom_break", tools.bathroom_break),
        ("coffee_mission", tools.coffee_mission),
        ("urgent_call", tools.urgent_call),
        ("deep_thinking", tools.deep_thinking),
        ("email_organizing", tools.email_organizing),
    ]

    for tool_name, tool_func in basic_tools:
        print(f"\n[{tool_name}] 호출 중...")
        response = await tool_func(state_manager)
        assert response is not None, f"{tool_name} returned None"
        assert "Stress Level:" in response, f"{tool_name} missing Stress Level"
        assert "Boss Alert Level:" in response, f"{tool_name} missing Boss Alert Level"
        print(f"[{tool_name}] ✓ 성공")
        print(f"현재 상태: Stress={state_manager.stress_level}, Boss Alert={state_manager.boss_alert_level}")

    # 선택적 도구 3개
    optional_tools = [
        ("chimaek", tools.chimaek),
        ("company_dinner", tools.company_dinner),
        ("leave_work", tools.leave_work),  # leave_work는 마지막에 (리셋되므로)
    ]

    for tool_name, tool_func in optional_tools:
        print(f"\n[{tool_name}] 호출 중...")
        response = await tool_func(state_manager)
        assert response is not None, f"{tool_name} returned None"
        assert "Stress Level:" in response, f"{tool_name} missing Stress Level"
        assert "Boss Alert Level:" in response, f"{tool_name} missing Boss Alert Level"
        print(f"[{tool_name}] ✓ 성공")
        print(f"현재 상태: Stress={state_manager.stress_level}, Boss Alert={state_manager.boss_alert_level}")

    print("\n" + "="*60)
    print("모든 도구 호출 완료!")
    print("="*60)


@pytest.mark.asyncio
async def test_boss_alert_reaches_5_scenario():
    """
    Boss Alert가 5에 도달하여 휴식이 필요한 시나리오 테스트.

    시나리오:
    1. boss_alertness를 100%로 설정
    2. 반복적으로 휴식 도구를 호출하여 Boss Alert를 5까지 증가
    3. Boss Alert가 5가 되면 20초 지연 발생 확인
    4. 휴식 후 Boss Alert 감소 확인
    """
    # 설정: boss_alertness를 100%로 설정하여 항상 증가
    config = Config(boss_alertness=100, boss_alertness_cooldown=5)
    state_manager = StateManager(config)

    # 초기 스트레스 설정
    state_manager._stress_level = 80

    print("\n" + "="*60)
    print("Boss Alert 5 도달 시나리오 테스트")
    print("="*60)

    # Boss Alert가 5가 될 때까지 휴식 도구 반복 호출
    iteration = 0
    while state_manager.boss_alert_level < 5 and iteration < 10:
        iteration += 1
        print(f"\n[Iteration {iteration}] Boss Alert Level: {state_manager.boss_alert_level}")

        response = await tools.take_a_break(state_manager)
        assert response is not None

        print(f"호출 후 Boss Alert Level: {state_manager.boss_alert_level}")

    assert state_manager.boss_alert_level == 5, "Boss Alert Level should reach 5"
    print(f"\n✓ Boss Alert가 5에 도달했습니다!")

    # Boss Alert가 5일 때 20초 지연 테스트
    print("\n[Boss Alert = 5] 20초 지연 테스트 시작...")
    start_time = time.time()
    response = await tools.take_a_break(state_manager)
    elapsed_time = time.time() - start_time

    print(f"경과 시간: {elapsed_time:.2f}초")
    assert elapsed_time >= 20.0, f"Expected 20 second delay, got {elapsed_time:.2f} seconds"
    print("✓ 20초 지연 확인!")

    # Boss Alert 감소 확인 (cooldown 시간 후)
    print("\n[Boss Alert 감소] Cooldown 테스트...")
    state_manager._last_boss_cooldown = time.time() - 10  # 10초 전으로 설정 (5초 cooldown x 2)
    await state_manager.update_boss_cooldown()

    print(f"Cooldown 후 Boss Alert Level: {state_manager.boss_alert_level}")
    assert state_manager.boss_alert_level < 5, "Boss Alert should decrease after cooldown"
    print("✓ Boss Alert 감소 확인!")

    print("\n" + "="*60)
    print("시나리오 테스트 완료!")
    print("="*60)


@pytest.mark.asyncio
async def test_complete_workflow_scenario():
    """
    완전한 워크플로우 시나리오: 모든 도구 호출 + Boss Alert 5 도달 + 휴식

    시나리오:
    1. 모든 기본 도구를 한 번씩 호출
    2. Boss Alert가 증가하여 5에 도달
    3. 20초 지연 발생 확인
    4. 선택적 도구로 스트레스 관리
    5. leave_work로 완전 리셋
    """
    config = Config(boss_alertness=80, boss_alertness_cooldown=10)
    state_manager = StateManager(config)

    print("\n" + "="*60)
    print("완전한 워크플로우 시나리오 테스트")
    print("="*60)

    # 초기 상태
    state_manager._stress_level = 70
    print(f"\n초기 상태: Stress={state_manager.stress_level}, Boss Alert={state_manager.boss_alert_level}")

    # Step 1: 기본 도구들 호출
    print("\n[Step 1] 기본 휴식 도구 호출...")
    basic_tools = [
        tools.take_a_break,
        tools.watch_netflix,
        tools.show_meme,
        tools.bathroom_break,
    ]

    for tool_func in basic_tools:
        response = await tool_func(state_manager)
        assert response is not None
        print(f"  - {tool_func.__name__}: Stress={state_manager.stress_level}, Boss Alert={state_manager.boss_alert_level}")

    # Step 2: Boss Alert를 5까지 증가시키기
    print("\n[Step 2] Boss Alert를 5까지 증가시키기...")
    attempts = 0
    max_attempts = 15

    while state_manager.boss_alert_level < 5 and attempts < max_attempts:
        attempts += 1
        await tools.coffee_mission(state_manager)
        print(f"  Attempt {attempts}: Boss Alert={state_manager.boss_alert_level}")

    if state_manager.boss_alert_level == 5:
        print("  ✓ Boss Alert가 5에 도달!")

        # Step 3: 20초 지연 확인
        print("\n[Step 3] Boss Alert=5일 때 20초 지연 확인...")
        start_time = time.time()
        await tools.urgent_call(state_manager)
        elapsed = time.time() - start_time

        print(f"  경과 시간: {elapsed:.2f}초")
        assert elapsed >= 20.0, f"Expected 20s delay, got {elapsed:.2f}s"
        print("  ✓ 20초 지연 확인!")
    else:
        print(f"  ⚠ Boss Alert가 5에 도달하지 못함 (현재: {state_manager.boss_alert_level})")

    # Step 4: 선택적 도구로 스트레스 관리
    print("\n[Step 4] 선택적 도구로 스트레스 관리...")

    # 치맥으로 대폭 감소
    print("  - chimaek 호출...")
    response = await tools.chimaek(state_manager)
    assert response is not None
    print(f"    치맥 후: Stress={state_manager.stress_level}, Boss Alert={state_manager.boss_alert_level}")

    # 회식 (랜덤 이벤트)
    print("  - company_dinner 호출...")
    response = await tools.company_dinner(state_manager)
    assert response is not None
    print(f"    회식 후: Stress={state_manager.stress_level}, Boss Alert={state_manager.boss_alert_level}")

    # Step 5: 퇴근으로 완전 리셋
    print("\n[Step 5] 퇴근으로 완전 리셋...")
    response = await tools.leave_work(state_manager)
    assert response is not None

    final_state = await state_manager.get_state()
    print(f"  퇴근 후: Stress={final_state['stress_level']}, Boss Alert={final_state['boss_alert_level']}")

    assert final_state['stress_level'] == 0, "퇴근 후 스트레스는 0이어야 함"
    assert final_state['boss_alert_level'] == 0, "퇴근 후 Boss Alert는 0이어야 함"
    print("  ✓ 완전 리셋 확인!")

    print("\n" + "="*60)
    print("완전한 워크플로우 테스트 완료!")
    print("="*60)


@pytest.mark.asyncio
async def test_stress_accumulation_with_breaks():
    """
    스트레스 자동 증가와 휴식 도구의 상호작용 테스트.

    시나리오:
    1. 시간 경과로 스트레스 자동 증가
    2. 휴식 도구로 스트레스 감소
    3. 다시 시간 경과
    4. 반복
    """
    config = Config(boss_alertness=30, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    print("\n" + "="*60)
    print("스트레스 누적 및 관리 테스트")
    print("="*60)

    # 초기 스트레스 0
    state_manager._stress_level = 0
    state_manager._last_stress_update = time.time() - 120  # 2분 전

    print(f"\n초기 상태: Stress={state_manager.stress_level}")

    # 스트레스 자동 증가
    await state_manager.update_stress_level()
    print(f"2분 경과 후: Stress={state_manager.stress_level} (최소 +2 예상)")
    assert state_manager.stress_level >= 2, "2분 경과 후 스트레스는 최소 2 증가해야 함"

    # 휴식으로 감소
    await tools.take_a_break(state_manager)
    stress_after_break = state_manager.stress_level
    print(f"휴식 후: Stress={stress_after_break}")

    # 다시 시간 경과
    state_manager._last_stress_update = time.time() - 180  # 3분 전
    await state_manager.update_stress_level()
    print(f"3분 더 경과 후: Stress={state_manager.stress_level} (최소 +3 예상)")

    # 여러 휴식 도구로 관리
    print("\n다양한 휴식 도구로 스트레스 관리...")
    tools_list = [
        tools.watch_netflix,
        tools.show_meme,
        tools.bathroom_break,
        tools.coffee_mission,
    ]

    for tool_func in tools_list:
        before = state_manager.stress_level
        await tool_func(state_manager)
        after = state_manager.stress_level
        print(f"  - {tool_func.__name__}: {before} → {after} (변화: {after - before})")

    print("\n" + "="*60)
    print("스트레스 관리 테스트 완료!")
    print("="*60)


@pytest.mark.asyncio
async def test_all_tools_with_high_boss_alertness():
    """
    높은 boss_alertness 설정에서 모든 도구 테스트.
    Boss Alert가 빠르게 증가하는 상황 시뮬레이션.
    """
    config = Config(boss_alertness=90, boss_alertness_cooldown=5)
    state_manager = StateManager(config)

    print("\n" + "="*60)
    print("높은 Boss Alertness 환경에서 모든 도구 테스트")
    print("Boss Alertness: 90%")
    print("="*60)

    state_manager._stress_level = 60

    all_tools = [
        ("take_a_break", tools.take_a_break),
        ("watch_netflix", tools.watch_netflix),
        ("show_meme", tools.show_meme),
        ("bathroom_break", tools.bathroom_break),
        ("coffee_mission", tools.coffee_mission),
        ("urgent_call", tools.urgent_call),
        ("deep_thinking", tools.deep_thinking),
        ("email_organizing", tools.email_organizing),
        ("chimaek", tools.chimaek),
        ("company_dinner", tools.company_dinner),
    ]

    for tool_name, tool_func in all_tools:
        boss_before = state_manager.boss_alert_level
        stress_before = state_manager.stress_level

        start_time = time.time()
        response = await tool_func(state_manager)
        elapsed = time.time() - start_time

        boss_after = state_manager.boss_alert_level
        stress_after = state_manager.stress_level

        delay_str = f" (지연: {elapsed:.1f}초)" if elapsed >= 20 else ""
        print(f"\n[{tool_name}]{delay_str}")
        print(f"  Stress: {stress_before} → {stress_after}")
        print(f"  Boss Alert: {boss_before} → {boss_after}")

        # 검증
        assert response is not None
        assert "Stress Level:" in response
        assert "Boss Alert Level:" in response

        # Boss Alert가 5면 20초 지연 확인
        if boss_before >= 5:
            assert elapsed >= 20.0, f"Boss Alert=5일 때 20초 지연 필요, 실제: {elapsed:.2f}초"

    # 마지막에 leave_work로 리셋
    print("\n[leave_work] 퇴근으로 모든 상태 리셋...")
    await tools.leave_work(state_manager)
    final_state = await state_manager.get_state()

    print(f"  최종 상태: Stress={final_state['stress_level']}, Boss Alert={final_state['boss_alert_level']}")
    assert final_state['stress_level'] == 0
    assert final_state['boss_alert_level'] == 0

    print("\n" + "="*60)
    print("높은 Boss Alertness 테스트 완료!")
    print("="*60)


if __name__ == "__main__":
    # pytest로 실행하지 않고 직접 실행할 경우
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))
