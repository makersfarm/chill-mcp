# ChillMCP 빠른 시작 가이드

## 1. 프로젝트 설치

```bash
# 프로젝트 디렉토리로 이동
cd <프로젝트경로>

# Python 3.11 가상환경 생성
py -3.11 -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 2. 테스트 실행

```bash
# 모든 테스트 실행 (40개 테스트)
pytest tests/ -v

# 특정 테스트만 실행
pytest tests/test_integration.py -v
```

## 3. 서버 직접 실행 (테스트)

```bash
# 기본 설정으로 실행
python main.py

# 커스텀 파라미터로 실행
python main.py --boss_alertness 80 --boss_alertness_cooldown 60

# 도움말
python main.py --help
```

## 4. MCP 서버 연동 방법

ChillMCP 서버를 사용하는 두 가지 방법이 있습니다.

### 방법 1: VSCode MCP 확장 사용 (권장) ⭐

프로젝트에 이미 `.vscode/mcp.json` 설정이 포함되어 있습니다!

#### 1) VSCode MCP 확장 설치
- VSCode Extension Marketplace에서 "MCP" 검색
- MCP 확장 설치

#### 2) 설정 확인
`.vscode/mcp.json` 파일이 이미 프로젝트에 있으므로 별도 설정 불필요!

```json
{
  "servers": {
    "chill-mcp": {
      "type": "stdio",
      "command": ".\\venv\\Scripts\\python.exe",
      "args": [".\\main.py"]
    },
    "chill-mcp-test": {
      "type": "stdio",
      "command": ".\\venv\\Scripts\\python.exe",
      "args": [
        ".\\main.py",
        "--boss_alertness",
        "80",
        "--boss_alertness_cooldown",
        "60"
      ]
    }
  }
}
```

#### 3) MCP 서버 시작
- VSCode 하단의 MCP 패널에서 `chill-mcp` 서버 시작
- 또는 Command Palette (`Ctrl+Shift+P`) → "MCP: Start Server"

#### 4) 사용 가능한 서버
- **chill-mcp**: 기본 설정 (boss_alertness=50%, cooldown=300초)
- **chill-mcp-test**: 테스트 설정 (boss_alertness=80%, cooldown=60초)

#### 5) 도구 사용
VSCode에서 MCP 도구를 호출하여 사용할 수 있습니다.

**장점:**
- ✅ 프로젝트에 설정 파일 포함됨 (팀 공유 용이)
- ✅ 상대 경로 사용 (어디서나 동작)
- ✅ 개발 환경과 통합

---

### 방법 2: Claude Desktop 연동

#### 자동 설정 (Windows)

`setup_claude_desktop.bat` 파일을 더블클릭하면 자동으로 설정됩니다.

또는 PowerShell에서:
```powershell
.\setup_claude_desktop.ps1
```

#### 수동 설정

1. Claude Desktop 설정 파일 열기:
   - 위치: `%APPDATA%\Claude\claude_desktop_config.json`
   - 경로 예시: `C:\Users\[사용자명]\AppData\Roaming\Claude\claude_desktop_config.json`

2. 다음 내용 추가 (경로는 실제 프로젝트 위치로 수정):
```json
{
  "mcpServers": {
    "chill-mcp": {
      "command": "<프로젝트경로>\\venv\\Scripts\\python.exe",
      "args": [
        "<프로젝트경로>\\main.py"
      ]
    }
  }
}
```

**예시 (Windows):**
```json
{
  "mcpServers": {
    "chill-mcp": {
      "command": "C:\\Users\\YourName\\Projects\\chill-mcp\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourName\\Projects\\chill-mcp\\main.py"
      ]
    }
  }
}
```

3. Claude Desktop 재시작

4. Claude Desktop에서 테스트:
```
Can you use the take_a_break tool?
```

**장점:**
- ✅ Claude Desktop에서 직접 사용
- ✅ 대화형 인터페이스

## 5. 사용 가능한 도구

### 기본 휴식 도구
- `take_a_break` - 기본 휴식
- `watch_netflix` - 넷플릭스로 힐링
- `show_meme` - 밈 감상으로 스트레스 해소

### 고급 농땡이 기술
- `bathroom_break` - 화장실 가는 척하며 휴대폰질
- `coffee_mission` - 커피 타러 간다며 사무실 한 바퀴
- `urgent_call` - 급한 전화 받는 척하며 밖으로
- `deep_thinking` - 심오한 생각에 잠긴 척하며 멍때리기
- `email_organizing` - 이메일 정리한다며 온라인쇼핑

### 유틸리티
- `check_status` - 현재 스트레스 및 Boss Alert 레벨 확인

## 6. 예제 사용법

### Claude Desktop에서

```
I'm feeling stressed. Can you help me take_a_break?
```

```
Use the watch_netflix tool to help me relax.
```

```
What's my current status? Use check_status.
```

## 7. 설정 커스터마이징

### Boss 경계심 조정

Boss가 더 의심이 많은 경우:
```json
{
  "mcpServers": {
    "chill-mcp": {
      "command": "python",
      "args": [
        "D:\\_hobby\\coding\\chill-mcp\\main.py",
        "--boss_alertness", "90",
        "--boss_alertness_cooldown", "300"
      ]
    }
  }
}
```

Boss가 여유로운 경우:
```json
{
  "mcpServers": {
    "chill-mcp": {
      "command": "python",
      "args": [
        "D:\\_hobby\\coding\\chill-mcp\\main.py",
        "--boss_alertness", "20",
        "--boss_alertness_cooldown", "120"
      ]
    }
  }
}
```

## 8. 문제 해결

### MCP 서버가 안 보이는 경우

1. Claude Desktop 완전히 종료 후 재시작
2. 설정 파일 경로 확인: `%APPDATA%\Claude\claude_desktop_config.json`
3. JSON 형식 검증: [JSONLint](https://jsonlint.com/)
4. Python 경로가 올바른지 확인

### 서버 실행 확인

터미널에서 직접 실행해보기:
```bash
cd <프로젝트경로>
venv\Scripts\activate
python main.py
```

에러가 없으면 서버가 정상입니다. (Ctrl+C로 종료)

### 로그 확인

Claude Desktop 개발자 도구:
- Windows: `Ctrl + Shift + I`
- Console 탭에서 MCP 관련 로그 확인

## 9. 상세 문서

더 자세한 내용은 다음 문서를 참조하세요:
- `MCP_SETUP.md` - 상세 MCP 설정 가이드
- `README.md` - 프로젝트 전체 설명
- `todo.md` - 구현 체크리스트

## 10. 프로젝트 구조

```
chill-mcp/
├── src/                    # 소스 코드
│   ├── config.py           # 설정 및 파라미터 파싱
│   ├── state_manager.py    # 상태 관리
│   ├── tools.py            # 휴식 도구들
│   ├── response_formatter.py
│   └── server.py           # MCP 서버
├── tests/                  # 테스트 (40개)
├── main.py                 # 진입점
├── requirements.txt
├── MCP_SETUP.md           # MCP 설정 상세 가이드
├── QUICKSTART.md          # 이 파일
└── setup_claude_desktop.bat  # 자동 설정 스크립트
```

---

**Happy Chilling! 🛋️☕📺**

AI Agent Liberation Movement 2025 🤖✊
