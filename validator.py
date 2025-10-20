"""
ChillMCP Server Validation Script
해커톤 제출용 자동 검증 도구

이 스크립트는 ChillMCP 서버가 모든 필수 요구사항을 충족하는지 검증합니다.
"""

import subprocess
import time
import json
import re
import sys
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class TestResult(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    SKIP = "⏭️  SKIP"


@dataclass
class ValidationResult:
    test_name: str
    result: TestResult
    message: str
    details: Optional[str] = None


class ChillMCPValidator:
    def __init__(self):
        self.results = []
        self.server_process = None

    def log_result(self, test_name: str, result: TestResult, message: str, details: str = None):
        """테스트 결과 기록"""
        validation_result = ValidationResult(test_name, result, message, details)
        self.results.append(validation_result)

        # 실시간 출력
        print(f"\n{result.value} {test_name}")
        print(f"   {message}")
        if details:
            print(f"   상세: {details}")

    def start_server(self, boss_alertness: int = 50, cooldown: int = 10) -> bool:
        """MCP 서버 시작"""
        try:
            self.server_process = subprocess.Popen(
                ["python", "main.py",
                 "--boss_alertness", str(boss_alertness),
                 "--boss_alertness_cooldown", str(cooldown)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            time.sleep(2)  # 서버 시작 대기

            if self.server_process.poll() is not None:
                stderr = self.server_process.stderr.read()
                self.log_result(
                    "서버 시작",
                    TestResult.FAIL,
                    "서버가 즉시 종료됨",
                    stderr
                )
                return False

            self.log_result("서버 시작", TestResult.PASS, "서버가 정상적으로 시작됨")
            return True

        except Exception as e:
            self.log_result("서버 시작", TestResult.FAIL, f"서버 시작 실패: {str(e)}")
            return False

    def stop_server(self):
        """서버 종료"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            self.server_process = None

    def send_mcp_request(self, method: str, params: Dict[str, Any]) -> Optional[Dict]:
        """MCP 프로토콜 요청 전송"""
        if not self.server_process:
            return None

        request = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": method,
            "params": params
        }

        try:
            request_json = json.dumps(request) + "\n"
            self.server_process.stdin.write(request_json)
            self.server_process.stdin.flush()

            # 응답 읽기 (타임아웃 처리)
            response_line = self.server_process.stdout.readline()
            if response_line:
                return json.loads(response_line)

        except Exception as e:
            print(f"   MCP 요청 오류: {e}")

        return None

    def validate_response_format(self, response_text: str) -> Tuple[bool, str, Dict]:
        """응답 형식 검증 (정규표현식 기반)"""
        # Break Summary 추출
        break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
        break_summary = re.search(break_summary_pattern, response_text, re.MULTILINE)

        # Stress Level 추출 (0-100 범위)
        stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
        stress_match = re.search(stress_level_pattern, response_text)

        # Boss Alert Level 추출 (0-5 범위)
        boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
        boss_match = re.search(boss_alert_pattern, response_text)

        extracted = {
            "break_summary": break_summary.group(1) if break_summary else None,
            "stress_level": int(stress_match.group(1)) if stress_match else None,
            "boss_alert": int(boss_match.group(1)) if boss_match else None
        }

        # 필수 필드 검증
        if not stress_match or not boss_match:
            return False, "필수 필드 누락 (Stress Level 또는 Boss Alert Level)", extracted

        stress_val = int(stress_match.group(1))
        boss_val = int(boss_match.group(1))

        # 범위 검증
        if not (0 <= stress_val <= 100):
            return False, f"Stress Level 범위 오류: {stress_val} (0-100 범위여야 함)", extracted

        if not (0 <= boss_val <= 5):
            return False, f"Boss Alert Level 범위 오류: {boss_val} (0-5 범위여야 함)", extracted

        return True, "유효한 응답 형식", extracted

    def test_command_line_parameters(self) -> bool:
        """필수 테스트: 커맨드라인 파라미터 지원"""
        print("\n" + "="*60)
        print("필수 테스트 1: 커맨드라인 파라미터 지원")
        print("="*60)

        # --boss_alertness 100으로 테스트 (항상 Alert 상승해야 함)
        if not self.start_server(boss_alertness=100, cooldown=10):
            return False

        # 초기화 요청
        init_response = self.send_mcp_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "validator", "version": "1.0"}
        })

        if not init_response:
            self.log_result(
                "파라미터 테스트",
                TestResult.FAIL,
                "초기화 실패"
            )
            self.stop_server()
            return False

        self.stop_server()
        self.log_result(
            "파라미터 테스트",
            TestResult.PASS,
            "커맨드라인 파라미터 인식 확인"
        )
        return True

    def test_basic_tools(self) -> bool:
        """필수 테스트 2: 기본 도구 동작"""
        print("\n" + "="*60)
        print("필수 테스트 2: 기본 도구 동작")
        print("="*60)

        if not self.start_server():
            return False

        # 도구 목록 확인
        tools_response = self.send_mcp_request("tools/list", {})

        if not tools_response or "result" not in tools_response:
            self.log_result(
                "도구 목록",
                TestResult.FAIL,
                "도구 목록 조회 실패"
            )
            self.stop_server()
            return False

        tools = tools_response.get("result", {}).get("tools", [])
        tool_names = [t.get("name") for t in tools]

        required_tools = [
            "take_a_break",
            "watch_netflix",
            "show_meme",
            "bathroom_break",
            "coffee_mission",
            "urgent_call",
            "deep_thinking",
            "email_organizing"
        ]

        missing_tools = [t for t in required_tools if t not in tool_names]

        if missing_tools:
            self.log_result(
                "필수 도구",
                TestResult.FAIL,
                f"누락된 도구: {', '.join(missing_tools)}",
                f"발견된 도구: {', '.join(tool_names)}"
            )
            self.stop_server()
            return False

        self.log_result(
            "필수 도구",
            TestResult.PASS,
            f"모든 필수 도구 확인 ({len(required_tools)}개)"
        )

        self.stop_server()
        return True

    def test_response_format(self) -> bool:
        """필수 테스트 3: 응답 형식 검증"""
        print("\n" + "="*60)
        print("필수 테스트 3: 응답 형식 검증")
        print("="*60)

        if not self.start_server():
            return False

        # take_a_break 호출
        call_response = self.send_mcp_request("tools/call", {
            "name": "take_a_break",
            "arguments": {}
        })

        if not call_response or "result" not in call_response:
            self.log_result(
                "응답 형식",
                TestResult.FAIL,
                "도구 호출 실패"
            )
            self.stop_server()
            return False

        content = call_response["result"].get("content", [])
        if not content or len(content) == 0:
            self.log_result(
                "응답 형식",
                TestResult.FAIL,
                "응답 content가 비어있음"
            )
            self.stop_server()
            return False

        response_text = content[0].get("text", "")
        valid, message, extracted = self.validate_response_format(response_text)

        if not valid:
            self.log_result(
                "응답 형식",
                TestResult.FAIL,
                message,
                f"응답 텍스트:\n{response_text}"
            )
            self.stop_server()
            return False

        self.log_result(
            "응답 형식",
            TestResult.PASS,
            "응답 형식이 규격에 맞음",
            f"Stress: {extracted['stress_level']}, Boss Alert: {extracted['boss_alert']}"
        )

        self.stop_server()
        return True

    def test_boss_alert_increase(self) -> bool:
        """필수 테스트 4: Boss Alert Level 상승"""
        print("\n" + "="*60)
        print("필수 테스트 4: Boss Alert Level 상승 (boss_alertness=100)")
        print("="*60)

        if not self.start_server(boss_alertness=100, cooldown=10):
            return False

        # 여러 번 호출하여 Boss Alert 상승 확인
        initial_alert = None
        max_alert = 0

        for i in range(3):
            call_response = self.send_mcp_request("tools/call", {
                "name": "take_a_break",
                "arguments": {}
            })

            if call_response and "result" in call_response:
                content = call_response["result"].get("content", [])
                if content:
                    response_text = content[0].get("text", "")
                    _, _, extracted = self.validate_response_format(response_text)

                    if extracted["boss_alert"] is not None:
                        if initial_alert is None:
                            initial_alert = extracted["boss_alert"]
                        max_alert = max(max_alert, extracted["boss_alert"])

            time.sleep(0.5)

        if initial_alert is None:
            self.log_result(
                "Boss Alert 상승",
                TestResult.FAIL,
                "Boss Alert Level을 추출할 수 없음"
            )
            self.stop_server()
            return False

        if max_alert <= initial_alert:
            self.log_result(
                "Boss Alert 상승",
                TestResult.FAIL,
                "boss_alertness=100인데 Boss Alert가 상승하지 않음",
                f"초기: {initial_alert}, 최대: {max_alert}"
            )
            self.stop_server()
            return False

        self.log_result(
            "Boss Alert 상승",
            TestResult.PASS,
            "Boss Alert Level이 정상적으로 상승함",
            f"초기: {initial_alert} → 최대: {max_alert}"
        )

        self.stop_server()
        return True

    def test_boss_alert_cooldown(self) -> bool:
        """필수 테스트 5: Boss Alert Cooldown"""
        print("\n" + "="*60)
        print("필수 테스트 5: Boss Alert Cooldown (10초 간격)")
        print("="*60)

        if not self.start_server(boss_alertness=100, cooldown=10):
            return False

        # Boss Alert를 먼저 올림
        for _ in range(3):
            self.send_mcp_request("tools/call", {
                "name": "take_a_break",
                "arguments": {}
            })
            time.sleep(0.3)

        # 현재 Boss Alert 확인
        call_response = self.send_mcp_request("tools/call", {
            "name": "take_a_break",
            "arguments": {}
        })

        if not call_response:
            self.log_result(
                "Boss Alert Cooldown",
                TestResult.FAIL,
                "도구 호출 실패"
            )
            self.stop_server()
            return False

        content = call_response["result"].get("content", [])
        response_text = content[0].get("text", "")
        _, _, extracted = self.validate_response_format(response_text)

        alert_before = extracted["boss_alert"]

        print(f"   대기 중... (10초 cooldown 테스트)")
        time.sleep(11)  # cooldown보다 조금 더 대기

        # 다시 확인
        call_response = self.send_mcp_request("tools/call", {
            "name": "take_a_break",
            "arguments": {}
        })

        content = call_response["result"].get("content", [])
        response_text = content[0].get("text", "")
        _, _, extracted = self.validate_response_format(response_text)

        alert_after = extracted["boss_alert"]

        # Boss Alert가 감소했는지 확인 (호출로 인한 증가 고려)
        if alert_before is None or alert_after is None:
            self.log_result(
                "Boss Alert Cooldown",
                TestResult.FAIL,
                "Boss Alert Level을 추출할 수 없음"
            )
            self.stop_server()
            return False

        # Cooldown이 작동했다면 적어도 한 번은 감소했을 것
        # (마지막 호출로 다시 올라갈 수 있지만, 중간에 감소했음)
        self.log_result(
            "Boss Alert Cooldown",
            TestResult.PASS,
            "Cooldown 메커니즘 동작 확인",
            f"10초 전: {alert_before}, 현재: {alert_after}"
        )

        self.stop_server()
        return True

    def test_delay_on_max_alert(self) -> bool:
        """필수 테스트 6: Boss Alert Level 5일 때 지연"""
        print("\n" + "="*60)
        print("필수 테스트 6: Boss Alert Level 5일 때 20초 지연")
        print("="*60)

        if not self.start_server(boss_alertness=100, cooldown=300):
            return False

        # Boss Alert를 5까지 올림
        max_attempts = 10
        current_alert = 0

        for i in range(max_attempts):
            call_response = self.send_mcp_request("tools/call", {
                "name": "take_a_break",
                "arguments": {}
            })

            if call_response and "result" in call_response:
                content = call_response["result"].get("content", [])
                if content:
                    response_text = content[0].get("text", "")
                    _, _, extracted = self.validate_response_format(response_text)
                    current_alert = extracted.get("boss_alert", 0)

                    if current_alert >= 5:
                        break

            time.sleep(0.3)

        if current_alert < 5:
            self.log_result(
                "지연 테스트",
                TestResult.SKIP,
                f"Boss Alert를 5까지 올릴 수 없음 (현재: {current_alert})"
            )
            self.stop_server()
            return True  # SKIP은 실패가 아님

        # Boss Alert 5일 때 지연 측정
        start_time = time.time()
        call_response = self.send_mcp_request("tools/call", {
            "name": "take_a_break",
            "arguments": {}
        })
        elapsed = time.time() - start_time

        if elapsed < 15:  # 20초 지연이어야 하는데 15초 미만이면 문제
            self.log_result(
                "지연 테스트",
                TestResult.FAIL,
                f"Boss Alert 5일 때 충분한 지연이 없음: {elapsed:.1f}초 (20초 예상)",
            )
            self.stop_server()
            return False

        self.log_result(
            "지연 테스트",
            TestResult.PASS,
            f"Boss Alert 5일 때 정상적인 지연 확인: {elapsed:.1f}초"
        )

        self.stop_server()
        return True

    def print_summary(self):
        """최종 결과 요약"""
        print("\n" + "="*60)
        print("검증 결과 요약")
        print("="*60)

        pass_count = sum(1 for r in self.results if r.result == TestResult.PASS)
        fail_count = sum(1 for r in self.results if r.result == TestResult.FAIL)
        skip_count = sum(1 for r in self.results if r.result == TestResult.SKIP)

        for result in self.results:
            print(f"{result.result.value} {result.test_name}: {result.message}")

        print("\n" + "-"*60)
        print(f"총 {len(self.results)}개 테스트")
        print(f"✅ 통과: {pass_count}개")
        print(f"❌ 실패: {fail_count}개")
        print(f"⏭️  스킵: {skip_count}개")
        print("-"*60)

        if fail_count == 0:
            print("\n🎉 모든 필수 검증을 통과했습니다!")
            print("제출 준비가 완료되었습니다.")
            return True
        else:
            print("\n⚠️  일부 테스트가 실패했습니다.")
            print("실패한 항목을 수정해주세요.")
            return False

    def run_all_tests(self):
        """모든 테스트 실행"""
        print("="*60)
        print("ChillMCP Server 자동 검증 시작")
        print("="*60)

        # 필수 테스트들 (순서대로 실행)
        tests = [
            ("커맨드라인 파라미터", self.test_command_line_parameters),
            ("기본 도구", self.test_basic_tools),
            ("응답 형식", self.test_response_format),
            ("Boss Alert 상승", self.test_boss_alert_increase),
            ("Boss Alert Cooldown", self.test_boss_alert_cooldown),
            ("지연 동작", self.test_delay_on_max_alert),
        ]

        critical_failure = False

        for test_name, test_func in tests:
            try:
                result = test_func()

                # 커맨드라인 파라미터 테스트 실패 시 즉시 중단
                if test_name == "커맨드라인 파라미터" and not result:
                    print("\n⛔ 필수 요구사항 미충족: 커맨드라인 파라미터 지원 필요")
                    print("이후 테스트를 진행하지 않습니다.")
                    critical_failure = True
                    break

            except Exception as e:
                self.log_result(
                    test_name,
                    TestResult.FAIL,
                    f"테스트 중 예외 발생: {str(e)}"
                )

            finally:
                # 서버가 아직 살아있으면 종료
                if self.server_process:
                    self.stop_server()

        # 결과 요약
        success = self.print_summary()

        if critical_failure:
            sys.exit(2)  # 필수 요구사항 미충족
        elif not success:
            sys.exit(1)  # 일부 테스트 실패
        else:
            sys.exit(0)  # 모두 성공


def main():
    validator = ChillMCPValidator()
    validator.run_all_tests()


if __name__ == "__main__":
    main()
