# MCP 프로토콜 및 FastMCP 조사 자료

## 1. MCP (Model Context Protocol) 개요

### MCP란?
- **Model Context Protocol**: LLM에게 컨텍스트와 도구를 제공하는 표준화된 프로토콜
- Anthropic이 주도하여 개발한 오픈 스탠다드
- AI 에이전트가 외부 도구와 데이터에 접근할 수 있는 표준 인터페이스 제공

### 핵심 개념
- **서버(Server)**: 도구(Tools)와 리소스(Resources)를 제공하는 주체
- **클라이언트(Client)**: AI 에이전트 (예: Claude)가 서버에 접근
- **Transport**: 클라이언트와 서버 간 통신 방식 (stdio, HTTP 등)

---

## 2. FastMCP 라이브러리

### 개요
- **FastMCP 2.0**: Python으로 MCP 서버를 빠르게 구축하는 프레임워크
- FastMCP 1.0은 2024년 공식 MCP SDK에 통합됨
- 현재 FastMCP 2.0은 기본 프로토콜을 넘어선 프로덕션급 기능 제공

### 설치
```bash
pip install fastmcp
```

### 주요 특징
1. **최소한의 보일러플레이트**: 함수 데코레이터만으로 도구 등록 가능
2. **자동 스키마 생성**: 타입 힌트로부터 자동으로 도구 스키마 생성
3. **다양한 Transport 지원**: stdio, HTTP 등
4. **프로덕션 기능**: 엔터프라이즈 인증, 배포 도구, 테스트 프레임워크
5. **고급 패턴**: 서버 조합, 프록시 등

---

## 3. 기본 사용법

### 최소 예제
```python
from fastmcp import FastMCP

# 서버 생성
mcp = FastMCP("Demo Server")

# 도구 등록 (@mcp.tool 데코레이터 사용)
@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# 서버 실행 (기본: stdio transport)
if __name__ == "__main__":
    mcp.run()
```

### ChillMCP 적용 예시
```python
from fastmcp import FastMCP

mcp = FastMCP("ChillMCP")

@mcp.tool
def take_a_break() -> str:
    """Take a short break to reduce stress"""
    # 상태 업데이트 로직
    return "Break Summary: Short break taken\nStress Level: 50\nBoss Alert Level: 1"

@mcp.tool
def watch_netflix(show: str = "your favorite show") -> str:
    """Watch Netflix to relax"""
    return f"Break Summary: Watching {show}\nStress Level: 30\nBoss Alert Level: 2"

if __name__ == "__main__":
    mcp.run()  # stdio transport로 실행
```

---

## 4. Transport 방식

### stdio Transport (이번 미션에서 사용)
- **특징**: 표준 입출력(stdin/stdout)을 통한 JSON-RPC 통신
- **장점**: 간단한 구현, 로컬 프로세스 간 통신에 적합
- **사용법**: `mcp.run()` (기본값)
- **통신 형식**: JSON-RPC 2.0

### HTTP Transport
- **특징**: HTTP 엔드포인트를 통한 통신
- **사용법**: `mcp.run(transport="http", host="0.0.0.0", port=8000)`
- **장점**: 원격 서버, 마이크로서비스 아키텍처에 적합

---

## 5. 도구(Tool) 등록 방법

### 기본 도구 등록
```python
@mcp.tool
def function_name(param1: type1, param2: type2) -> return_type:
    """도구 설명 (LLM에게 표시됨)"""
    # 구현
    return result
```

### 타입 힌트의 중요성
- FastMCP는 타입 힌트로부터 자동으로 JSON Schema 생성
- LLM이 도구를 올바르게 사용하도록 돕는 메타데이터 제공
- 필수는 아니지만 강력 권장

### 선택적 파라미터
```python
@mcp.tool
def coffee_mission(duration: int = 5) -> str:
    """Get coffee (default: 5 minutes)"""
    return f"Coffee mission for {duration} minutes"
```

---

## 6. 상태 관리 전략

MCP 서버는 기본적으로 **상태를 유지**할 수 있습니다.

### 클래스 기반 상태 관리
```python
from fastmcp import FastMCP
import time

class ChillMCPServer:
    def __init__(self):
        self.stress_level = 50
        self.boss_alert_level = 0
        self.last_activity = time.time()
        self.mcp = FastMCP("ChillMCP")

        # 도구 등록
        self.mcp.tool(self.take_a_break)

    def take_a_break(self) -> str:
        """Take a break"""
        self.stress_level = max(0, self.stress_level - 10)
        self.boss_alert_level = min(5, self.boss_alert_level + 1)

        return f"""Break Summary: Short break taken
Stress Level: {self.stress_level}
Boss Alert Level: {self.boss_alert_level}"""

    def run(self):
        self.mcp.run()

if __name__ == "__main__":
    server = ChillMCPServer()
    server.run()
```

---

## 7. JSON-RPC 프로토콜 구조

### 요청 예시
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "take_a_break",
    "arguments": {}
  }
}
```

### 응답 예시
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Break Summary: Short break\nStress Level: 40\nBoss Alert Level: 1"
      }
    ]
  }
}
```

---

## 8. 커맨드라인 파라미터 처리

### argparse 사용 예시
```python
import argparse
from fastmcp import FastMCP

def main():
    parser = argparse.ArgumentParser(description="ChillMCP Server")
    parser.add_argument("--boss_alertness", type=int, default=50,
                        help="Boss alertness probability (0-100)")
    parser.add_argument("--boss_alertness_cooldown", type=int, default=300,
                        help="Boss alert cooldown in seconds")

    args = parser.parse_args()

    # 서버 설정에 파라미터 전달
    server = ChillMCPServer(
        boss_alertness=args.boss_alertness,
        cooldown=args.boss_alertness_cooldown
    )
    server.run()

if __name__ == "__main__":
    main()
```

---

## 9. 비동기 처리 (지연 구현)

### Boss Alert Level 5일 때 20초 지연
```python
import asyncio

@mcp.tool
async def take_a_break() -> str:
    """Take a break (may be delayed if boss is watching)"""

    if self.boss_alert_level >= 5:
        # Boss가 감시 중일 때 20초 지연
        await asyncio.sleep(20)

    # 나머지 로직
    return result
```

### 동기 버전 (threading)
```python
import time

@mcp.tool
def take_a_break() -> str:
    """Take a break"""

    if self.boss_alert_level >= 5:
        time.sleep(20)  # 20초 대기

    # 나머지 로직
    return result
```

---

## 10. 백그라운드 태스크 (Stress 자동 증가)

### Threading을 이용한 주기적 업데이트
```python
import threading
import time

class ChillMCPServer:
    def __init__(self):
        self.stress_level = 50
        self.running = True

        # 백그라운드 스레드 시작
        self.stress_thread = threading.Thread(target=self._increase_stress, daemon=True)
        self.stress_thread.start()

    def _increase_stress(self):
        """1분마다 스트레스 1포인트 증가"""
        while self.running:
            time.sleep(60)  # 1분 대기
            self.stress_level = min(100, self.stress_level + 1)

    def run(self):
        try:
            self.mcp.run()
        finally:
            self.running = False
```

---

## 11. 실전 팁

### 디버깅
```python
# FastMCP는 기본적으로 stderr로 로그 출력
import sys

print("Debug message", file=sys.stderr)
```

### 응답 형식 준수
```python
def format_response(summary: str, stress: int, boss_alert: int) -> str:
    """표준 응답 형식 생성"""
    return f"""Break Summary: {summary}
Stress Level: {stress}
Boss Alert Level: {boss_alert}"""
```

### 범위 제한
```python
def clamp(value: int, min_val: int, max_val: int) -> int:
    """값을 범위 내로 제한"""
    return max(min_val, min(max_val, value))

# 사용
self.stress_level = clamp(self.stress_level - 10, 0, 100)
self.boss_alert_level = clamp(self.boss_alert_level + 1, 0, 5)
```

---

## 12. 추가 리소스

- **공식 문서**: https://gofastmcp.com/
- **GitHub**: https://github.com/jlowin/fastmcp
- **MCP 사양**: https://github.com/modelcontextprotocol
- **DataCamp 튜토리얼**: Building MCP Server with FastMCP 2.0
- **FreeCodeCamp**: Learn MCP Essentials and FastMCP

---

## 13. ChillMCP 구현 체크리스트

### 필수 구현
- [ ] FastMCP 서버 초기화
- [ ] 8개 필수 도구 등록 (take_a_break, watch_netflix, show_meme, bathroom_break, coffee_mission, urgent_call, deep_thinking, email_organizing)
- [ ] 상태 관리 (stress_level, boss_alert_level)
- [ ] 커맨드라인 파라미터 처리 (--boss_alertness, --boss_alertness_cooldown)
- [ ] 응답 형식 준수 (Break Summary, Stress Level, Boss Alert Level)
- [ ] Boss Alert Level 5일 때 20초 지연
- [ ] Stress Level 자동 증가 (1분에 1포인트)
- [ ] Boss Alert Level 자동 감소 (cooldown 주기마다 1포인트)

### 선택적 구현
- [ ] 치맥 도구
- [ ] 퇴근 도구
- [ ] 회식 도구
- [ ] 창의적인 Break Summary 메시지
- [ ] 이모지 활용

---

## 14. 구현 시 주의사항

1. **stdio transport 사용**: `mcp.run()` (기본값)으로 실행
2. **정규표현식 호환**: 응답 형식이 README의 정규표현식과 일치해야 함
3. **범위 검증**: Stress Level (0-100), Boss Alert Level (0-5)
4. **확률 처리**: boss_alertness는 퍼센트 확률 (0-100)
5. **타입 안전성**: Python 타입 힌트 적극 활용

---

**작성일**: 2025-10-18
**작성자**: YJL (ChillMCP 팀)
**목적**: 데일리 스크럼 및 팀 공유
