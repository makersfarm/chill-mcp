# ChillMCP 시작 가이드

## 빠른 설치

### 1. 프로젝트 설치

```bash
# 프로젝트 디렉토리로 이동
cd <프로젝트경로>

# Python 3.11 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 서버 실행 테스트

```bash
# 기본 설정으로 실행
python main.py

# 커스텀 파라미터로 실행
python main.py --boss_alertness 80 --boss_alertness_cooldown 60

# 도움말
python main.py --help
```

### 3. 테스트 실행

```bash
# 전체 테스트 실행 (40개)
pytest tests/ -v

# ASCII 아트 데모
python test_ascii.py
```

---

## 실제 사용 방법

### 방법 1: Claude Desktop 연동 (추천)

#### Step 1: 설정 파일 수정

Windows 설정 파일 위치:
```
%APPDATA%\Claude\claude_desktop_config.json
```

macOS/Linux:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Step 2: MCP 서버 추가

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "<프로젝트-절대경로>/main.py",
        "--boss_alertness", "50",
        "--boss_alertness_cooldown", "300"
      ]
    }
  }
}
```

**Windows 예시:**
```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "C:\\Users\\YourName\\Projects\\chill-mcp\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourName\\Projects\\chill-mcp\\main.py"
      ]
    }
  }
}
```

#### Step 3: Claude Desktop 재시작

설정 후 Claude Desktop을 완전히 종료하고 다시 시작하세요.

#### Step 4: 사용해보기

```
You: 스트레스 받아, 휴식 좀 취해줘
Claude: take_a_break 도구를 사용하겠습니다!

[ASCII 아트 + 상태 대시보드 표시]
```

---

### 방법 2: VSCode MCP 확장 사용

프로젝트에 `.vscode/mcp.json` 설정이 포함되어 있습니다.

#### 1) VSCode MCP 확장 설치
- VSCode Extension Marketplace에서 "MCP" 검색
- MCP 확장 설치

#### 2) MCP 서버 시작
- VSCode 하단 MCP 패널에서 `chill-mcp` 서버 시작
- 또는 Command Palette (`Ctrl+Shift+P`) → "MCP: Start Server"

#### 3) 사용 가능한 서버
- **chill-mcp**: 기본 설정
- **chill-mcp-test**: 테스트 설정 (빠른 cooldown)

---

### 방법 3: MCP Inspector (개발/디버깅)

```bash
# MCP Inspector 설치
npm install -g @modelcontextprotocol/inspector

# Inspector 실행
mcp-inspector python main.py
```

웹 브라우저에서 도구 목록이 나타나며, 각 도구를 클릭하여 테스트할 수 있습니다.

---

## 사용 가능한 도구

### 기본 휴식 도구 (필수 8개)
1. `take_a_break` - 기본 휴식 🛋️
2. `watch_netflix` - 넷플릭스 시청 📺
3. `show_meme` - 밈 구경 😂
4. `bathroom_break` - 화장실 타임 🚽
5. `coffee_mission` - 커피 미션 ☕
6. `urgent_call` - 긴급 전화 📞
7. `deep_thinking` - 심오한 사색 💭
8. `email_organizing` - 이메일 정리 📧

### 선택적 도구 (추가 기능)
9. `chimaek` - 치맥 타임! 🍗🍺
10. `leave_work` - 퇴근! 🏃
11. `company_dinner` - 회식 (랜덤 이벤트) 🍻

### 유틸리티
12. `check_status` - 현재 상태 확인

---

## 설정 커스터마이징

### Boss 경계심 조정

Boss가 매우 의심이 많은 경우:
```bash
python main.py --boss_alertness 100 --boss_alertness_cooldown 300
```

Boss가 여유로운 경우:
```bash
python main.py --boss_alertness 20 --boss_alertness_cooldown 60
```

### 빠른 테스트용 설정
```bash
python main.py --boss_alertness 50 --boss_alertness_cooldown 10
```

---

## 문제 해결

### 서버가 시작되지 않을 때

```bash
# Python 버전 확인 (3.11+ 필요)
python --version

# 의존성 재설치
pip install -r requirements.txt

# 가상환경이 활성화되어 있는지 확인
which python  # macOS/Linux
where python  # Windows
```

### Claude Desktop이 도구를 찾지 못할 때

1. **설정 파일 경로 확인**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **JSON 형식 검증**
   - [JSONLint](https://jsonlint.com/)에서 검증

3. **Python 경로를 절대 경로로 변경**

4. **Claude Desktop 개발자 도구에서 로그 확인**
   - `View` → `Toggle Developer Tools` → `Console` 탭

### ASCII 아트가 깨질 때

Windows:
```bash
chcp 65001
```

또는 터미널 설정에서 UTF-8 인코딩으로 변경하세요.

---

## 다음 단계

- [사용 예시](USAGE_EXAMPLES.md) - 다양한 사용 시나리오
- [구현 상세](../IMPLEMENTATION.md) - 기술적 구현 내용
- [MCP 연구 자료](MCP_RESEARCH.md) - MCP 프로토콜 학습 자료

---

**Happy Chilling! 🛋️☕📺**
