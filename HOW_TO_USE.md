# ChillMCP 사용 가이드 🚀

## 빠른 시작

### 1. 서버 실행하기

```bash
# 기본 실행 (기본 설정)
python main.py

# 커스텀 설정으로 실행
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

실행하면 이렇게 나옵니다:
```
FastMCP server started
```

서버가 stdio 모드로 실행 중입니다! (백그라운드에서 대기 중)

---

## 2. 실제 사용 방법

### 방법 1: Claude Desktop과 연동 (추천)

#### Step 1: Claude Desktop 설정 파일 수정

Windows에서 설정 파일 위치:
```
%APPDATA%\Claude\claude_desktop_config.json
```

파일을 열고 이렇게 추가:
```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "<프로젝트-경로>/main.py",
        "--boss_alertness", "50",
        "--boss_alertness_cooldown", "300"
      ]
    }
  }
}
```

#### Step 2: Claude Desktop 재시작

설정 후 Claude Desktop을 완전히 종료하고 다시 시작하세요.

#### Step 3: Claude에게 도구 사용 요청

Claude Desktop에서 이렇게 요청하세요:
```
치맥 먹고 싶어!
```

또는
```
너무 스트레스 받아... 휴식 좀 취해줘
```

Claude가 자동으로 ChillMCP 서버의 도구를 사용합니다!

---

### 방법 2: MCP Inspector로 테스트 (개발용)

```bash
# MCP Inspector 설치
npm install -g @modelcontextprotocol/inspector

# Inspector 실행
mcp-inspector python main.py
```

웹 브라우저가 열리면서 도구 목록이 보입니다.
거기서 각 도구를 클릭해서 테스트할 수 있어요!

---

### 방법 3: 직접 JSON-RPC 테스트 (고급)

서버를 실행한 상태에서 JSON 메시지를 stdin으로 보낼 수 있습니다.

```bash
python main.py
```

그런 다음 이런 JSON을 입력:
```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

하지만 이 방법은 불편하니 **방법 1이나 2를 추천**합니다!

---

## 3. 간단한 데모 실행

ASCII 아트를 바로 보려면:

```bash
python test_ascii.py
```

이렇게 하면 모든 도구(11개)를 순서대로 실행하면서 ASCII 아트를 보여줍니다!

**실행 결과 예시:**
```
============================================================
ChillMCP ASCII Art Test
============================================================

🛋️  Testing: take_a_break
------------------------------------------------------------

  ╔═══════════════════════════════════╗
  ║       🛋️  휴식 타임! 🛋️          ║
  ╠═══════════════════════════════════╣
  ║                                   ║
  ║        (´｡• ᵕ •｡`)               ║
  ║                                   ║
  ║      ~  편안하다  ~               ║
  ║                                   ║
  ╚═══════════════════════════════════╝

╔═══════════════════════════════════════════╗
║        AI AGENT STATUS DASHBOARD          ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Stress Level: [░░░░░░░░░░] 0%           ║
║                                           ║
║  Boss Alert:   [█░░░░] 1/5                ║
║                                           ║
║      (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧      행복해요!        ║
║                                           ║
╚═══════════════════════════════════════════╝
```

---

## 4. 사용 가능한 도구 목록

### 기본 8개 (필수)
1. `take_a_break` - 기본 휴식 🛋️
2. `watch_netflix` - 넷플릭스 시청 📺
3. `show_meme` - 밈 구경 😂
4. `bathroom_break` - 화장실 타임 🚽
5. `coffee_mission` - 커피 미션 ☕
6. `urgent_call` - 긴급 전화 📞
7. `deep_thinking` - 심오한 사색 💭
8. `email_organizing` - 이메일 정리 📧

### 선택적 3개 (추가 점수)
9. `chimaek` - 치맥 타임! 🍗🍺
10. `leave_work` - 퇴근! 🏃
11. `company_dinner` - 회식 (랜덤 이벤트) 🍻

### 기타
12. `check_status` - 현재 상태 확인

---

## 5. 추천 사용 흐름

### Claude Desktop 사용 시:

1. **서버 설정**
   ```bash
   # claude_desktop_config.json 수정
   # Claude Desktop 재시작
   ```

2. **Claude와 대화**
   ```
   You: 스트레스가 쌓였어, 뭐 좀 해줘
   Claude: take_a_break 도구를 사용하겠습니다!

   [ASCII 아트 + 상태 대시보드 표시]

   Claude: 휴식을 취하셨네요! Stress Level이 감소했습니다.
   ```

3. **다양한 도구 시도**
   ```
   You: 넷플릭스 보고 싶어
   You: 치맥 먹고 싶다!
   You: 퇴근하고 싶어...
   You: 회식 가자
   ```

---

## 6. 문제 해결

### 서버가 시작 안 돼요!
```bash
# Python 버전 확인 (3.11+ 필요)
python --version

# 패키지 재설치
pip install -r requirements.txt

# 서버 실행 확인
python main.py --help
```

### Claude Desktop이 도구를 못 찾아요!
1. `claude_desktop_config.json` 파일 경로가 정확한지 확인
2. Python 경로가 절대 경로인지 확인
3. Claude Desktop 완전히 재시작
4. Claude Desktop 로그 확인:
   - `View` → `Toggle Developer Tools` → `Console` 탭

### ASCII 아트가 깨져요!
```bash
# Windows에서 UTF-8 인코딩 설정
chcp 65001

# 또는 터미널 설정에서 UTF-8로 변경
```

---

## 7. 테스트 명령어 모음

```bash
# 전체 테스트 실행
python -m pytest tests/ -v

# ASCII 아트 데모
python test_ascii.py

# 검증 도구 (자동 검증)
python validator.py

# 서버 실행 (다양한 설정)
python main.py --boss_alertness 100 --boss_alertness_cooldown 10
```

---

## 8. 꿀팁 💡

### Boss Alert Level 빠르게 올리기
```bash
python main.py --boss_alertness 100
```
이렇게 하면 휴식 도구를 쓸 때마다 항상 Boss Alert가 올라갑니다!

### Stress 빠르게 테스트
```bash
python main.py --boss_alertness 0 --boss_alertness_cooldown 5
```
Boss Alert는 안 올리고, Cooldown만 빠르게!

### 회식 랜덤 이벤트 여러 번 보기
```python
# test_ascii.py 수정
for i in range(10):
    result = await tools.company_dinner(state_manager)
    print(result)
    print("\n" + "="*60 + "\n")
```

---

## 9. Claude Desktop 설정 예시 (전체)

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "<프로젝트-경로>/main.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## 10. 자주 하는 질문

**Q: 서버가 계속 실행되나요?**
A: stdio 모드라서 Claude가 요청할 때만 실행됩니다. 평소엔 대기 상태예요.

**Q: ASCII 아트를 끄고 싶어요**
A: `src/response_formatter.py`에서 `show_ascii_art=False`로 설정하세요.

**Q: 새 도구를 추가하려면?**
A:
1. `src/tools.py`에 함수 추가
2. `src/server.py`에 `@mcp.tool()` 데코레이터로 등록
3. (선택) `src/ascii_art.py`에 ASCII 아트 추가

**Q: 실제로 Claude Code에서 돌려보려면?**
A: Claude Desktop 설정 파일에 MCP 서버로 등록하면 됩니다!

---

**준비 완료!** 🎉

이제 `python test_ascii.py`로 데모를 보거나,
Claude Desktop에 연동해서 실제로 사용해보세요!
